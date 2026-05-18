"""
CONFIG.PY - Configuração Centralizada
"""
import os
import json
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURAÇÕES TCE-MA
# ============================================================================

ENTIDADES_MONITORADAS = {
    "São Luís": "4216402",
    "Paço do Lumiar": "4215607",
    "Raposa": "4216089",
}

EXERCICIOS_MONITORADOS = [2024, 2025, 2026]

PALAVRAS_PREVIDENCIA = [
    "previdência",
    "previdenciária",
    "aposentadoria",
    "pensão",
    "fgts",
    "pasep",
    "pis",
]

# ============================================================================
# CONFIGURAÇÃO SUPABASE (Banco de Dados)
# ============================================================================

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://seu-projeto.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sua-chave-supabase")

# ============================================================================
# CONFIGURAÇÃO TCE-MA
# ============================================================================

URL_BASE = "https://www2.tce.ma.gov.br"
URL_BUSCA = f"{URL_BASE}/consultaprocessos"
TIMEOUT_REQUISICAO = 30

# ============================================================================
# CONFIGURAÇÃO DE EXECUÇÃO
# ============================================================================

AMBIENTE = os.getenv("AMBIENTE", "development")
DEBUG = AMBIENTE == "development"

# ============================================================================
# VARIÁVEIS DE AMBIENTE (exemplo)
# ============================================================================

"""
No Vercel Dashboard, adicione as seguintes variáveis de ambiente:

SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-supabase-publica
AMBIENTE=production

"""
