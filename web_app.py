# -*- coding: utf-8 -*-
"""
CÔNG CỤ GIAO DIỆN WEB CHỈNH SỬA TÀI LIỆU PDF SCAN (WEB UI APP)
Backend FastAPI phục vụ Web App chỉnh sửa PDF scan chính xác cao:
- Hiển thị tài liệu PDF scan trực quan, phóng to/thu nhỏ mượt mà.
- Kéo quét chọn vùng (ROI) tương tác trực tiếp trên trình duyệt.
- Tự động bóc tách 100% thuộc tính: Font, Cỡ, Độ đậm nét, Độ nghiêng, Màu mực, Màu giấy, Baseline Y, Độ rỗ.
- Tùy chỉnh mức độ rỗ (roughness) thời gian thực và so sánh Before/After.
- Quản lý hàng đợi sửa đổi hàng loạt (Batch Queue) và xuất PDF chuẩn scan 300 DPI.
"""

import os
import sys
import io
import json
import base64
import time
from typing import Optional, List, Dict, Any
from pathlib import Path

# Đảm bảo UTF-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import công cụ cốt lõi từ edit_scanned_pdf.py
try:
    from edit_scanned_pdf import ScannedPdfEditor, parse_roughness
except ImportError:
    raise RuntimeError("Không tìm thấy file 'edit_scanned_pdf.py' trong cùng thư mục!")

if getattr(sys, 'frozen', False):
    # Đang chạy dưới dạng file .exe độc lập (PyInstaller)
    BUNDLE_DIR = Path(getattr(sys, '_MEIPASS', sys.executable))
    BASE_DIR = Path(sys.executable).parent
    # Ưu tiên thư mục static ngoài nếu có để cập nhật CSS/JS ngay lập tức không cần build lại
    if (BASE_DIR / "static").exists():
        STATIC_DIR = BASE_DIR / "static"
    elif (BASE_DIR.parent / "static").exists():
        STATIC_DIR = BASE_DIR.parent / "static"
    elif (BUNDLE_DIR / "static").exists():
        STATIC_DIR = BUNDLE_DIR / "static"
    else:
        STATIC_DIR = BASE_DIR / "static"
else:
    BASE_DIR = Path(__file__).resolve().parent
    STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

app = FastAPI(title="PDF Scan Text Modifier Studio", version="1.0.0")

# Cache dữ liệu trang scan đang mở để tăng tốc độ tải
PAGE_CACHE: Dict[str, Image.Image] = {}


def get_cached_page_image(pdf_path: str, page_num: int = 0) -> Image.Image:
    """Tải và lưu đệm ảnh scan gốc của trang PDF."""
    cache_key = f"{pdf_path}:{page_num}:{os.path.getmtime(pdf_path)}"
    if cache_key in PAGE_CACHE:
        return PAGE_CACHE[cache_key]
    
    # Dọn dẹp cache nếu quá nhiều trang
    if len(PAGE_CACHE) > 10:
        PAGE_CACHE.clear()
        
    doc = fitz.open(pdf_path)
    if page_num >= len(doc):
        doc.close()
        raise HTTPException(status_code=400, detail=f"Trang {page_num} không tồn tại (tài liệu có {len(doc)} trang)")
    
    page = doc[page_num]
    images = page.get_images()
    if not images:
        doc.close()
        raise HTTPException(status_code=400, detail=f"Không tìm thấy ảnh scan trong trang {page_num}")
        
    img_xref = images[0][0]
    base_img = doc.extract_image(img_xref)
    img_pil = Image.open(io.BytesIO(base_img["image"])).convert("RGB")
    doc.close()
    
    PAGE_CACHE[cache_key] = img_pil
    return img_pil


def image_to_base64_jpeg(im: Image.Image, quality: int = 90) -> str:
    """Chuyển PIL Image thành chuỗi Base64 Data URL JPEG."""
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=quality)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    pdf: str
    page: int = 0
    box: List[int]  # [x, y, w, h]


class PreviewRequest(BaseModel):
    pdf: str
    page: int = 0
    action: str = "replace"  # "replace" hoặc "insert"
    box: List[int]           # [x, y, w, h]
    text: str = ""
    font_name: str = "auto"
    font_size: int = 0
    align: str = "auto"
    roughness: Any = 1.0
    color: Optional[List[int]] = None
    bg_color: Optional[List[int]] = None


class BatchEditItem(BaseModel):
    id: Optional[str] = None
    enabled: bool = True
    page: int = 0
    action: str = "replace"  # "replace" hoặc "insert"
    box: List[int]           # [x, y, w, h]
    text: str = ""
    font_name: str = "auto"
    font_size: int = 0
    align: str = "auto"
    roughness: Any = 1.0
    color: Optional[List[int]] = None
    bg_color: Optional[List[int]] = None
    description: Optional[str] = ""


class BatchApplyRequest(BaseModel):
    pdf: str
    output_name: Optional[str] = None
    save_to_source_dir: bool = True
    edits: List[BatchEditItem]


class OpenLocationRequest(BaseModel):
    filename: str


class UploadPdfRequest(BaseModel):
    filename: str
    data_base64: str


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/documents")
def list_documents():
    """Liệt kê danh sách các file PDF scan có sẵn trong thư mục làm việc."""
    pdf_files = []
    for f in BASE_DIR.glob("*.pdf"):
        try:
            stat = f.stat()
            pdf_files.append({
                "name": f.name,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
            })
        except Exception:
            continue
    pdf_files.sort(key=lambda x: x["name"].lower())
    return {"documents": pdf_files}


@app.get("/api/document/{filename}/info")
def get_document_info(filename: str):
    """Lấy thông tin chi tiết số trang, kích thước của file PDF."""
    pdf_path = BASE_DIR / filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"Không tìm thấy file '{filename}'")
    
    try:
        doc = fitz.open(str(pdf_path))
        num_pages = len(doc)
        pages_info = []
        
        for i in range(num_pages):
            page = doc[i]
            images = page.get_images()
            has_scan = len(images) > 0
            w, h = 0, 0
            if has_scan:
                try:
                    img_xref = images[0][0]
                    base_img = doc.extract_image(img_xref)
                    w = base_img["width"]
                    h = base_img["height"]
                except Exception:
                    pass
            pages_info.append({
                "page": i,
                "display_num": i + 1,
                "has_scan": has_scan,
                "width": w,
                "height": h,
                "page_rect": [page.rect.x0, page.rect.y0, page.rect.x1, page.rect.y1]
            })
            
        doc.close()
        return {
            "filename": filename,
            "num_pages": num_pages,
            "pages": pages_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi mở tài liệu PDF: {str(e)}")


@app.get("/api/document/{filename}/page/{page_num}")
def get_page_image(
    filename: str,
    page_num: int = 0,
    max_dim: Optional[int] = Query(None, description="Thu nhỏ ảnh để tải nhanh (thumbnail/preview)")
):
    """Xuất ảnh của trang PDF scan (hỗ trợ scale để xem mượt mà)."""
    pdf_path = BASE_DIR / filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"Không tìm thấy file '{filename}'")
    
    img_pil = get_cached_page_image(str(pdf_path), page_num)
    
    # Nếu yêu cầu thu nhỏ (cho thumbnail hoặc hiển thị vừa màn hình)
    if max_dim and max(img_pil.size) > max_dim:
        scale = max_dim / float(max(img_pil.size))
        new_w = max(1, int(round(img_pil.width * scale)))
        new_h = max(1, int(round(img_pil.height * scale)))
        resized = img_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        resized.save(buf, format="JPEG", quality=85)
    else:
        buf = io.BytesIO()
        img_pil.save(buf, format="JPEG", quality=92)
        
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/jpeg")


@app.post("/api/analyze")
def analyze_roi(req: AnalyzeRequest):
    """
    Bóc tách toàn bộ thuộc tính văn bản trong vùng chọn ROI:
    Cỡ font, độ đậm, độ nghiêng, màu mực, màu giấy nền, độ rỗ thớ giấy, baseline Y.
    """
    pdf_path = BASE_DIR / req.pdf
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"Không tìm thấy file '{req.pdf}'")
    
    if len(req.box) != 4:
        raise HTTPException(status_code=400, detail="Tọa độ box phải có 4 phần tử [x, y, w, h]")
        
    x, y, w, h = req.box
    if w <= 0 or h <= 0:
        raise HTTPException(status_code=400, detail="Chiều rộng và chiều cao vùng chọn phải > 0")

    try:
        editor = ScannedPdfEditor(str(pdf_path), page_num=req.page)
        analysis = editor.analyze_region(x, y, w, h)
        
        # Cắt ảnh vùng chọn để gửi về xem trước
        crop_box = (max(0, x), max(0, y), min(editor.width, x + w), min(editor.height, y + h))
        crop_im = editor.image.crop(crop_box)
        crop_b64 = image_to_base64_jpeg(crop_im, quality=95)
        
        return {
            "success": True,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "analysis": analysis,
            "crop_image": crop_b64,
            "page_width": editor.width,
            "page_height": editor.height
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi bóc tách vùng chọn: {str(e)}")


@app.post("/api/preview")
def preview_edit(req: PreviewRequest):
    """
    Xem trước kết quả sửa chữ / chèn chữ thời gian thực (mô phỏng độ rỗ, màu mực, màu nền).
    Trả về ảnh so sánh Trước (Before) và Sau (After) kèm độ rỗ thực tế.
    """
    pdf_path = BASE_DIR / req.pdf
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"Không tìm thấy file '{req.pdf}'")
        
    x, y, w, h = req.box
    try:
        editor = ScannedPdfEditor(str(pdf_path), page_num=req.page)
        
        # Tạo vùng đệm xung quanh (padding 30px) để thấy rõ độ tiệp nền giấy
        pad_x = 40
        pad_y = 30
        crop_x = max(0, x - pad_x)
        crop_y = max(0, y - pad_y)
        crop_w = min(editor.width - crop_x, w + pad_x * 2)
        crop_h = min(editor.height - crop_y, h + pad_y * 2)
        
        # Ảnh gốc trước khi sửa (Before)
        before_crop = editor.image.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
        before_b64 = image_to_base64_jpeg(before_crop, quality=95)
        
        # Thực hiện sửa đổi trên bản sao
        r_val = parse_roughness(req.roughness)
        col = tuple(req.color) if req.color else None
        bg_col = tuple(req.bg_color) if req.bg_color else None
        
        if req.action == "replace":
            editor.replace_region(
                box=(x, y, w, h),
                new_text=req.text,
                font_name=req.font_name,
                font_size=req.font_size,
                align=req.align,
                text_color=col,
                bg_color=bg_col,
                roughness=r_val
            )
        else:  # insert
            # Với insert, y là baseline Y
            baseline_y = y if y > 0 else (y + h)
            target_x = x
            editor.insert_text(
                text=req.text,
                x=target_x,
                y=baseline_y,
                font_name=req.font_name if req.font_name != "auto" else "times.ttf",
                font_size=req.font_size if req.font_size > 0 else 52,
                align=req.align if req.align != "auto" else "left",
                color=col if col else (55, 52, 50),
                roughness=r_val,
                bg_color=bg_col
            )
            
        # Ảnh sau khi sửa (After)
        after_crop = editor.image.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
        after_b64 = image_to_base64_jpeg(after_crop, quality=95)
        
        return {
            "success": True,
            "before_image": before_b64,
            "after_image": after_b64,
            "crop_coords": {"x": crop_x, "y": crop_y, "w": crop_w, "h": crop_h},
            "roughness_applied": r_val
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tạo bản xem trước: {str(e)}")


@app.post("/api/apply-batch")
def apply_batch_edits(req: BatchApplyRequest):
    """
    Thực thi toàn bộ danh sách chỉnh sửa (Sửa hàng loạt) và xuất ra file PDF mới.
    """
    pdf_path = BASE_DIR / req.pdf
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"Không tìm thấy file '{req.pdf}'")
    
    if not req.edits:
        raise HTTPException(status_code=400, detail="Danh sách chỉnh sửa trống!")

    # Xác định tên file xuất ra và đường dẫn lưu file
    if not req.output_name or not req.output_name.strip():
        stem = pdf_path.stem
        output_filename = f"{stem}_DaSua.pdf"
    else:
        output_filename = req.output_name.strip()
        if not output_filename.lower().endswith(".pdf"):
            output_filename += ".pdf"
            
    # Lưu cùng thư mục với file PDF gốc (hoặc BASE_DIR)
    target_dir = pdf_path.parent if req.save_to_source_dir else BASE_DIR
    output_path = target_dir / output_filename
    
    try:
        # Gom các chỉnh sửa theo từng trang để tránh mở/đóng nhiều lần
        edits_by_page: Dict[int, List[BatchEditItem]] = {}
        for edit in req.edits:
            if not edit.enabled:
                continue
            edits_by_page.setdefault(edit.page, []).append(edit)
            
        if not edits_by_page:
            return {"success": False, "message": "Không có chỉnh sửa nào được kích hoạt (enabled=True)"}
            
        # Sao chép PDF gốc sang file đích trước khi ghi đè các trang
        import shutil
        shutil.copy2(str(pdf_path), str(output_path))
        
        applied_count = 0
        
        for page_num, edit_list in edits_by_page.items():
            editor = ScannedPdfEditor(str(output_path), page_num=page_num)
            for item in edit_list:
                r_val = parse_roughness(item.roughness)
                col = tuple(item.color) if item.color else None
                bg_col = tuple(item.bg_color) if item.bg_color else None
                x, y, w, h = item.box
                
                if item.action == "replace":
                    editor.replace_region(
                        box=(x, y, w, h),
                        new_text=item.text,
                        font_name=item.font_name,
                        font_size=item.font_size,
                        align=item.align,
                        text_color=col,
                        bg_color=bg_col,
                        roughness=r_val
                    )
                else:  # insert
                    editor.insert_text(
                        text=item.text,
                        x=x,
                        y=y,
                        font_name=item.font_name if item.font_name != "auto" else "times.ttf",
                        font_size=item.font_size if item.font_size > 0 else 52,
                        align=item.align if item.align != "auto" else "left",
                        color=col if col else (55, 52, 50),
                        roughness=r_val,
                        bg_color=bg_col
                    )
                applied_count += 1
                
            # Lưu lại trang vào file PDF đích
            editor.save(str(output_path))
            
        return {
            "success": True,
            "applied_count": applied_count,
            "output_filename": output_filename,
            "saved_path": str(output_path.resolve()),
            "source_dir": str(target_dir.resolve()),
            "download_url": f"/api/download/{output_filename}",
            "message": f"Đã lưu thành công {applied_count} chỉnh sửa vào file '{output_path.resolve()}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi thực hiện sửa hàng loạt: {str(e)}")


@app.post("/api/open-file-location")
def open_file_location(req: OpenLocationRequest):
    """Mở thư mục chứa file trong Windows Explorer và chọn trực tiếp vào file."""
    path = (BASE_DIR / req.filename).resolve()
    if not path.exists():
        path = Path(req.filename).resolve()
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Không tìm thấy file: {req.filename}")
        
    if sys.platform == "win32":
        import subprocess
        try:
            subprocess.Popen(f'explorer.exe /select,"{str(path)}"')
            return {"success": True, "path": str(path)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi mở thư mục: {str(e)}")
    return {"success": True, "path": str(path)}


@app.get("/api/download/{filename:path}")
def download_file(filename: str):
    """Tải file PDF kết quả về máy người dùng."""
    file_path = BASE_DIR / filename
    if not file_path.exists():
        file_path = Path(filename)
    if not file_path.exists():
        found = list(BASE_DIR.rglob(Path(filename).name))
        if found:
            file_path = found[0]
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File không tồn tại")
    return FileResponse(
        str(file_path),
        media_type="application/pdf",
        filename=Path(filename).name,
        headers={"Content-Disposition": f'attachment; filename="{Path(filename).name}"'}
    )


@app.post("/api/upload")
def upload_pdf(req: UploadPdfRequest):
    """Tải file PDF mới từ máy tính người dùng lên server."""
    try:
        # Bóc tách phần base64 nếu có prefix data URL
        raw_b64 = req.data_base64
        if "," in raw_b64:
            raw_b64 = raw_b64.split(",", 1)[1]
            
        data = base64.b64decode(raw_b64)
        safe_name = Path(req.filename).name
        if not safe_name.lower().endswith(".pdf"):
            safe_name += ".pdf"
            
        target_path = BASE_DIR / safe_name
        with open(target_path, "wb") as f:
            f.write(data)
            
        return {
            "success": True,
            "filename": safe_name,
            "size_bytes": len(data),
            "message": f"Đã tải lên thành công '{safe_name}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tải lên file PDF: {str(e)}")


@app.get("/api/system-fonts")
def get_system_fonts():
    """Danh sách các font chữ chuẩn hệ thống hỗ trợ chỉnh sửa tài liệu scan."""
    curated_fonts = [
        {"id": "times.ttf", "family": "Times New Roman", "style": "Regular (Thường)", "rec": True},
        {"id": "timesbd.ttf", "family": "Times New Roman", "style": "Bold (Đậm)", "rec": True},
        {"id": "timesi.ttf", "family": "Times New Roman", "style": "Italic (Nghiêng)", "rec": True},
        {"id": "timesbi.ttf", "family": "Times New Roman", "style": "Bold Italic (Đậm Nghiêng)", "rec": True},
        {"id": "arial.ttf", "family": "Arial", "style": "Regular (Thường)", "rec": True},
        {"id": "arialbd.ttf", "family": "Arial", "style": "Bold (Đậm)", "rec": True},
        {"id": "ariali.ttf", "family": "Arial", "style": "Italic (Nghiêng)", "rec": True},
        {"id": "arialbi.ttf", "family": "Arial", "style": "Bold Italic (Đậm Nghiêng)", "rec": True},
        {"id": "calibri.ttf", "family": "Calibri", "style": "Regular (Thường)", "rec": True},
        {"id": "calibrib.ttf", "family": "Calibri", "style": "Bold (Đậm)", "rec": True},
        {"id": "calibrii.ttf", "family": "Calibri", "style": "Italic (Nghiêng)", "rec": True},
        {"id": "tahoma.ttf", "family": "Tahoma", "style": "Regular (Thường)", "rec": True},
        {"id": "tahomabd.ttf", "family": "Tahoma", "style": "Bold (Đậm)", "rec": True},
        {"id": "cour.ttf", "family": "Courier New", "style": "Regular (Máy đánh chữ)", "rec": False},
        {"id": "courbd.ttf", "family": "Courier New", "style": "Bold (Máy đánh chữ Đậm)", "rec": False},
        {"id": "GOTHIC.TTF", "family": "Century Gothic", "style": "Regular (Thường)", "rec": False},
        {"id": "GOTHICB.TTF", "family": "Century Gothic", "style": "Bold (Đậm)", "rec": False}
    ]
    return {"fonts": curated_fonts}


# Phục vụ các file tĩnh UI
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_index():
    """Mở giao diện Web App chính."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        return HTMLResponse("<h1>Đang khởi tạo giao diện UI App...</h1>", status_code=200)
    return FileResponse(str(index_path))


def run_server(host="0.0.0.0", port=8000):
    import uvicorn
    print("\n" + "=" * 76)
    print(" CÔNG CỤ CHỈNH SỬA TÀI LIỆU SCAN PDF - GIAO DIỆN WEB STUDIO")
    print(f" • Địa chỉ truy cập trực tiếp: http://localhost:{port}/")
    print(" • Nhấn Ctrl + C trên cửa sổ lệnh để dừng máy chủ bất kỳ lúc nào.")
    print("=" * 76 + "\n")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
