# 转换当前目录及子目录下的所有文本文件
Get-ChildItem -Path . -Recurse -File | Where-Object { $_.Extension -match '\.(sh)$' } | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $content = $content -replace "`r`n", "`n"
    Set-Content -Path $_.FullName -Value $content -NoNewline -Encoding UTF8
    Write-Host "Converted: $($_.FullName)"
}