from typing import TYPE_CHECKING

from playwright.sync_api import Locator, expect

if TYPE_CHECKING:
    from playwright.sync_api import Page


class ExpectBase:
    page: 'Page'

    def expect_visible(self, target: str | Locator, timeout: int = 5_000) -> None:
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        expect(locator).to_be_visible(timeout=timeout)

    def expect_enabled(self, target: str | Locator, timeout: int = 5_000) -> None:
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        expect(locator).to_be_enabled(timeout=timeout)

    def expect_not_visible(self, target: str | Locator, timeout: int = 5_000) -> None:
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        expect(locator).not_to_be_visible(timeout=timeout)

    def expect_value(
        self,
        target: str | Locator,
        value: str,
        timeout: int = 5_000,
    ) -> None:
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        expect(locator).to_have_value(value, timeout=timeout)

    def expect_text(
        self,
        target: str | Locator,
        value: str,
        timeout: int = 5_000,
    ) -> None:
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        expect(locator).to_have_text(value, timeout=timeout)

    def expect_image_loaded(
        self,
        src: str,
        scope: Locator | None = None,
        timeout: int = 15_000,
    ) -> Locator:
        image_scope = scope if scope is not None else self.page
        image = image_scope.locator(f'img[src="{src}"]').first
        self.expect_visible(image, timeout=timeout)

        is_loaded = image.evaluate(
            f"""(image) => new Promise((resolve) => {{
                const loaded = () => image.naturalWidth > 0 && image.naturalHeight > 0;
                if (image.complete) {{
                    resolve(loaded());
                    return;
                }}

                const timeout = setTimeout(() => resolve(false), {timeout});
                image.addEventListener('load', () => {{
                    clearTimeout(timeout);
                    resolve(loaded());
                }}, {{once: true}});
                image.addEventListener('error', () => {{
                    clearTimeout(timeout);
                    resolve(false);
                }}, {{once: true}});
            }})"""
        )
        assert is_loaded, f'이미지 로드 실패: {src}'
        return image
