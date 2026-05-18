#!/bin/bash

################################################################################
# SCRIPT DE ORGANIZAÇÃO - VERCEL + PYTHON
# Para: Linux e macOS
# 
# Uso:
#   1. Coloque este arquivo na pasta raiz (seu-projeto-tce/)
#   2. Coloque todos os 24 arquivos também na pasta raiz
#   3. Execute: bash organizar.sh
#   4. Pronto! Tudo está organizado!
################################################################################

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🚀 ORGANIZANDO ARQUIVOS - VERCEL + PYTHON              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
NC='\033[0m' # No Color

# Pasta atual
PASTA_ATUAL=$(pwd)

echo -e "${AZUL}📁 Pasta atual: $PASTA_ATUAL${NC}"
echo ""

# ============================================================================
# 1. CRIAR PASTAS
# ============================================================================

echo -e "${AZUL}1️⃣  Criando pastas...${NC}"

mkdir -p api
mkdir -p pages/api
mkdir -p components
mkdir -p styles
mkdir -p public

echo -e "${VERDE}✅ Pastas criadas${NC}"
echo ""

# ============================================================================
# 2. MOVER ARQUIVOS DE CONFIGURAÇÃO (RAIZ)
# ============================================================================

echo -e "${AZUL}2️⃣  Organizando arquivos de configuração...${NC}"

# Renomear e manter na raiz
if [ -f "vercel_atualizado.json" ]; then
  mv vercel_atualizado.json vercel.json && echo -e "${VERDE}✅ vercel.json${NC}"
else
  echo -e "${AMARELO}⚠️  vercel_atualizado.json não encontrado${NC}"
fi

[ -f "next.config.js" ] && echo -e "${VERDE}✅ next.config.js${NC}" || echo -e "${AMARELO}⚠️  next.config.js não encontrado${NC}"
[ -f "tailwind.config.js" ] && echo -e "${VERDE}✅ tailwind.config.js${NC}" || echo -e "${AMARELO}⚠️  tailwind.config.js não encontrado${NC}"
[ -f "postcss.config.js" ] && echo -e "${VERDE}✅ postcss.config.js${NC}" || echo -e "${AMARELO}⚠️  postcss.config.js não encontrado${NC}"
[ -f "package.json" ] && echo -e "${VERDE}✅ package.json${NC}" || echo -e "${AMARELO}⚠️  package.json não encontrado${NC}"
[ -f "requirements.txt" ] && echo -e "${VERDE}✅ requirements.txt${NC}" || echo -e "${AMARELO}⚠️  requirements.txt não encontrado${NC}"
[ -f "config.py" ] && echo -e "${VERDE}✅ config.py${NC}" || echo -e "${AMARELO}⚠️  config.py não encontrado${NC}"
[ -f ".env.example" ] && echo -e "${VERDE}✅ .env.example${NC}" || echo -e "${AMARELO}⚠️  .env.example não encontrado${NC}"

echo ""

# ============================================================================
# 3. MOVER ARQUIVOS PYTHON (api/)
# ============================================================================

echo -e "${AZUL}3️⃣  Organizando arquivos Python (api/)...${NC}"

if [ -f "api_busca_semanal.py" ]; then
  mv api_busca_semanal.py api/busca_semanal.py && echo -e "${VERDE}✅ api/busca_semanal.py${NC}"
else
  echo -e "${AMARELO}⚠️  api_busca_semanal.py não encontrado${NC}"
fi

if [ -f "api_monitoramento_diario.py" ]; then
  mv api_monitoramento_diario.py api/monitoramento_diario.py && echo -e "${VERDE}✅ api/monitoramento_diario.py${NC}"
else
  echo -e "${AMARELO}⚠️  api_monitoramento_diario.py não encontrado${NC}"
fi

if [ -f "api_scraping_documentos.py" ]; then
  mv api_scraping_documentos.py api/scraping_documentos.py && echo -e "${VERDE}✅ api/scraping_documentos.py${NC}"
else
  echo -e "${AMARELO}⚠️  api_scraping_documentos.py não encontrado${NC}"
fi

echo ""

# ============================================================================
# 4. MOVER ARQUIVOS REACT PAGES (pages/)
# ============================================================================

echo -e "${AZUL}4️⃣  Organizando arquivos React (pages/)...${NC}"

if [ -f "pages_index.jsx" ]; then
  mv pages_index.jsx pages/index.jsx && echo -e "${VERDE}✅ pages/index.jsx${NC}"
else
  echo -e "${AMARELO}⚠️  pages_index.jsx não encontrado${NC}"
fi

if [ -f "pages__app.jsx" ]; then
  mv pages__app.jsx pages/_app.jsx && echo -e "${VERDE}✅ pages/_app.jsx${NC}"
else
  echo -e "${AMARELO}⚠️  pages__app.jsx não encontrado${NC}"
fi

echo ""

# ============================================================================
# 5. MOVER ENDPOINTS API (pages/api/)
# ============================================================================

echo -e "${AZUL}5️⃣  Organizando endpoints (pages/api/)...${NC}"

if [ -f "pages_api_processos.js" ]; then
  mv pages_api_processos.js pages/api/processos.js && echo -e "${VERDE}✅ pages/api/processos.js${NC}"
else
  echo -e "${AMARELO}⚠️  pages_api_processos.js não encontrado${NC}"
fi

if [ -f "pages_api_monitorados.js" ]; then
  mv pages_api_monitorados.js pages/api/monitorados.js && echo -e "${VERDE}✅ pages/api/monitorados.js${NC}"
else
  echo -e "${AMARELO}⚠️  pages_api_monitorados.js não encontrado${NC}"
fi

if [ -f "pages_api_historico.js" ]; then
  mv pages_api_historico.js pages/api/historico.js && echo -e "${VERDE}✅ pages/api/historico.js${NC}"
else
  echo -e "${AMARELO}⚠️  pages_api_historico.js não encontrado${NC}"
fi

if [ -f "pages_api_documentos.js" ]; then
  mv pages_api_documentos.js pages/api/documentos.js && echo -e "${VERDE}✅ pages/api/documentos.js${NC}"
else
  echo -e "${AMARELO}⚠️  pages_api_documentos.js não encontrado${NC}"
fi

echo ""

# ============================================================================
# 6. MOVER COMPONENTES (components/)
# ============================================================================

echo -e "${AZUL}6️⃣  Organizando componentes (components/)...${NC}"

if [ -f "components_DocumentosProcesso.jsx" ]; then
  mv components_DocumentosProcesso.jsx components/DocumentosProcesso.jsx && echo -e "${VERDE}✅ components/DocumentosProcesso.jsx${NC}"
else
  echo -e "${AMARELO}⚠️  components_DocumentosProcesso.jsx não encontrado${NC}"
fi

echo ""

# ============================================================================
# 7. MOVER ESTILOS (styles/)
# ============================================================================

echo -e "${AZUL}7️⃣  Organizando estilos (styles/)...${NC}"

if [ -f "styles_globals.css" ]; then
  mv styles_globals.css styles/globals.css && echo -e "${VERDE}✅ styles/globals.css${NC}"
else
  echo -e "${AMARELO}⚠️  styles_globals.css não encontrado${NC}"
fi

echo ""

# ============================================================================
# 8. DOCUMENTAÇÃO E SQL (RAIZ)
# ============================================================================

echo -e "${AZUL}8️⃣  Verificando documentação e SQL...${NC}"

[ -f "GUIA_SCRAPER_REAL.md" ] && echo -e "${VERDE}✅ GUIA_SCRAPER_REAL.md${NC}" || echo -e "${AMARELO}⚠️  GUIA_SCRAPER_REAL.md não encontrado${NC}"
[ -f "SQL_CRIAR_TABELAS_DOCUMENTOS.sql" ] && echo -e "${VERDE}✅ SQL_CRIAR_TABELAS_DOCUMENTOS.sql${NC}" || echo -e "${AMARELO}⚠️  SQL_CRIAR_TABELAS_DOCUMENTOS.sql não encontrado${NC}"
[ -f "README_COMECE_AQUI.txt" ] && echo -e "${VERDE}✅ README_COMECE_AQUI.txt${NC}" || echo -e "${AMARELO}⚠️  README_COMECE_AQUI.txt não encontrado${NC}"
[ -f "00_INDICE_COMPLETO.txt" ] && echo -e "${VERDE}✅ 00_INDICE_COMPLETO.txt${NC}" || echo -e "${AMARELO}⚠️  00_INDICE_COMPLETO.txt não encontrado${NC}"
[ -f "01_ESTRUTURA_VISUAL.txt" ] && echo -e "${VERDE}✅ 01_ESTRUTURA_VISUAL.txt${NC}" || echo -e "${AMARELO}⚠️  01_ESTRUTURA_VISUAL.txt não encontrado${NC}"

echo ""

# ============================================================================
# 9. RESUMO FINAL
# ============================================================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ ORGANIZAÇÃO CONCLUÍDA!                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${VERDE}Próximos passos:${NC}"
echo ""
echo "1. cp .env.example .env.local"
echo "2. Edite .env.local com suas credenciais Supabase"
echo "3. npm install"
echo "4. pip install -r requirements.txt"
echo "5. Execute SQL no Supabase (SQL_CRIAR_TABELAS_DOCUMENTOS.sql)"
echo "6. npm run dev"
echo ""
echo -e "${AZUL}Para mais informações, leia: GUIA_SCRAPER_REAL.md${NC}"
echo ""
