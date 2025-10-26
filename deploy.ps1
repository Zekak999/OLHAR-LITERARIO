# Script de Deploy Automático - Olhar Literário
# Este script faz commit, push e deploy no Railway automaticamente

param(
    [string]$mensagem = "Atualização automática do projeto"
)

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Deploy Automático - Olhar Literário" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar se há alterações
Write-Host "[1/4] Verificando alterações..." -ForegroundColor Yellow
git add .

$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "Nenhuma alteração detectada. Deploy não necessário." -ForegroundColor Green
    exit 0
}

Write-Host "Alterações detectadas!" -ForegroundColor Green
Write-Host ""

# 2. Fazer commit
Write-Host "[2/4] Fazendo commit das alterações..." -ForegroundColor Yellow
git commit -m "$mensagem"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao fazer commit!" -ForegroundColor Red
    exit 1
}

Write-Host "Commit realizado com sucesso!" -ForegroundColor Green
Write-Host ""

# 3. Fazer push para GitHub
Write-Host "[3/4] Enviando para GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao fazer push!" -ForegroundColor Red
    exit 1
}

Write-Host "Push realizado com sucesso!" -ForegroundColor Green
Write-Host ""

# 4. Disparar deploy no Railway
Write-Host "[4/4] Disparando deploy no Railway..." -ForegroundColor Yellow
Write-Host "O Railway detectará as alterações automaticamente e fará o deploy." -ForegroundColor Cyan
Write-Host ""

Write-Host "=====================================" -ForegroundColor Green
Write-Host "  Deploy Concluido com Sucesso!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "1. Aguarde 2-3 minutos para o Railway processar o deploy" -ForegroundColor White
Write-Host "2. Acesse seu projeto no Railway para acompanhar o deploy" -ForegroundColor White
Write-Host "3. Teste as alteracoes no site hospedado" -ForegroundColor White
Write-Host ""
