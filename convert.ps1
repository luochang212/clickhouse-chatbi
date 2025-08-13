# 将当前目录及子目录下特定后缀的文件转换为 LF 格式
Get-ChildItem -Path . -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -match '\.(sh|yml|env)$' } | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    $content = $content -replace "`r`n", "`n"
    Set-Content -Path $_.FullName -Value $content -NoNewline -Encoding UTF8
    Write-Host "Converted: $($_.FullName)"
}