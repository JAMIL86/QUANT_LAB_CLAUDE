param(
    [string]$OmniRouteUrl = "http://127.0.0.1:20128",
    [string]$ApiKey       = $env:OMNIROUTE_API_KEY,
    [string]$PrimaryCombo = "auto/coding:free"
)

$ErrorActionPreference = "Continue"

function Write-Step($m){ Write-Host "`n[AutoHeal] $m" -ForegroundColor Cyan }
function Write-Ok($m)  { Write-Host "  OK  $m" -ForegroundColor Green }
function Write-Warn($m){ Write-Host "  !!  $m" -ForegroundColor Yellow }
function Write-Err($m) { Write-Host "  XX  $m" -ForegroundColor Red }

$headers = @{ "Content-Type" = "application/json" }
if ($ApiKey) { $headers["x-api-key"] = $ApiKey }

Write-Step "1/4 - Verificando OmniRoute em $OmniRouteUrl"
$online = $false
try {
    $r = Invoke-RestMethod -Uri "$OmniRouteUrl/v1/models" -Headers $headers -TimeoutSec 10 -ErrorAction Stop
    Write-Ok "Online e autenticado ($($r.data.Count) modelos visiveis)"
    $online = $true
} catch {
    $status = 0
    if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
    if ($status -eq 401 -or $status -eq 403) {
        Write-Ok "Online, mas auth falhou (HTTP $status). Verifique OMNIROUTE_API_KEY."
        exit 1
    } elseif ($status -eq 0) {
        Write-Err "Offline: conexao recusada. OmniRoute nao esta ativo."
        exit 1
    } else {
        Write-Warn "Respondeu HTTP $status. Seguindo."
        $online = $true
    }
}

$dummyTools = @(@{
    type = "function"
    function = @{
        name = "ping_test"
        description = "ping"
        parameters = @{ type = "object"; properties = @{ msg = @{ type = "string" } }; required = @("msg") }
    }
})

Write-Step "2/4 - Testando '$PrimaryCombo' COM tool calling"
$payload = @{
    model = $PrimaryCombo
    messages = @(@{ role = "user"; content = "ping" })
    stream = $false
    max_tokens = 32
    tools = $dummyTools
} | ConvertTo-Json -Depth 20 -Compress

try {
    Invoke-RestMethod -Uri "$OmniRouteUrl/v1/chat/completions" -Method Post -Headers $headers -Body $payload -TimeoutSec 60 -ErrorAction Stop | Out-Null
    Write-Ok "O combo JA aceita tools. Nada a corrigir!"
    exit 0
} catch {
    $status = 0; $body = $_.Exception.Message
    if ($_.Exception.Response) {
        $status = [int]$_.Exception.Response.StatusCode
        try { $body = (New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())).ReadToEnd() } catch {}
    }
    if ($status -eq 400 -and $body -match "No target in combo" -and $body -match "tool calling") {
        Write-Err "Erro 400 confirmado: '$PrimaryCombo' nao tem alvo com tool calling."
    } else {
        Write-Warn "Falhou HTTP $status (nao e erro de tool calling)"
        Write-Host "      $($body.Substring(0,[Math]::Min(200,$body.Length)))" -ForegroundColor DarkGray
        exit 2
    }
}

Write-Step "3/4 - Procurando modelo free que aceite tools"
$candidatos = @(
    "oc/big-pickle",
    "qwen/qwen3-coder",
    "deepseek/deepseek-chat-v3.1",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemini-2.0-flash-exp:free"
)

$modeloBom = $null
foreach ($m in $candidatos) {
    Write-Host "   Tentando $m ..." -ForegroundColor Gray
    $p = @{
        model = $m
        messages = @(@{ role = "user"; content = "ping" })
        stream = $false
        max_tokens = 32
        tools = $dummyTools
    } | ConvertTo-Json -Depth 20 -Compress
    try {
        Invoke-RestMethod -Uri "$OmniRouteUrl/v1/chat/completions" -Method Post -Headers $headers -Body $p -TimeoutSec 60 -ErrorAction Stop | Out-Null
        Write-Ok "FUNCIONOU: $m aceita tools"
        $modeloBom = $m
        break
    } catch {
        $s = 0
        if ($_.Exception.Response) { $s = [int]$_.Exception.Response.StatusCode }
        Write-Warn "$m falhou (HTTP $s)"
    }
}

if (-not $modeloBom) {
    Write-Err "Nenhum modelo free testado aceita tools."
    Write-Host ">>> Atualize OmniRoute para >= v3.8.51 (placeholder tools)" -ForegroundColor Yellow
    exit 3
}

Write-Step "4/4 - Gravando recomendacao"
@{
    geradoEm = (Get-Date).ToString("o")
    urlFuncional = $OmniRouteUrl
    comboOriginal = $PrimaryCombo
    modeloRecomendado = $modeloBom
} | ConvertTo-Json -Depth 5 | Out-File -FilePath (Join-Path $PSScriptRoot "omniroute-recomendado.json") -Encoding UTF8

Write-Ok "Recomendacao salva em omniroute-recomendado.json"
Write-Host "`n>>> No settings.json troque ANTHROPIC_MODEL para: $modeloBom" -ForegroundColor Yellow

