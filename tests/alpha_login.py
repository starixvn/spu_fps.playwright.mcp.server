import logging
from typing import Any, Dict, Optional, List
from mcp.server.fastmcp import FastMCP
from playwright.async_api import Page, Browser, async_playwright, BrowserContext
import os
from datetime import datetime
from enum import Enum
import asyncio

# MCP Server init
mcp = FastMCP("alpha_test")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Enum cho browser
class BrowserType(str, Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"

# Kết quả test
class TestResult:
    def __init__(self):
        self.success: bool = False
        self.message: str = ""
        self.screenshots: List[str] = []
        self.error: Optional[str] = None
        self.steps_completed: List[str] = []
        self.execution_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "screenshots": self.screenshots,
            "error": self.error,
            "steps_completed": self.steps_completed,
            "execution_time": self.execution_time
        }

# Cấu hình test
class AlphaTestConfig:
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        browser_type: BrowserType = BrowserType.CHROMIUM,
        headless: bool = False,
        screenshot_dir: str = "screenshots",
        viewport_size: Dict[str, int] = {"width": 1280, "height": 720},
        timeout: int = 30000,
        retry_count: int = 3,
        base_url: str = "https://alp8.nexdev.net"
    ):
        self.username = username or os.getenv('ALPHA_TEST_USER', 'sutest01')
        self.password = password or os.getenv('ALPHA_TEST_PASSWORD', '1234aa')
        self.browser_type = browser_type
        self.headless = headless
        self.screenshot_dir = screenshot_dir
        self.viewport_size = viewport_size
        self.timeout = timeout
        self.retry_count = retry_count
        self.base_url = base_url

# Chụp ảnh
async def take_screenshot(page: Page, name: str, config: AlphaTestConfig, result: TestResult) -> None:
    try:
        os.makedirs(config.screenshot_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{config.screenshot_dir}/{name}_{timestamp}.png"
        await page.screenshot(path=filename)
        result.screenshots.append(filename)
        logging.info(f"Screenshot saved: {filename}")
    except Exception as e:
        logging.error(f"Failed to take screenshot: {str(e)}")
        result.error = f"Screenshot failed: {str(e)}"

# Retry lại thao tác
async def retry_action(action, max_retries: int = 3) -> Any:
    for attempt in range(max_retries):
        try:
            return await action()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(2 ** attempt)

# ✅ MCP TOOL với docstring chi tiết
@mcp.tool()
async def test_alpha_login_flow(
    username: Optional[str] = None,
    password: Optional[str] = None,
    browser_type: str = "chromium",
    headless: bool = False,
    viewport_width: int = 800,
    viewport_height: int = 600,
    timeout: int = 30000,
    retry_count: int = 3,
    base_url: Optional[str] = None,
    take_screenshots: bool = True,
    environment: str = "default"
) -> Dict[str, Any]:
    """
    Test the alpha login flow with flexible configuration.

    Args:
        username (Optional[str]): Optional test username. Defaults to env ALPHA_TEST_USER or 'sutest01'.
        password (Optional[str]): Optional test password. Defaults to env ALPHA_TEST_PASSWORD or '1234aa'.
        browser_type (str): Browser to use: 'chromium', 'firefox', or 'webkit'.
        headless (bool): Run browser in headless mode.
        viewport_width (int): Browser width in pixels.
        viewport_height (int): Browser height in pixels.
        timeout (int): Timeout in ms for Playwright operations.
        retry_count (int): Number of retries for each failed action.
        base_url (Optional[str]): Website URL to test. Defaults to 'https://alp8.nexdev.net'.
        take_screenshots (bool): Capture screenshots during steps.
        environment (str): Test environment name (default/test/production...).

    Returns:
        Dict[str, Any]: Result object including success status, screenshots, steps, and error message.
    """
    config = AlphaTestConfig(
        username=username,
        password=password,
        browser_type=BrowserType(browser_type),
        headless=headless,
        viewport_size={"width": viewport_width, "height": viewport_height},
        timeout=timeout,
        retry_count=retry_count,
        base_url=base_url or "https://alp8.nexdev.net"
    )

    result = TestResult()
    start_time = datetime.now()

    try:
        async with async_playwright() as p:
            browser_types = {
                BrowserType.CHROMIUM: p.chromium,
                BrowserType.FIREFOX: p.firefox,
                BrowserType.WEBKIT: p.webkit
            }

            browser = await browser_types[config.browser_type].launch(headless=config.headless)
            context = await browser.new_context(viewport=config.viewport_size)
            page = await context.new_page()

            # Bắt đầu điều hướng
            logging.info(f"Navigating to {config.base_url}")
            await retry_action(lambda: page.goto(config.base_url, timeout=config.timeout), config.retry_count)
            result.steps_completed.append("navigation")

            if take_screenshots:
                await take_screenshot(page, "initial_page", config, result)

            await retry_action(lambda: page.wait_for_selector('#txtUserName', timeout=config.timeout), config.retry_count)
            await page.fill('#txtUserName', config.username)

            if take_screenshots:
                await take_screenshot(page, "before_verify", config, result)

            await page.click('#btnVerify')
            await page.wait_for_selector('#loginRegion', timeout=config.timeout)
            result.steps_completed.append("username_verification")

            await retry_action(lambda: page.wait_for_selector('#txtPassWord', timeout=config.timeout), config.retry_count)
            await page.fill('#txtPassWord', config.password)

            if take_screenshots:
                await take_screenshot(page, "before_login", config, result)

            await page.click('#btnLogin')
            await page.wait_for_load_state("networkidle")
            result.steps_completed.append("password_submission")

            if take_screenshots:
                await take_screenshot(page, "after_login", config, result)

            await browser.close()
            result.success = True
            result.message = "Successfully completed login flow test"

    except Exception as e:
        error_msg = f"Test failed with error: {str(e)}"
        logging.error(error_msg)
        result.error = error_msg
    finally:
        result.execution_time = (datetime.now() - start_time).total_seconds()

    return result.to_dict()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')