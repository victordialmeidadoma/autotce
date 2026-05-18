# 🔍 GUIA DO SCRAPER REAL DE DOCUMENTOS

## O QUE VOCÊ RECEBEU

Um **scraper real** que:
- ✅ Acessa páginas do TCE-MA de verdade
- ✅ Extrai documentos gerais com data e teor completo
- ✅ Detecta novos documentos automaticamente
- ✅ Roda diariamente de madrugada (00:00)
- ✅ Salva tudo estruturado no Supabase

---

## ARQUIVOS NOVOS

```
api_scraping_documentos.py        ← Função Python serverless (Vercel)
SQL_CRIAR_TABELAS_DOCUMENTOS.sql  ← Script para criar tabelas
pages_api_documentos.js            ← Endpoint para listar documentos
components_DocumentosProcesso.jsx  ← Component React para exibir
vercel_atualizado.json            ← Config com novo cron job
```

---

## ⚙️ SETUP (5 PASSOS)

### Passo 1: Criar Tabelas no Supabase

1. Vá em Supabase → SQL Editor
2. Copie todo o conteúdo de `SQL_CRIAR_TABELAS_DOCUMENTOS.sql`
3. Cole no SQL Editor
4. Clique "Run"

✅ Tabelas criadas!

### Passo 2: Copiar Arquivo Python

```
Copiar: api_scraping_documentos.py
Para:   seu-projeto-tce/api/scraping_documentos.py
```

### Passo 3: Copiar Arquivo JavaScript

```
Copiar: pages_api_documentos.js
Para:   seu-projeto-tce/pages/api/documentos.js
```

### Passo 4: Copiar Component React

```
Copiar: components_DocumentosProcesso.jsx
Para:   seu-projeto-tce/components/DocumentosProcesso.jsx
```

### Passo 5: Atualizar vercel.json

```
Copiar: vercel_atualizado.json
Para:   seu-projeto-tce/vercel.json
```

---

## 🎯 COMO FUNCIONA

### Cronograma de Execução

```
Segunda-feira 09:00  → Busca semanal por ente/exercício
Todo dia 08:00       → Monitoramento de movimentações
Todo dia 18:00       → Monitoramento de movimentações
Todo dia 00:00 ⭐    → SCRAPING DE DOCUMENTOS (Novo!)
```

### Fluxo do Scraper

```
1. Vercel acorda à meia-noite (00:00)
   ↓
2. Busca lista de processos monitorados em Supabase
   ↓
3. Para cada processo:
   ├─ Acessa página real do TCE-MA
   ├─ Extrai documentos gerais
   ├─ Para cada documento:
   │  ├─ Extrai: Título, Data, Teor
   │  ├─ Compara com documentos anteriores
   │  └─ Se for novo: Salva e ALERTA
   └─ Atualiza Supabase
   ↓
4. Salva log da execução
   ↓
5. Dashboard mostra documentos novos
```

---

## 📊 ESTRUTURA DO BANCO

### Tabela: `documentos_processo`

```
id                    | Chave primária
numero                | "3154"
ano                   | 2025
titulo_documento      | "Documento Processo - 0001786087 - MPTCE/SEC"
data_documento        | "07/05/2026"
teor_completo         | "[Conteúdo completo do documento]"
data_deteccao         | Quando foi detectado
eh_novo               | true/false
```

---

## 🖥️ COMO USAR NO DASHBOARD

### No seu Dashboard:

```javascript
// pages/index.jsx - Adicionar dentro do componente

import DocumentosProcesso from '../components/DocumentosProcesso'

export default function Home() {
  const [numeroSelecionado, setNumeroSelecionado] = useState('3154')
  const [anoSelecionado, setAnoSelecionado] = useState(2025)
  
  return (
    <div>
      {/* ... seus outros componentes ... */}
      
      <DocumentosProcesso 
        numero={numeroSelecionado} 
        ano={anoSelecionado} 
      />
    </div>
  )
}
```

### O que você verá:

```
📄 Documentos Gerais (4)

┌─ Documento Processo - 0001786087 - MPTCE/SEC              [NOVO] ▼
│  07/05/2026
│
│  [Conteúdo completo do documento...]
│  Última atualização: 18/05/2026 00:05
│
├─ Documento Processo - 0001786027 - GCSUB2/MNN              ▼
│  07/05/2026
│
└─ ...
```

---

## 🔧 TESTANDO LOCALMENTE

### Teste 1: Verificar se está extraindo dados

```bash
# No seu projeto, execute:
python -c "
from api.scraping_documentos import testar_scraping_local
testar_scraping_local('3154', '2025')
"
```

Deve retornar:
```
📊 RESULTADO DO SCRAPING:
Processos: 3154/2025
Documentos encontrados: 4

📄 Documento Processo - 0001786087 - MPTCE/SEC
   Data: 07/05/2026
   Teor: [Conteúdo...]
```

### Teste 2: Verificar API

```bash
curl "http://localhost:3000/api/documentos?numero=3154&ano=2025"
```

Deve retornar JSON com documentos.

---

## 🚀 DEPLOY NO VERCEL

### 1. Fazer commit e push

```bash
git add .
git commit -m "Adicionar scraper real de documentos"
git push
```

### 2. Vercel faz deploy automaticamente

### 3. Verificar se está funcionando

```
# Chamar manualmente o cron job
curl https://seu-projeto.vercel.app/api/scraping_documentos
```

Deve retornar:
```json
{
  "status": "sucesso",
  "processos_verificados": 5,
  "mudancas_detectadas": 2,
  "timestamp": "2026-05-18T23:05:00Z",
  "mudancas": [
    {
      "processo": "3154/2025",
      "tipo": "novo_documento",
      "titulo": "Documento Processo - 0001786087"
    }
  ]
}
```

---

## 📈 MONITORAR EXECUÇÕES

### No Vercel Dashboard:

1. Vá em **Deployments → Logs**
2. Procure por "scraping_documentos"
3. Veja status de cada execução

### No Supabase:

1. Vá em **SQL Editor**
2. Execute:

```sql
SELECT * FROM logs WHERE tipo = 'scraping_documentos' ORDER BY data_execucao DESC LIMIT 10;
```

Verá histórico de todas as execuções!

---

## 🎨 CUSTOMIZAÇÕES

### Mudar horário do scraping

Em `vercel.json`:
```json
{
  "path": "/api/scraping_documentos",
  "schedule": "0 23 * * *"  // 23:00 em vez de 00:00
}
```

### Adicionar mais informações extraídas

Em `api_scraping_documentos.py`, expandir:
```python
documentos.append({
    "titulo": titulo,
    "data": data,
    "teor": teor,
    "autor": autor,        # ← Novo
    "categoria": categoria # ← Novo
})
```

### Filtrar documentos

Em `pages/api/documentos.js`:
```javascript
let query = supabase
  .from('documentos_processo')
  .select('*')
  .eq('numero', numero)
  .eq('ano', parseInt(ano))
  
// Adicionar filtro
if (filtro) {
  query = query.ilike('titulo_documento', `%${filtro}%`)
}
```

---

## ⚠️ TROUBLESHOOTING

### "Documentos não estão sendo extraídos"

**Causa**: Estrutura HTML do TCE-MA pode ter mudado

**Solução**: 
1. Abra a página real no navegador
2. Inspecione o HTML (F12)
3. Procure pelos seletores CSS usados
4. Atualize `_extrair_documentos_gerais()` com novos seletores

### "Teor não está sendo extraído"

**Causa**: Link do documento é diferente

**Solução**:
1. Clique manualmente em um documento
2. Veja a URL que aparece
3. Atualize `_extrair_teor_documento()` com a URL correta

### "Timeout ao acessar TCE-MA"

**Causa**: Servidor TCE-MA está lento

**Solução**: Aumentar timeout em `api_scraping_documentos.py`:
```python
response = requests.get(url, headers=headers, timeout=60)  # 60 segundos
```

### "Supabase: unique constraint violated"

**Causa**: Documento duplicado

**Solução**: Automático! O código detecta e não duplica.

---

## 📚 ESTRUTURA DE PASTAS FINAL

```
seu-projeto-tce/
├── api/
│   ├── busca_semanal.py
│   ├── monitoramento_diario.py
│   └── scraping_documentos.py        ← NOVO
│
├── pages/
│   ├── index.jsx
│   ├── _app.jsx
│   └── api/
│       ├── processos.js
│       ├── monitorados.js
│       ├── historico.js
│       └── documentos.js             ← NOVO
│
├── components/
│   └── DocumentosProcesso.jsx        ← NOVO
│
├── styles/
│   └── globals.css
│
├── vercel.json                       ← ATUALIZADO
├── package.json
├── requirements.txt
├── config.py
└── .env.local
```

---

## 🎉 RESULTADO FINAL

Você terá:

✅ **Dashboard completo** mostrando documentos com teor
✅ **Alertas automáticos** quando novos documentos aparecem
✅ **Histórico** de todas as movimentações
✅ **Funcionamento 24/7** sem trabalho manual
✅ **Dados estruturados** em Supabase

---

**Próximos passos:**

1. ✅ Criar tabelas (SQL)
2. ✅ Copiar arquivos
3. ✅ Testar localmente
4. ✅ Deploy no Vercel
5. ✅ Monitorar logs

Pronto? Você tem tudo para transformar seu workflow! 🚀
