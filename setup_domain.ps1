# Cấu hình ánh xạ tên miền pdfscanmodifier vào 127.0.0.1
$hostsPath = "$env:windir\System32\drivers\etc\hosts"

try {
    $content = Get-Content $hostsPath -Raw -ErrorAction SilentlyContinue
    if ($content -and $content -notmatch '\bpdfscanmodifier\b') {
        try {
            Add-Content -Path $hostsPath -Value "`r`n127.0.0.1 pdfscanmodifier`r`n::1 pdfscanmodifier" -Encoding utf8 -ErrorAction Stop
        } catch {
            # Yêu cầu quyền Administrator qua UAC nếu chạy trên desktop
            try {
                Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `"Add-Content -Path '$env:windir\System32\drivers\etc\hosts' -Value '`r`n127.0.0.1 pdfscanmodifier`r`n::1 pdfscanmodifier' -Encoding utf8`"" -Wait -ErrorAction SilentlyContinue
            } catch {}
        }
    }
} catch {}
