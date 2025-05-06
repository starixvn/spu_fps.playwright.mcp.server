
# 🔐 Alpha Login Test with MCP + Playwright

Dự án này cung cấp một công cụ kiểm thử tự động (automation test tool) cho flow đăng nhập trang web Alpha, sử dụng [Playwright](https://playwright.dev/) kết hợp với [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Kết quả test được thiết kế để tích hợp với hệ thống MCP-based AI Agent hoặc automation runner.

---

## 📁 Cấu trúc thư mục

```
.
├── main.py                # Điểm khởi động MCP server
├── alpha_login.py         # Tool kiểm thử chính (login flow)
├── helpers.py             # Hàm tiện ích hỗ trợ retry, logging
├── models.py              # Định nghĩa cấu hình test và kết quả test
├── alpha_login.cpython... # Bytecode (auto-generated)
└── README.md              # Tài liệu này
```

---

## 🚀 Chạy thử nghiệm

### 1. Cài đặt dependencies

```bash
pip install playwright
pip install mcp
playwright install
```

### 2. Thiết lập biến môi trường (tuỳ chọn)

```bash
export ALPHA_TEST_USER=sutest01
export ALPHA_TEST_PASSWORD=1234aa
```

### 3. Chạy server MCP

```bash
python main.py
```

Server sẽ lắng nghe qua `stdio` và có thể được tích hợp vào các công cụ AI Agent như Claude, ChatGPT hoặc các hệ thống automation nội bộ.

---

## 🧪 Tool đã đăng ký

### `test_alpha_login_flow`

Chạy test login bằng Playwright, với các bước:

1. Truy cập trang đăng nhập
2. Nhập username và xác nhận
3. Nhập mật khẩu và submit
4. Kiểm tra trạng thái đăng nhập thành công

#### Tham số

| Tên tham số      | Kiểu       | Mặc định       | Mô tả |
|------------------|------------|----------------|------|
| username         | Optional[str] | env           | Tên đăng nhập |
| password         | Optional[str] | env           | Mật khẩu |
| browser_type     | str        | "chromium"     | Trình duyệt (chromium, firefox, webkit) |
| headless         | bool       | True           | Có hiển thị giao diện không |
| viewport_width   | int        | 1280           | Chiều rộng cửa sổ trình duyệt |
| viewport_height  | int        | 720            | Chiều cao cửa sổ trình duyệt |
| timeout          | int        | 30000          | Thời gian timeout cho mỗi hành động |
| retry_count      | int        | 3              | Số lần retry khi lỗi |
| base_url         | Optional[str] | ENV_URLS      | URL trang login |
| take_screenshots | bool       | True           | Có chụp ảnh màn hình không |
| environment      | str        | "default"      | `default`, `test`, `prod` |

#### Kết quả

Trả về dictionary chứa:
- `success`: kết quả test
- `message`: thông điệp mô tả
- `error`: lỗi nếu có
- `screenshots`: các ảnh chụp (nếu có)
- `steps_completed`: danh sách các bước đã hoàn thành
- `execution_time`: thời gian thực thi

---

## 🛠 Kỹ thuật nổi bật

- ✅ **Playwright async**: Kiểm thử UI đa trình duyệt.
- ✅ **Retry với backoff**: Tự động thử lại bước test nếu thất bại tạm thời.
- ✅ **Tích hợp MCP server**: Sẵn sàng để tương tác với các AI Agent hoặc workflow automation.

---

## 📌 Ghi chú

- Code được tổ chức rõ ràng theo `helpers`, `models`, `main`, `test tool`.
- Có thể mở rộng thêm nhiều công cụ test khác bằng cách tạo hàm mới và dùng `@tool(...)`.
- Được thiết kế để dễ dàng nhúng vào hệ thống kiểm thử tự động hoặc trợ lý AI.

---

## 📧 Liên hệ

Liên hệ nhóm phát triển để biết thêm chi tiết hoặc tích hợp vào workflow riêng của bạn.
