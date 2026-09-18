# Hướng Dẫn Sử Dụng Script Chỉnh Sửa File PDF Scan (`edit_scanned_pdf.py`)

Bộ công cụ chuyên biệt để chỉnh sửa tài liệu dạng **ảnh scan từ máy quét** (báo giá, hợp đồng, hóa đơn, chứng từ `CCF_...`).

Điểm đột phá của phiên bản mới là **Cơ chế Tự Động Khớp Thuộc Tính 100% (Auto-Matching)**: Script tự động phân tích chữ cũ trước khi xóa để nhận diện chính xác kiểu chữ (**ĐẬM / NGHIÊNG / ĐỨNG**), đo cỡ font, xác định chân chữ (baseline), hút màu mực scan thực tế và hòa màu nền giấy. Bạn không cần phải đoán hay chỉnh tay phức tạp.

---

## MỤC LỤC
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
5. [Cú Pháp Các Lệnh CLI Chính](#5-cú-pháp-các-lệnh-cli-chính)
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
  + **Tùy chỉnh linh hoạt qua cờ `--roughness`:** Mặc định là `1.0` (tự nhiên nhất). Bạn có thể tăng lên `1.2..1.5` cho scan giấy xơ thô, hoặc giảm về `0.5..0.8` cho văn bản in nét mịn.
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
     • Tham số tương ứng             : --box 2096 1086 260 50

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
     • Màu mực quét (Ink Color)     : RGB(74, 75, 81)  (Mã Hex: #4A4B51)
     • Màu giấy nền (Paper Color)   : RGB(253, 254, 254)  (Mã Hex: #FDFEFE)
     • Độ rỗ hạt mực (Roughness)    : std ~30.2 (điểm rỗ thớ giấy scan)
     • Độ nhiễu giấy nền (Grain)    : std ~1.85 (kết cấu thớ giấy)
     • Độ mờ tán sắc (Blur Radius)  : 0.38..0.42 (tán sắc tự nhiên)

  5. GỢI Ý CĂN LỀ (ALIGNMENT):
     • Khuyến nghị                  : Căn lề PHẢI (right - số liệu/tiền tệ/bảng tính)
----------------------------------------------------------------------------
[+] CÂU LỆNH MẪU ĂN LIỀN (CHÍNH XÁC 100% THUỘC TÍNH & ĐỘ RỖ):
python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "NỘI_DUNG_MỚI"
============================================================================
```

### Ý nghĩa từng chỉ số:
1. **Kiểu dáng chữ & Độ đậm nét (Font Style & Weight):** 
   - Nếu là chữ ĐẬM: Script đề xuất `timesbd.ttf` (Times New Roman Bold).
   - Nếu là chữ THƯỜNG: Script đề xuất `times.ttf` (Times New Roman Regular).
   - Nếu là chữ NGHIÊNG: Script đề xuất `timesi.ttf` (Times New Roman Italic).
2. **Cỡ font quy đổi (Font Size):** Cỡ font chuẩn (point size) tương thích với Windows Typography Engine khi in lên độ phân giải scan gốc.
3. **Màu mực & Độ rỗ scan:** Trích xuất màu mực lõi thực tế và độ phân tán hạt mực (`std ~30`), giúp nét chữ mới có các điểm rỗ vi mô tự nhiên như bản scan.
4. **Màu giấy & Kết cấu giấy:** Tái tạo thớ giấy nền cục bộ khi xóa, không để lại mảng phẳng trơn láng.
5. **Gợi ý căn lề (Alignment):** Tự động phát hiện loại nội dung để gợi ý lề phải (cho số tiền trong ô) hoặc căn giữa/trái.

---

## 5. Cú Pháp Các Lệnh CLI Chính

### Lệnh 1: `replace` (Thay thế văn bản)
```bash
python edit_scanned_pdf.py replace --pdf <FILE> --box <X Y W H> --text <NỘI_DUNG> [CÁC_CỜ_TÙY_CHỌN]
```
- **Chế độ Tự Động 100% (Khuyên dùng - Ngắn gọn nhất):**
  Không cần truyền `--font`, `--size`, `--align`, `--color`. Script sẽ tự động trích xuất các thuộc tính và độ rỗ từ chữ cũ trước khi xóa:
  ```bash
  python edit_scanned_pdf.py replace --pdf "CCF_000372_.pdf" --box 2096 1086 260 50 --text "270,750,000"
  ```
- **Chế độ Chỉnh tay Chuyên sâu (Khi muốn ép kiểu chữ và độ rỗ theo ý muốn):**
  - `--font`: Tên file font (`timesbd.ttf`, `times.ttf`, `timesi.ttf`, `arial.ttf`, `GOTHIC.TTF`...).
  - `--size`: Cỡ font số nguyên (ví dụ: `52`, `54`).
  - `--align`: Căn lề: `right` (số tiền), `center` (tiêu đề), `left` (đoạn văn).
  - `--roughness`: Hệ số rỗ thớ giấy và hạt mực scan (mặc định: `1.0`; đặt `1.2..1.5` nếu muốn rỗ nhiều hơn; đặt `0.5..0.8` nếu muốn mịn hơn; đặt `0.0` nếu muốn phẳng).
  - `--color R G B`: Ép màu mực (ví dụ: `--color 74 75 81`).
  - `--bg-color R G B`: Ép màu giấy nền (ví dụ: `--bg-color 254 254 254`).
  - `--out`: Tên file PDF xuất ra (nếu không truyền sẽ ghi đè file gốc).

---

### Lệnh 2: `insert` (Chèn chữ/số vào tọa độ trống)
Dùng khi tài liệu có sẵn khoảng trống (chấm lửng `...` hoặc ô chưa điền):
```bash
python edit_scanned_pdf.py insert --pdf <FILE> --text <CHỮ> --x <X> --y <Y> [--font <FONT>] [--size <SIZE>] [--align <left|center|right>] [--roughness <1.0>]
```

---

### Lệnh 3: `preview` (Cắt xem trước tọa độ)
Giúp xem nhanh vùng cắt để kiểm tra vị trí xem có chạm viền không:
```bash
python edit_scanned_pdf.py preview --pdf <FILE> --crop <X Y W H> --out "preview.png"
```

---

### Lệnh 4: `extract` (Xuất trang scan ra ảnh)
```bash
python edit_scanned_pdf.py extract --pdf <FILE> --page 0 --out "trang_scan.jpg"
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
- **Tình huống:** Bạn cần sửa đồng thời 4 ô trên cùng một trang: Đơn giá, Thành tiền, Thuế VAT và Tổng tiền, sau đó lưu lại file mới.
- Tạo một file script ngắn (ví dụ `sua_hang_loat.py`):
  ```python
  from edit_scanned_pdf import ScannedPdfEditor

  # Mở file PDF scan
  editor = ScannedPdfEditor("CCF_000372_.pdf", page_num=0)

  # 1. Sửa Số lượng (dòng 1) - Tự động nhận diện chữ thường
  editor.replace_region(box=(1615, 992, 135, 55), new_text="4,750")

  # 2. Sửa Thành tiền (dòng 1) - Tự động nhận diện chữ thường
  editor.replace_region(box=(2096, 996, 260, 53), new_text="270,750,000")

  # 3. Sửa Cộng tiền hàng (dòng 2) - Tự động nhận diện chữ ĐẬM (Bold)
  editor.replace_region(box=(2096, 1086, 260, 50), new_text="270,750,000")

  # 4. Sửa Thuế GTGT 8% (dòng 3) - Tự động nhận diện chữ ĐẬM (Bold)
  editor.replace_region(box=(2096, 1170, 260, 50), new_text="21,660,000")

  # 5. Sửa Tổng cộng thanh toán (dòng 4) - Tự động nhận diện chữ ĐẬM (Bold)
  editor.replace_region(box=(2096, 1260, 260, 50), new_text="292,410,000")

  # Lưu kết quả ra file mới
  editor.save("CCF_000372_DaCapNhatToanBo.pdf")
  print("[OK] Đã cập nhật xong toàn bộ bảng biểu!")
  ```
  Chạy lệnh: `python sua_hang_loat.py`

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
