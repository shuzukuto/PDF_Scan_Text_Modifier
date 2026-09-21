/**
 * PDF SCAN TEXT MODIFIER STUDIO — FRONTEND APPLICATION CONTROLLER
 * Tuân thủ tiêu chuẩn UI/UX Pro Max & Frontend Design
 */

(function () {
  'use strict';

  // APPLICATION STATE
  const state = {
    currentDoc: null,
    currentPage: 0,
    pageCount: 0,
    docInfo: null,
    
    // Page Image & Canvas Dimensions
    pageImg: null,
    naturalWidth: 0,
    naturalHeight: 0,
    
    // Canvas Pan & Zoom
    scale: 1.0,
    panX: 0,
    panY: 0,
    isPanning: false,
    startPanX: 0,
    startPanY: 0,
    
    // Active Tool: 'select', 'hand', 'loupe'
    activeTool: 'select',
    
    // Selection ROI in native scan pixel coordinates: {x, y, w, h}
    roi: null,
    isSelecting: false,
    isMovingRoi: false,
    isResizing: false,
    startRoi: null,
    startSelectX: 0,
    startSelectY: 0,
    activeHandle: null,
    
    // Last Analysis Results from /api/analyze
    currentAnalysis: null,
    
    // Batch Edit Queue
    queue: [],
    editingQueueItemId: null,
    
    // UI Theme
    theme: localStorage.getItem('scan_studio_theme') || 'dark',
    
    // Split Comparison Slider (0 to 100%)
    splitPos: 50,
    isDraggingSplit: false
  };

  // DOM ELEMENTS CACHE
  const dom = {
    docSelect: document.getElementById('doc-select'),
    btnUploadTrigger: document.getElementById('btn-upload-trigger'),
    fileUploader: document.getElementById('file-uploader'),
    pagesList: document.getElementById('pages-list'),
    pageCountBadge: document.getElementById('page-count-badge'),
    docMetaCard: document.getElementById('doc-meta-card'),
    metaResolution: document.getElementById('meta-resolution'),
    metaFilesize: document.getElementById('meta-filesize'),
    
    // Canvas Viewport & Stage
    viewport: document.getElementById('canvas-viewport'),
    stage: document.getElementById('canvas-stage'),
    canvas: document.getElementById('pdf-canvas'),
    emptyState: document.getElementById('canvas-empty-state'),
    btnEmptyUpload: document.getElementById('btn-empty-upload'),
    
    // Selection Box Overlay & Handles
    selectionBox: document.getElementById('selection-box'),
    hudCoords: document.getElementById('hud-coords'),
    baselineGuide: document.getElementById('baseline-guide'),
    floatingBar: document.getElementById('canvas-floating-bar'),
    floatRoiInfo: document.getElementById('float-roi-info'),
    btnQuickAnalyze: document.getElementById('btn-quick-analyze'),
    btnQuickReplace: document.getElementById('btn-quick-replace'),
    btnQuickClear: document.getElementById('btn-quick-clear'),
    
    // Loupe
    loupeLens: document.getElementById('loupe-lens'),
    loupeCanvas: document.getElementById('loupe-canvas'),
    loupeBadge: document.getElementById('loupe-badge'),
    
    // Toolbar Tools
    toolSelect: document.getElementById('tool-select'),
    toolHand: document.getElementById('tool-hand'),
    toolLoupe: document.getElementById('tool-loupe'),
    btnZoomIn: document.getElementById('btn-zoom-in'),
    btnZoomOut: document.getElementById('btn-zoom-out'),
    btnZoomLevel: document.getElementById('btn-zoom-level'),
    btnZoomFit: document.getElementById('btn-zoom-fit'),
    
    // Theme & Shortcuts
    btnThemeToggle: document.getElementById('btn-theme-toggle'),
    iconSun: document.getElementById('icon-sun'),
    iconMoon: document.getElementById('icon-moon'),
    btnShortcutsTrigger: document.getElementById('btn-shortcuts-trigger'),
    shortcutsModal: document.getElementById('shortcuts-modal'),
    btnCloseModal: document.getElementById('btn-close-modal'),
    
    // Tabs
    tabBtnInspect: document.getElementById('tab-btn-inspect'),
    tabBtnEdit: document.getElementById('tab-btn-edit'),
    tabBtnQueue: document.getElementById('tab-btn-queue'),
    tabContentInspect: document.getElementById('tab-content-inspect'),
    tabContentEdit: document.getElementById('tab-content-edit'),
    tabContentQueue: document.getElementById('tab-content-queue'),
    badgeQueueCount: document.getElementById('badge-queue-count'),
    tabBadgeQueue: document.getElementById('tab-badge-queue'),
    
    // Tab 1: Inspector Elements
    cropContainer: document.getElementById('crop-preview-container'),
    inspectCoordsBox: document.getElementById('inspect-coords-box'),
    inspectBaselineHud: document.getElementById('inspect-baseline-hud'),
    inspectStyleDesc: document.getElementById('inspect-style-desc'),
    inspectFontSize: document.getElementById('inspect-font-size'),
    inspectStroke: document.getElementById('inspect-stroke'),
    inspectDensity: document.getElementById('inspect-density'),
    inspectFontFile: document.getElementById('inspect-font-file'),
    inspectFontAlt: document.getElementById('inspect-font-alt'),
    inspectAlignRec: document.getElementById('inspect-align-rec'),
    swatchInk: document.getElementById('swatch-ink'),
    inspectInkHex: document.getElementById('inspect-ink-hex'),
    inspectInkStd: document.getElementById('inspect-ink-std'),
    swatchBg: document.getElementById('swatch-bg'),
    inspectBgHex: document.getElementById('inspect-bg-hex'),
    inspectBgStd: document.getElementById('inspect-bg-std'),
    btnReanalyze: document.getElementById('btn-reanalyze'),
    btnLoadToEdit: document.getElementById('btn-load-to-edit'),
    
    // Tab 2: Edit Studio
    modeReplace: document.getElementById('mode-replace'),
    modeInsert: document.getElementById('mode-insert'),
    inputNewText: document.getElementById('input-new-text'),
    selectFont: document.getElementById('select-font'),
    inputFontSize: document.getElementById('input-font-size'),
    alignBtns: document.querySelectorAll('.align-btn'),
    sliderRoughness: document.getElementById('slider-roughness'),
    roughnessValDisplay: document.getElementById('roughness-val-display'),
    roughnessChips: document.querySelectorAll('.chip-btn'),
    pickerInk: document.getElementById('picker-ink'),
    hexInk: document.getElementById('hex-ink'),
    pickerBg: document.getElementById('picker-bg'),
    hexBg: document.getElementById('hex-bg'),
    groupBgColor: document.getElementById('group-bg-color'),
    btnRefreshPreview: document.getElementById('btn-refresh-preview'),
    splitSliderWrap: document.getElementById('split-slider-wrap'),
    splitLayerAfter: document.getElementById('split-layer-after'),
    splitHandle: document.getElementById('split-handle'),
    imgCompareBefore: document.getElementById('img-compare-before'),
    imgCompareAfter: document.getElementById('img-compare-after'),
    btnAddQueue: document.getElementById('btn-add-to-queue'),
    btnCancelEditMode: document.getElementById('btn-cancel-edit-mode'),
    
    // Tab 3: Queue
    queueList: document.getElementById('queue-list'),
    inputOutputName: document.getElementById('input-output-name'),
    chkSaveSameDir: document.getElementById('chk-save-same-dir'),
    chkDownloadBrowser: document.getElementById('chk-download-browser'),
    btnRunBatch: document.getElementById('btn-run-batch'),
    saveSuccessBox: document.getElementById('save-success-box'),
    savedFilePath: document.getElementById('saved-file-path'),
    btnOpenSavedFolder: document.getElementById('btn-open-saved-folder'),
    btnExportPdf: document.getElementById('btn-export-pdf'),
    btnExportRecipe: document.getElementById('btn-export-recipe'),
    btnImportRecipeTrigger: document.getElementById('btn-import-recipe-trigger'),
    recipeUploader: document.getElementById('recipe-uploader'),
    btnClearQueue: document.getElementById('btn-clear-queue'),
    
    // Status Bar & Toasts
    statusMessage: document.getElementById('status-message'),
    chipCursor: document.getElementById('chip-cursor'),
    chipSelection: document.getElementById('chip-selection'),
    chipZoom: document.getElementById('chip-zoom'),
    toastContainer: document.getElementById('toast-container')
  };

  const ctx = dom.canvas.getContext('2d');
  const loupeCtx = dom.loupeCanvas.getContext('2d');

  // ========================================================================
  // INITIALIZATION
  // ========================================================================
  async function init() {
    applyTheme(state.theme);
    bindEvents();
    setupSplitSlider();
    await loadDocumentsList();
    showToast('Chào mừng bạn đến với PDF Scan Text Modifier Studio!', 'info');
  }

  // ========================================================================
  // THEME & TOAST SYSTEM
  // ========================================================================
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('scan_studio_theme', theme);
    if (theme === 'light') {
      dom.iconSun.classList.add('hidden');
      dom.iconMoon.classList.remove('hidden');
    } else {
      dom.iconSun.classList.remove('hidden');
      dom.iconMoon.classList.add('hidden');
    }
  }

  function showToast(msg, type = 'info', duration = 3500) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = msg;
    dom.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 250);
    }, duration);
  }

  function setStatus(msg) {
    dom.statusMessage.textContent = msg;
  }

  // ========================================================================
  // DOCUMENT & PAGE LOADING
  // ========================================================================
  async function loadDocumentsList(selectFilename = null) {
    try {
      const res = await fetch('/api/documents');
      const data = await res.json();
      dom.docSelect.innerHTML = '';
      
      if (!data.documents || data.documents.length === 0) {
        dom.docSelect.innerHTML = '<option value="">Không có file PDF nào</option>';
        dom.emptyState.classList.remove('hidden');
        return;
      }
      
      data.documents.forEach((doc) => {
        const opt = document.createElement('option');
        opt.value = doc.name;
        opt.textContent = `${doc.name} (${doc.size_mb} MB)`;
        dom.docSelect.appendChild(opt);
      });
      
      const targetDoc = selectFilename || (data.documents[0] ? data.documents[0].name : null);
      if (targetDoc) {
        dom.docSelect.value = targetDoc;
        await loadDocument(targetDoc);
      }
    } catch (err) {
      showToast('Lỗi tải danh sách tài liệu: ' + err.message, 'error');
    }
  }

  async function loadDocument(filename) {
    if (!filename) return;
    state.currentDoc = filename;
    setStatus(`Đang mở tài liệu '${filename}'...`);
    
    try {
      const res = await fetch(`/api/document/${encodeURIComponent(filename)}/info`);
      if (!res.ok) throw new Error('Không thể tải thông tin tài liệu');
      const info = await res.json();
      state.docInfo = info;
      state.pageCount = info.num_pages;
      
      dom.pageCountBadge.textContent = `${info.num_pages} trang`;
      dom.emptyState.classList.add('hidden');
      
      // Đề xuất tên file xuất ra mặc định
      const stem = filename.replace(/\.pdf$/i, '');
      dom.inputOutputName.value = `${stem}_DaSua.pdf`;
      
      // Render danh sách thumbnail các trang
      renderPageThumbnails(info);
      
      // Tải trang đầu tiên
      await loadPage(0);
      setStatus(`Đã mở tài liệu '${filename}'`);
    } catch (err) {
      showToast('Lỗi mở PDF: ' + err.message, 'error');
      setStatus('Lỗi mở tài liệu');
    }
  }

  function renderPageThumbnails(info) {
    dom.pagesList.innerHTML = '';
    info.pages.forEach((p) => {
      const item = document.createElement('div');
      item.className = `page-thumb-item ${p.page === state.currentPage ? 'active' : ''}`;
      item.dataset.page = p.page;
      
      item.innerHTML = `
        <div class="thumb-img-wrap">
          <img src="/api/document/${encodeURIComponent(state.currentDoc)}/page/${p.page}?max_dim=240" loading="lazy" alt="Trang ${p.display_num}">
        </div>
        <div class="thumb-meta">
          <span>Trang ${p.display_num}</span>
          <span class="font-mono">${p.width}x${p.height}</span>
        </div>
      `;
      
      item.addEventListener('click', () => loadPage(p.page));
      dom.pagesList.appendChild(item);
    });
  }

  async function loadPage(pageNum) {
    state.currentPage = pageNum;
    
    // Cập nhật trạng thái thumbnail active
    document.querySelectorAll('.page-thumb-item').forEach((el) => {
      el.classList.toggle('active', parseInt(el.dataset.page, 10) === pageNum);
    });
    
    setStatus(`Đang tải ảnh scan trang ${pageNum + 1}...`);
    clearSelection();
    
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.src = `/api/document/${encodeURIComponent(state.currentDoc)}/page/${pageNum}`;
    
    img.onload = () => {
      state.pageImg = img;
      state.naturalWidth = img.naturalWidth;
      state.naturalHeight = img.naturalHeight;
      
      dom.canvas.width = img.naturalWidth;
      dom.canvas.height = img.naturalHeight;
      
      dom.metaResolution.textContent = `${img.naturalWidth} x ${img.naturalHeight} px`;
      dom.docMetaCard.style.display = 'block';
      
      // Tự động căn vừa khít màn hình lúc đầu
      fitToWindow();
      renderCanvas();
      setStatus(`Sẵn sàng — Trang ${pageNum + 1} (${img.naturalWidth}x${img.naturalHeight} px)`);
    };
    
    img.onerror = () => {
      showToast(`Không thể tải ảnh scan trang ${pageNum + 1}`, 'error');
    };
  }

  // ========================================================================
  // CANVAS ENGINE (ZOOM, PAN, DRAW)
  // ========================================================================
  function renderCanvas() {
    if (!state.pageImg) return;
    ctx.clearRect(0, 0, dom.canvas.width, dom.canvas.height);
    ctx.drawImage(state.pageImg, 0, 0);
    updateStageTransform();
    updateSelectionOverlay();
  }

  function updateStageTransform() {
    dom.stage.style.transform = `translate(${state.panX}px, ${state.panY}px) scale(${state.scale})`;
    dom.chipZoom.textContent = `Scale: ${Math.round(state.scale * 100)}%`;
    dom.btnZoomLevel.textContent = `${Math.round(state.scale * 100)}%`;
    updateSelectionOverlay();
  }

  function zoomAt(targetScale, focalClientX, focalClientY) {
    const clampedScale = Math.max(0.08, Math.min(6.0, targetScale));
    const rect = dom.viewport.getBoundingClientRect();
    const cx = focalClientX !== undefined ? focalClientX - rect.left : rect.width / 2;
    const cy = focalClientY !== undefined ? focalClientY - rect.top : rect.height / 2;
    
    // Duy trì tâm zoom tại con trỏ chuột
    const canvasX = (cx - state.panX) / state.scale;
    const canvasY = (cy - state.panY) / state.scale;
    
    state.scale = clampedScale;
    state.panX = cx - canvasX * state.scale;
    state.panY = cy - canvasY * state.scale;
    
    renderCanvas();
  }

  function fitToWindow() {
    if (!state.naturalWidth || !state.naturalHeight) return;
    const vpRect = dom.viewport.getBoundingClientRect();
    const pad = 40;
    const scaleX = (vpRect.width - pad) / state.naturalWidth;
    const scaleY = (vpRect.height - pad) / state.naturalHeight;
    state.scale = Math.min(scaleX, scaleY, 1.0);
    state.panX = (vpRect.width - state.naturalWidth * state.scale) / 2;
    state.panY = (vpRect.height - state.naturalHeight * state.scale) / 2;
    renderCanvas();
  }

  function clientToCanvasCoords(clientX, clientY) {
    const rect = dom.viewport.getBoundingClientRect();
    const vx = clientX - rect.left;
    const vy = clientY - rect.top;
    const cx = Math.round((vx - state.panX) / state.scale);
    const cy = Math.round((vy - state.panY) / state.scale);
    return {
      x: Math.max(0, Math.min(state.naturalWidth, cx)),
      y: Math.max(0, Math.min(state.naturalHeight, cy))
    };
  }

  // ========================================================================
  // INTERACTIVE ROI SELECTION BOX
  // ========================================================================
  function setRoi(x, y, w, h) {
    if (!state.naturalWidth) return;
    
    // Chuẩn hóa x, y, w, h
    const rx = Math.max(0, Math.min(state.naturalWidth - 1, Math.round(x)));
    const ry = Math.max(0, Math.min(state.naturalHeight - 1, Math.round(y)));
    const rw = Math.max(1, Math.min(state.naturalWidth - rx, Math.round(w)));
    const rh = Math.max(1, Math.min(state.naturalHeight - ry, Math.round(h)));
    
    state.roi = { x: rx, y: ry, w: rw, h: rh };
    updateSelectionOverlay();
    
    // Cập nhật thông tin lên Floating Bar và HUD
    dom.hudCoords.textContent = `X: ${rx}, Y: ${ry} | ${rw} × ${rh} px`;
    dom.chipSelection.textContent = `Box: [${rx}, ${ry}, ${rw}, ${rh}]`;
    dom.floatRoiInfo.textContent = `[${rx}, ${ry}, ${rw}, ${rh}]`;
    dom.floatingBar.classList.remove('hidden');
  }

  function clearSelection() {
    state.roi = null;
    state.isSelecting = false;
    state.isMovingRoi = false;
    state.isResizing = false;
    state.startRoi = null;
    dom.selectionBox.classList.add('hidden');
    dom.selectionBox.classList.remove('is-dragging');
    dom.floatingBar.classList.add('hidden');
    dom.baselineGuide.classList.add('hidden');
    dom.chipSelection.textContent = 'Box: --';
  }

  function updateSelectionOverlay() {
    if (!state.roi || !state.naturalWidth) {
      dom.selectionBox.classList.add('hidden');
      return;
    }
    
    // Tính toán tọa độ và kích thước trong không gian màn hình (Screen space)
    const screenX = Math.round(state.panX + state.roi.x * state.scale);
    const screenY = Math.round(state.panY + state.roi.y * state.scale);
    const screenW = Math.max(2, Math.round(state.roi.w * state.scale));
    const screenH = Math.max(2, Math.round(state.roi.h * state.scale));
    
    dom.selectionBox.classList.remove('hidden');
    dom.selectionBox.style.left = `${screenX}px`;
    dom.selectionBox.style.top = `${screenY}px`;
    dom.selectionBox.style.width = `${screenW}px`;
    dom.selectionBox.style.height = `${screenH}px`;
    
    // Tự động lật HUD xuống dưới nếu vùng chọn quá sát cạnh trên (< 35px)
    if (screenY < 35) {
      dom.hudCoords.parentElement.classList.add('flipped');
    } else {
      dom.hudCoords.parentElement.classList.remove('flipped');
    }
    
    dom.hudCoords.textContent = `X: ${state.roi.x}, Y: ${state.roi.y} | ${state.roi.w} × ${state.roi.h} px`;
    
    // Nếu có đường chân chữ baseline Y từ phân tích thì vẽ đường kẻ vàng
    if (state.currentAnalysis && state.currentAnalysis.baseline_y) {
      const bY = state.currentAnalysis.baseline_y;
      const relScreenY = Math.round((bY - state.roi.y) * state.scale);
      dom.baselineGuide.classList.remove('hidden');
      dom.baselineGuide.style.top = `${relScreenY}px`;
      dom.baselineGuide.querySelector('.baseline-label').textContent = `Baseline Y: ${bY}`;
    } else {
      dom.baselineGuide.classList.add('hidden');
    }
  }

  // ========================================================================
  // SMART INSPECTOR & ATTRIBUTES EXTRACTION (API /api/analyze)
  // ========================================================================
  async function runAnalysis() {
    if (!state.roi || !state.currentDoc) {
      showToast('Vui lòng kéo chuột chọn một vùng trên trang PDF trước!', 'warning');
      return;
    }
    
    setStatus('Đang bóc tách font, cỡ chữ, độ đậm, màu mực, độ rỗ thớ giấy...');
    switchTab('inspect');
    
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pdf: state.currentDoc,
          page: state.currentPage,
          box: [state.roi.x, state.roi.y, state.roi.w, state.roi.h]
        })
      });
      
      if (!res.ok) throw new Error('Không thể phân tích vùng chọn');
      const data = await res.json();
      state.currentAnalysis = data.analysis;
      
      // Hiển thị kết quả bóc tách
      renderAnalysisResults(data);
      updateSelectionOverlay();
      showToast('Đã bóc tách thành công 100% thuộc tính văn bản!', 'success');
      setStatus('Đã bóc tách thuộc tính thành công');
    } catch (err) {
      showToast('Lỗi bóc tách: ' + err.message, 'error');
      setStatus('Lỗi bóc tách thuộc tính');
    }
  }

  function renderAnalysisResults(data) {
    const a = data.analysis;
    
    // Ảnh cắt vùng chọn
    dom.cropContainer.innerHTML = `<img src="${data.crop_image}" alt="Vùng chọn">`;
    dom.inspectCoordsBox.textContent = `Hộp: [${data.x}, ${data.y}, ${data.w}, ${data.h}]`;
    dom.inspectBaselineHud.textContent = `Baseline Y: ${a.baseline_y}`;
    
    // Thuộc tính hình thái ký tự
    dom.inspectStyleDesc.textContent = a.style_desc;
    dom.inspectFontSize.textContent = `${a.font_size} pt`;
    dom.inspectStroke.textContent = `${a.stroke_width} px`;
    dom.inspectDensity.textContent = `${Math.round(a.density * 100)}%`;
    
    dom.inspectFontFile.textContent = a.font_file;
    dom.inspectFontAlt.textContent = a.font_alt;
    dom.inspectAlignRec.textContent = a.align_recommendation;
    
    // Màu sắc & độ rỗ
    dom.swatchInk.style.backgroundColor = a.ink_hex;
    dom.inspectInkHex.textContent = a.ink_hex;
    dom.inspectInkStd.textContent = `std ~${a.ink_std}`;
    
    dom.swatchBg.style.backgroundColor = a.bg_hex;
    dom.inspectBgHex.textContent = a.bg_hex;
    dom.inspectBgStd.textContent = `std ~${a.bg_std}`;
  }

  function loadAnalysisToEditStudio() {
    cancelStudioEditMode();
    if (!state.currentAnalysis) {
      showToast('Chưa có dữ liệu bóc tách nào để nạp!', 'warning');
      return;
    }
    const a = state.currentAnalysis;
    
    // Nạp font và cỡ chữ
    dom.selectFont.value = a.font_file || 'auto';
    dom.inputFontSize.value = a.font_size || 52;
    
    // Nạp căn lề
    setAlign(a.suggested_align || 'auto');
    
    // Nạp màu mực và màu giấy nền
    dom.pickerInk.value = a.ink_hex || '#373432';
    dom.hexInk.value = a.ink_hex || '#373432';
    dom.pickerBg.value = a.bg_hex || '#FEFEFE';
    dom.hexBg.value = a.bg_hex || '#FEFEFE';
    
    // Chuyển sang Tab 2: Bộ sửa chữ
    switchTab('edit');
    dom.inputNewText.focus();
    showToast('Đã nạp toàn bộ thuộc tính gốc vào Bộ sửa chữ!', 'success');
  }

  // ========================================================================
  // EDIT STUDIO & REAL-TIME BEFORE / AFTER PREVIEW (API /api/preview)
  // ========================================================================
  function setAlign(align) {
    dom.alignBtns.forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.align === align);
    });
  }

  function getSelectedAlign() {
    const active = document.querySelector('.align-btn.active');
    return active ? active.dataset.align : 'auto';
  }

  function setRoughness(val) {
    const num = parseFloat(val);
    dom.sliderRoughness.value = num;
    let label = `${num.toFixed(1)}`;
    if (num === 0.0) label += ' (Tắt rỗ / phẳng)';
    else if (num <= 0.7) label += ' (Mịn nhẹ)';
    else if (num <= 1.1) label += ' (Chuẩn tự nhiên)';
    else label += ' (Rỗ thô scan)';
    dom.roughnessValDisplay.textContent = label;
    
    dom.roughnessChips.forEach((c) => {
      c.classList.toggle('active', parseFloat(c.dataset.r) === num);
    });
  }

  async function updatePreview() {
    if (!state.roi || !state.currentDoc) {
      showToast('Vui lòng chọn một vùng trên tài liệu trước khi xem thử!', 'warning');
      return;
    }
    
    const isReplace = dom.modeReplace.classList.contains('active');
    const newText = dom.inputNewText.value;
    const fontName = dom.selectFont.value;
    const fontSize = parseInt(dom.inputFontSize.value, 10) || 52;
    const align = getSelectedAlign();
    const roughness = parseFloat(dom.sliderRoughness.value) || 1.0;
    
    // Hex sang RGB
    const hexToRgb = (hex) => {
      const num = parseInt(hex.replace('#', ''), 16);
      return [(num >> 16) & 255, (num >> 8) & 255, num & 255];
    };
    
    const inkRgb = hexToRgb(dom.hexInk.value || '#373432');
    const bgRgb = hexToRgb(dom.hexBg.value || '#FEFEFE');
    
    setStatus('Đang tạo bản xem thử với mô phỏng độ rỗ scan...');
    try {
      const res = await fetch('/api/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pdf: state.currentDoc,
          page: state.currentPage,
          action: isReplace ? 'replace' : 'insert',
          box: [state.roi.x, state.roi.y, state.roi.w, state.roi.h],
          text: newText,
          font_name: fontName,
          font_size: fontSize,
          align: align,
          roughness: roughness,
          color: inkRgb,
          bg_color: bgRgb
        })
      });
      
      if (!res.ok) throw new Error('Không thể tạo bản xem trước');
      const data = await res.json();
      
      // Hiển thị hai ảnh Before & After
      dom.imgCompareBefore.src = data.before_image;
      dom.imgCompareAfter.src = data.after_image;
      
      setStatus('Đã cập nhật bản so sánh Trước / Sau');
    } catch (err) {
      showToast('Lỗi xem thử: ' + err.message, 'error');
      setStatus('Lỗi tạo xem thử');
    }
  }

  // ========================================================================
  // SPLIT COMPARISON SLIDER
  // ========================================================================
  function setupSplitSlider() {
    const wrap = dom.splitSliderWrap;
    
    function setSplit(percent) {
      const p = Math.max(0, Math.min(100, percent));
      state.splitPos = p;
      dom.splitLayerAfter.style.clipPath = `inset(0 0 0 ${p}%)`;
      dom.splitHandle.style.left = `${p}%`;
    }
    
    wrap.addEventListener('mousedown', (e) => {
      state.isDraggingSplit = true;
      const rect = wrap.getBoundingClientRect();
      setSplit(((e.clientX - rect.left) / rect.width) * 100);
    });
    
    window.addEventListener('mousemove', (e) => {
      if (!state.isDraggingSplit) return;
      const rect = wrap.getBoundingClientRect();
      setSplit(((e.clientX - rect.left) / rect.width) * 100);
    });
    
    window.addEventListener('mouseup', () => {
      state.isDraggingSplit = false;
    });
  }

  // ========================================================================
  // BATCH QUEUE MANAGEMENT (API /api/apply-batch)
  // ========================================================================
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function rgbToHex(rgb) {
    if (!rgb || !Array.isArray(rgb) || rgb.length < 3) return '#373432';
    return '#' + rgb.slice(0, 3).map(x => {
      const hex = Math.max(0, Math.min(255, Math.round(x))).toString(16);
      return hex.length === 1 ? '0' + hex : hex;
    }).join('').toUpperCase();
  }

  function hexToRgb(hex) {
    if (!hex) return [55, 52, 50];
    const cleaned = hex.replace('#', '').trim();
    if (cleaned.length === 3) {
      const r = parseInt(cleaned[0] + cleaned[0], 16);
      const g = parseInt(cleaned[1] + cleaned[1], 16);
      const b = parseInt(cleaned[2] + cleaned[2], 16);
      return [r, g, b];
    }
    const num = parseInt(cleaned, 16);
    if (isNaN(num)) return [55, 52, 50];
    return [(num >> 16) & 255, (num >> 8) & 255, num & 255];
  }

  function cancelStudioEditMode() {
    state.editingQueueItemId = null;
    dom.btnAddQueue.innerHTML = `
      <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
      <span>Thêm vào hàng đợi sửa</span>
    `;
    if (dom.btnCancelEditMode) dom.btnCancelEditMode.classList.add('hidden');
  }

  function loadQueueItemToStudio(item) {
    state.editingQueueItemId = item.id;
    
    const activateItem = () => {
      setRoi(...item.box);
      
      if (item.action === 'replace') {
        dom.modeReplace.click();
      } else {
        dom.modeInsert.click();
      }
      
      dom.inputNewText.value = item.text || '';
      dom.selectFont.value = item.font_name || 'times.ttf';
      dom.inputFontSize.value = item.font_size || 52;
      setAlign(item.align || 'auto');
      setRoughness(item.roughness !== undefined ? item.roughness : 1.0);
      
      if (item.color) {
        const inkH = rgbToHex(item.color);
        dom.pickerInk.value = inkH;
        dom.hexInk.value = inkH;
      }
      if (item.bg_color) {
        const bgH = rgbToHex(item.bg_color);
        dom.pickerBg.value = bgH;
        dom.hexBg.value = bgH;
      }
      
      dom.btnAddQueue.innerHTML = `
        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
          <polyline points="17 21 17 13 7 13 7 21"></polyline>
          <polyline points="7 3 7 8 15 8"></polyline>
        </svg>
        <span>Lưu cập nhật vào hàng đợi</span>
      `;
      if (dom.btnCancelEditMode) dom.btnCancelEditMode.classList.remove('hidden');
      
      switchTab('edit');
      updatePreview();
      showToast(`Đang sửa mục: "${item.text || '[Xóa]'}" trong Studio`, 'info');
    };

    if (state.currentPage !== item.page) {
      loadPage(item.page).then(activateItem);
    } else {
      activateItem();
    }
  }

  function addToQueue() {
    if (!state.roi) {
      showToast('Vui lòng chọn vùng cần sửa trên trang PDF trước!', 'warning');
      return;
    }
    
    const isReplace = dom.modeReplace.classList.contains('active');
    const newText = dom.inputNewText.value;
    const fontName = dom.selectFont.value;
    const fontSize = parseInt(dom.inputFontSize.value, 10) || 52;
    const align = getSelectedAlign();
    const roughness = parseFloat(dom.sliderRoughness.value) || 1.0;

    // Trường hợp đang cập nhật một mục có sẵn từ Studio
    if (state.editingQueueItemId) {
      const existing = state.queue.find(q => q.id === state.editingQueueItemId);
      if (existing) {
        existing.page = state.currentPage;
        existing.action = isReplace ? 'replace' : 'insert';
        existing.box = [state.roi.x, state.roi.y, state.roi.w, state.roi.h];
        existing.text = newText;
        existing.font_name = fontName;
        existing.font_size = fontSize;
        existing.align = align;
        existing.roughness = roughness;
        existing.color = hexToRgb(dom.hexInk.value || '#373432');
        existing.bg_color = hexToRgb(dom.hexBg.value || '#FEFEFE');
        existing.description = `Trang ${state.currentPage + 1}: ${isReplace ? 'Thay' : 'Chèn'} "${newText || '[Xóa]'}"`;
        
        cancelStudioEditMode();
        renderQueue();
        updateQueueBadges();
        switchTab('queue');
        showToast('Đã lưu cập nhật mục trong hàng đợi thành công!', 'success');
        return;
      }
    }
    
    const item = {
      id: 'edit_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
      enabled: true,
      page: state.currentPage,
      action: isReplace ? 'replace' : 'insert',
      box: [state.roi.x, state.roi.y, state.roi.w, state.roi.h],
      text: newText,
      font_name: fontName,
      font_size: fontSize,
      align: align,
      roughness: roughness,
      color: hexToRgb(dom.hexInk.value || '#373432'),
      bg_color: hexToRgb(dom.hexBg.value || '#FEFEFE'),
      description: `Trang ${state.currentPage + 1}: ${isReplace ? 'Thay' : 'Chèn'} "${newText || '[Xóa]'}"`
    };
    
    state.queue.push(item);
    renderQueue();
    updateQueueBadges();
    switchTab('queue');
    showToast(`Đã thêm vị trí vào hàng đợi (Tổng: ${state.queue.length} mục)`, 'success');
  }

  function renderQueue() {
    dom.queueList.innerHTML = '';
    if (state.queue.length === 0) {
      dom.queueList.innerHTML = `
        <div class="empty-queue-msg">
          <p>Chưa có mục nào trong hàng đợi.</p>
          <p class="text-muted">Chọn vùng trên trang PDF, bóc tách và nhấn "Thêm vào hàng đợi sửa" để tích lũy nhiều vị trí.</p>
        </div>
      `;
      return;
    }
    
    state.queue.forEach((item, idx) => {
      const card = document.createElement('div');
      card.className = `queue-card ${item.enabled ? '' : 'disabled'}`;
      card.dataset.id = item.id;
      
      const inkHex = rgbToHex(item.color || [55, 52, 50]);
      const bgHex = rgbToHex(item.bg_color || [254, 254, 254]);
      
      card.innerHTML = `
        <div class="queue-card-top">
          <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; flex: 1; min-width: 0;">
            <input type="checkbox" class="queue-check" ${item.enabled ? 'checked' : ''}>
            <span class="queue-card-text font-mono" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${escapeHtml(item.text) || '<em>[Xóa trắng]</em>'}</span>
          </label>
          <div class="queue-card-actions">
            <button class="btn btn-ghost btn-xs btn-edit-item" title="Sửa thông số mục này">
              <svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2" fill="none">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>
            <button class="btn btn-ghost btn-xs text-danger btn-delete-item" title="Xóa mục này">
              <svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2" fill="none">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
        <div class="queue-card-meta font-mono">
          <span>T${item.page + 1}</span>
          <span>Box:[${item.box.join(',')}]</span>
          <span>Font:${item.font_name.replace('.ttf','')}</span>
          <span>${item.font_size}pt</span>
          <span>Lề:${item.align}</span>
          <span class="text-cyan">R:${item.roughness}</span>
          <span style="display:inline-flex; align-items:center; gap:3px;" title="Màu mực: ${inkHex}">
            <span style="display:inline-block; width:9px; height:9px; border-radius:2px; background-color:${inkHex}; border:1px solid rgba(255,255,255,0.25);"></span>
            <span>${inkHex}</span>
          </span>
          <span style="display:inline-flex; align-items:center; gap:3px;" title="Màu nền giấy: ${bgHex}">
            <span style="display:inline-block; width:9px; height:9px; border-radius:2px; background-color:${bgHex}; border:1px solid rgba(255,255,255,0.25);"></span>
            <span>${bgHex}</span>
          </span>
        </div>

        <!-- Inline Edit Panel -->
        <div class="queue-edit-form hidden">
          <div class="form-group-sm">
            <label class="form-label-xs">Nội dung chữ thay thế:</label>
            <input type="text" class="form-input form-input-sm edit-inline-text font-mono" value="${escapeHtml(item.text || '')}">
          </div>
          <div class="form-row-sm">
            <div class="form-group-sm">
              <label class="form-label-xs">Font:</label>
              <select class="form-select form-select-sm edit-inline-font font-mono">
                <option value="times.ttf" ${item.font_name === 'times.ttf' ? 'selected' : ''}>Times New Roman</option>
                <option value="timesbd.ttf" ${item.font_name === 'timesbd.ttf' ? 'selected' : ''}>Times Bold</option>
                <option value="timesi.ttf" ${item.font_name === 'timesi.ttf' ? 'selected' : ''}>Times Italic</option>
                <option value="timesbi.ttf" ${item.font_name === 'timesbi.ttf' ? 'selected' : ''}>Times Bold Italic</option>
                <option value="arial.ttf" ${item.font_name === 'arial.ttf' ? 'selected' : ''}>Arial Regular</option>
                <option value="arialbd.ttf" ${item.font_name === 'arialbd.ttf' ? 'selected' : ''}>Arial Bold</option>
                <option value="ariali.ttf" ${item.font_name === 'ariali.ttf' ? 'selected' : ''}>Arial Italic</option>
                <option value="calibri.ttf" ${item.font_name === 'calibri.ttf' ? 'selected' : ''}>Calibri Regular</option>
                <option value="calibrib.ttf" ${item.font_name === 'calibrib.ttf' ? 'selected' : ''}>Calibri Bold</option>
                <option value="tahoma.ttf" ${item.font_name === 'tahoma.ttf' ? 'selected' : ''}>Tahoma Regular</option>
                <option value="cour.ttf" ${item.font_name === 'cour.ttf' ? 'selected' : ''}>Courier New</option>
                <option value="GOTHIC.TTF" ${item.font_name === 'GOTHIC.TTF' ? 'selected' : ''}>Century Gothic</option>
              </select>
            </div>
            <div class="form-group-sm">
              <label class="form-label-xs">Cỡ chữ (pt):</label>
              <input type="number" class="form-input form-input-sm edit-inline-size font-mono" value="${item.font_size}" min="10" max="150">
            </div>
          </div>
          <div class="form-row-sm">
            <div class="form-group-sm">
              <label class="form-label-xs">Căn lề:</label>
              <select class="form-select form-select-sm edit-inline-align">
                <option value="auto" ${item.align === 'auto' ? 'selected' : ''}>auto (Tự động)</option>
                <option value="left" ${item.align === 'left' ? 'selected' : ''}>Trái (left)</option>
                <option value="center" ${item.align === 'center' ? 'selected' : ''}>Giữa (center)</option>
                <option value="right" ${item.align === 'right' ? 'selected' : ''}>Phải (right - số)</option>
              </select>
            </div>
            <div class="form-group-sm">
              <label class="form-label-xs">Độ rỗ (0.0-2.0):</label>
              <input type="number" step="0.1" class="form-input form-input-sm edit-inline-roughness font-mono" value="${item.roughness}" min="0.0" max="2.0">
            </div>
          </div>
          <!-- BỔ SUNG THAY ĐỔI MÃ MÀU TRỰC TIẾP -->
          <div class="form-row-sm">
            <div class="form-group-sm">
              <label class="form-label-xs">Màu mực (Ink Color):</label>
              <div style="display: flex; align-items: center; gap: 4px;">
                <input type="color" class="edit-inline-picker-ink" value="${inkHex}" style="width: 28px; height: 28px; padding: 1px; border: 1px solid var(--border-color); border-radius: 4px; cursor: pointer; background: transparent;">
                <input type="text" class="form-input form-input-sm edit-inline-hex-ink font-mono" value="${inkHex}" maxlength="7" style="flex: 1;">
              </div>
            </div>
            <div class="form-group-sm">
              <label class="form-label-xs">Màu nền giấy (Paper BG):</label>
              <div style="display: flex; align-items: center; gap: 4px;">
                <input type="color" class="edit-inline-picker-bg" value="${bgHex}" style="width: 28px; height: 28px; padding: 1px; border: 1px solid var(--border-color); border-radius: 4px; cursor: pointer; background: transparent;">
                <input type="text" class="form-input form-input-sm edit-inline-hex-bg font-mono" value="${bgHex}" maxlength="7" style="flex: 1;">
              </div>
            </div>
          </div>
          <div class="form-group-sm">
            <label class="form-label-xs">Tọa độ Box [X, Y, W, H]:</label>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px;">
              <input type="number" class="form-input form-input-sm edit-box-x font-mono" value="${item.box[0]}" title="X">
              <input type="number" class="form-input form-input-sm edit-box-y font-mono" value="${item.box[1]}" title="Y">
              <input type="number" class="form-input form-input-sm edit-box-w font-mono" value="${item.box[2]}" title="W">
              <input type="number" class="form-input form-input-sm edit-box-h font-mono" value="${item.box[3]}" title="H">
            </div>
          </div>
          <div class="queue-edit-buttons">
            <button class="btn btn-sm btn-primary btn-save-inline" style="flex: 1;">
              <span>Lưu</span>
            </button>
            <button class="btn btn-sm btn-secondary btn-cancel-inline">
              <span>Hủy</span>
            </button>
            <button class="btn btn-sm btn-ghost btn-open-studio" title="Mở trong Studio để xem thử trực quan Before / After">
              <span>Studio ↗</span>
            </button>
          </div>
        </div>
      `;
      
      const editForm = card.querySelector('.queue-edit-form');
      const btnEdit = card.querySelector('.btn-edit-item');
      const btnSaveInline = card.querySelector('.btn-save-inline');
      const btnCancelInline = card.querySelector('.btn-cancel-inline');
      const btnOpenStudio = card.querySelector('.btn-open-studio');
      
      // Đồng bộ hai chiều cho bảng chọn màu mực và màu nền giấy
      const pickerInk = card.querySelector('.edit-inline-picker-ink');
      const hexInk = card.querySelector('.edit-inline-hex-ink');
      const pickerBg = card.querySelector('.edit-inline-picker-bg');
      const hexBg = card.querySelector('.edit-inline-hex-bg');

      pickerInk.addEventListener('input', (e) => {
        hexInk.value = e.target.value.toUpperCase();
      });
      hexInk.addEventListener('input', (e) => {
        if (/^#[0-9A-Fa-f]{6}$/.test(e.target.value)) {
          pickerInk.value = e.target.value;
        }
      });

      pickerBg.addEventListener('input', (e) => {
        hexBg.value = e.target.value.toUpperCase();
      });
      hexBg.addEventListener('input', (e) => {
        if (/^#[0-9A-Fa-f]{6}$/.test(e.target.value)) {
          pickerBg.value = e.target.value;
        }
      });
      
      // Bật/tắt form sửa trực tiếp
      btnEdit.addEventListener('click', (e) => {
        e.stopPropagation();
        editForm.classList.toggle('hidden');
      });
      
      // Hủy sửa trực tiếp
      btnCancelInline.addEventListener('click', (e) => {
        e.stopPropagation();
        editForm.classList.add('hidden');
      });
      
      // Lưu thông số đã sửa trực tiếp
      btnSaveInline.addEventListener('click', (e) => {
        e.stopPropagation();
        const inlineText = card.querySelector('.edit-inline-text').value;
        const inlineFont = card.querySelector('.edit-inline-font').value;
        const inlineSize = parseInt(card.querySelector('.edit-inline-size').value, 10) || item.font_size;
        const inlineAlign = card.querySelector('.edit-inline-align').value;
        const inlineRoughness = parseFloat(card.querySelector('.edit-inline-roughness').value);
        const bx = parseInt(card.querySelector('.edit-box-x').value, 10) || item.box[0];
        const by = parseInt(card.querySelector('.edit-box-y').value, 10) || item.box[1];
        const bw = parseInt(card.querySelector('.edit-box-w').value, 10) || item.box[2];
        const bh = parseInt(card.querySelector('.edit-box-h').value, 10) || item.box[3];
        const inlineInk = hexToRgb(hexInk.value || pickerInk.value);
        const inlineBg = hexToRgb(hexBg.value || pickerBg.value);
        
        item.text = inlineText;
        item.font_name = inlineFont;
        item.font_size = inlineSize;
        item.align = inlineAlign;
        item.roughness = isNaN(inlineRoughness) ? item.roughness : inlineRoughness;
        item.box = [bx, by, bw, bh];
        item.color = inlineInk;
        item.bg_color = inlineBg;
        item.description = `Trang ${item.page + 1}: ${item.action === 'replace' ? 'Thay' : 'Chèn'} "${item.text || '[Xóa]'}"`;
        
        // Cập nhật lại ROI trên canvas nếu đang xem đúng trang
        if (state.currentPage === item.page) {
          setRoi(bx, by, bw, bh);
        }
        
        renderQueue();
        showToast(`Đã cập nhật mục "${item.text || '[Xóa]'}" thành công!`, 'success');
      });
      
      // Mở trong Studio với Preview trực quan
      btnOpenStudio.addEventListener('click', (e) => {
        e.stopPropagation();
        loadQueueItemToStudio(item);
      });
      
      // Checkbox kích hoạt
      card.querySelector('.queue-check').addEventListener('change', (e) => {
        item.enabled = e.target.checked;
        card.classList.toggle('disabled', !item.enabled);
        updateQueueBadges();
      });
      
      // Xóa mục
      card.querySelector('.btn-delete-item').addEventListener('click', (e) => {
        e.stopPropagation();
        if (state.editingQueueItemId === item.id) {
          cancelStudioEditMode();
        }
        state.queue.splice(idx, 1);
        renderQueue();
        updateQueueBadges();
      });
      
      // Nhấp vào thẻ để nhảy tới vùng đó trên trang
      card.addEventListener('click', (e) => {
        if (e.target.closest('.queue-check') || e.target.closest('.btn-delete-item') || e.target.closest('.btn-edit-item') || e.target.closest('.queue-edit-form')) return;
        if (state.currentPage !== item.page) {
          loadPage(item.page).then(() => setRoi(...item.box));
        } else {
          setRoi(...item.box);
        }
      });
      
      dom.queueList.appendChild(card);
    });
  }

  function updateQueueBadges() {
    const activeCount = state.queue.filter((q) => q.enabled).length;
    dom.badgeQueueCount.textContent = activeCount;
    dom.tabBadgeQueue.textContent = state.queue.length;
  }

  async function executeBatchEdits() {
    if (state.queue.length === 0) {
      showToast('Hàng đợi chỉnh sửa đang trống!', 'warning');
      return;
    }
    
    const activeEdits = state.queue.filter((q) => q.enabled);
    if (activeEdits.length === 0) {
      showToast('Không có mục nào trong hàng đợi được chọn (checkbox)', 'warning');
      return;
    }
    
    const outName = dom.inputOutputName.value.trim() || `${state.currentDoc.replace(/\.pdf$/i, '')}_DaSua.pdf`;
    const saveToSourceDir = dom.chkSaveSameDir ? dom.chkSaveSameDir.checked : true;
    const downloadBrowser = dom.chkDownloadBrowser ? dom.chkDownloadBrowser.checked : true;
    
    setStatus(`Đang áp dụng ${activeEdits.length} chỉnh sửa vào file '${outName}'...`);
    dom.btnRunBatch.disabled = true;
    dom.btnRunBatch.innerHTML = '<span>Đang xử lý xuất PDF...</span>';
    
    try {
      const res = await fetch('/api/apply-batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pdf: state.currentDoc,
          output_name: outName,
          save_to_source_dir: saveToSourceDir,
          edits: activeEdits
        })
      });
      
      if (!res.ok) throw new Error('Lỗi từ máy chủ khi thực hiện sửa hàng loạt');
      const data = await res.json();
      
      if (data.success) {
        showToast(`Xuất file thành công! (${data.applied_count} vị trí)`, 'success', 5000);
        setStatus(`Đã lưu file '${data.output_filename}'`);
        
        // Hiển thị hộp thông tin lưu file và nút mở thư mục
        if (dom.saveSuccessBox && dom.savedFilePath) {
          dom.savedFilePath.textContent = data.saved_path || data.output_filename;
          dom.saveSuccessBox.classList.remove('hidden');
          
          if (dom.btnOpenSavedFolder) {
            dom.btnOpenSavedFolder.onclick = async () => {
              try {
                const openRes = await fetch('/api/open-file-location', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ filename: data.saved_path || data.output_filename })
                });
                const openData = await openRes.json();
                if (openData.success) {
                  showToast('Đang mở thư mục trong Windows Explorer...', 'info');
                } else {
                  showToast('Không thể mở thư mục: ' + (openData.detail || 'Lỗi'), 'error');
                }
              } catch (e) {
                showToast('Lỗi mở thư mục: ' + e.message, 'error');
              }
            };
          }
        }
        
        // Tải file qua trình duyệt nếu được chọn
        if (downloadBrowser) {
          const a = document.createElement('a');
          a.href = data.download_url;
          a.download = data.output_filename;
          document.body.appendChild(a);
          a.click();
          a.remove();
        }
        
        // Tải lại danh sách tài liệu
        await loadDocumentsList(data.output_filename);
      } else {
        throw new Error(data.message || 'Lỗi không xác định');
      }
    } catch (err) {
      showToast('Lỗi xuất PDF: ' + err.message, 'error');
      setStatus('Lỗi xuất PDF');
    } finally {
      dom.btnRunBatch.disabled = false;
      dom.btnRunBatch.innerHTML = `
        <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <span>Chạy cập nhật & Tải PDF</span>
      `;
    }
  }

  // ========================================================================
  // SAVE & LOAD JSON RECIPES
  // ========================================================================
  function exportRecipeJson() {
    if (state.queue.length === 0) {
      showToast('Hàng đợi trống, không có cấu hình để lưu!', 'warning');
      return;
    }
    const recipe = {
      app: "PDF_Scan_Text_Modifier",
      version: "1.0.0",
      pdf: state.currentDoc,
      timestamp: new Date().toISOString(),
      edits: state.queue
    };
    const blob = new Blob([JSON.stringify(recipe, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${state.currentDoc.replace(/\.pdf$/i, '')}_cau_hinh_sua.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Đã xuất file cấu hình JSON thành công!', 'success');
  }

  function importRecipeJson(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const recipe = JSON.parse(e.target.result);
        if (!recipe.edits || !Array.isArray(recipe.edits)) {
          throw new Error('Định dạng file JSON cấu hình không hợp lệ');
        }
        state.queue = recipe.edits;
        renderQueue();
        updateQueueBadges();
        switchTab('queue');
        showToast(`Đã nạp thành công ${recipe.edits.length} vị trí từ file JSON!`, 'success');
      } catch (err) {
        showToast('Lỗi đọc file JSON: ' + err.message, 'error');
      }
    };
    reader.readAsText(file);
  }

  // ========================================================================
  // FILE UPLOAD (DRAG & DROP / FILE INPUT)
  // ========================================================================
  async function uploadPdfFile(file) {
    if (!file || !file.name.toLowerCase().endsWith('.pdf')) {
      showToast('Vui lòng chọn file định dạng .PDF!', 'warning');
      return;
    }
    
    setStatus(`Đang tải lên file '${file.name}'...`);
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const b64 = e.target.result;
        const res = await fetch('/api/upload', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            filename: file.name,
            data_base64: b64
          })
        });
        if (!res.ok) throw new Error('Không thể tải lên file');
        const data = await res.json();
        showToast(`Đã tải lên thành công '${data.filename}'!`, 'success');
        await loadDocumentsList(data.filename);
      } catch (err) {
        showToast('Lỗi tải lên: ' + err.message, 'error');
        setStatus('Lỗi tải lên PDF');
      }
    };
    reader.readAsDataURL(file);
  }

  // ========================================================================
  // TABS SWITCHER
  // ========================================================================
  function switchTab(tabName) {
    const tabs = {
      inspect: { btn: dom.tabBtnInspect, pane: dom.tabContentInspect },
      edit: { btn: dom.tabBtnEdit, pane: dom.tabContentEdit },
      queue: { btn: dom.tabBtnQueue, pane: dom.tabContentQueue }
    };
    
    Object.keys(tabs).forEach((k) => {
      const active = (k === tabName);
      tabs[k].btn.classList.toggle('active', active);
      tabs[k].pane.classList.toggle('active', active);
    });
  }

  // ========================================================================
  // EVENT BINDINGS
  // ========================================================================
  function bindEvents() {
    // Theme Toggle
    dom.btnThemeToggle.addEventListener('click', () => {
      applyTheme(state.theme === 'dark' ? 'light' : 'dark');
    });

    // Shortcuts Modal
    dom.btnShortcutsTrigger.addEventListener('click', () => dom.shortcutsModal.classList.remove('hidden'));
    dom.btnCloseModal.addEventListener('click', () => dom.shortcutsModal.classList.add('hidden'));
    dom.shortcutsModal.addEventListener('click', (e) => {
      if (e.target === dom.shortcutsModal) dom.shortcutsModal.classList.add('hidden');
    });

    // Document Selector
    dom.docSelect.addEventListener('change', (e) => loadDocument(e.target.value));

    // Upload Triggers
    dom.btnUploadTrigger.addEventListener('click', () => dom.fileUploader.click());
    dom.btnEmptyUpload.addEventListener('click', () => dom.fileUploader.click());
    dom.fileUploader.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) uploadPdfFile(e.target.files[0]);
    });

    // Drag & Drop PDF onto Viewport
    dom.viewport.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'copy';
    });
    dom.viewport.addEventListener('drop', (e) => {
      e.preventDefault();
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        uploadPdfFile(e.dataTransfer.files[0]);
      }
    });

    // Tools Switching
    function setActiveTool(tool) {
      state.activeTool = tool;
      dom.toolSelect.classList.toggle('active', tool === 'select');
      dom.toolHand.classList.toggle('active', tool === 'hand');
      dom.toolLoupe.classList.toggle('active', tool === 'loupe');
      dom.viewport.classList.toggle('hand-mode', tool === 'hand');
      dom.loupeLens.classList.toggle('hidden', tool !== 'loupe');
    }

    dom.toolSelect.addEventListener('click', () => setActiveTool('select'));
    dom.toolHand.addEventListener('click', () => setActiveTool('hand'));
    dom.toolLoupe.addEventListener('click', () => setActiveTool(state.activeTool === 'loupe' ? 'select' : 'loupe'));

    // Zoom Buttons
    dom.btnZoomIn.addEventListener('click', () => zoomAt(state.scale * 1.25));
    dom.btnZoomOut.addEventListener('click', () => zoomAt(state.scale / 1.25));
    dom.btnZoomFit.addEventListener('click', () => fitToWindow());
    dom.btnZoomLevel.addEventListener('click', () => zoomAt(1.0));

    // Mouse Wheel Zoom
    dom.viewport.addEventListener('wheel', (e) => {
      e.preventDefault();
      const factor = e.deltaY < 0 ? 1.15 : 0.87;
      zoomAt(state.scale * factor, e.clientX, e.clientY);
    }, { passive: false });

    // Canvas Mouse Interaction (Pan, Select, Move ROI, Resize ROI, Loupe)
    dom.viewport.addEventListener('mousedown', (e) => {
      // 1. Pan mode: Chuột giữa, công cụ Hand, hoặc giữ Alt
      if (e.button === 1 || state.activeTool === 'hand' || e.altKey) {
        state.isPanning = true;
        state.startPanX = e.clientX - state.panX;
        state.startPanY = e.clientY - state.panY;
        dom.viewport.classList.add('hand-mode');
        return;
      }

      if (e.button !== 0) return; // Chỉ xử lý chuột trái
      if (!state.naturalWidth) return;

      const coords = clientToCanvasCoords(e.clientX, e.clientY);

      // 2. Bấm vào Resize Handle của selection box
      if (e.target.classList.contains('handle')) {
        e.stopPropagation();
        state.isResizing = true;
        state.activeHandle = e.target.dataset.handle;
        state.startRoi = { ...state.roi };
        state.startSelectX = coords.x;
        state.startSelectY = coords.y;
        return;
      }

      // 3. Bấm vào bên trong selection box -> Di chuyển (Move) vùng chọn
      if (e.target.closest('#selection-box')) {
        e.stopPropagation();
        state.isMovingRoi = true;
        state.startRoi = { ...state.roi };
        state.startSelectX = coords.x;
        state.startSelectY = coords.y;
        return;
      }

      // 4. Bắt đầu kéo chọn vùng mới
      if (state.activeTool === 'select') {
        state.isSelecting = true;
        state.startSelectX = coords.x;
        state.startSelectY = coords.y;
        dom.selectionBox.classList.add('is-dragging');
        setRoi(coords.x, coords.y, 1, 1);
      }
    });

    window.addEventListener('mousemove', (e) => {
      // Cập nhật tọa độ cursor lên status bar
      const coords = clientToCanvasCoords(e.clientX, e.clientY);
      dom.chipCursor.textContent = `X: ${coords.x}, Y: ${coords.y}`;

      // Xử lý Pan
      if (state.isPanning) {
        state.panX = e.clientX - state.startPanX;
        state.panY = e.clientY - state.startPanY;
        updateStageTransform();
        return;
      }

      // Xử lý Di chuyển (Move) ROI
      if (state.isMovingRoi && state.startRoi) {
        const dx = coords.x - state.startSelectX;
        const dy = coords.y - state.startSelectY;
        const newX = Math.max(0, Math.min(state.naturalWidth - state.startRoi.w, state.startRoi.x + dx));
        const newY = Math.max(0, Math.min(state.naturalHeight - state.startRoi.h, state.startRoi.y + dy));
        setRoi(newX, newY, state.startRoi.w, state.startRoi.h);
        return;
      }

      // Xử lý Thay đổi kích thước (Resize) ROI qua Handles
      if (state.isResizing && state.activeHandle && state.startRoi) {
        const h = state.activeHandle;
        let { x, y, w, h: rh } = state.startRoi;
        const dx = coords.x - state.startSelectX;
        const dy = coords.y - state.startSelectY;

        if (h.includes('e')) {
          w = Math.max(8, Math.min(state.naturalWidth - x, state.startRoi.w + dx));
        }
        if (h.includes('w')) {
          const maxNewX = state.startRoi.x + state.startRoi.w - 8;
          const targetX = state.startRoi.x + dx;
          x = Math.max(0, Math.min(maxNewX, targetX));
          w = (state.startRoi.x + state.startRoi.w) - x;
        }
        if (h.includes('s')) {
          rh = Math.max(8, Math.min(state.naturalHeight - y, state.startRoi.h + dy));
        }
        if (h.includes('n')) {
          const maxNewY = state.startRoi.y + state.startRoi.h - 8;
          const targetY = state.startRoi.y + dy;
          y = Math.max(0, Math.min(maxNewY, targetY));
          rh = (state.startRoi.y + state.startRoi.h) - y;
        }

        setRoi(x, y, w, rh);
        return;
      }

      // Xử lý Kéo tạo Selection Box mới
      if (state.isSelecting) {
        const x = Math.min(state.startSelectX, coords.x);
        const y = Math.min(state.startSelectY, coords.y);
        const w = Math.abs(coords.x - state.startSelectX);
        const h = Math.abs(coords.y - state.startSelectY);
        setRoi(x, y, w, h);
        return;
      }

      // Xử lý Kính lúp (Loupe)
      if (state.activeTool === 'loupe' && state.pageImg) {
        const vpRect = dom.viewport.getBoundingClientRect();
        dom.loupeLens.style.left = `${e.clientX - vpRect.left}px`;
        dom.loupeLens.style.top = `${e.clientY - vpRect.top}px`;
        
        // Vẽ phần ảnh phóng đại 3x
        const zoomPower = 3;
        const srcW = dom.loupeCanvas.width / zoomPower;
        const srcH = dom.loupeCanvas.height / zoomPower;
        const srcX = coords.x - srcW / 2;
        const srcY = coords.y - srcH / 2;
        
        loupeCtx.imageSmoothingEnabled = false; // Hiển thị rõ pixel scan
        loupeCtx.clearRect(0, 0, dom.loupeCanvas.width, dom.loupeCanvas.height);
        loupeCtx.drawImage(
          state.pageImg,
          srcX, srcY, srcW, srcH,
          0, 0, dom.loupeCanvas.width, dom.loupeCanvas.height
        );
      }
    });

    window.addEventListener('mouseup', () => {
      if (state.isPanning) {
        state.isPanning = false;
        if (state.activeTool !== 'hand') dom.viewport.classList.remove('hand-mode');
      }

      dom.selectionBox.classList.remove('is-dragging');

      if (state.isMovingRoi) {
        state.isMovingRoi = false;
        state.startRoi = null;
        if (state.roi && state.roi.w >= 10 && state.roi.h >= 8 && state.currentDoc) {
          runAnalysis();
        }
      }

      if (state.isResizing) {
        state.isResizing = false;
        state.activeHandle = null;
        state.startRoi = null;
        if (state.roi && state.roi.w >= 10 && state.roi.h >= 8 && state.currentDoc) {
          runAnalysis();
        }
      }

      if (state.isSelecting) {
        state.isSelecting = false;
        // Nếu click mà không kéo (kích thước quá nhỏ < 6px) -> huỷ vùng chọn nhỏ
        if (state.roi && (state.roi.w < 6 || state.roi.h < 6)) {
          clearSelection();
        } else if (state.roi && state.roi.w >= 10 && state.roi.h >= 8 && state.currentDoc) {
          runAnalysis();
        }
      }
    });

    // Floating Bar Actions
    dom.btnQuickAnalyze.addEventListener('click', () => runAnalysis());
    dom.btnQuickReplace.addEventListener('click', () => {
      if (!state.currentAnalysis) runAnalysis();
      switchTab('edit');
      dom.inputNewText.focus();
    });
    if (dom.btnQuickClear) {
      dom.btnQuickClear.addEventListener('click', () => clearSelection());
    }

    // Tab Buttons Click
    dom.tabBtnInspect.addEventListener('click', () => switchTab('inspect'));
    dom.tabBtnEdit.addEventListener('click', () => switchTab('edit'));
    dom.tabBtnQueue.addEventListener('click', () => switchTab('queue'));

    // Inspector Actions
    dom.btnReanalyze.addEventListener('click', () => runAnalysis());
    dom.btnLoadToEdit.addEventListener('click', () => loadAnalysisToEditStudio());

    // Edit Studio Actions
    dom.modeReplace.addEventListener('click', () => {
      dom.modeReplace.classList.add('active');
      dom.modeInsert.classList.remove('active');
      dom.groupBgColor.style.display = 'block';
    });
    dom.modeInsert.addEventListener('click', () => {
      dom.modeInsert.classList.add('active');
      dom.modeReplace.classList.remove('active');
      dom.groupBgColor.style.display = 'none';
    });

    dom.alignBtns.forEach((btn) => {
      btn.addEventListener('click', () => setAlign(btn.dataset.align));
    });

    // Roughness Slider & Chips
    dom.sliderRoughness.addEventListener('input', (e) => setRoughness(e.target.value));
    dom.roughnessChips.forEach((chip) => {
      chip.addEventListener('click', () => setRoughness(chip.dataset.r));
    });

    // Sync Color Inputs
    dom.pickerInk.addEventListener('input', (e) => { dom.hexInk.value = e.target.value.toUpperCase(); });
    dom.hexInk.addEventListener('input', (e) => {
      if (/^#[0-9A-Fa-f]{6}$/.test(e.target.value)) dom.pickerInk.value = e.target.value;
    });
    dom.pickerBg.addEventListener('input', (e) => { dom.hexBg.value = e.target.value.toUpperCase(); });
    dom.hexBg.addEventListener('input', (e) => {
      if (/^#[0-9A-Fa-f]{6}$/.test(e.target.value)) dom.pickerBg.value = e.target.value;
    });

    // Preview & Queue
    dom.btnRefreshPreview.addEventListener('click', () => updatePreview());
    dom.btnAddQueue.addEventListener('click', () => addToQueue());
    if (dom.btnCancelEditMode) {
      dom.btnCancelEditMode.addEventListener('click', () => {
        cancelStudioEditMode();
        showToast('Đã hủy chế độ sửa, quay về thêm mới', 'info');
      });
    }

    // Batch & Export
    dom.btnRunBatch.addEventListener('click', () => executeBatchEdits());
    dom.btnExportPdf.addEventListener('click', () => {
      if (state.queue.length === 0 && state.roi) {
        addToQueue();
      }
      switchTab('queue');
      executeBatchEdits();
    });

    // Recipes JSON
    dom.btnExportRecipe.addEventListener('click', () => exportRecipeJson());
    dom.btnImportRecipeTrigger.addEventListener('click', () => dom.recipeUploader.click());
    dom.recipeUploader.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) importRecipeJson(e.target.files[0]);
    });
    dom.btnClearQueue.addEventListener('click', () => {
      if (confirm('Bạn có chắc chắn muốn xóa toàn bộ hàng đợi sửa đổi không?')) {
        state.queue = [];
        renderQueue();
        updateQueueBadges();
        showToast('Đã xóa sạch hàng đợi', 'info');
      }
    });

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      // Bỏ qua nếu đang gõ chữ trong ô input
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        if (e.key === 'Enter') {
          updatePreview();
        }
        return;
      }

      if (e.key === 'v' || e.key === 'V') setActiveTool('select');
      else if (e.key === 'h' || e.key === 'H') setActiveTool('hand');
      else if (e.key === 'm' || e.key === 'M') setActiveTool(state.activeTool === 'loupe' ? 'select' : 'loupe');
      else if (e.key === 'Escape') clearSelection();
      else if (e.key === 'Enter' && state.roi) runAnalysis();
      else if (e.key === '+' || e.key === '=') zoomAt(state.scale * 1.25);
      else if (e.key === '-' || e.key === '_') zoomAt(state.scale / 1.25);
      else if (e.ctrlKey && e.key === '0') { e.preventDefault(); fitToWindow(); }
      else if (e.ctrlKey && e.key === '1') { e.preventDefault(); zoomAt(1.0); }
    });
  }

  // Khởi chạy khi DOM sẵn sàng
  document.addEventListener('DOMContentLoaded', init);
})();
