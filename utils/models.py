import os
from typing import Optional, Dict, List

class AlphaTestConfig:
    """
    Cấu hình cho 1 lần chạy test Alpha web.

    Các tham số có thể được truyền trực tiếp hoặc lấy từ biến môi trường (username/password).
    """

    def __init__(
        self,
        username: Optional[str],
        password: Optional[str],
        browser_type: str,
        headless: bool,
        viewport_size: Dict[str, int],
        timeout: int,
        retry_count: int,
        base_url: str,
        screenshot: bool
    ):
        self.username = username or os.getenv("ALPHA_TEST_USER", "sutest01")
        self.password = password or os.getenv("ALPHA_TEST_PASSWORD", "1234aa")
        self.browser_type = browser_type
        self.headless = headless
        self.viewport_size = viewport_size
        self.timeout = timeout
        self.retry_count = retry_count
        self.base_url = base_url
        self.screenshot = screenshot


class TestResult:
    """
    Kết quả chạy một ca kiểm thử, bao gồm trạng thái, lỗi, thời gian và ảnh chụp.
    """

    def __init__(self):
        self.success: bool = False
        self.message: str = ""
        self.screenshots: List[str] = []
        self.error: Optional[str] = None
        self.steps_completed: List[str] = []
        self.execution_time: float = 0.0

    def to_dict(self) -> Dict:
        """
        Trả về kết quả dưới dạng dict để tiện trả JSON cho MCP tool.

        Returns:
            dict: Thông tin chi tiết kết quả test.
        """
        return {
            "success": self.success,
            "message": self.message,
            "screenshots": self.screenshots,
            "error": self.error,
            "steps_completed": self.steps_completed,
            "execution_time": self.execution_time
        }
