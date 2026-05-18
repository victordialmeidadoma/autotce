-- SQL PARA SUPABASE
-- Cole isso no SQL Editor do Supabase para criar as tabelas

-- ============================================================================
-- TABELA: documentos_processo
-- Armazena documentos de cada processo com data e teor completo
-- ============================================================================

CREATE TABLE IF NOT EXISTS documentos_processo (
  id BIGSERIAL PRIMARY KEY,
  numero VARCHAR(20) NOT NULL,
  ano INTEGER NOT NULL,
  titulo_documento TEXT NOT NULL,
  data_documento VARCHAR(20),
  teor_completo TEXT,
  data_deteccao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  data_atualizacao TIMESTAMP WITH TIME ZONE,
  eh_novo BOOLEAN DEFAULT TRUE,
  
  -- Garantir que não há duplicatas
  UNIQUE(numero, ano, titulo_documento)
);

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_documentos_numero ON documentos_processo(numero);
CREATE INDEX IF NOT EXISTS idx_documentos_ano ON documentos_processo(ano);
CREATE INDEX IF NOT EXISTS idx_documentos_data ON documentos_processo(data_deteccao);
CREATE INDEX IF NOT EXISTS idx_documentos_novo ON documentos_processo(eh_novo);

-- ============================================================================
-- TABELA: historico_teor_documentos (OPCIONAL)
-- Rastreia mudanças no teor dos documentos ao longo do tempo
-- ============================================================================

CREATE TABLE IF NOT EXISTS historico_teor_documentos (
  id BIGSERIAL PRIMARY KEY,
  numero VARCHAR(20) NOT NULL,
  ano INTEGER NOT NULL,
  titulo_documento TEXT NOT NULL,
  teor_anterior TEXT,
  teor_novo TEXT,
  data_mudanca TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- ATUALIZAR TABELA: processos_monitorados
-- Adicionar informações sobre documentos
-- ============================================================================

ALTER TABLE processos_monitorados
ADD COLUMN IF NOT EXISTS total_documentos INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS ultimo_documento TEXT,
ADD COLUMN IF NOT EXISTS data_ultimo_documento TIMESTAMP WITH TIME ZONE;

-- ============================================================================
-- VIEW: documentos_recentes
-- Mostra documentos adicionados nos últimos 7 dias
-- ============================================================================

CREATE OR REPLACE VIEW documentos_recentes AS
SELECT 
  numero,
  ano,
  titulo_documento,
  data_documento,
  data_deteccao,
  teor_completo,
  eh_novo,
  EXTRACT(DAY FROM NOW() - data_deteccao) as dias_desde_deteccao
FROM documentos_processo
WHERE data_deteccao > NOW() - INTERVAL '7 days'
ORDER BY data_deteccao DESC;

-- ============================================================================
-- VIEW: resumo_documentos_por_processo
-- Resumo da quantidade de documentos por processo
-- ============================================================================

CREATE OR REPLACE VIEW resumo_documentos_por_processo AS
SELECT 
  numero,
  ano,
  COUNT(*) as total_documentos,
  COUNT(CASE WHEN eh_novo = TRUE THEN 1 END) as novos_documentos,
  MAX(data_deteccao) as ultima_atualizacao,
  MAX(titulo_documento) as ultimo_documento
FROM documentos_processo
GROUP BY numero, ano
ORDER BY ultima_atualizacao DESC;

-- ============================================================================
-- COMENTÁRIOS (Para documentação)
-- ============================================================================

COMMENT ON TABLE documentos_processo IS 'Armazena documentos de cada processo do TCE-MA com data e teor completo';
COMMENT ON COLUMN documentos_processo.numero IS 'Número do processo (ex: 3154)';
COMMENT ON COLUMN documentos_processo.ano IS 'Ano do processo (ex: 2025)';
COMMENT ON COLUMN documentos_processo.titulo_documento IS 'Título do documento extraído';
COMMENT ON COLUMN documentos_processo.data_documento IS 'Data do documento no formato DD/MM/YYYY';
COMMENT ON COLUMN documentos_processo.teor_completo IS 'Conteúdo completo do documento';
COMMENT ON COLUMN documentos_processo.eh_novo IS 'TRUE se foi adicionado na última verificação';

-- ============================================================================
-- GRANTS (Permissões)
-- Permitir acesso público para leitura
-- ============================================================================

ALTER TABLE documentos_processo ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir leitura pública" ON documentos_processo
  FOR SELECT
  USING (true);

-- ============================================================================
-- Pronto!
-- Agora você pode:
-- 1. Inserir documentos via scraper
-- 2. Consultar via views
-- 3. Visualizar mudanças
-- ============================================================================
