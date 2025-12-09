@echo off
REM Script para abrir ambos os portais em terminais separados

echo Iniciando Plataforma de Gestao de Servicos...
echo.

REM Verificar se pandas está instalado
python -m pip show pandas >nul 2>&1
if errorlevel 1 (
    echo [!] pandas nao encontrado. Instalando...
    python -m pip install pandas
)

REM Abrir PortalCliente em novo terminal
echo [1] Abrindo PortalCliente em novo terminal...
start "Portal Cliente" cmd /k "cd /d c:\Users\Utilizador\Desktop\GitHub\PlataformaGestao_Servicos\trabalhosIndividuais && python PortalCliente.py"

REM Aguardar um pouco
timeout /t 2 /nobreak

REM Abrir PortalServicos em novo terminal
echo [2] Abrindo PortalServicos em novo terminal...
start "Portal de Servicos" cmd /k "cd /d c:\Users\Utilizador\Desktop\GitHub\PlataformaGestao_Servicos\trabalhoFinal && python PortalServicos.py"

echo.
echo [*] Ambos os portais foram inicializados!
echo [*] - Portal Cliente: gerencia pedidos (cria CSVs)
echo [*] - Portal Servicos: sincroniza dados (le CSVs)
echo.
pause
