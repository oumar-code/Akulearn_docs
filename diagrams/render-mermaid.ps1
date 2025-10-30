# Render all .mmd files in docs/diagrams to PNG using mermaid-cli
# Usage: install mermaid-cli first: npm i -g @mermaid-js/mermaid-cli

$inDir = Join-Path $PSScriptRoot ""
Get-ChildItem -Path $inDir -Filter *.mmd -Recurse | ForEach-Object {
    $in = $_.FullName
    $out = Join-Path $in.DirectoryName ($_.BaseName + ".png")
    Write-Host "Rendering $in -> $out"
    # mmdc must be installed and on PATH
    mmdc -i $in -o $out
}
Write-Host "Render script finished. Check docs/diagrams for PNG files."