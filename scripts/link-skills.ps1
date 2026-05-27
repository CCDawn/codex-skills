$ErrorActionPreference = "Stop"

# Development convenience only. The formal install flow for this repository is
# copying real directories into ~/.codex/skills via install_codex_library.py.

$repo = Split-Path -Parent $PSScriptRoot
$dest = Join-Path $HOME ".claude\skills"

New-Item -ItemType Directory -Force -Path $dest | Out-Null

Get-ChildItem -Path (Join-Path $repo "skills") -Recurse -Filter SKILL.md | ForEach-Object {
    $src = $_.Directory.FullName
    $name = Split-Path $src -Leaf
    $target = Join-Path $dest $name

    if (Test-Path $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }

    New-Item -ItemType Junction -Path $target -Target $src | Out-Null
    Write-Output "linked $name -> $src"
}
