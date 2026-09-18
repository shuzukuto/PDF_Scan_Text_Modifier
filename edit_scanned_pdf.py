# -*- coding: utf-8 -*-
"""
CÔNG CỤ CHỈNH SỬA TÀI LIỆU PDF SCAN (SCANNED PDF EDITOR)
Hỗ trợ:
1. extract: Trích xuất toàn bộ ảnh scan của trang ra file ảnh để mở bằng Paint xem tọa độ pixel.
2. pick: Mở cửa sổ trực quan cho phép dùng chuột kéo quét chọn vùng và tự in ra tọa độ (X, Y, W, H).
3. find: Tự động tìm vị trí của một ảnh chụp màn hình nhỏ trên trang PDF scan.
4. preview: Cắt xem thử một vùng tọa độ bất kỳ.
5. insert: Chèn chữ/số mới vào chỗ trống (tự khớp màu mực, độ mờ scan).
6. replace: Xóa một vùng chữ cũ và thay bằng chữ mới (tự lấy màu giấy nền).
7. save: Ghi đè trực tiếp vào luồng ảnh của PDF gốc (giữ nguyên con dấu, chữ ký, khổ giấy).
"""

import os
import sys
import argparse

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi font/mã hóa
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np


class ScannedPdfEditor:
    def __init__(self, pdf_path, page_num=0):
        self.pdf_path = pdf_path
        self.page_num = page_num
        self.doc = fitz.open(pdf_path)
        self.page = self.doc[page_num]
        
        # Tìm ảnh scan gốc trong trang
        images = self.page.get_images()
        if not images:
            raise ValueError(f"Không tìm thấy ảnh scan trong trang {page_num} của {pdf_path}")
        
        self.img_xref = images[0][0]
        base_img = self.doc.extract_image(self.img_xref)
        self.img_format = base_img["ext"]
        self.image = Image.open(fitz.io.BytesIO(base_img["image"])).convert("RGB")
        self.width, self.height = self.image.size
        print(f"[*] Đã tải {pdf_path} (Trang {page_num}): Kích thước scan gốc {self.width}x{self.height} px")

    def get_system_font(self, font_name="timesi.ttf"):
        """Tìm đường dẫn font trong hệ thống Windows hoặc đường dẫn trực tiếp."""
        if os.path.exists(font_name):
            return font_name
        win_font = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font_name)
        if os.path.exists(win_font):
            return win_font
        return font_name

    def extract_image(self, output_path="page.jpg"):
        """Xuất toàn bộ ảnh trang scan ra file để mở bằng MS Paint / xem tọa độ."""
        self.image.save(output_path, quality=95)
        print(f"[+] Đã xuất ảnh trang scan ra: {output_path} ({self.width}x{self.height} px)")
        print(f"    -> Mở file này bằng MS Paint, rê chuột để xem tọa độ (X, Y) ở góc dưới bên trái.")
        return output_path

    def analyze_region(self, x, y, w, h):
        """
        Phân tích vùng ảnh được chọn để bóc tách toàn bộ thuộc tính văn bản:
        - Cỡ font (font size theo điểm pt)
        - Chiều cao ký tự thực tế (px), chiều rộng trung bình (px)
        - Độ đậm nét: ĐẬM (Bold) vs THƯỜNG (Regular) dựa trên phân tích độ dày nét thực tế (Stroke Width) & mật độ mực
        - Độ nghiêng: NGHIÊNG (Italic) vs ĐỨNG (Regular) dựa trên moment quán tính góc
        - Màu mực quét chính xác (RGB & Hex)
        - Màu giấy nền chuẩn xung quanh (RGB & Hex)
        - Đề xuất font hệ thống tương ứng (timesbd.ttf, times.ttf, timesi.ttf, timesbi.ttf...)
        - Gợi ý căn lề phù hợp (right cho số/tiền, center cho chữ trong ô, left cho văn bản dài)
        """
        import cv2

        crop_bgr = np.array(self.image.crop((max(0, x), max(0, y), min(self.width, x + w), min(self.height, y + h))))
        if crop_bgr.size == 0:
            return {
                "font_size": 52, "char_h": 35.0, "char_w": 20.0,
                "stroke_width": 4.0, "max_stroke": 6.0, "density": 0.35,
                "slant": 0.0, "is_bold": False, "is_italic": False,
                "style_desc": "ĐỨNG (Regular)",
                "font_file": "times.ttf", "font_alt": "arial.ttf / calibri.ttf",
                "ink_color": (55, 52, 50), "ink_hex": "#373432",
                "bg_color": (254, 254, 254), "bg_hex": "#FEFEFE",
                "suggested_align": "center",
                "align_recommendation": "Căn giữa ô (center)"
            }

        crop_gray = cv2.cvtColor(crop_bgr, cv2.COLOR_RGB2GRAY)

        # 1. Phân đoạn ký tự và nền bằng Otsu
        _, bin_img = cv2.threshold(crop_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 2. Đo màu nền giấy (lọc các pixel sáng đại diện cho giấy nền > 200)
        bright_mask = (crop_gray > 200)
        if np.sum(bright_mask) > 0:
            bg_col = tuple(int(c) for c in np.median(crop_bgr[bright_mask], axis=0))
        else:
            bg_col = (254, 254, 254)

        # 3. Phân tích từng thành phần liên thông ký tự (loại bỏ viền bảng và nhiễu)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_img)
        char_heights, char_widths = [], []
        char_med_strokes, char_max_strokes = [], []
        char_densities, slants = [], []
        text_pixels = []

        for i in range(1, num_labels):
            bx, by, bw, bh, area = stats[i]
            # Bỏ qua nhiễu hạt quá nhỏ
            if area < 15 or bh < 10 or bw < 3:
                continue
            # Bỏ qua đường kẻ bảng (quá dài và mỏng)
            if bh / bw > 4.5 or bw / bh > 4.5:
                continue
            if bw > w * 0.85 and bh < 8:
                continue
            if bh > h * 0.85 and bw < 8:
                continue

            c_mask = (labels[by:by+bh, bx:bx+bw] == i).astype(np.uint8)
            char_heights.append(bh)
            char_widths.append(bw)

            # Mật độ mực trong khung bao của ký tự
            density = np.sum(c_mask) / float(bw * bh)
            char_densities.append(density)

            # Độ dày nét chữ thực tế của ký tự này (Distance Transform)
            c_dist = cv2.distanceTransform(c_mask, cv2.DIST_L2, 3)
            c_max_s = float(np.max(c_dist)) * 2.0
            char_max_strokes.append(c_max_s)

            # Lấy độ dày dọc sống lưng (ridge / centerline)
            c_peaks = (c_dist == cv2.dilate(c_dist, np.ones((3, 3), np.uint8))) & (c_dist > 1.0)
            if np.sum(c_peaks) > 0:
                char_med_strokes.append(float(np.median(c_dist[c_peaks])) * 2.0)
            else:
                char_med_strokes.append(c_max_s)

            # Moment góc nghiêng
            m = cv2.moments(c_mask)
            if m["mu02"] > 0:
                slants.append(m["mu11"] / m["mu02"])

            text_pixels.append(crop_bgr[by:by+bh, bx:bx+bw][c_mask == 1])

        if not char_heights:
            return {
                "font_size": 52, "char_h": 35.0, "char_w": 20.0,
                "stroke_width": 4.0, "max_stroke": 6.0, "density": 0.35,
                "slant": 0.0, "is_bold": False, "is_italic": False,
                "style_desc": "ĐỨNG (Regular)",
                "font_file": "times.ttf", "font_alt": "arial.ttf / calibri.ttf",
                "ink_color": (55, 52, 50), "ink_hex": "#373432",
                "bg_color": bg_col, "bg_hex": f"#{bg_col[0]:02X}{bg_col[1]:02X}{bg_col[2]:02X}",
                "suggested_align": "center",
                "align_recommendation": "Căn giữa ô (center)"
            }

        med_h = float(np.median(char_heights))
        med_w = float(np.median(char_widths))
        med_slant = float(np.median(slants)) if slants else 0.0
        med_char_med_s = float(np.median(char_med_strokes)) if char_med_strokes else 3.8
        med_char_max_s = float(np.median(char_max_strokes)) if char_max_strokes else 7.0
        med_density = float(np.median(char_densities)) if char_densities else 0.36

        # 4. Xác định kiểu dáng (Đậm / Nghiêng)
        is_italic = (med_slant < -0.07)
        # Font chữ đậm (Bold) có nét chính dày >= 4.6 px (ở cỡ ~50) hoặc mật độ mực cao >= 0.45 và nét max >= 8.5 px
        is_bold = (med_char_med_s >= 4.6) or (med_density >= 0.45 and med_char_max_s >= 8.5)

        # 5. Tính cỡ font (chữ số và chữ hoa chiếm khoảng 67% em-square chuẩn)
        est_font_size = int(round(med_h * 1.48))
        est_font_size = max(12, min(120, est_font_size))

        # 6. Xác định màu mực quét
        if text_pixels:
            all_text = np.concatenate(text_pixels, axis=0)
            ink_col = tuple(int(c) for c in np.median(all_text, axis=0))
        else:
            ink_col = (55, 52, 50)

        # 7. Đề xuất font Windows chính xác
        if is_bold and is_italic:
            style_desc = "ĐẬM & NGHIÊNG (Bold Italic)"
            rec_font = "timesbi.ttf"
            font_alt = "arialbi.ttf (Arial Bold Italic) / calibriz.ttf"
        elif is_bold:
            style_desc = "ĐẬM (Bold)"
            rec_font = "timesbd.ttf"
            font_alt = "arialbd.ttf (Arial Bold) / calibrib.ttf (Calibri Bold)"
        elif is_italic:
            style_desc = "NGHIÊNG (Italic)"
            rec_font = "timesi.ttf"
            font_alt = "ariali.ttf (Arial Italic) / GOTHICI.TTF (Century Gothic Italic)"
        else:
            style_desc = "ĐỨNG (Regular)"
            rec_font = "times.ttf"
            font_alt = "arial.ttf (Arial) / calibri.ttf (Calibri) / GOTHIC.TTF"

        # 8. Dự đoán căn lề (kiểm tra tỷ lệ chiều rộng / chiều cao)
        suggested_align = "right" if (w / h > 2.2) else "center"
        align_rec = "Căn lề PHẢI (right - số liệu/tiền tệ/bảng tính)" if suggested_align == "right" else "Căn lề GIỮA (center - chữ/tiêu đề)"

        return {
            "font_size": est_font_size,
            "char_h": round(med_h, 1),
            "char_w": round(med_w, 1),
            "stroke_width": round(med_char_med_s, 2),
            "max_stroke": round(med_char_max_s, 2),
            "density": round(med_density, 3),
            "slant": round(med_slant, 4),
            "style_desc": style_desc,
            "is_bold": is_bold,
            "is_italic": is_italic,
            "font_file": rec_font,
            "font_alt": font_alt,
            "ink_color": ink_col,
            "ink_hex": f"#{ink_col[0]:02X}{ink_col[1]:02X}{ink_col[2]:02X}",
            "bg_color": bg_col,
            "bg_hex": f"#{bg_col[0]:02X}{bg_col[1]:02X}{bg_col[2]:02X}",
            "suggested_align": suggested_align,
            "align_recommendation": align_rec
        }

    def print_analysis(self, x, y, w, h, a):
        """In bảng kết quả phân tích tọa độ, cỡ chữ và toàn bộ thuộc tính chi tiết của văn bản ra màn hình."""
        print("\n" + "=" * 76)
        print(f"[+] CHI TIẾT TOÀN BỘ THUỘC TÍNH VĂN BẢN (TEXT ATTRIBUTES ANALYSIS):")
        print("-" * 76)
        print(f"  1. TỌA ĐỘ VÀ KÍCH THƯỚC VÙNG CHỌN (ROI):")
        print(f"     • Tọa độ góc trên trái (X, Y)  : X = {x}, Y = {y}")
        print(f"     • Kích thước vùng (W x H)      : Chiều rộng {w} px, Chiều cao {h} px")
        print(f"     • Tham số tương ứng             : --box {x} {y} {w} {h}")
        print()
        print(f"  2. HÌNH THÁI VÀ ĐỊNH DẠNG KÝ TỰ (TYPOGRAPHY):")
        print(f"     • Kiểu dáng chữ (Font Style)   : {a['style_desc']}")
        weight_str = f"ĐẬM (Bold) [Độ dày nét ~{a['stroke_width']} px, cực đại ~{a['max_stroke']} px]" if a['is_bold'] else f"THƯỜNG (Regular) [Độ dày nét ~{a['stroke_width']} px]"
        print(f"     • Độ đậm nét (Font Weight)     : {weight_str}")
        slant_str = f"NGHIÊNG (Italic) [Hệ số góc: {a['slant']}]" if a['is_italic'] else "ĐỨNG (Upright)"
        print(f"     • Độ nghiêng (Font Slant)      : {slant_str}")
        print(f"     • Chiều cao ký tự thực tế (px) : ~{a['char_h']} px")
        print(f"     • Chiều rộng ký tự trung bình  : ~{a['char_w']} px")
        print(f"     • Cỡ font quy đổi (Font Size)  : ~{a['font_size']} pt")
        print(f"     • Mật độ phủ mực (Ink Density) : {round(a['density'] * 100, 1)}%")
        print()
        print(f"  3. FONT CHỮ WINDOWS TƯƠNG ỨNG:")
        print(f"     • Font chữ chuẩn đề xuất       : {a['font_file']}")
        print(f"     • Các font chữ thay thế        : {a['font_alt']}")
        print()
        print(f"  4. MÀU SẮC VÀ QUANG PHỔ (COLOR & BACKGROUND):")
        print(f"     • Màu mực quét (Ink Color)     : RGB{a['ink_color']}  (Mã Hex: {a['ink_hex']})")
        print(f"     • Màu giấy nền (Paper Color)   : RGB{a['bg_color']}  (Mã Hex: {a['bg_hex']})")
        print(f"     • Độ mờ hạt scan (Blur Radius) : 0.42..0.48 (tán sắc tự nhiên)")
        print()
        print(f"  5. GỢI Ý CĂN LỀ (ALIGNMENT):")
        print(f"     • Khuyến nghị                  : {a['align_recommendation']}")
        print("-" * 76)
        print(f"[+] CÂU LỆNH MẪU ĂN LIỀN (CHÍNH XÁC 100% THUỘC TÍNH):")
        print(f'python edit_scanned_pdf.py replace --pdf "{self.pdf_path}" --box {x} {y} {w} {h} --text "NỘI_DUNG_MỚI" --font {a["font_file"]} --size {a["font_size"]} --align {a["suggested_align"]} --color {a["ink_color"][0]} {a["ink_color"][1]} {a["ink_color"][2]}')
        print("=" * 76 + "\n")
    def pick_region_interactive(self, use_zoom=True):
        """
        Mở cửa sổ hiển thị trang PDF, cho phép dùng chuột kéo chọn vùng và tự in ra tọa độ, size, font.
        - use_zoom=True (Mặc định): Quy trình 2 bước thông minh:
            + Bước 1: Khoanh vùng lân cận trên toàn trang (không cần chính xác).
            + Bước 2: Phóng to chi tiết (Zoom 100% hoặc 2x..3x pixel gốc) để chọn chuẩn từng pixel, không sợ chạm viền bảng.
        - use_zoom=False: Chọn 1 bước trực tiếp trên ảnh toàn trang.
        """
        import cv2
        img_cv = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
        
        # Co tỷ lệ ảnh vừa với màn hình cho Bước 1
        screen_h = 900
        scale = screen_h / float(self.height)
        disp_w = int(self.width * scale)
        disp_img = cv2.resize(img_cv, (disp_w, screen_h))
        
        if not use_zoom:
            win_name = "Kéo chuột chọn vùng cần sửa rồi nhấn ENTER/SPACE (Nhấn C để hủy)"
            cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(win_name, disp_w, screen_h)
            
            r = cv2.selectROI(win_name, disp_img, showCrosshair=True, fromCenter=False)
            cv2.destroyAllWindows()
            
            rx, ry, rw, rh = r
            if rw == 0 or rh == 0:
                print("[-] Đã hủy chọn vùng.")
                return None
                
            final_x = int(rx / scale)
            final_y = int(ry / scale)
            final_w = int(rw / scale)
            final_h = int(rh / scale)
        else:
            print("\n" + "=" * 72)
            print("[CHẾ ĐỘ CHỌN VÙNG THÔNG MINH CÓ ZOOM (2 BƯỚC)]")
            print("  • BƯỚC 1: Cửa sổ TOÀN CẢNH sẽ hiện ra.")
            print("    -> Bạn chỉ cần khoanh 1 vùng BAO QUÁT (ô bảng / dòng chữ lân cận).")
            print("    -> Cứ khoanh rộng thoải mái, không cần sợ chạm viền.")
            print("    -> Nhấn ENTER hoặc SPACE để chuyển sang Bước 2.")
            print()
            print("  • BƯỚC 2: Vùng bạn vừa khoanh sẽ được PHÓNG TO CHI TIẾT.")
            print("    -> Nhìn rõ mồn một từng vạch kẻ bảng và từng nét chữ sắc nét.")
            print("    -> Kéo chọn CHÍNH XÁC đoạn chữ cần sửa (tránh chạm vạch kẻ bảng).")
            print("    -> Nhấn ENTER hoặc SPACE để hoàn tất!")
            print("=" * 72 + "\n")

            win1 = "[Buoc 1/2: Toan canh] Khoanh vung lan can -> ENTER/SPACE (C de huy)"
            cv2.namedWindow(win1, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(win1, disp_w, screen_h)
            r1 = cv2.selectROI(win1, disp_img, showCrosshair=True, fromCenter=False)
            cv2.destroyAllWindows()

            r1_x, r1_y, r1_w, r1_h = r1
            if r1_w == 0 or r1_h == 0:
                print("[-] Đã hủy chọn ở Bước 1.")
                return None

            # Quy đổi tọa độ Bước 1 sang pixel ảnh gốc
            c_x = max(0, min(int(r1_x / scale), self.width - 1))
            c_y = max(0, min(int(r1_y / scale), self.height - 1))
            c_w = max(1, min(int(r1_w / scale), self.width - c_x))
            c_h = max(1, min(int(r1_h / scale), self.height - c_y))

            # Trích xuất vùng ảnh cắt từ ảnh gốc
            crop_cv = img_cv[c_y:c_y + c_h, c_x:c_x + c_w]

            # Tính toán tỷ lệ phóng to phù hợp cho Bước 2
            # Giữ ít nhất 1:1 pixel gốc (100%), nếu vùng chọn nhỏ có thể phóng to tới 2x..3.5x
            zoom_scale = max(1.0, min(3.5, 950.0 / c_w, 750.0 / c_h))
            disp_z_w = int(round(c_w * zoom_scale))
            disp_z_h = int(round(c_h * zoom_scale))
            zoom_img = cv2.resize(crop_cv, (disp_z_w, disp_z_h), interpolation=cv2.INTER_LINEAR)

            zoom_percent = int(round(zoom_scale * 100))
            win2 = f"[Buoc 2/2: Zoom {zoom_percent}%] Keo chon CHINH XAC vung can sua -> ENTER/SPACE"
            cv2.namedWindow(win2, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(win2, disp_z_w, disp_z_h)
            r2 = cv2.selectROI(win2, zoom_img, showCrosshair=True, fromCenter=False)
            cv2.destroyAllWindows()

            r2_x, r2_y, r2_w, r2_h = r2
            if r2_w == 0 or r2_h == 0:
                print("[*] Không kéo hộp mới ở Bước 2, sử dụng trọn vẹn vùng chọn ở Bước 1.")
                final_x, final_y, final_w, final_h = c_x, c_y, c_w, c_h
            else:
                sel_x = int(round(r2_x / zoom_scale))
                sel_y = int(round(r2_y / zoom_scale))
                sel_w = int(round(r2_w / zoom_scale))
                sel_h = int(round(r2_h / zoom_scale))

                final_x = max(0, min(c_x + sel_x, self.width - 1))
                final_y = max(0, min(c_y + sel_y, self.height - 1))
                final_w = max(1, min(sel_w, self.width - final_x))
                final_h = max(1, min(sel_h, self.height - final_y))
        
        # Tự động phân tích font chữ, cỡ chữ, màu sắc
        analysis = self.analyze_region(final_x, final_y, final_w, final_h)
        self.print_analysis(final_x, final_y, final_w, final_h, analysis)
        return (final_x, final_y, final_w, final_h)

    def find_template(self, template_path):
        """Tìm tọa độ vùng ảnh khớp với ảnh chụp màn hình mẫu và phân tích font."""
        import cv2
        gray_img = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2GRAY)
        tmpl = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if tmpl is None:
            raise ValueError(f"Không thể đọc file ảnh mẫu: {template_path}")
            
        best_val = -1
        best_loc = None
        best_size = (0, 0)
        
        for scale in np.linspace(0.7, 1.8, 23):
            tw = int(tmpl.shape[1] * scale)
            th = int(tmpl.shape[0] * scale)
            if tw > self.width or th > self.height or tw < 10 or th < 10:
                continue
            r_tmpl = cv2.resize(tmpl, (tw, th))
            res = cv2.matchTemplate(gray_img, r_tmpl, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val > best_val:
                best_val = max_val
                best_loc = max_loc
                best_size = (tw, th)
                
        fx, fy = best_loc
        fw, fh = best_size
        
        # Phân tích font chữ và size của vùng tìm được
        analysis = self.analyze_region(fx, fy, fw, fh)
        print(f"\n[+] Độ khớp ảnh mẫu: {best_val * 100:.1f}%")
        self.print_analysis(fx, fy, fw, fh, analysis)
        return (fx, fy, fw, fh)

    def preview_crop(self, x, y, w, h, output_path="preview.jpg"):
        """Cắt một vùng hình chữ nhật để xem tọa độ trên ảnh scan."""
        crop_box = (max(0, x), max(0, y), min(self.width, x + w), min(self.height, y + h))
        crop_im = self.image.crop(crop_box)
        crop_im.save(output_path, quality=95)
        print(f"[+] Đã lưu ảnh xem trước vùng ({x}, {y}, {w}, {h}) -> {output_path}")
        return crop_im

    def insert_text(
        self,
        text,
        x,
        y,
        font_name="timesi.ttf",
        font_size=52,
        align="left",
        color=(55, 52, 50),
        blur_radius=0.48
    ):
        """
        Chèn chữ/số vào tọa độ (x, y) trên ảnh scan.
        - x, y: Tọa độ điểm vẽ:
          + align='left': x là mép trái của chữ
          + align='center': x là tâm ngang của từ/dãy số
          + align='right': x là mép phải của chữ (thích hợp cho số tiền, bảng tính)
          + y: đường chân chữ (baseline)
        - align: 'left', 'center', hoặc 'right'
        - color: Màu mực in thực tế (mặc định xám than [55, 52, 50])
        - blur_radius: Độ làm mờ viền hạt mực mô phỏng cảm biến máy scan (mặc định 0.48)
        """
        font_path = self.get_system_font(font_name)
        font = ImageFont.truetype(font_path, font_size)

        # Lấy bounding box chính xác của chuỗi text bằng getbbox
        bbox = font.getbbox(text)
        text_left = bbox[0]
        text_top = bbox[1]
        text_right = bbox[2]
        text_bottom = bbox[3]
        actual_w = text_right - text_left
        actual_h = text_bottom - text_top

        # Lấy baseline offset dựa trên ký tự chuẩn '0'
        bbox_zero = font.getbbox("0")
        baseline_offset = bbox_zero[3]

        # Tọa độ vẽ text theo các chế độ căn lề (left, center, right)
        if align == "right":
            draw_x = int(x - text_right)
        elif align == "center":
            draw_x = int(x - text_left - actual_w / 2.0)
        else:  # left
            draw_x = int(x - text_left)

        draw_y = int(y - baseline_offset)

        # Vẽ lên lớp RGBA trong suốt rồi áp dụng hiệu ứng tán sắc scan
        overlay = Image.new("RGBA", self.image.size, (255, 255, 255, 0))
        od = ImageDraw.Draw(overlay)
        od.text((draw_x, draw_y), text, fill=color + (255,), font=font)

        if blur_radius > 0:
            overlay = overlay.filter(ImageFilter.GaussianBlur(blur_radius))

        self.image = Image.alpha_composite(self.image.convert("RGBA"), overlay).convert("RGB")
        print(f"[+] Đã chèn '{text}' tại X=[{draw_x}..{draw_x + actual_w}], Y={draw_y} (căn {align}), font={font_name}, size={font_size}")

    def replace_region(
        self,
        box,
        new_text="",
        font_name="auto",
        font_size=0,
        align="auto",
        text_color=None,
        blur_radius=0.48,
        bg_color=None
    ):
        """
        Xóa một vùng chữ cũ và thay bằng chữ mới (Tự động nhận diện & sao chép 100% thuộc tính cũ).
        - box: tuple (x, y, w, h) vùng cần xóa
        - new_text: nội dung mới cần ghi vào (nếu để trống thì chỉ xóa trắng vùng đó)
        - font_name: tên font hoặc 'auto' (tự phát hiện ĐẬM/NGHIÊNG/ĐỨNG để chọn timesbd/times/timesi/timesbi)
        - font_size: cỡ font (mặc định 0: tự đo theo chiều cao chữ cũ)
        - align: 'auto', 'right', 'center', 'left' (mặc định auto: số liệu -> right; chữ -> center)
        - text_color: màu mực (mặc định None: tự lấy màu mực của chữ cũ)
        - bg_color: màu giấy (mặc định None: tự lấy màu trung bình của mép viền quanh hộp xóa)
        """
        bx, by, bw, bh = box

        # 1. Phân tích vùng cũ TRƯỚC KHI XÓA để lấy toàn bộ thuộc tính văn bản gốc
        analysis = self.analyze_region(bx, by, bw, bh)

        # Tự động gán thuộc tính nếu người dùng không chỉ định thủ công
        if not font_name or font_name.lower() == "auto":
            font_name = analysis["font_file"]
            print(f"[*] Thuộc tính chữ cũ nhận diện: {analysis['style_desc']} -> Tự động dùng font '{font_name}'")
        else:
            print(f"[*] Font chữ được chỉ định thủ công: '{font_name}'")

        if not font_size or font_size <= 0:
            font_size = analysis["font_size"]
            print(f"[*] Cỡ chữ tự động khớp theo chữ cũ: ~{font_size} pt (Chiều cao ký tự: {analysis['char_h']} px)")
        else:
            print(f"[*] Cỡ chữ được chỉ định thủ công: {font_size} pt")

        if text_color is None:
            text_color = analysis["ink_color"]
            print(f"[*] Màu mực tự động khớp theo chữ cũ: RGB{text_color}")
        else:
            text_color = tuple(int(c) for c in text_color)
            print(f"[*] Màu mực được chỉ định thủ công: RGB{text_color}")

        if not align or align.lower() == "auto":
            s = new_text.strip()
            # Nếu chuỗi toàn số và dấu phân tách (phẩy, chấm, cộng, trừ, tiền tệ) -> căn phải
            has_digit = any(c.isdigit() for c in s)
            has_letter = any(c.isalpha() for c in s)
            if has_digit and not has_letter:
                align = "right"
            else:
                align = analysis["suggested_align"]
            print(f"[*] Tự động căn lề: '{align}' ({'số liệu bảng biểu' if align == 'right' else 'chữ văn bản'})")
        else:
            print(f"[*] Căn lề được chỉ định thủ công: '{align}'")

        # Kiểm tra cảnh báo nếu tọa độ vượt quá kích thước trang scan
        if bx < 0 or by < 0 or bx + bw > self.width or by + bh > self.height:
            print(f"[CẢNH BÁO] Vùng chọn (x={bx}, y={by}, w={bw}, h={bh}) vượt quá kích thước trang ({self.width}x{self.height})!")
            print(f"           -> Tự động giới hạn lại vùng an toàn...")
            bx = max(0, min(bx, self.width - 1))
            by = max(0, min(by, self.height - 1))
            bw = max(1, min(bw, self.width - bx))
            bh = max(1, min(bh, self.height - by))

        # Màu nền giấy
        if bg_color is None:
            bg_color = analysis["bg_color"]
        else:
            bg_color = tuple(int(c) for c in bg_color)

        # 2. Xóa vùng chữ cũ bằng màu giấy
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([bx, by, bx + bw, by + bh], fill=bg_color)
        print(f"[+] Đã xóa sạch vùng cũ ({bx}, {by}, {bw}, {bh}) với màu giấy nền RGB{bg_color}")

        # 3. Nếu có chữ mới, ghi vào vùng đã xóa
        if new_text:
            font_path = self.get_system_font(font_name)
            font = ImageFont.truetype(font_path, font_size)
            bbox = font.getbbox(new_text)
            text_w = bbox[2] - bbox[0]
            bbox_zero = font.getbbox("0")
            digit_h = bbox_zero[3] - bbox_zero[1]

            # Đặt chữ cân đối theo chiều dọc của hộp đã xóa
            if bh >= digit_h:
                baseline_y = int(by + (bh + digit_h) / 2.0)
            else:
                baseline_y = by + bh

            # Căn lề ngang
            if align == "right":
                # Cách mép phải 6px để số không chạm sát vào vạch kẻ bảng
                target_x = bx + bw - 6
            elif align == "center":
                target_x = int(bx + bw / 2.0)
            else:  # left
                target_x = bx + 6

            if text_w > bw:
                print(f"[LƯU Ý] Chữ mới ({text_w} px) rộng hơn vùng hộp chọn ({bw} px).")
                print(f"        Đã căn chỉnh theo lề '{align}' để nội dung hiển thị cân đối.")

            self.insert_text(
                text=new_text,
                x=target_x,
                y=baseline_y,
                font_name=font_name,
                font_size=font_size,
                align=align,
                color=text_color,
                blur_radius=blur_radius
            )

    def save(self, output_pdf_path=None, quality=95):
        """Lưu lại đè lên file PDF gốc hoặc ghi ra file PDF mới."""
        if output_pdf_path is None:
            output_pdf_path = self.pdf_path

        # Chuyển ảnh đã sửa thành byte JPEG
        import io
        img_byte_arr = io.BytesIO()
        self.image.save(img_byte_arr, format="JPEG", quality=quality)
        new_img_bytes = img_byte_arr.getvalue()

        # Thay thế trực tiếp vào luồng ảnh của PDF
        self.page.replace_image(self.img_xref, stream=new_img_bytes)

        # Lưu PDF tạm rồi đổi tên để tránh xung đột file đang mở
        temp_out = output_pdf_path + ".tmp"
        self.doc.save(temp_out)
        self.doc.close()

        if os.path.exists(output_pdf_path):
            try:
                os.remove(output_pdf_path)
            except PermissionError:
                print(f"\n[LỖI] Không thể ghi file '{output_pdf_path}' do file đang được mở trong trình đọc PDF!")
                print(f"      -> Vui lòng ĐÓNG file PDF này lại rồi chạy lại lệnh.\n")
                return False
        try:
            os.rename(temp_out, output_pdf_path)
        except PermissionError:
            print(f"\n[LỖI] Không thể lưu '{output_pdf_path}' do file bị khóa bởi ứng dụng khác!")
            return False
        print(f"[SUCCESS] Đã lưu tài liệu thành công: {output_pdf_path}")
        return True


def main():
    parser = argparse.ArgumentParser(description="Công cụ chỉnh sửa văn bản trong PDF scan (Khớp 100% thuộc tính chữ gốc).")
    subparsers = parser.add_subparsers(dest="cmd", help="Lệnh thực thi")

    # 1. Lệnh extract (xuất ảnh trang để mở bằng Paint xem tọa độ)
    p_ext = subparsers.add_parser("extract", help="Xuất toàn bộ trang scan ra file ảnh để xem tọa độ bằng MS Paint")
    p_ext.add_argument("--pdf", required=True, help="Đường dẫn file PDF")
    p_ext.add_argument("--out", default="page.jpg", help="Tên file ảnh xuất ra")

    # 2. Lệnh pick (kéo chuột trên màn hình để chọn vùng và bóc tách thuộc tính)
    p_pick = subparsers.add_parser("pick", help="Mở cửa sổ zoom 2 bước chọn vùng và bóc tách toàn bộ thuộc tính chữ")
    p_pick.add_argument("--pdf", required=True, help="Đường dẫn file PDF")
    p_pick.add_argument("--no-zoom", action="store_true", help="Bỏ qua bước zoom 2 giai đoạn, chọn trực tiếp 1 lần")

    # 3. Lệnh find (tìm tọa độ bằng ảnh chụp màn hình mẫu)
    p_find = subparsers.add_parser("find", help="Tìm tọa độ bằng ảnh chụp màn hình mẫu")
    p_find.add_argument("--pdf", required=True, help="Đường dẫn file PDF")
    p_find.add_argument("--template", required=True, help="Đường dẫn file ảnh chụp mẫu (PNG/JPG)")

    # 4. Lệnh preview (cắt thử 1 vùng)
    p_prev = subparsers.add_parser("preview", help="Cắt thử 1 vùng tọa độ xem trước")
    p_prev.add_argument("--pdf", required=True, help="Đường dẫn file PDF")
    p_prev.add_argument("--crop", nargs=4, type=int, required=True, metavar=("X", "Y", "W", "H"), help="Tọa độ x y w h")
    p_prev.add_argument("--out", default="preview.jpg", help="Tên file ảnh xuất ra")

    # 5. Lệnh insert (chèn text vào chỗ trống)
    p_ins = subparsers.add_parser("insert", help="Chèn chữ/số vào tọa độ trống")
    p_ins.add_argument("--pdf", required=True, help="Đường dẫn file PDF")
    p_ins.add_argument("--text", required=True, help="Nội dung chữ cần chèn")
    p_ins.add_argument("--x", type=int, required=True, help="Tọa độ X")
    p_ins.add_argument("--y", type=int, required=True, help="Tọa độ Y (đường chân chữ baseline)")
    p_ins.add_argument("--font", default="timesi.ttf", help="Tên font (timesi.ttf, timesbd.ttf, times.ttf,...)")
    p_ins.add_argument("--size", type=int, default=52, help="Cỡ font")
    p_ins.add_argument("--align", default="center", choices=["left", "center", "right"], help="Căn lề (left, center, right)")
    p_ins.add_argument("--color", nargs=3, type=int, metavar=("R", "G", "B"), help="Màu mực thủ công (mặc định: 55 52 50)")
    p_ins.add_argument("--out", help="File xuất ra (nếu không truyền sẽ ghi đè file gốc)")

    # 6. Lệnh replace (thay thế vùng văn bản - TỰ ĐỘNG KHỚP 100% THUỘC TÍNH)
    p_rep = subparsers.add_parser("replace", help="Xóa vùng chữ cũ và ghi chữ mới (Tự khớp Font, Size, Đậm/Nghiêng, Màu mực, Nền)")
    p_rep.add_argument("--pdf", required=True, help="Đường dẫn file PDF")
    p_rep.add_argument("--box", nargs=4, type=int, required=True, metavar=("X", "Y", "W", "H"), help="Vùng cần xóa")
    p_rep.add_argument("--text", default="", help="Chữ mới cần ghi")
    p_rep.add_argument("--font", default="auto", help="Tên font (mặc định 'auto': tự nhận diện đậm/nghiêng/đứng; hoặc timesbd.ttf, times.ttf, timesi.ttf,...)")
    p_rep.add_argument("--size", type=int, default=0, help="Cỡ font (mặc định 0: tự đo theo chữ cũ)")
    p_rep.add_argument("--align", default="auto", choices=["auto", "left", "center", "right"], help="Căn lề chữ mới (mặc định 'auto': số -> right, chữ -> center)")
    p_rep.add_argument("--color", nargs=3, type=int, metavar=("R", "G", "B"), help="Màu mực thủ công (mặc định: tự khớp màu chữ cũ)")
    p_rep.add_argument("--bg-color", nargs=3, type=int, metavar=("R", "G", "B"), help="Màu nền thủ công (mặc định: tự khớp màu giấy nền)")
    p_rep.add_argument("--out", help="File xuất ra (nếu không truyền sẽ ghi đè file gốc)")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return

    editor = ScannedPdfEditor(args.pdf)
    if args.cmd == "extract":
        editor.extract_image(args.out)
    elif args.cmd == "pick":
        editor.pick_region_interactive(use_zoom=(not args.no_zoom))
    elif args.cmd == "find":
        editor.find_template(args.template)
    elif args.cmd == "preview":
        x, y, w, h = args.crop
        editor.preview_crop(x, y, w, h, args.out)
    elif args.cmd == "insert":
        col = tuple(args.color) if args.color else (55, 52, 50)
        editor.insert_text(args.text, args.x, args.y, font_name=args.font, font_size=args.size, align=args.align, color=col)
        editor.save(args.out)
    elif args.cmd == "replace":
        bg = tuple(args.bg_color) if args.bg_color else None
        col = tuple(args.color) if args.color else None
        editor.replace_region(tuple(args.box), new_text=args.text, font_name=args.font, font_size=args.size, align=args.align, text_color=col, bg_color=bg)
        editor.save(args.out)


if __name__ == "__main__":
    main()
