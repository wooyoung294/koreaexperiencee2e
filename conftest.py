import glob
import json
import os
import platform
from pathlib import Path
from urllib.parse import urlsplit

import allure
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright
import pytest

from components.header import Header
from pages.home_popup_page import HomePopupPage
from pages.login_page import LoginPage

PROJECT_ROOT = Path(__file__).resolve().parent
VIDEO_DIR = PROJECT_ROOT / 'test-results' / 'videos'

pytest_plugins = [
    f'steps.{Path(file).stem}'
    for file in glob.glob(str(PROJECT_ROOT / 'steps' / '*_steps.py'))
]


def _as_bool(value: str | bool | None, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return value.lower() in {'1', 'true', 'yes', 'on'}


def _popup_storage_init_script(base_url: str, show_popup: bool) -> str:
    parsed_url = urlsplit(base_url)
    target_origin = f'{parsed_url.scheme}://{parsed_url.netloc}'
    storage_action = (
        f"localStorage.removeItem('{HomePopupPage.DISMISSED_STORAGE_KEY}');"
        if show_popup
        else f"localStorage.setItem('{HomePopupPage.DISMISSED_STORAGE_KEY}', today);"
    )

    return f"""(() => {{
        if (window.location.origin !== {json.dumps(target_origin)}) return;

        const today = new Date().toISOString().slice(0, 10);
        {storage_action}
    }})();"""


class AuthenticatedSession:
    def __init__(self, browser: Browser, base_url: str, config):
        self.browser = browser
        self.base_url = base_url
        self.config = config
        self._storage_state: dict | None = None
        self._initialized = False

    def get_storage_state(self) -> dict | None:
        if self._initialized:
            return self._storage_state

        self._initialized = True
        if not (os.getenv('ID') and os.getenv('PASSWORD')):
            return None

        context = self.browser.new_context(
            base_url=self.base_url,
            locale='ko-KR',
            timezone_id='Asia/Seoul',
            ignore_https_errors=self.config.e2e_ignore_https_errors,
            viewport={'width': 1440, 'height': 900},
        )
        context.add_init_script(
            script=_popup_storage_init_script(self.base_url, show_popup=False)
        )
        page = context.new_page()

        try:
            page.goto(
                f'{self.base_url.rstrip("/")}/login',
                wait_until='domcontentloaded',
            )
            login_page = LoginPage(page)
            login_page.fill_credentials_from_env()
            login_page.submit_login()
            Header(page).verify_logged_in()
            self.update_storage_state(context)
            return self._storage_state
        finally:
            context.close()

    def update_storage_state(self, context: BrowserContext) -> None:
        self._storage_state = context.storage_state(indexed_db=True)


def pytest_addoption(parser):
    group = parser.getgroup('e2e')
    group.addoption('--env', default='qa', help='실행 환경 이름 (기본값: qa)')


def pytest_configure(config):
    env_name = config.getoption('--env')
    env_file = PROJECT_ROOT / f'.env.{env_name}'
    load_dotenv(env_file if env_file.exists() else PROJECT_ROOT / '.env', override=False)

    config.e2e_env = env_name
    config.e2e_base_url = config.getoption('--base-url') or os.getenv(
        'BASE_URL', 'https://koreaexperience.kr/ko'
    )
    selected_browsers = config.getoption('--browser')
    config.e2e_browser = (
        selected_browsers[0] if selected_browsers else os.getenv('BROWSER', 'chromium')
    )
    config.e2e_headless = not config.getoption('--headed') and _as_bool(
        os.getenv('HEADLESS'), default=True
    )
    config.e2e_ignore_https_errors = _as_bool(os.getenv('IGNORE_HTTPS_ERRORS'))


@pytest.fixture(scope='session')
def env_name(request) -> str:
    return request.config.e2e_env


@pytest.fixture(scope='session')
def base_url(request) -> str:
    return request.config.e2e_base_url


@pytest.fixture(scope='session')
def browser(playwright: Playwright, request) -> Browser:
    browser_type = getattr(playwright, request.config.e2e_browser)
    instance = browser_type.launch(headless=request.config.e2e_headless)
    yield instance
    instance.close()


@pytest.fixture(scope='session')
def authenticated_session(
    browser: Browser,
    base_url: str,
    request,
) -> AuthenticatedSession:
    return AuthenticatedSession(browser, base_url, request.config)


@pytest.fixture
def web_function_driver(
    browser: Browser,
    base_url: str,
    authenticated_session: AuthenticatedSession,
    request,
) -> Page:
    popup_scenario = request.node.get_closest_marker('popup') is not None
    sensitive_scenario = request.node.get_closest_marker('login') is not None
    context_options = {
        'base_url': base_url,
        'locale': 'ko-KR',
        'timezone_id': 'Asia/Seoul',
        'ignore_https_errors': request.config.e2e_ignore_https_errors,
        'viewport': {'width': 1440, 'height': 900},
    }
    if not sensitive_scenario:
        VIDEO_DIR.mkdir(parents=True, exist_ok=True)
        context_options['record_video_dir'] = str(VIDEO_DIR)
        context_options['record_video_size'] = {'width': 1440, 'height': 900}

    storage_state = None
    if not sensitive_scenario:
        storage_state = authenticated_session.get_storage_state()
        if storage_state is not None:
            context_options['storage_state'] = storage_state

    context = browser.new_context(
        **context_options,
    )
    context.add_init_script(
        script=_popup_storage_init_script(base_url, show_popup=popup_scenario)
    )
    current_page = context.new_page()
    request.node._e2e_page = current_page

    console_errors: list[str] = []
    current_page.on(
        'console',
        lambda message: console_errors.append(message.text) if message.type == 'error' else None,
    )
    request.node._e2e_console_errors = console_errors

    current_page.goto(base_url, wait_until='domcontentloaded')
    if storage_state is not None:
        Header(current_page).verify_logged_in()

    yield current_page

    report = getattr(request.node, 'rep_call', None)
    if storage_state is not None and report and report.passed:
        authenticated_session.update_storage_state(context)

    video = current_page.video if not sensitive_scenario else None
    context.close()

    if video is not None:
        video_name = f'web_{request.node.name}_video.webm'
        allure.attach.file(
            video.path(),
            name=video_name,
            attachment_type=allure.attachment_type.WEBM,
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f'rep_{report.when}', report)

    if report.when != 'call' or not report.failed:
        return

    current_page = getattr(item, '_e2e_page', None)
    sensitive_scenario = item.get_closest_marker('login') is not None
    if sensitive_scenario:
        allure.attach(
            '민감정보 보호를 위해 로그인 실패 증적을 저장하지 않습니다.',
            name='Sensitive test evidence policy',
            attachment_type=allure.attachment_type.TEXT,
        )
        return

    if current_page and not current_page.is_closed():
        allure.attach(
            current_page.screenshot(full_page=True),
            name='Failure screenshot',
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(current_page.url, name='Current URL', attachment_type=allure.attachment_type.TEXT)

    console_errors = getattr(item, '_e2e_console_errors', [])
    if console_errors:
        allure.attach(
            '\n'.join(console_errors),
            name='Console errors',
            attachment_type=allure.attachment_type.TEXT,
        )


def pytest_bdd_before_scenario(request, feature, scenario):
    allure.dynamic.title(scenario.name)
    allure.dynamic.feature(feature.name)
    allure.dynamic.story(scenario.name)


def pytest_collection_modifyitems(items):
    login_credentials_configured = bool(
        os.getenv('ID') and os.getenv('PASSWORD')
    )
    if login_credentials_configured:
        return

    skip_login = pytest.mark.skip(
        reason='ID와 PASSWORD 환경변수가 설정되지 않았습니다.'
    )
    for item in items:
        if item.get_closest_marker('login'):
            item.add_marker(skip_login)


def pytest_sessionfinish(session):
    results_dir = PROJECT_ROOT / 'allure-results'
    results_dir.mkdir(exist_ok=True)
    properties = {
        'OS': platform.platform(),
        'ENV': getattr(session.config, 'e2e_env', 'qa'),
        'BASE_URL': getattr(session.config, 'e2e_base_url', ''),
        'BROWSER': getattr(session.config, 'e2e_browser', ''),
    }
    content = ''.join(f'{key}={value}\n' for key, value in properties.items())
    (results_dir / 'environment.properties').write_text(content, encoding='utf-8')
