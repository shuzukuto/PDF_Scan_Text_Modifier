# -*- coding: utf-8 -*-
"""
ANONYMOUS USAGE TELEMETRY MODULE FOR PDF SCAN TEXT MODIFIER
Tuân thủ tiêu chuẩn mã nguồn mở MIT License:
- 100% ẨN DANH: Tuyệt đối không thu thập nội dung tài liệu, tên file hay thông tin cá nhân.
- Tự sinh Anonymous Client ID (UUID ngẫu nhiên) duy nhất cho mỗi máy để đếm DAU/WAU/MAU.
- Chạy ngầm trong nền (Daemon Thread), không gây trễ hay ảnh hưởng khi mất mạng.
- Cho phép người dùng tắt bất cứ lúc nào (Opt-out).
"""

import os
import sys
import uuid
import json
import platform
import threading
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Any

# Google Analytics 4 Credentials (Measurement Protocol)
GA_MEASUREMENT_ID = "G-YNMPPM82TP"
GA_API_SECRET = "wBZ28U1gRkCU90s3Xemfpg"
GA_ENDPOINT = f"https://www.google-analytics.com/mp/collect?api_secret={GA_API_SECRET}&measurement_id={GA_MEASUREMENT_ID}"

APP_VERSION = "1.0.1"

# Thư mục lưu cấu hình client ID ẩn danh
CONFIG_DIR = Path.home() / ".pdf_scan_modifier"
CLIENT_ID_FILE = CONFIG_DIR / "anonymous_client_id"
OPT_OUT_FILE = CONFIG_DIR / "telemetry_disabled"


def get_anonymous_client_id() -> str:
    """Lấy hoặc tự động sinh một mã client ID ẩn danh (UUID v4) duy nhất cho máy."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if CLIENT_ID_FILE.exists():
            cid = CLIENT_ID_FILE.read_text(encoding="utf-8").strip()
            if cid:
                return cid
        new_id = str(uuid.uuid4())
        CLIENT_ID_FILE.write_text(new_id, encoding="utf-8")
        return new_id
    except Exception:
        return str(uuid.uuid4())


def is_telemetry_enabled() -> bool:
    """Kiểm tra trạng thái bật/tắt gửi số liệu thống kê ẩn danh."""
    try:
        if OPT_OUT_FILE.exists():
            return False
        if os.environ.get("PDF_SCAN_TELEMETRY_OPT_OUT", "").strip().lower() in ("1", "true", "yes"):
            return False
        return True
    except Exception:
        return True


def set_telemetry_enabled(enabled: bool):
    """Bật hoặc tắt thống kê ẩn danh theo lựa chọn của người dùng."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not enabled:
            OPT_OUT_FILE.write_text("1", encoding="utf-8")
        else:
            if OPT_OUT_FILE.exists():
                OPT_OUT_FILE.unlink()
    except Exception:
        pass


def _send_payload_async(payload: dict):
    """Gửi payload JSON tới Google Analytics 4 ngầm trong luồng phụ (không lag app)."""
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            GA_ENDPOINT,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": f"PDFScanModifier/{APP_VERSION} ({platform.system()}; {platform.release()})"
            }
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            pass  # Google trả về HTTP 204 No Content khi thành công
    except Exception:
        # Nếu mất mạng, lỗi DNS hoặc timeout -> âm thầm bỏ qua, tuyệt đối không ảnh hưởng app
        pass


def track_event(event_name: str, params: Optional[Dict[str, Any]] = None):
    """
    Ghi nhận một sự kiện thống kê ẩn danh tới Google Analytics 4.
    Được thực thi trong luồng riêng biệt (Daemon Thread).
    """
    if not is_telemetry_enabled():
        return

    try:
        client_id = get_anonymous_client_id()
        event_params = {
            "app_version": APP_VERSION,
            "os_name": platform.system(),
            "os_release": platform.release(),
            "engagement_time_msec": 1000,
        }
        if params:
            event_params.update(params)

        payload = {
            "client_id": client_id,
            "events": [
                {
                    "name": event_name,
                    "params": event_params
                }
            ]
        }

        # Bắn request trong thread daemon để không làm chậm luồng chính
        t = threading.Thread(target=_send_payload_async, args=(payload,), daemon=True)
        t.start()
    except Exception:
        pass
