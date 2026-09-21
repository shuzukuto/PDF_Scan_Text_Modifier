# -*- coding: utf-8 -*-
"""
TRÌNH KHỞI CHẠY GIAO DIỆN WEB STUDIO (PDF SCAN TEXT MODIFIER)
Hỗ trợ:
- Tên miền riêng: http://pdfscanmodifier:8000/
- Tự động phát hiện xung đột cổng và chọn cổng trống thông minh
- Tự động mở trình duyệt web khi server sẵn sàng
"""

import sys
import os
import socket
import argparse
import webbrowser
import threading
import time

# Đảm bảo UTF-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def is_custom_domain_available(domain="pdfscanmodifier"):
    """Kiểm tra máy tính đã cấu hình tên miền trong file hosts chưa."""
    try:
        ip = socket.gethostbyname(domain)
        if ip.startswith("127.") or ip == "::1":
            return True
    except Exception:
        pass
    return False


def find_available_port(preferred_port=8000):
    """Kiểm tra cổng, nếu bị trùng với ứng dụng khác thì tự động tìm cổng trống."""
    # Kiểm tra cổng ưu tiên
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', preferred_port)) != 0:
            return preferred_port, False
            
    # Nếu preferred_port đã bị chiếm dụng, thử các cổng dự phòng
    backup_ports = [8000, 8001, 8088, 8989, 8501, 9000]
    for p in backup_ports:
        if p == preferred_port:
            continue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', p)) != 0:
                return p, True
                
    return preferred_port, False


def open_browser(url):
    """Chờ 1.2 giây để server kịp khởi động rồi tự động mở trình duyệt."""
    time.sleep(1.2)
    print(f"[*] Đang tự động mở trình duyệt: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Khởi chạy PDF Scan Text Modifier Studio")
    parser.add_argument("--port", type=int, default=8000, help="Cổng chạy server (mặc định: 8000)")
    parser.add_argument("--host", default="0.0.0.0", help="Địa chỉ host lắng nghe (mặc định: 0.0.0.0)")
    parser.add_argument("--no-browser", action="store_true", help="Không tự động mở trình duyệt")
    args = parser.parse_args()

    try:
        import uvicorn
        from web_app import app
    except ImportError as e:
        print("[LỖI] Thiếu thư viện để chạy Giao diện Web:")
        print(f"      {e}")
        print("      Vui lòng cài đặt bằng lệnh: pip install -r requirements.txt")
        sys.exit(1)

    # 1. Kiểm tra xung đột cổng
    port, port_changed = find_available_port(args.port)
    
    # 2. Kiểm tra tên miền riêng pdfscanmodifier
    has_domain = is_custom_domain_available("pdfscanmodifier")
    
    if has_domain:
        display_host = "pdfscanmodifier"
    else:
        display_host = "localhost"
        
    access_url = f"http://{display_host}:{port}/"

    print("=" * 76)
    print("    CÔNG CỤ CHỈNH SỬA TÀI LIỆU SCAN PDF — GIAO DIỆN WEB STUDIO")
    print("=" * 76)
    
    if port_changed:
        print(f"[CẢNH BÁO] Cổng {args.port} đang được ứng dụng khác sử dụng!")
        print(f"           -> Hệ thống tự động chuyển sang cổng an toàn: {port}")
        print()

    print(f" 🌐 ĐỊA CHỈ TRUY CẬP: {access_url}")
    print(f"    (Hoặc: http://localhost:{port}/ | http://127.0.0.1:{port}/)")
    print()

    if not has_domain:
        print(" 💡 MẸO TÊN MIỀN RIÊNG:")
        print("    Để dùng tên miền ngắn đẹp http://pdfscanmodifier:8000/ không lo trùng lặp,")
        print("    bạn chỉ cần nhấp đúp vào file 'cai_dat_ten_mien.bat' 1 lần duy nhất!")
        print()

    print(" • Nhấn Ctrl + C để dừng máy chủ bất cứ lúc nào.")
    print("=" * 76 + "\n")

    # Mở trình duyệt ở luồng phụ
    if not args.no_browser:
        threading.Thread(target=open_browser, args=(access_url,), daemon=True).start()

    # Lắng nghe trên 0.0.0.0 để nhận cả pdfscanmodifier, localhost và 127.0.0.1
    uvicorn.run(app, host=args.host, port=port, log_level="info")


if __name__ == "__main__":
    main()
