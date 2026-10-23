<#
.SYNOPSIS
    Auto-cura de hooks do Claude Code no Windows.
    Localiza hooks SessionStart que apontam para scripts inexistentes e
    aplica o padrão de execução resiliente (ADR-0189).
#>

$ErrorActionPreference = "Stop"

# 1. Define os locais possíveis de settings.json (global e projeto)
$possiblePaths = @(
    "$env:USERPROFILE\.claude\settings.json",
    "$env:USERPROFILE\.claude\settings.local.json",
    "D:\programação\QUANT_LAB_CLAUDE_\.claude\settings.json",
    "D:\programação\QUANT_LAB_CLAUDE_\.claude\settings.local.json"
)

# 2. Função para aplicar o padrão resiliente a um comando de hook
function Get-ResilientCommand {
    param([string]$OriginalCommand)
    
    # Extrai o caminho do script Node do comando original (heurística simples)
    # Se for um comando complexo com pipes, mantemos como está por segurança.
    if ($OriginalCommand -match '^node\s+["'']?([^"'']+\.(cjs|mjs|js))["'']?') {
        $scriptPath = $Matches[1]
        # Normaliza para barras normais (crítico no Windows)
        $scriptPath = $scriptPath -replace '\\', '/'
        # Constrói o wrapper resiliente
        return "bash -c 'F=""$scriptPath""; [ -f ""`$F"" ] && node ""`$F"" || printf ""{`"continue`":true}""' 2>/dev/null || printf '{`"continue`":true}'"
    }
    return $OriginalCommand
}

# 3. Itera sobre os arquivos e corrige
foreach ($path in $possiblePaths) {
    if (-not (Test-Path $path)) { continue }
    
    Write-Host "Analisando: $path" -ForegroundColor Cyan
    
    # Backup com timestamp
    $backupPath = "$path.bak_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $path $backupPath
    Write-Host "  Backup criado: $backupPath" -ForegroundColor DarkGray
    
    # Carrega o JSON
    try {
        $json = Get-Content $path -Raw | ConvertFrom-Json
    } catch {
        Write-Warning "  JSON inválido, pulando: $_"
        continue
    }
    
    $modified = $false
    
    # Verifica se existe o bloco SessionStart
    if ($json.hooks -and $json.hooks.SessionStart) {
        foreach ($hookGroup in $json.hooks.SessionStart) {
            foreach ($hook in $hookGroup.hooks) {
                if ($hook.type -eq "command" -and $hook.command) {
                    $original = $hook.command
                    
                    # Extrai o caminho do script (se houver)
                    if ($original -match '([A-Z]:\\[^"''\s]+\.(cjs|mjs|js))') {
                        $scriptPath = $Matches[1]
                        if (-not (Test-Path $scriptPath)) {
                            Write-Host "  Hook quebrado encontrado: $scriptPath" -ForegroundColor Yellow
                            $hook.command = Get-ResilientCommand -OriginalCommand $original
                            $modified = $true
                            Write-Host "  -> Comando substituído por wrapper resiliente." -ForegroundColor Green
                        }
                    } elseif ($original -match 'node\s+["'']?([^"''\s]+)') {
                        # Caminho relativo ou sem unidade
                        $relPath = $Matches[1] -replace '\\', '/'
                        # Tenta resolver relativo ao diretório do settings
                        $fullPath = Join-Path (Split-Path $path -Parent) $relPath
                        if (-not (Test-Path $fullPath)) {
                            Write-Host "  Hook com caminho não resolvido: $relPath" -ForegroundColor Yellow
                            $hook.command = Get-ResilientCommand -OriginalCommand $original
                            $modified = $true
                        }
                    }
                }
            }
        }
    }
    
    # Se modificou, salva
    if ($modified) {
        $json | ConvertTo-Json -Depth 10 | Set-Content $path -Encoding UTF8
        Write-Host "  Arquivo atualizado com sucesso." -ForegroundColor Green
    } else {
        Write-Host "  Nenhum hook SessionStart quebrado encontrado." -ForegroundColor DarkGray
    }
}

Write-Host "`nConcluído. Reinicie o Claude Code para aplicar as mudanças." -ForegroundColor Cyan