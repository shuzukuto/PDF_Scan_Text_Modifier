# Hướng Dẫn Sử Dụng Script Chỉnh Sửa File PDF Scan (`edit_scanned_pdf.py`)

Bộ công cụ chuyên biệt để chỉnh sửa tài liệu dạng **ảnh scan từ máy quét** (báo giá, hợp đồng, hóa đơn, chứng từ `CCF_...`).

Điểm đột phá của phiên bản mới là **Cơ chế Tự Động Khớp Thuộc Tính 100% (Auto-Matching)**: Script tự động phân tích chữ cũ trước khi xóa để nhận diện chính xác kiểu chữ (**ĐẬM / NGHIÊNG / ĐỨNG**), đo cỡ font, xác định chân chữ (baseline), hút màu mực scan thực tế và hòa màu nền giấy. Bạn không cần phải đoán hay chỉnh tay phức tạp.

---

## MỤC LỤC
0. [🌟 Giao Diện Web Studio Trực Quan (Chạy 1-chạm `run_scaned_pdf_modifier.bat`)](#0-giao-diện-web-studio-trực-quan-chạy-1-chạm-run_scaned_pdf_modifierbat)
   - [Cách 1: Khởi chạy 1-chạm Tất Cả Trong Một (`run_scaned_pdf_modifier.bat`)](#cách-1-khởi-chạy-1-chạm-tất-cả-trong-một-run_scaned_pdf_modifierbat)
   - [Cách 2: Tự động cài đặt 1-click cho máy mới tinh (`cai_dat_tu_dong.bat`)](#cách-2-tự-động-cài-đặt-1-click-cho-máy-mới-tinh-cai_dat_tu_dongbat)
   - [Các tính năng vượt trội của Giao diện Studio](#các-tính-năng-vượt-trội-của-giao-diện-studio)
1. [Hướng Dẫn Cài Đặt Dành Cho Người Mới (Không Cần Biết Lập Trình)](#1-hướng-dẫn-cài-đặt-dành-cho-người-mới-không-cần-biết-lập-trình)
   - [Bước 1: Cài đặt Python trên máy tính Windows](#bước-1-cài-đặt-python-trên-máy-tính-windows-nếu-chưa-có)
   - [Bước 2: Mở cửa sổ dòng lệnh tại thư mục làm việc](#bước-2-mở-cửa-sổ-dòng-lệnh-ngay-tại-thư-mục-chứa-file)
   - [Bước 3: Cài đặt các thư viện cần thiết bằng 1 lệnh duy nhất](#bước-3-cài-đặt-các-thư-viện-cần-thiết-bằng-1-lệnh-duy-nhất)
   - [Bước 4: Kiểm tra cài đặt thành công](#bước-4-kiểm-tra-cài-đặt-thành-công)
   - [Xử lý các lỗi thường gặp của người mới](#xử-lý-các-lỗi-thường-gặp-troubleshooting)
2. [Cơ chế Tự Động Khớp Thuộc Tính (Auto-Detect)](#2-cơ-chế-tự-động-khớp-thuộc-tính-auto-detect)
3. [Cách Xác Định Tọa Độ Và Bóc Tách Thuộc Tính](#3-cách-xác-định-tọa-độ-và-bóc-tách-thuộc-tính)
   - [Cách 1: Lệnh `pick` (Có Zoom 2 bước thông minh - Khuyên dùng)](#cách-1-lệnh-pick-có-zoom-2-bước-thông-minh---khuyên-dùng)
   - [Cách 2: Lệnh `find` (Tìm nhanh bằng ảnh chụp màn hình)](#cách-2-lệnh-find-tìm-nhanh-bằng-ảnh-chụp-màn-hình)
   - [Cách 3: Lệnh `extract` (Xem tọa độ bằng MS Paint)](#cách-3-lệnh-extract-xem-tọa-độ-thủ-công-bằng-ms-paint)
4. [Giải Thích Bảng Phân Tích Thuộc Tính Của Lệnh `pick`](#4-giải-thích-bảng-phân-tích-thuộc-tính-của-lệnh-pick)
5. [Hướng Dẫn Chi Tiết Toàn Diện Về Lệnh `replace`, `insert` Và Các Tham Số](#5-hướng-dẫn-chi-tiết-toàn-diện-về-lệnh-replace-insert-và-các-tham-số)
   - [5.1. So Sánh Nhanh & Khi Nào Dùng Lệnh Nào?](#51-so-sánh-nhanh--khi-nào-dùng-lệnh-nào)
   - [5.2. Lệnh `replace` — Xóa Chữ Cũ Và Thay Thế Bằng Chữ Mới](#52-lệnh-replace--xóa-chữ-cũ-và-thay-thế-bằng-chữ-mới)
   - [5.3. Lệnh `insert` — Chèn Chữ Mới Vào Tọa Độ Trống](#53-lệnh-insert--chèn-chữ-mới-vào-tọa-độ-trống)
   - [5.4. Bảng Tra Cứu Toàn Diện Mức Độ Rỗ (`-r` hoặc `--roughness`)](#54-bảng-tra-cứu-toàn-diện-mức-độ-rỗ--r-hoặc---roughness)
   - [5.5. Các Lệnh Tiện Ích Hỗ Trợ Khác (`preview`, `extract`)](#55-các-lệnh-tiện-ích-hỗ-trợ-khác-preview-extract)
6. [Toàn Bộ 10 Ví Dụ Thực Tế & Câu Lệnh Mẫu Ăn Liền](#6-toàn-bộ-10-ví-dụ-thực-tế--câu-lệnh-mẫu-ăn-liền)
   - [Ví dụ 1: Sửa số lượng, đơn giá dòng chi tiết (Chữ thường)](#ví-dụ-1-sửa-số-lượng-đơn-giá-dòng-chi-tiết-chữ-thường)
   - [Ví dụ 2: Sửa số tiền Tổng phụ, VAT, Tổng thanh toán (Chữ ĐẬM khớp 100%)](#ví-dụ-2-sửa-số-tiền-tổng-phụ-vat-tổng-thanh-toán-chữ-đậm-bold-khớp-100)
   - [Ví dụ 3: Sửa ngày tháng năm (Chữ NGHIÊNG Italic)](#ví-dụ-3-sửa-ngày-tháng-năm-chữ-nghiêng-italic)
   - [Ví dụ 4: Sửa Tên công ty / Tiêu đề chứng từ (Chữ ĐẬM in hoa)](#ví-dụ-4-sửa-tên-công-ty--tiêu-đề-chứng-từ-chữ-đậm-in-hoa)
   - [Ví dụ 5: Sửa Địa chỉ, Điện thoại, Email (Văn bản dài căn trái)](#ví-dụ-5-sửa-địa-chỉ-điện-thoại-email-văn-bản-dài-căn-trái)
   - [Ví dụ 6: Sửa Số báo giá, Số hợp đồng, Mã chứng từ](#ví-dụ-6-sửa-số-báo-giá-số-hợp-đồng-mã-chứng-từ)
   - [Ví dụ 7: Xóa trắng hoàn toàn một vùng (Xóa bỏ nội dung thừa)](#ví-dụ-7-xóa-trắng-hoàn-toàn-một-vùng-xóa-bỏ-nội-dung-thừa)
   - [Ví dụ 8: Điền thêm số vào chỗ trống chấm chấm `...`](#ví-dụ-8-điền-thêm-số-vào-chỗ-trống-chấm-chấm-)
   - [Ví dụ 9: Sửa trên trang scan nền xám, ngả vàng hoặc scan màu](#ví-dụ-9-sửa-trên-trang-scan-nền-xám-ngả-vàng-hoặc-scan-màu)
   - [Ví dụ 10: Chạy script Python tự động sửa hàng loạt nhiều ô](#ví-dụ-10-chạy-script-python-tự-động-sửa-hàng-loạt-nhiều-ô)
7. [Bảng Tra Cứu Font Chữ Windows Tương Thích](#7-bảng-tra-cứu-font-chữ-windows-tương-thích)
8. [Bí Quyết Giúp Chữ Mới Tự Nhiên Tuyệt Đối](#8-bí-quyết-giúp-chữ-mới-tự-nhiên-tuyệt-đối)

---

## 0. Giao Diện Web Studio Trực Quan (Chạy 1-Chạm `run_scaned_pdf_modifier.bat`)

Dành cho người dùng muốn chỉnh sửa trực quan trên màn hình kéo thả chuột thay vì gõ lệnh trong cửa sổ console:

```text
       ┌─────────────────────────────────────────────────────────────┐
       │     PDF SCAN TEXT MODIFIER STUDIO — GIAO DIỆN CHUYÊN NGHIỆP  │
       ├─────────────────┬───────────────────────────┬───────────────┤
       │ 📄 Danh sách    │ 🖼️ Canvas Tương Tác       │ ⚙️ Bóc Tách   │
       │    các trang    │   • Kéo chuột chọn vùng   │   & Bộ Sửa    │
       │    Thumbnail    │   • Kính lúp phóng đại 3x │   • Roughness │
       │    1, 2, 3...   │   • Tọa độ HUD & Baseline │   • Before /  │
       │                 │   • Pan & Zoom 10% - 600% │     After     │
       └─────────────────┴───────────────────────────┴───────────────┘
```

### Cách 1: Khởi chạy 1-chạm Tất Cả Trong Một (`run_scaned_pdf_modifier.bat`)
- Nhấp đúp chuột vào file duy nhất **`run_scaned_pdf_modifier.bat`** ngay trong thư mục dự án.
- File này được tích hợp thông minh **Run & Use (Chạy là Dùng Ngay)**:
  1. **Tự động cấu hình tên miền riêng**: Thiết lập tên miền riêng **`http://pdfscanmodifier:8000/`** vào hệ thống (không lo trùng cổng hay trùng URL với bất kỳ phần mềm nào khác).
  2. **Ưu tiên chạy bản độc lập không cần Python**: Tự động phát hiện và khởi động ngay file EXE đóng gói độc lập (`dist\PDF_Scan_Modifier\PDF_Scan_Modifier.exe`).
  3. **Tự động chuyển tiếp Python**: Nếu chạy từ source code, file sẽ tự động gọi môi trường Python có sẵn trên máy để bật ứng dụng.
  4. Tự động bật máy chủ và mở trình duyệt web lên màn hình chỉ trong 1 giây!

### Cách 2: Tự động cài đặt 1-click cho máy mới tinh (`cai_dat_tu_dong.bat`)
- Dành cho trường hợp gửi mã nguồn cho người khác trên máy tính mới chưa có Python:
  - Chỉ cần nhấp đúp vào file **`cai_dat_tu_dong.bat`**, máy tính sẽ tự động tải Python chính thức, tự cài ngầm, tự tải toàn bộ thư viện và mở ứng dụng cho bạn từ A đến Z!

### Các tính năng vượt trội của Giao diện Studio:
- 🖱️ **Kéo quét chọn vùng trực quan (Interactive ROI):** Dùng chuột kéo chọn bất kỳ vùng chữ nào trên trang scan, có 8 điểm nắn chỉnh kích thước (handles) và hiển thị tọa độ pixel gốc ngay lập tức.
- 🔬 **Kính lúp kiểm tra hạt mực (Magnifier Loupe):** Nhấn phím `M` để bật kính lúp 3x soi rõ từng chấm rỗ thớ giấy và viền nét chữ scan gốc.
- ⚡ **Bóc tách 1 chạm (Smart Inspector):** Tự động phát hiện cỡ font (pt), kiểu dáng (Đậm/Nghiêng/Đứng), độ dày nét (stroke), mật độ mực (%), màu mực in, màu nền giấy và **đường chân chữ Baseline Y**.
- 🎚️ **Thanh trượt độ rỗ thời gian thực (Roughness Slider):** Tùy chỉnh mức độ rỗ từ `0.0` (phẳng mịn) đến `2.0` (rỗ thô scan) với các nút chọn nhanh: *Tắt (0.0)*, *Mịn (0.6)*, *Chuẩn scan (1.0)*, *Rỗ đậm (1.4)*.
- ↔️ **Thanh trượt so sánh Trước / Sau (Before & After Split View):** Vuốt thanh phân cách để đối chiếu trực tiếp chất lượng chữ mới so với chữ cũ trước khi xuất file.
- 📋 **Hàng đợi sửa hàng loạt (Batch Queue):** Thêm nhiều vị trí cần sửa trên nhiều trang, bật/tắt từng mục tùy ý.
- 💾 **Lưu & Nạp công thức JSON (Recipe):** Lưu lại toàn bộ danh sách tọa độ và nội dung sửa thành file `.json` để dùng lại cho các tài liệu tương tự.
- 📥 **Xuất PDF chuẩn 300 DPI:** Nhấn nút "Xuất PDF", hệ thống tự động xử lý và tải file PDF hoàn chỉnh về máy tính.

---

## 1. Hướng Dẫn Cài Đặt Dành Cho Người Mới (Không Cần Biết Lập Trình)

Dù bạn chưa từng lập trình bao giờ, chỉ cần làm theo **đúng 4 bước đơn giản** dưới đây là có thể sử dụng được ngay:

### Bước 1: Cài đặt Python trên máy tính Windows (nếu chưa có)
1. Truy cập trang web chính thức: [python.org/downloads](https://www.python.org/downloads/) và bấm nút màu vàng **Download Python** (phiên bản 3.10, 3.11 hoặc 3.12 đều tốt).
2. Mở file cài đặt vừa tải về.
3. ⚠️ **BƯỚC QUAN TRỌNG NHẤT:** Ở màn hình cài đặt đầu tiên, bạn nhìn xuống dưới cùng và **BẮT BUỘC TÍCH VÀO Ô VUÔNG**:
   > ☑ **Add python.exe to PATH** (hoặc *Add Python to environment variables*)
   *(Nếu không tích ô này, máy tính sẽ không nhận lệnh `python` trong cửa sổ dòng lệnh).*
4. Nhấn **Install Now** và chờ khoảng 1 phút cho cài đặt hoàn tất, sau đó bấm **Close**.

---

### Bước 2: Mở cửa sổ dòng lệnh ngay tại thư mục chứa file
Bạn **không cần** phải gõ lệnh chuyển thư mục phức tạp (`cd ...`), chỉ cần làm mẹo sau:
1. Mở thư mục đang chứa file PDF và file script `edit_scanned_pdf.py` bằng trình duyệt file của Windows (File Explorer).
2. Nhấp chuột trái vào **Thanh địa chỉ ở trên cùng** của cửa sổ thư mục (nơi đang hiển thị đường dẫn thư mục).
3. Gõ chữ `cmd` hoặc `powershell` rồi nhấn phím **Enter**.
4. Cửa sổ dòng lệnh màu đen (hoặc xanh) sẽ hiện ra ngay lập tức tại đúng thư mục của bạn!

---

### Bước 3: Cài đặt các thư viện cần thiết bằng 1 lệnh duy nhất
Tại cửa sổ dòng lệnh vừa mở, bạn copy dòng lệnh sau, dán vào và nhấn **Enter**:

```bash
pip install -r requirements.txt
```

*(Hoặc nếu bạn muốn gõ trực tiếp tên các thư viện thì chạy lệnh sau):*
```bash
pip install pymupdf pillow opencv-python numpy
```

Chờ máy tính tải và cài đặt trong khoảng 30 giây đến 1 phút cho đến khi hiện chữ `Successfully installed...`.

#### 💡 Giải thích dễ hiểu vai trò của từng thư viện:
- **`pymupdf` (fitz):** Dùng để đọc file PDF, trích xuất từng trang scan ra ảnh với độ phân giải gốc siêu nét và lưu lại file PDF thành phẩm.
- **`pillow` (PIL):** Dùng để vẽ chữ mới đè lên ảnh scan với đúng font chữ, kích cỡ và màu sắc như thiết kế.
- **`opencv-python`:** Bộ não thị giác máy tính - mở cửa sổ tương tác để bạn chọn vùng cần sửa, phóng to khu vực (Zoom), đo độ dày nét chữ để phân biệt chữ Đậm/Thường, và hòa màu nền giấy.
- **`numpy`:** Thư viện tính toán ma trận điểm ảnh (pixel) để xử lý quang phổ màu mực và làm mịn hạt scan tự nhiên.

---

### Bước 4: Kiểm tra cài đặt thành công
Gõ lệnh sau vào cửa sổ dòng lệnh và nhấn **Enter**:

```bash
python edit_scanned_pdf.py --help
```

Nếu màn hình hiển thị danh sách trợ giúp các lệnh:
```text
usage: edit_scanned_pdf.py [-h] {extract,pick,find,preview,insert,replace} ...
Công cụ chỉnh sửa văn bản trong PDF scan (Khớp 100% thuộc tính chữ gốc).
```
👉 **Chúc mừng bạn! Bạn đã cài đặt thành công 100% và có thể bắt đầu chỉnh sửa PDF ngay.**

---

### Xử lý các lỗi thường gặp (Troubleshooting)

| Hiện tượng / Báo lỗi | Nguyên nhân | Cách khắc phục cực nhanh |
| :--- | :--- | :--- |
| `'python' is not recognized as an internal or external command...` | Khi cài Python bạn đã **quên tích ô "Add python.exe to PATH"** | Chạy lại file cài đặt Python, chọn **Modify** hoặc cài lại và nhớ **tích vào ô "Add python.exe to PATH"**. Sau đó đóng cửa sổ cmd mở lại. |
| `'pip' is not recognized...` | Biến môi trường pip chưa được nhận diện | Gõ lệnh thay thế: `python -m pip install -r requirements.txt` |
| `No module named 'fitz'` hoặc `cv2` | Chưa cài thư viện hoặc cài vào phiên bản Python khác | Chạy lại: `python -m pip install pymupdf pillow opencv-python numpy` |
| Bấm phím chuột trong cửa sổ `pick` nhưng không phản hồi | Chưa nhấn đúng phím hoàn thành | Sau khi kéo chuột khoanh vùng chữ nhật xong, nhấn phím **ENTER** hoặc phím **SPACE** (phím cách). Muốn hủy bỏ thì nhấn phím **c**. |

---

## 2. Cơ Chế Tự Động Khớp Thuộc Tính (Auto-Detect)

Ở các phiên bản trước, người dùng thường gặp vấn đề: chữ cũ in đậm (Bold) nhưng chữ mới thay thế lại bị in thường (Regular), hoặc màu chữ quá đen sắc nhọn làm lộ vết chỉnh sửa.

Phiên bản hiện tại tích hợp **thuật toán phân tích thị giác máy tính chuyên sâu**:
- **Độ dày nét ký tự (Stroke Width):** Dùng thuật toán biến đổi khoảng cách Euclid (`distanceTransform`) trên từng nét chữ liên thông để đo độ dày xương sống nét chữ và độ dày cực đại. Phân biệt chính xác tuyệt đối chữ **ĐẬM (Bold)** với chữ **THƯỜNG (Regular)**.
- **Mật độ phủ mực (Ink Density):** Tính toán tỷ lệ mực quang học trong vùng lõi văn bản (chữ đậm ~48-55%, chữ thường ~30-40%).
- **Góc nghiêng (Skew/Slant Angle):** Đo góc lệch nét dọc để nhận diện chữ **NGHIÊNG (Italic)**.
- **Hút màu mực quét thực tế (Ink Color Sampling):** Không dùng màu đen thuần túy `(0, 0, 0)` của máy in điện tử mà tự động lấy mẫu quang phổ các pixel tối nhất của chữ scan cũ (thường là xám chì `RGB(74, 75, 81)`).
- **Độ rỗ thớ giấy & Điểm rỗ vi hạt scan (Scan Roughness & Micro-Pores):** Văn bản in ra giấy rồi scan qua máy quét **không bao giờ là các khối màu phẳng lì như vector máy tính**. Script tự động mô phỏng đầy đủ:
  + **Điểm rỗ (Micro-Pores / Pinhole Voids):** Tái tạo các vi lỗ bọt khí mực li ti và các khe lõm của thớ sợi giấy lộ sáng bên trong nét chữ.
  + **Viền chữ gồ ghề tự nhiên (Edge Roughness & Jitter):** Khử hoàn toàn cảm giác mép viền thẳng tắp của đồ họa vi tính, thay bằng đường biên hơi gợn theo thớ giấy scan thật.
  + **Hạt mực scan đa tầng (Multi-Scale Toner Grain):** Phân bố quang phổ hạt mực với độ sâu lõi chữ (Centerline Core Darkening - giữa nét đậm hơn, mép nét nhạt dần).
  + **Tái tạo kết cấu giấy nền khi xóa (Paper Background Grain Inpainting):** Vùng bị xóa được điền đầy bằng màu giấy nền kết hợp với độ nhiễu hạt sensor (std ~ 1.8..3.0) của chính trang giấy scan đó, không để lại mảng chữ nhật phẳng lì.
  +- **Tùy chỉnh linh hoạt qua cờ `-r` hoặc `--roughness`:** Mặc định là `1.0` (tự nhiên nhất). Bạn có thể chỉnh theo số thực `0.0 .. 2.0` hoặc dùng tên mức độ:
    + `-r off` / `0.0`: Tắt hoàn toàn độ rỗ (vùng xóa phẳng sạch, chữ phẳng mịn).
    + `-r low` / `0.6`: Độ rỗ nhẹ cho bản in nét thanh, giấy mịn.
    + `-r med` / `1.0`: Mức chuẩn tự nhiên mặc định cho scan máy quét văn phòng.
    + `-r high` / `1.4`: Độ rỗ đậm cho giấy scan xơ thô hoặc máy photocopy cũ.
- **Tự căn lề thông minh (Auto Alignment):** Tự động căn lề phải (`right`) cho các chuỗi số/tiền tệ và căn giữa (`center`) cho từ ngữ.

> **Lợi ích:** Khi chạy lệnh `replace`, bạn **không cần gõ `--font`, `--size`, `--color`**. Script sẽ tự động làm tất cả để chữ mới khớp 100% với văn bản gốc cả về hình dáng, màu mực lẫn độ rỗ scan!

---

## 3. Cách Xác Định Tọa Độ Và Bóc Tách Thuộc Tính

### Cách 1: Lệnh `pick` (Có Zoom 2 bước thông minh - Khuyên dùng)
```bash
python edit_scanned_pdf.py pick --pdf "CCF_000372_.pdf"
```

**Quy trình 2 bước cực kỳ dễ làm:**
1. **Bước 1 (Toàn cảnh):** Cửa sổ tài liệu toàn trang sẽ mở ra. Bạn dùng chuột **kéo một ô chữ nhật bao quát rộng rãi** xung quanh ô bảng hoặc dòng chữ cần sửa -> Nhấn **ENTER** hoặc **SPACE**.
2. **Bước 2 (Phóng to chi tiết):** Vùng bạn vừa khoanh sẽ được **phóng to sắc nét** (tỷ lệ 100% pixel gốc hoặc phóng đại 2x..3.5x). Bạn nhìn rõ từng nét chữ và vạch kẻ bảng. Lúc này bạn chỉ cần kéo chuột chọn **gọn gàng phần chữ** (tránh chạm vào các đường kẻ bảng) -> Nhấn **ENTER** hoặc **SPACE**.

Ngay lập tức, Terminal sẽ hiển thị toàn bộ thuộc tính chi tiết kèm câu lệnh ăn liền!

*(Mẹo: Thêm `--page 1` nếu muốn chọn ở trang 2; thêm `--no-zoom` nếu chỉ muốn chọn nhanh 1 bước).*

---

### Cách 2: Lệnh `find` (Tìm nhanh bằng ảnh chụp màn hình)
Nếu không muốn mở cửa sổ chọn:
1. Mở file PDF trên màn hình.
2. Nhấn tổ hợp phím **`Win + Shift + S`**, kéo chuột chụp lấy đúng đoạn chữ cần sửa và lưu lại thành `anh_mau.png`.
3. Chạy lệnh:
   ```bash
   python edit_scanned_pdf.py find --pdf "CCF_000372_.pdf" --template "anh_mau.png"
   ```
4. Script sẽ đối chiếu mẫu ảnh và trả về chính xác tọa độ `--box X Y W H`.

---

### Cách 3: Lệnh `extract` (Xem tọa độ thủ công bằng MS Paint)
1. Xuất trang scan ra file ảnh độ phân giải gốc:
   ```bash
   python edit_scanned_pdf.py extract --pdf "CCF_000372_.pdf" --out "trang_scan.jpg"
   ```
2. Mở `trang_scan.jpg` bằng **MS Paint**.
3. Rê chuột vào góc trên bên trái của đoạn chữ cần sửa -> nhìn xuống góc dưới cùng bên trái màn hình MS Paint để đọc tọa độ `X, Y`.
4. Dùng công cụ **Select** kéo bao quanh đoạn chữ -> nhìn thanh trạng thái dưới đáy để đọc kích thước `Width x Height`.

---

## 4. Giải Thích Bảng Phân Tích Thuộc Tính Của Lệnh `pick`

Khi bạn chọn vùng bằng lệnh `pick`, script sẽ phân tích và in ra bảng kết quả trực quan như sau:

```text
============================================================================
[+] CHI TIẾT TOÀN BỘ THUỘC TÍNH VĂN BẢN (TEXT ATTRIBUTES ANALYSIS):
----------------------------------------------------------------------------
  1. TỌA ĐỘ VÀ KÍCH THƯỚC VÙNG CHỌN (ROI):
     • Tọa độ góc trên trái (X, Y)  : X = 2096, Y = 1086
     • Kích thước vùng (W x H)      : Chiều rộng 260 px, Chiều cao 50 px
     • Hộp vùng xóa (cho replace)   : --box 2096 1086 260 50
     • ĐƯỜNG CHÂN CHỮ Y (BASELINE)  : Y = 1129  (dùng trực tiếp cho tham số --y của lệnh insert)

  2. HÌNH THÁI VÀ ĐỊNH DẠNG KÝ TỰ (TYPOGRAPHY):
     • Kiểu dáng chữ (Font Style)   : ĐẬM (Bold)
     • Độ đậm nét (Font Weight)     : ĐẬM (Bold) [Độ dày nét ~5.73 px, cực đại ~11.46 px]
     • Độ nghiêng (Font Slant)      : ĐỨNG (Upright)
     • Chiều cao ký tự thực tế (px) : ~35.0 px
     • Chiều rộng ký tự trung bình  : ~21.0 px
     • Cỡ font quy đổi (Font Size)  : ~52 pt
     • Mật độ phủ mực (Ink Density) : 49.8%

  3. FONT CHỮ WINDOWS TƯƠNG ỨNG:
     • Font chữ chuẩn đề xuất       : timesbd.ttf
     • Các font chữ thay thế        : arialbd.ttf (Arial Bold) / calibrib.ttf (Calibri Bold)

  4. MÀU SẮC VÀ ĐỘ RỖ THỚ GIẤY (COLOR & TEXTURE):
     • Màu mực quét (Ink Color)     : RGB(58, 58, 64)  (Mã Hex: #3A3A40)
     • Màu giấy nền (Paper Color)   : RGB(253, 254, 254)  (Mã Hex: #FDFEFE)
     • Độ rỗ hạt mực (Roughness)    : std ~34.0 (điểm rỗ thớ giấy scan)
     • Độ nhiễu giấy nền (Grain)    : std ~1.85 (kết cấu thớ giấy)
     • Độ mờ tán sắc (Blur Radius)  : 0.38..0.42 (tán sắc tự nhiên)

  5. GỢI Ý CĂN LỀ & TỌA ĐỘ CHÈN (ALIGNMENT & INSERT):
     • Căn lề khuyến nghị           : Căn lề PHẢI (right - số liệu/tiền tệ/bảng tính)
     • Tọa độ chèn mẫu (insert)     : --x 2356 --y 1129
----------------------------------------------------------------------------
[+] CÂU LỆNH MẪU ĂN LIỀN (COPY DÙNG NGAY):

  1. LỆNH THAY THẾ (replace - Tự động xóa cũ & ghi mới, khớp 100% thuộc tính):
     python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "NỘI_DUNG_MỚI"

     * Tùy chọn thêm độ rỗ nếu cần:
       - Rỗ nhiều (giấy xơ thô, scan cũ) : thêm -r 1.3  (hoặc -r high)
       - Rỗ nhẹ (bản in nét thanh, mịn)  : thêm -r 0.6  (hoặc -r low)
       - Tắt rỗ (chữ phẳng sắc nét)      : thêm -r 0.0  (hoặc -r off)

  2. LỆNH CHÈN THÊM (insert - Không xóa nền, chèn đúng đường chân chữ Baseline Y=1129):
     python edit_scanned_pdf.py insert --pdf "CCF_000372_.pdf" --text "NỘI_DUNG_MỚI" --x 2356 --y 1129 --font timesbd.ttf --size 52 --align right
============================================================================
```

### Ý nghĩa từng chỉ số:
1. **Kiểu dáng chữ & Độ đậm nét (Font Style & Weight):** 
   - Nếu là chữ ĐẬM: Script đề xuất `timesbd.ttf` (Times New Roman Bold).
   - Nếu là chữ THƯỜNG: Script đề xuất `times.ttf` (Times New Roman Regular).
   - Nếu là chữ NGHIÊNG: Script đề xuất `timesi.ttf` (Times New Roman Italic).
2. **Cỡ font quy đổi (Font Size):** Cỡ font chuẩn (point size) tương thích với Windows Typography Engine khi in lên độ phân giải scan gốc.
3. **Màu mực & Độ rỗ scan:** Trích xuất màu mực lõi thực tế và độ phân tán hạt mực (`std ~30..34`), giúp nét chữ mới có các điểm rỗ vi mô tự nhiên như bản scan.
4. **Màu giấy & Kết cấu giấy:** Tái tạo thớ giấy nền cục bộ khi xóa, không để lại mảng phẳng trơn láng.
5. **Gợi ý căn lề (Alignment):** Tự động phát hiện loại nội dung để gợi ý lề phải (cho số tiền trong ô) hoặc căn giữa/trái.
6. **Đường chân chữ Y (Baseline):** Script tự động quét toàn bộ đáy ký tự của các chữ cũ trong ô và in ra chính xác tọa độ đường chân chữ `Y`. Bạn chỉ việc copy giá trị `Y` này gán vào lệnh `insert --y <Y>`, **hoàn toàn không cần phải tính toán thủ công rườm rà**.

## 5. Hướng Dẫn Chi Tiết Toàn Diện Về Lệnh `replace`, `insert` Và Các Tham Số

### 5.1. So Sánh Nhanh & Khi Nào Dùng Lệnh Nào?

| Tiêu chí | Lệnh `pick` | Lệnh `replace` | Lệnh `insert` |
| :--- | :--- | :--- | :--- |
| **Mục đích chính** | **Khảo sát & Bóc tách:** Mở cửa sổ zoom tương tác, đo đạc tọa độ và toàn bộ thuộc tính văn bản cũ. | **Xóa cũ & Thay mới:** Xóa vùng chữ cũ bằng màu giấy có thớ hạt và ghi chữ mới tự động khớp 100% thuộc tính. | **Chèn thêm:** Ghi chữ/số vào khoảng trống hoặc dòng chấm `...` mà **không xóa** bất kỳ vùng nền nào. |
| **Đầu vào bắt buộc** | `--pdf` | `--pdf`, `--box X Y W H` | `--pdf`, `--text "..."`, `--x X`, `--y Y` |
| **Cơ chế xử lý nền giấy** | Không can thiệp file | **Tự động xóa nền:** Hòa màu giấy xung quanh + tạo nhiễu thớ giấy tự nhiên (Inpainting) | **Không xóa nền:** Chỉ phủ hạt mực mới đè lên nền giấy hiện tại |
| **Căn lề (Alignment)** | Phân tích & Gợi ý | Tự động căn theo hộp `--box` (số -> `right`, chữ -> `center`) | Căn theo tọa độ điểm mốc `--x` (`left`, `center`, `right`) |
| **Tình huống áp dụng** | Dùng đầu tiên trước khi muốn sửa bất kỳ vị trí nào để lấy tọa độ và thuộc tính. | Sửa số lượng, đơn giá, tổng tiền, thuế VAT, ngày tháng, tên công ty, hoặc xóa trắng nội dung thừa. | Điền số vào chỗ trống chấm chấm `......`, bổ sung số trang, đóng dấu mã hiệu vào lề giấy. |

---

### 5.2. Lệnh `replace` — Xóa Chữ Cũ Và Thay Thế Bằng Chữ Mới (Auto-Matching 100%)

#### 💡 Cơ chế hoạt động 4 bước bên trong lệnh `replace`:
1. **Bước 1 (Bóc tách văn bản cũ):** Trước khi xóa, thuật toán quét vùng `--box` để đo chính xác chiều cao ký tự, độ dày nét (`distanceTransform` để xác định Đậm hay Thường), độ nghiêng nét (Italic), trích xuất dải màu quang phổ mực lõi tối nhất và đo độ nhiễu hạt giấy nền xung quanh.
2. **Bước 2 (Xóa sạch thông minh có kết cấu - Texture Inpainting):** Vùng `--box` được xóa bằng màu giấy nền trung bình kết hợp với việc tái tạo vi nhiễu thớ giấy tự nhiên (`paper_noise`), triệt tiêu hoàn toàn mảng trắng bóc phẳng lì lộ liễu.
3. **Bước 3 (Định vị chân chữ & Căn lề):** Tự động gióng đường chân chữ (Baseline) khớp hàng với văn bản xung quanh. Nếu là số tiền -> căn lề phải (`right`); nếu là từ ngữ -> căn giữa (`center`).
4. **Bước 4 (Vẽ chữ mới mô phỏng scan thật):** Áp dụng điểm rỗ mực li ti (Micro-pores), viền gợn sóng thớ giấy (Edge jitter), hạt tán sắc đa tầng và làm mờ quang học đầu quét (Optical blur), biến chữ mới hoàn toàn tiệp vào trang giấy scan thật.

---

#### 📋 Cú Pháp Tổng Quát Của Lệnh `replace`:
```bash
python edit_scanned_pdf.py replace --pdf <FILE> --box <X Y W H> --text <NỘI_DUNG> [CÁC_THAM_SỐ_TÙY_CHỌN]
```

#### 🔍 Bảng Giải Thích Chi Tiết TẤT CẢ Các Tham Số Của Lệnh `replace`:

| Tham số | Bắt buộc? | Giá trị mặc định | Giải thích chi tiết & Tác dụng | Khi nào nên chỉnh tay? |
| :--- | :---: | :---: | :--- | :--- |
| **`--pdf`** | **BẮT BUỘC** | *Không* | Đường dẫn tới file PDF scan gốc cần chỉnh sửa (ví dụ: `"CCF_000372_.pdf"`). | Luôn phải cung cấp. Nếu đường dẫn có dấu cách, bắt buộc bọc trong dấu ngoặc kép `""`. |
| **`--box X Y W H`** | **BẮT BUỘC** | *Không* | **Bộ 4 số nguyên (pixel)** xác định tọa độ và kích thước khung chữ nhật cần xóa:<br>• `X`: Tọa độ góc trên - bên trái (hoành độ).<br>• `Y`: Tọa độ góc trên - bên trái (tung độ).<br>• `W`: Chiều rộng (Width) của vùng xóa.<br>• `H`: Chiều cao (Height) của vùng xóa. | Lấy trực tiếp từ kết quả in ra của lệnh `pick`. **Mẹo:** Khoanh vừa vặn chữ, chừa mép cách đường kẻ bảng 2-4 px để không bị xóa mất viền kẻ. |
| **`--text`** | Tùy chọn | `""` *(Rỗng)* | Nội dung văn bản/số liệu mới cần ghi đè vào (ví dụ: `"270,750,000"`, `"Hải Phòng, ngày..."`). Hỗ trợ đầy đủ tiếng Việt có dấu Unicode. | **Mẹo Xóa Trắng (Whiteout):** Nếu muốn **xóa bỏ một vùng chữ/dấu mộc thừa** mà không viết gì vào, hãy truyền `--text ""` hoặc không truyền `--text`. |
| **`--font`** | Tùy chọn | `'auto'` | Tên file font chữ TrueType (`.ttf`) trong `C:\Windows\Fonts`.<br>• Khi để `'auto'` (mặc định): Script tự phân tích chữ cũ, nếu chữ cũ là **ĐẬM** -> nạp `timesbd.ttf`; nếu **THƯỜNG** -> nạp `times.ttf`; nếu **NGHIÊNG** -> nạp `timesi.ttf`. | Khi muốn chủ động đổi sang font chữ khác hẳn so với văn bản gốc, ví dụ: `--font arial.ttf`, `--font calibrib.ttf`, `--font GOTHIC.TTF`. |
| **`--size`** | Tùy chọn | `0` *(Tự đo)* | Cỡ font point size nguyên.<br>• Khi để `0` (mặc định): Script tự đo chiều cao ký tự của chữ cũ và quy đổi ra cỡ font tương ứng chính xác 100%. | Khi muốn ép cỡ chữ to hơn hoặc nhỏ hơn so với chữ cũ (ví dụ: `--size 52`, `--size 54`). |
| **`--align`** | Tùy chọn | `'auto'` | Hướng căn lề chữ mới bên trong khung `--box`:<br>• `'auto'` (mặc định): Tự động nhận diện. Nếu `--text` là số liệu/tiền tệ -> căn phải (`right`); nếu là chữ từ ngữ -> căn giữa (`center`).<br>• `right`: Căn mép phải.<br>• `center`: Căn chính giữa.<br>• `left`: Căn mép trái. | • Đặt `right` khi sửa cột số tiền, số lượng trong bảng biểu để thẳng hàng đơn vị.<br>• Đặt `left` khi sửa văn bản dài, tên công ty, địa chỉ, số hợp đồng.<br>• Đặt `center` cho tiêu đề, mã cột ngắn. |
| **`-r`, `--roughness`** | Tùy chọn | `1.0` *(Chuẩn)* | **Hệ số mức độ rỗ thớ giấy và hạt mực scan**:<br>• Nhận số thực: `0.0` đến `2.0` (ví dụ: `1.2`, `1.5`, `0.6`).<br>• Hoặc nhận tên mức: `off` (0.0), `low` (0.6), `med` (1.0), `high` (1.4).<br>*(Xem chi tiết bảng quy đổi ở mục 5.4).* | • Đặt `-r high` (hoặc `1.3..1.5`) khi scan tài liệu cũ giấy xơ thô hoặc photocopy.<br>• Đặt `-r low` (hoặc `0.6`) khi bản scan nét mịn, giấy bóng.<br>• Đặt `-r off` (hoặc `0.0`) khi muốn chữ phẳng mịn tuyệt đối không rỗ. |
| **`--color R G B`** | Tùy chọn | `None` *(Tự hút)* | Màu mực quang phổ (3 số Red Green Blue từ 0-255).<br>• Mặc định: Tự động trích xuất màu mực thực tế của chữ cũ (thường là xám chì `74 75 81`). | Khi muốn đổi màu chữ sang màu mực khác (ví dụ mực xanh `--color 30 50 120` hoặc ép xám đậm `--color 60 60 65`). **Không nên** dùng `0 0 0` đen kịt vì sẽ bị giả tạo. |
| **`--bg-color R G B`** | Tùy chọn | `None` *(Tự lấy)* | Màu nền giấy (3 số Red Green Blue từ 0-255).<br>• Mặc định: Tự lấy mẫu màu trung bình của dải mép viền quanh hộp `--box`. | Khi vùng xóa nằm trên nền giấy màu đặc biệt (giấy ngả vàng, giấy xám chì) mà mép viền bị dính đường kẻ. |
| **`--out`** | Tùy chọn | `None` *(Ghi đè)* | Đường dẫn file PDF thành phẩm xuất ra.<br>• Nếu không truyền: **Ghi đè trực tiếp lên file gốc `--pdf`**.<br>• Nếu có truyền: Tạo ra file PDF mới. | Khuyên bạn nên luôn đặt tên file mới (ví dụ: `--out "CCF_DaSua.pdf"`) trong những lần chạy đầu tiên để kiểm tra kết quả trước khi ghi đè. |

---

#### 🚀 3 Phong Cách Chạy Lệnh `replace` Phổ Biến Nhất:

##### 1. Chế độ Siêu Tự Động (Khuyên Dùng Nhất — Ngắn gọn nhất):
Bạn chỉ cần truyền đúng 3 tham số: `--pdf`, `--box`, `--text`. Script tự động lo từ A đến Z:
```bash
python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "270,750,000" --out "KetQua.pdf"
```

##### 2. Chế độ Tinh Chỉnh Độ Rỗ Nhanh (Thêm cờ `-r`):
```bash
# Thêm độ rỗ hạt mực rõ nét hơn (-r 1.3 hoặc -r high):
python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "270,750,000" -r high

# Giảm độ rỗ cho nét chữ thanh mảnh (-r 0.6 hoặc -r low):
python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "270,750,000" -r low

# Tắt hoàn toàn độ rỗ, chữ phẳng nét mịn (-r off hoặc -r 0.0):
python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "270,750,000" -r off
```

##### 3. Chế độ Xóa Trắng (Bút Xóa Nền Giấy):
Muốn xóa bỏ một con dấu thừa, chữ ký cũ hoặc ô bị in lỗi mà không muốn viết chữ gì:
```bash
python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 1800 2800 350 150 --text ""
```

---

### 5.3. Lệnh `insert` — Chèn Chữ Mới Vào Tọa Độ Trống (Không Xóa Nền)

Lệnh `insert` được dùng khi trang PDF scan của bạn **đã có sẵn một khoảng trống** (ví dụ: mẫu biểu có sẵn dòng chấm chấm `Thời hạn thực hiện: ....... ngày`, hoặc các ô form chưa được điền số liệu). Điểm khác biệt mấu chốt so với `replace` là lệnh này **không xóa bất kỳ vùng nền nào**, nó chỉ phủ lớp mực mới có độ rỗ scan tự nhiên lên đúng tọa độ bạn chỉ định.

#### 📋 Cú Pháp Tổng Quát Của Lệnh `insert`:
```bash
python edit_scanned_pdf.py insert --pdf <FILE> --text <CHỮ> --x <X> --y <Y> [CÁC_THAM_SỐ_TÙY_CHỌN]
```

#### 🔍 Bảng Giải Thích Chi Tiết TẤT CẢ Các Tham Số Của Lệnh `insert`:

| Tham số | Bắt buộc? | Giá trị mặc định | Giải thích chi tiết & Tác dụng | Khi nào nên chỉnh tay? |
| :--- | :---: | :---: | :--- | :--- |
| **`--pdf`** | **BẮT BUỘC** | *Không* | Đường dẫn tới file PDF scan gốc cần chèn chữ. | Luôn phải cung cấp. |
| **`--text`** | **BẮT BUỘC** | *Không* | Nội dung chữ hoặc số cần chèn vào (ví dụ: `"45"`, `"Nguyễn Văn A"`). | Luôn phải cung cấp. |
| **`--x`** | **BẮT BUỘC** | *Không* | **Tọa độ hoành độ X (pixel)** để bắt đầu đặt chữ:<br>• Nếu `--align left`: X là vị trí mép bên trái của chữ đầu tiên.<br>• Nếu `--align center`: X là vị trí điểm chính giữa của toàn bộ đoạn chữ.<br>• Nếu `--align right`: X là vị trí mép bên phải của chữ cuối cùng. | Bắt buộc. Xác định qua lệnh `pick` hoặc mở ảnh bằng MS Paint để xem tọa độ. |
| **`--y`** | **BẮT BUỘC** | *Không* | **Tọa độ tung độ Y (pixel) — ĐÂY LÀ ĐƯỜNG CHÂN CHỮ (BASELINE)**:<br>⚠️ *Lưu ý:* Đây **không phải** là mép trên của chữ, mà là **đường kẻ mà các con chữ đứng lên trên nó** (như dòng kẻ ô ly tập viết).<br>👉 **ĐÃ ĐƯỢC TỰ ĐỘNG HÓA:** Lệnh `pick` giờ đây tự động đo và in sẵn giá trị này (`ĐƯỜNG CHÂN CHỮ Y (BASELINE): Y = ...`), bạn chỉ việc copy dán vào mà **không cần tính toán rườm rà**! |
| **`--font`** | Tùy chọn | `'times.ttf'` | Tên font chữ Windows TrueType (`times.ttf`, `timesbd.ttf`, `timesi.ttf`, `arial.ttf`...). | Đặt `timesbd.ttf` nếu muốn chèn chữ ĐẬM, `timesi.ttf` nếu muốn chèn chữ NGHIÊNG. |
| **`--size`** | Tùy chọn | `52` | Cỡ font chữ (pt). Mặc định `52` tương đương với chữ văn phòng tiêu chuẩn trên độ phân giải scan 300 DPI. | Tăng giảm tùy theo độ rộng hẹp của khoảng trống (ví dụ `--size 48` hoặc `--size 56`). |
| **`--align`** | Tùy chọn | `'left'` | Căn lề của đoạn chữ so với điểm `--x`:<br>• `left`: Chữ phát triển sang bên phải điểm X.<br>• `center`: Chữ mở rộng đều sang hai bên điểm X.<br>• `right`: Chữ kết thúc tại điểm X. | • Dùng `center` khi điền vào giữa khoảng trống chấm chấm `......`.<br>• Dùng `left` khi viết tiếp sau một đoạn văn bản có sẵn. |
| **`-r`, `--roughness`** | Tùy chọn | `1.0` *(Chuẩn)* | Mức độ rỗ của hạt mực scan (`0.0..2.0` hoặc `off`, `low`, `med`, `high`). | Tương tự lệnh `replace`. |
| **`--color R G B`** | Tùy chọn | `55 52 50` | Màu mực scan quang phổ. Mặc định là xám đen chì tự nhiên của mực in trên giấy. | Có thể tùy biến mã màu mong muốn. |
| **`--out`** | Tùy chọn | `None` *(Ghi đè)* | Đường dẫn file PDF kết quả xuất ra. | Khuyên dùng đặt file mới để đối chiếu. |

---

#### 🎯 Cách Lấy Tọa Độ `--x` Và Đường Chân Chữ `--y` Cực Nhanh Từ Lệnh `pick` (Không Cần Tính Toán):

1. **Lấy trực tiếp từ lệnh `pick` (Khuyên dùng nhất — Ăn liền 100%):**
   - Bạn chỉ cần chạy lệnh `pick` khoanh vào một chữ đã có sẵn ở cùng hàng đó.
   - Script tự động đo đáy ký tự thực tế và in ra ngay:
     ```text
     • ĐƯỜNG CHÂN CHỮ Y (BASELINE)  : Y = 1129  (dùng trực tiếp cho tham số --y của lệnh insert)
     • Tọa độ chèn mẫu (insert)     : --x 2356 --y 1129
     ```
   - Đồng thời ở cuối bảng kết quả của `pick`, script đã tạo sẵn câu lệnh mẫu hoàn chỉnh cho `insert`:
     ```bash
     python edit_scanned_pdf.py insert --pdf "CCF_000372_.pdf" --text "NỘI_DUNG_MỚI" --x 2356 --y 1129 --font timesbd.ttf --size 52 --align right
     ```
   - 👉 Bạn chỉ cần **copy nguyên câu lệnh mẫu**, đổi chữ `"NỘI_DUNG_MỚI"` thành nội dung của bạn là xong! Hoàn toàn không mất công tính toán.

2. **Cách tính thủ công (Dành cho ai muốn hiểu nguyên lý hình học):**
   - Nếu bạn đo tọa độ ô bằng MS Paint hoặc các công cụ đồ họa khác:
     $$\text{Y}_{\text{insert (Baseline)}} \approx \text{Y}_{\text{box}} + \text{H}_{\text{box}} - 6 \text{ đến } 10 \text{ px}$$
   - *Ví dụ:* Nếu chữ cùng hàng có mép trên `Y = 1580`, chiều cao `H = 50` thì đường chân chữ `Y` sẽ vào khoảng: $1580 + 50 - 8 = 1622$.

---

### 5.4. Bảng Tra Cứu Toàn Diện Mức Độ Rỗ (`-r` hoặc `--roughness`)

Cả lệnh `replace` và `insert` đều hỗ trợ tham số `-r` (hoặc `--roughness`) để điều chỉnh mức độ rỗ:

| Cách gõ tham số | Giá trị số quy đổi | Mô tả & Tình huống khuyên dùng |
| :--- | :---: | :--- |
| **`-r off`** hoặc **`-r 0.0`** | `0.0` | **Tắt rỗ hoàn toàn:** Chữ phẳng nét, vùng xóa phẳng hoàn toàn. Phù hợp tài liệu PDF kỹ thuật số không qua máy scan. |
| **`-r low`** hoặc **`-r 0.6`** | `0.6` | **Rỗ nhẹ / Nét mịn:** Chữ in laser trên giấy mịn văn phòng, tài liệu scan độ phân giải cao còn mới. |
| **`-r med`** hoặc **`-r 1.0`** | `1.0` *(Mặc định)* | **Chuẩn tự nhiên:** Mô phỏng hoàn hảo độ rỗ vi hạt scan văn phòng thông dụng. |
| **`-r high`** hoặc **`-r 1.4`** | `1.4` | **Rỗ đậm / Giấy thô:** Scan từ bản photocopy cũ, máy quét nhiều bụi hạt, giấy xơ xước. |
| **`-r 1.2` / `-r 1.6`...** | Tự do `0.0..2.0` | Tùy biến tự do bất kỳ số thực nào bạn muốn. |

*(Script cũng tự hiểu các từ tiếng Việt: `-r nhe`, `-r chuan`, `-r dam`, `-r nhieu`, `-r khong`).*

---

### 5.5. Các Lệnh Tiện Ích Hỗ Trợ Khác (`preview`, `extract`)

#### Lệnh `preview` (Cắt xem trước tọa độ)
Giúp xem nhanh vùng cắt để kiểm tra vị trí xem có chạm viền kẻ bảng hay không trước khi thực hiện thay thế:
```bash
python edit_scanned_pdf.py preview --pdf "CCF_000372_.pdf" --crop 2096 1086 260 50 --out "preview.png"
```

#### Lệnh `extract` (Xuất trang scan ra ảnh gốc)
Xuất toàn bộ trang scan ra ảnh chất lượng cao để mở trong MS Paint đo tọa độ thủ công:
```bash
python edit_scanned_pdf.py extract --pdf "CCF_000372_.pdf" --page 0 --out "trang_scan.jpg"
```

---

## 6. Toàn Bộ 10 Ví Dụ Thực Tế & Câu Lệnh Mẫu Ăn Liền

Dưới đây là tổng hợp tất cả các tác vụ phổ biến nhất trên thực tế kèm câu lệnh thực thi ngay:

### Ví dụ 1: Sửa số lượng, đơn giá dòng chi tiết (Chữ thường)
- **Tình huống:** Sửa số lượng dòng hàng từ `5,000` thành `4,750` (chữ đứng, bình thường).
- **Lệnh tự động:**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 1615 992 135 55 --text "4,750" --out "CCF_SuaSoLuong.pdf"
  ```
- **Lệnh chỉ định chi tiết:**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 1615 992 135 55 --text "4,750" --font times.ttf --size 54 --align right --out "CCF_SuaSoLuong.pdf"
  ```

---

### Ví dụ 2: Sửa số tiền Tổng phụ, VAT, Tổng thanh toán (Chữ ĐẬM (Bold) khớp 100%)
- **Tình huống:** Dòng "Cộng tiền hàng" (Subtotal) đang là `256,500,000` (chữ ĐẬM), cần đổi thành `270,750,000` (phải giữ nguyên chữ ĐẬM, cùng màu mực, không bị biến thành chữ thường).
- **Lệnh tự động (Script tự phát hiện chữ Đậm và tự áp dụng `timesbd.ttf`):**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "270,750,000" --out "CCF_SuaSubtotal.pdf"
  ```
- **Lệnh chỉ định chi tiết:**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "270,750,000" --font timesbd.ttf --size 52 --align right --color 74 75 81 --out "CCF_SuaSubtotal.pdf"
  ```

---

### Ví dụ 3: Sửa ngày tháng năm (Chữ NGHIÊNG Italic)
- **Tình huống:** Sửa dòng địa danh ngày tháng ở góc trên báo giá (ví dụ: `Hải Phòng, ngày 10 tháng 9 năm 2026`).
- **Lệnh tự động:**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 1510 460 830 55 --text "Hải Phòng, ngày 15 tháng 9 năm 2026"
  ```
- **Lệnh chỉ định chi tiết:**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 1510 460 830 55 --text "Hải Phòng, ngày 15 tháng 9 năm 2026" --font timesi.ttf --size 52 --align center
  ```

---

### Ví dụ 4: Sửa Tên công ty / Tiêu đề chứng từ (Chữ ĐẬM in hoa)
- **Tình huống:** Sửa tên công ty khách hàng hoặc tiêu đề báo giá với cỡ chữ to và in đậm.
- **Lệnh thực hiện:**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 420 540 1450 65 --text "CÔNG TY TNHH PHÁT TRIỂN CÔNG NGHỆ Á CHÂU" --font timesbd.ttf --size 56 --align left
  ```

---

### Ví dụ 5: Sửa Địa chỉ, Điện thoại, Email (Văn bản dài căn trái)
- **Tình huống:** Sửa địa chỉ khách hàng hoặc người liên hệ trong phần thông tin giao dịch.
- **Lệnh thực hiện:**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 420 610 1200 50 --text "Số 128 Đường Lê Duẩn, Phường Cửa Nam, Quận Hoàn Kiếm, TP. Hà Nội" --font times.ttf --size 48 --align left
  ```

---

### Ví dụ 6: Sửa Số báo giá, Số hợp đồng, Mã chứng từ
- **Tình huống:** Đổi số báo giá từ `BG-2026/08` thành `BG-2026/09-KTS`.
- **Lệnh thực hiện:**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 450 380 400 45 --text "Số: BG-2026/09-KTS" --font times.ttf --size 50 --align left
  ```

---

### Ví dụ 7: Xóa trắng hoàn toàn một vùng (Xóa bỏ nội dung thừa)
- **Tình huống:** Xóa một con dấu cũ, một dòng chữ ghi chú thừa, hoặc xóa trắng một ô mà không viết gì vào:
- **Lệnh thực hiện (chỉ cần truyền `--text ""`):**
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 1800 2800 350 150 --text ""
  ```
  *(Script sẽ hòa màu giấy nền tự nhiên lấp đầy vùng xóa, biến nó thành giấy sạch hoàn toàn).*

---

### Ví dụ 8: Điền thêm số vào chỗ trống chấm chấm `...`
- **Tình huống:** Mẫu biểu có sẵn đoạn in sẵn `Thời hạn giao hàng: ...... ngày`, cần điền số `45` vào chỗ trống mà không muốn xóa dòng chữ xung quanh.
- **Lệnh thực hiện (dùng lệnh `insert`):**
  ```bash
  python edit_scanned_pdf.py insert --pdf "CCF_000372_.pdf" --text "45" --x 820 --y 1580 --font times.ttf --size 50 --align center
  ```

---

### Ví dụ 9: Sửa trên trang scan nền xám, ngả vàng hoặc scan màu
- **Tình huống:** File scan từ máy quét cũ có màu giấy xám đục hoặc vàng ngà.
- Script mặc định tự tính toán dải màu nền xung quanh vùng chọn. Nếu muốn chỉ định chính xác mã màu nền của trang giấy:
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 996 260 53 --text "270,750,000" --bg-color 235 237 230
  ```

---

### Ví dụ 10: Chạy script Python tự động sửa hàng loạt nhiều ô

- **Tình huống:** Bạn cần sửa đồng thời 5 vị trí trên cùng một trang scan: Số lượng, Thành tiền, Thuế VAT, Tổng tiền, hoặc điền thêm ngày tháng, chỉ với **1 lần bấm chạy duy nhất** thay vì phải gõ lệnh terminal 5 lần riêng biệt.
- **Dự án đã tạo sẵn file:** File script mẫu [`sua_hang_loat.py`](file:///f:/TempFiles/New%20folder%20(9)/sua_hang_loat.py) đã có sẵn ngay trong thư mục mã nguồn.

#### ⚠️ HƯỚNG DẪN QUAN TRỌNG VỀ VỊ TRÍ LƯU FILE `sua_hang_loat.py`:
- File `sua_hang_loat.py` **BẮT BUỘC PHẢI ĐẶT CÙNG THƯ MỤC** với file `edit_scanned_pdf.py` và file PDF cần sửa.
- **Lý do:** Lệnh đầu tiên trong script là `from edit_scanned_pdf import ScannedPdfEditor` sẽ nạp bộ não xử lý thị giác máy tính từ file `edit_scanned_pdf.py`. Nếu 2 file này nằm ở 2 thư mục khác nhau, Python sẽ báo lỗi `ModuleNotFoundError: No module named 'edit_scanned_pdf'`.

```text
📁 Thư mục làm việc của bạn (ví dụ F:\TempFiles\New folder (9)\):
   ├── edit_scanned_pdf.py             <-- Script công cụ chính (BẮT BUỘC)
   ├── sua_hang_loat.py                <-- Script sửa hàng loạt (CÙNG THƯ MỤC)
   ├── requirements.txt                <-- Danh sách thư viện cài đặt
   ├── CCF_000372_.pdf                 <-- File PDF scan gốc cần sửa
   └── CCF_000372_DaCapNhatToanBo.pdf  <-- File PDF kết quả sinh ra sau khi chạy
```

#### 📝 Nội dung đầy đủ của file `sua_hang_loat.py` (Bạn có thể mở bằng Notepad để sửa tùy ý):
```python
# -*- coding: utf-8 -*-
"""
SCRIPT SỬA HÀNG LOẠT VĂN BẢN TRÊN FILE PDF SCAN (sua_hang_loat.py)
"""
import os
import sys

# Import bộ công cụ chỉnh sửa từ file edit_scanned_pdf.py (cùng thư mục)
try:
    from edit_scanned_pdf import ScannedPdfEditor
except ImportError:
    print("[LỖI] Không tìm thấy file 'edit_scanned_pdf.py' trong cùng thư mục!")
    print("      Vui lòng đảm bảo 'sua_hang_loat.py' và 'edit_scanned_pdf.py' nằm chung một folder.")
    sys.exit(1)


def main():
    # 1. CẤU HÌNH TÊN FILE VÀ THÔNG SỐ CHUNG
    input_pdf = "CCF_000372_.pdf"                 # File PDF gốc cần sửa
    output_pdf = "CCF_000372_DaCapNhatToanBo.pdf"  # File kết quả xuất ra
    page_number = 0                               # Trang cần sửa (0 là trang 1, 1 là trang 2...)
    default_roughness = 1.0                       # Độ rỗ mặc định (1.0 là chuẩn tự nhiên)

    if not os.path.exists(input_pdf):
        print(f"[LỖI] Không tìm thấy file '{input_pdf}'! Hãy kiểm tra lại tên file.")
        return

    print("=" * 76)
    print(f"[*] BẮT ĐẦU CẬP NHẬT HÀNG LOẠT FILE SCAN: {input_pdf}")
    print(f"[*] File kết quả xuất ra                 : {output_pdf}")
    print("=" * 76)

    # Khởi tạo đối tượng chỉnh sửa
    editor = ScannedPdfEditor(input_pdf, page_num=page_number, default_roughness=default_roughness)

    # 2. DANH SÁCH CÁC VỊ TRÍ CẦN SỬA (Lấy tọa độ từ lệnh pick)
    # [Vị trí 1] Sửa Số lượng (dòng 1) - Dùng "auto" toàn diện: tự nhận diện chữ thường, tự căn lề số
    print("\n--- [1/5] Đang sửa Số lượng (Dòng 1)... ---")
    editor.replace_region(
        box=(1615, 992, 135, 55),    # Tọa độ (X, Y, Width, Height)
        new_text="4,750",             # Nội dung mới
        font_name="auto",             # Font: "auto" (tự nhận diện), hoặc ép: "times.ttf"
        font_size=0,                  # Cỡ chữ: 0 (tự đo theo chữ cũ), hoặc ép số: 52
        align="auto",                 # Căn lề: "auto" (số tự căn phải), hoặc "right", "center", "left"
        roughness=1.0                 # Độ rỗ thớ giấy và mực scan (1.0 là chuẩn tự nhiên)
    )

    # [Vị trí 2] Sửa Thành tiền (dòng 1) - Chỉ định rõ chữ thường times.ttf, cỡ 52, căn phải
    print("\n--- [2/5] Đang sửa Thành tiền (Dòng 1)... ---")
    editor.replace_region(
        box=(2096, 996, 260, 53),
        new_text="270,750,000",
        font_name="times.ttf",        # Chỉ định font chữ thường
        font_size=52,                 # Chỉ định cỡ font
        align="right",                # Căn lề phải
        roughness=1.0                 # Độ rỗ chuẩn
    )

    # [Vị trí 3] Sửa Cộng tiền hàng (dòng 2) - Chỉ định chữ ĐẬM timesbd.ttf, cỡ 52, căn phải, rỗ 1.2
    print("\n--- [3/5] Đang sửa Cộng tiền hàng (Chữ Đậm)... ---")
    editor.replace_region(
        box=(2096, 1086, 260, 50),
        new_text="270,750,000",
        font_name="timesbd.ttf",      # Chỉ định font chữ ĐẬM (Times Bold)
        font_size=52,                 # Cỡ font
        align="right",                # Căn lề phải
        roughness=1.2                 # Tùy chọn tăng nhẹ độ rỗ scan
    )

    # [Vị trí 4] Sửa Thuế GTGT 8% (dòng 3) - Tự động nhận diện chữ ĐẬM, căn phải, rỗ 'high'
    print("\n--- [4/5] Đang sửa Thuế GTGT 8% (Chữ Đậm)... ---")
    editor.replace_region(
        box=(2096, 1170, 260, 50),
        new_text="21,660,000",
        font_name="auto",             # Tự động phát hiện chữ ĐẬM
        font_size=0,                  # Tự động đo cỡ chữ
        align="right",                # Căn lề phải
        roughness="high"              # Mức độ rỗ đậm (tương đương 1.4)
    )

    # [Vị trí 5] Sửa Tổng cộng thanh toán (dòng 4) - Chỉ định chữ ĐẬM timesbd.ttf, cỡ 50, căn phải
    print("\n--- [5/5] Đang sửa Tổng cộng thanh toán (Chữ Đậm)... ---")
    editor.replace_region(
        box=(2096, 1260, 260, 50),
        new_text="292,410,000",
        font_name="timesbd.ttf",      # Font chữ ĐẬM
        font_size=50,                 # Cỡ font
        align="right",                # Căn lề phải
        roughness=1.0                 # Độ rỗ chuẩn
    )

    # 3. CÁC TÍNH NĂNG NÂNG CAO KHÁC (Nếu không cần dùng, bạn chỉ việc bôi đen xóa đi)
    # [Ví dụ A] Chèn thêm chữ vào dòng chấm chấm ... (không xóa nền)
    print("\n--- [Ví dụ A] Đang chèn thêm số vào chỗ trống chấm chấm... ---")
    editor.insert_text(
        text="45", x=820, y=1580, font_name="times.ttf", size=50, align="center", roughness=1.0
    )

    # [Ví dụ B] Xóa trắng một con dấu/chữ thừa (Whiteout nền giấy tự nhiên)
    print("\n--- [Ví dụ B] Đang xóa trắng vùng thừa... ---")
    editor.replace_region(
        box=(1800, 2800, 350, 150), new_text="", roughness=1.0
    )

    # 4. LƯU FILE KẾT QUẢ
    print("\n" + "=" * 76)
    print(f"[*] Đang lưu file PDF kết quả vào: {output_pdf}...")
    editor.save(output_pdf)
    print(f"[THÀNH CÔNG] ĐÃ HOÀN TẤT CẬP NHẬT TOÀN BỘ CÁC VỊ TRÍ!")
    print(f"👉 File mới đã sẵn sàng: {output_pdf}")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    main()
```

#### ▶️ Cách Chạy:
Mở cửa sổ dòng lệnh (cmd/powershell) tại thư mục chứa file và gõ:
```bash
python sua_hang_loat.py
```
Toàn bộ các ô bảng biểu sẽ được tự động cập nhật đồng loạt chỉ trong vài giây!

---

## 7. Bảng Tra Cứu Font Chữ Windows Tương Thích

Script tự động tìm font trong thư mục hệ thống `C:\Windows\Fonts`. Dưới đây là các font thông dụng nhất trong văn bản hành chính và báo giá tại Việt Nam:

| Kiểu chữ thực tế | Tên file font | Đặc điểm nhận diện & Ứng dụng |
| :--- | :--- | :--- |
| **Times New Roman ĐỨNG** | `times.ttf` | Chữ có chân, thanh mảnh. Dùng cho nội dung văn bản, số liệu chi tiết dòng hàng. |
| **Times New Roman ĐẬM** | `timesbd.ttf` | Nét dày, đậm. Dùng cho dòng **Tổng tiền, Cộng tiền hàng, Thuế GTGT, Tiêu đề**. |
| **Times New Roman NGHIÊNG** | `timesi.ttf` | Nét nghiêng mềm mại. Dùng cho **Ngày tháng năm, Ghi chú, Ký tên**. |
| **Times New Roman ĐẬM NGHIÊNG** | `timesbi.ttf` | Vừa đậm vừa nghiêng. Dùng cho tiểu mục nhấn mạnh. |
| **Arial ĐỨNG** | `arial.ttf` | Không chân, vuông vắn, hiện đại. Dùng cho bảng kỹ thuật, mã linh kiện. |
| **Arial ĐẬM** | `arialbd.ttf` | Không chân, nét đậm. Dùng cho tiêu đề bản vẽ, mã đơn hàng nổi bật. |
| **Century Gothic** | `GOTHIC.TTF` | Kiểu chữ tròn hiện đại (chữ `a` một tầng tròn). Báo giá phong cách nước ngoài. |
| **Century Gothic Đậm** | `GOTHICB.TTF` | Kiểu chữ tròn nét đậm. |
| **Calibri Đứng / Đậm** | `calibri.ttf` / `calibrib.ttf` | Font văn phòng mặc định của Microsoft Word/Excel đời mới. |

---

## 8. Bí Quyết Giúp Chữ Mới Tự Nhiên Tuyệt Đối

1. **Khoanh vùng chọn gọn gàng:**
   - Dùng lệnh `pick` với tính năng Zoom để nhìn rõ đường viền.
   - **Tuyệt đối không khoanh chạm vào các vạch kẻ ngang/dọc của bảng biểu**. Hãy để khoảng hở cách mép viền khoảng 2-4 pixel.
2. **Luôn dùng căn lề phải (`right`) cho các cột số tiền:**
   - Trong bảng tính kế toán, số liệu luôn được gióng thẳng theo hàng đơn vị ở bên phải. Căn lề phải đảm bảo số tiền mới thẳng hàng tuyệt đối với các số ở các dòng khác.
3. **Độ hòa sắc và hạt nhiễu:**
   - Script tự động tính toán bán kính làm mờ tán sắc (Blur radius ~0.45px) mô phỏng lại hiện tượng quang học của đầu quét máy scan, giúp mép chữ không bị sắc lẹm giả tạo mà hòa cùng độ phân giải giấy scan gốc.
