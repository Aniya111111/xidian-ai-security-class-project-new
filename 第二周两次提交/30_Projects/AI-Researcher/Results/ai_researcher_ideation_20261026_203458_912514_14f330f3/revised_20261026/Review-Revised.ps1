param([switch]$Execute)
$ErrorActionPreference = 'Stop'
$project = 'E:\xidian-ai-security-class-project-new-main\projects\project-02-ai-scientist-v2'
$python = Join-Path $project '.venv-review\Scripts\python.exe'
$script = Join-Path $project 'review_obsidian.py'
$draft = Join-Path $PSScriptRoot 'revised.md'
$evidence = Join-Path $PSScriptRoot 'review_evidence.md'
$output = 'E:\oblidian\file\safetyAI\Agent-IFC\30_Projects\AI-Scientist-v2\Reviews'
foreach ($file in @($python, $script, $draft, $evidence)) {
    if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Missing file: $file" }
}
$reviewArgs = @($script, '--input', $draft, '--evidence', $evidence,
    '--output-dir', $output, '--model', 'qwen3.7-flash', '--direct', '--max-output-tokens', '3000')
if (-not $Execute) { $reviewArgs += '--dry-run' }
Push-Location $project
try {
    & $python @reviewArgs
    if ($LASTEXITCODE -ne 0) { throw "Review failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
