import asyncio
import logging
from typing import Any

# Ghi nhận một bước test đã hoàn tất, tiện log và lưu kết quả
def log_step(result, step: str):
    """
    Ghi lại bước test đã thực hiện và log ra console.

    Args:
        result: Đối tượng TestResult để cập nhật trạng thái.
        step (str): Tên bước đã hoàn thành.
    """
    result.steps_completed.append(step)
    logging.info(f"[STEP] {step}")

# Retry lại một hành động async nhiều lần với exponential backoff
async def retry_action(action, max_retries: int = 3) -> Any:
    """
    Lặp lại một hành động async tối đa N lần nếu có lỗi.

    Args:
        action: Hàm async không có đối số.
        max_retries (int): Số lần thử lại tối đa.

    Returns:
        Kết quả từ action nếu thành công.

    Raises:
        Exception: Lỗi cuối cùng nếu vẫn thất bại sau nhiều lần thử.
    """
    for attempt in range(max_retries):
        try:
            return await action()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = 2 ** attempt
            logging.warning(f"[RETRY] Attempt {attempt + 1} failed, retrying in {delay}s...")
            await asyncio.sleep(delay)

# Mapping các environment → URL thực tế
ENV_URLS = {
    "default": "https://alp8.nexdev.net",
    "test": "https://test.example.com",
    "prod": "https://prod.example.com"
}
