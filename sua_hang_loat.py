# -*- coding: utf-8 -*-
"""
================================================================================
SCRIPT SỬA HÀNG LOẠT VĂN BẢN TRÊN FILE PDF SCAN (sua_hang_loat.py)
================================================================================
Mục đích:
  - Cho phép người dùng chỉnh sửa đồng thời NHIỀU VỊ TRÍ (ô bảng, số tiền, ngày tháng,
    tiêu đề...) trên cùng một hoặc nhiều trang scan chỉ với 1 lần bấm chạy.
  - Tự động sao chép 100% thuộc tính chữ cũ (Đậm/Thường, Font, Cỡ, Màu mực, Độ rỗ scan).
  - Bạn có thể thoải mái thêm/bớt/sửa các dòng lệnh bên dưới theo nhu cầu thực tế.

LƯU Ý VỊ TRÍ FILE:
  - File 'sua_hang_loat.py' BẮT BUỘC phải đặt CÙNG MỘT THƯ MỤC với file 'edit_scanned_pdf.py'
    và file PDF cần chỉnh sửa để Python có thể import được công cụ.
================================================================================
"""

import os
import sys

# Import bộ công cụ chỉnh sửa ScannedPdfEditor từ file edit_scanned_pdf.py (cùng thư mục)
try:
    from edit_scanned_pdf import ScannedPdfEditor
except ImportError:
    print("[LỖI] Không tìm thấy file 'edit_scanned_pdf.py' trong cùng thư mục!")
    print("      Vui lòng đảm bảo 'sua_hang_loat.py' và 'edit_scanned_pdf.py' nằm chung một folder.")
    sys.exit(1)


def main():
    # ============================================================================
    # 1. CẤU HÌNH ĐƯỜNG DẪN FILE & THÔNG SỐ CHUNG
    # ============================================================================
    # Tên file PDF scan gốc cần chỉnh sửa
    input_pdf = "CCF_000372_.pdf"

    # Tên file PDF kết quả sau khi sửa xong (không ghi đè file gốc để dễ đối chiếu)
    output_pdf = "CCF_000372_DaCapNhatToanBo.pdf"

    # Trang cần sửa (0 là trang 1, 1 là trang 2, 2 là trang 3...)
    page_number = 0

    # Độ rỗ tự nhiên mặc định cho toàn bộ trang (1.0 là chuẩn scan, 1.3 là rỗ thô, 0.6 là mịn, 0.0 là phẳng)
    default_roughness = 1.0

    # Kiểm tra file gốc có tồn tại không
    if not os.path.exists(input_pdf):
        print(f"[LỖI] Không tìm thấy file '{input_pdf}'! Hãy kiểm tra lại tên file.")
        return

    print("=" * 76)
    print(f"[*] BẮT ĐẦU CẬP NHẬT HÀNG LOẠT FILE SCAN: {input_pdf}")
    print(f"[*] File kết quả xuất ra                 : {output_pdf}")
    print("=" * 76)

    # Khởi tạo đối tượng chỉnh sửa
    editor = ScannedPdfEditor(input_pdf, page_num=page_number, default_roughness=default_roughness)

    # ============================================================================
    # 2. DANH SÁCH CÁC VỊ TRÍ CẦN THAY THẾ (replace_region)
    #    - Tọa độ box=(X, Y, W, H) lấy trực tiếp từ lệnh: python edit_scanned_pdf.py pick
    #    - font_name: "auto" (tự nhận diện Đậm/Thường), hoặc ép font: "times.ttf", "timesbd.ttf", "arial.ttf"...
    #    - font_size: 0 (tự động đo cỡ theo chữ cũ), hoặc ép cỡ cụ thể: 52, 54, 48...
    #    - align: "auto" (số -> right, chữ -> center), hoặc ép lề: "right", "center", "left"
    #    - roughness: Mức độ rỗ scan (1.0 chuẩn tự nhiên; 1.3 rỗ đậm; 0.6 mịn nhẹ; 0.0 tắt rỗ)
    #    - text_color: None (tự hút màu mực chữ cũ), hoặc chỉ định RGB: (55, 52, 50)
    #    - bg_color: None (tự lấy mẫu màu giấy nền), hoặc chỉ định RGB: (254, 254, 254)
    # ============================================================================

    # [VỊ TRÍ 1] Sửa Số lượng (Dòng chi tiết số 1)
    # Gợi ý: Dùng chế độ "auto" toàn diện — script tự nhận diện chữ thường, tự căn lề số
    print("\n--- [1/5] Đang sửa Số lượng (Dòng 1)... ---")
    editor.replace_region(
        box=(1615, 992, 135, 55),    # Tọa độ vùng xóa (X, Y, Width, Height)
        new_text="4,750",             # Nội dung mới cần ghi
        font_name="auto",             # Font chữ: "auto" (tự nhận diện), hoặc "times.ttf"
        font_size=0,                  # Cỡ font: 0 (tự đo theo chữ cũ), hoặc ép số vd: 52
        align="auto",                 # Căn lề: "auto" (số tự căn phải), hoặc "right", "center", "left"
        roughness=1.0                 # Độ rỗ thớ giấy và mực scan (1.0 là chuẩn tự nhiên)
    )

    # [VỊ TRÍ 2] Sửa Thành tiền (Dòng chi tiết số 1)
    # Gợi ý: Chỉ định tường minh chữ thường times.ttf, cỡ 52, căn phải right
    print("\n--- [2/5] Đang sửa Thành tiền (Dòng 1)... ---")
    editor.replace_region(
        box=(2096, 996, 260, 53),
        new_text="270,750,000",
        font_name="times.ttf",        # Chỉ định rõ font chữ thường
        font_size=52,                 # Chỉ định rõ cỡ font 52
        align="right",                # Căn lề phải thẳng hàng đơn vị
        roughness=1.0                 # Mức độ rỗ chuẩn tự nhiên
    )

    # [VỊ TRÍ 3] Sửa 'Cộng tiền hàng' (Dòng tổng phụ - Subtotal)
    # Gợi ý: Chỉ định chữ ĐẬM timesbd.ttf, cỡ 52, căn phải, tăng độ rỗ lên 1.2
    print("\n--- [3/5] Đang sửa Cộng tiền hàng (Chữ Đậm)... ---")
    editor.replace_region(
        box=(2096, 1086, 260, 50),
        new_text="270,750,000",
        font_name="timesbd.ttf",      # Chỉ định font chữ ĐẬM (Times Bold)
        font_size=52,                 # Cỡ font
        align="right",                # Căn lề phải
        roughness=1.2                 # Tùy chọn tăng nhẹ độ rỗ scan cho đậm nét hơn
    )

    # [VỊ TRÍ 4] Sửa Tiền Thuế GTGT (VAT 8%)
    # Gợi ý: Để "auto" font (tự phát hiện ĐẬM), căn phải, độ rỗ mức "high"
    print("\n--- [4/5] Đang sửa Thuế GTGT 8% (Chữ Đậm)... ---")
    editor.replace_region(
        box=(2096, 1170, 260, 50),
        new_text="21,660,000",
        font_name="auto",             # Tự động phát hiện chữ ĐẬM từ chữ cũ
        font_size=0,                  # Tự động đo cỡ chữ
        align="right",                # Căn lề phải
        roughness="high"              # Mức độ rỗ đậm (tương đương 1.4)
    )

    # [VỊ TRÍ 5] Sửa 'Tổng cộng thanh toán' (Total)
    # Gợi ý: Chỉ định font ĐẬM timesbd.ttf, cỡ 50, căn phải
    print("\n--- [5/5] Đang sửa Tổng cộng thanh toán (Chữ Đậm)... ---")
    editor.replace_region(
        box=(2096, 1260, 260, 50),
        new_text="292,410,000",
        font_name="timesbd.ttf",      # Font chữ ĐẬM
        font_size=50,                 # Cỡ font
        align="right",                # Căn lề phải
        roughness=1.0                 # Độ rỗ chuẩn
    )

    # ============================================================================
    # 3. CÁC TÍNH NĂNG NÂNG CAO KHÁC (Bỏ comment '#' ở đầu dòng nếu muốn dùng)
    # ============================================================================

    # [VÍ DỤ A - CHÈN THÊM CHỮ/SỐ VÀO CHỖ TRỐNG CHẤM CHẤM BẰNG insert_text]
    # Không xóa nền, chèn trực tiếp lên đường chân chữ Y (Baseline lấy từ lệnh pick)
    # print("\n--- [Ví dụ A] Đang chèn thêm số vào chỗ trống chấm chấm... ---")
    # editor.insert_text(
    #     text="45",                  # Chữ/số cần điền
    #     x=820,                      # Tọa độ X
    #     y=1580,                     # Đường chân chữ Baseline Y (từ lệnh pick)
    #     font_name="times.ttf",      # Font chữ ("times.ttf", "timesbd.ttf", "timesi.ttf"...)
    #     font_size=50,               # Cỡ chữ (pt)
    #     align="center",             # Căn lề ('center', 'left', 'right')
    #     roughness=1.0               # Mức độ rỗ hạt mực scan
    # )

    # [VÍ DỤ B - XÓA TRẮNG HOÀN TOÀN MỘT VÙNG (BÚT XÓA NỀN GIẤY WHITEOUT)]
    # Xóa sạch con dấu thừa, ghi chú cũ và điền màu giấy nền tự nhiên (không viết gì)
    # print("\n--- [Ví dụ B] Đang xóa trắng vùng thừa... ---")
    # editor.replace_region(
    #     box=(1800, 2800, 350, 150), # Tọa độ vùng cần xóa trắng
    #     new_text="",                # new_text="" sẽ tự động xóa sạch không viết chữ
    #     roughness=1.0               # Độ rỗ kết cấu giấy nền
    # )

    # ============================================================================
    # 4. LƯU FILE KẾT QUẢ
    # ============================================================================
    print("\n" + "=" * 76)
    print(f"[*] Đang lưu file PDF kết quả vào: {output_pdf}...")
    editor.save(output_pdf)
    print(f"[THÀNH CÔNG] ĐÃ HOÀN TẤT CẬP NHẬT TOÀN BỘ CÁC VỊ TRÍ!")
    print(f"👉 File mới đã sẵn sàng: {output_pdf}")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    main()
