"""
SCRAPER REAL - TCE-MA
Extrai documentos gerais, teor completo e detecta mudanças
Agendado para rodar de madrugada (00:00 - horário comercial não tem movimentações)
"""

from http.server import BaseHTTPRequestHandler
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import logging
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Executa scraping de madrugada"""
        try:
            logger.info("🔍 Iniciando scraping de madrugada...")
            
            # Conectar ao Supabase
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            # Obter processos monitorados
            response = supabase.table("processos_monitorados").select("numero,ano").execute()
            processos = response.data
            
            todas_mudancas = []
            
            # Para cada processo monitorado
            for processo in processos:
                numero = processo["numero"]
                ano = processo["ano"]
                chave = f"{numero}/{ano}"
                
                logger.info(f"   Processando: {chave}")
                
                try:
                    # Fazer scraping do processo
                    documentos = self._extrair_documentos_gerais(numero, ano)
                    
                    if documentos:
                        # Carregar documentos anteriores
                        try:
                            doc_anterior = supabase.table("documentos_processo") \
                                .select("*") \
                                .eq("numero", numero) \
                                .eq("ano", ano) \
                                .execute()
                            docs_anteriores = {d["titulo_documento"]: d for d in doc_anterior.data}
                        except:
                            docs_anteriores = {}
                        
                        # Detectar novos documentos
                        for doc in documentos:
                            titulo = doc["titulo"]
                            
                            if titulo not in docs_anteriores:
                                # Novo documento!
                                logger.warning(f"   ✅ NOVO DOCUMENTO: {titulo}")
                                
                                # Salvar novo documento
                                supabase.table("documentos_processo").insert({
                                    "numero": numero,
                                    "ano": ano,
                                    "titulo_documento": titulo,
                                    "data_documento": doc["data"],
                                    "teor_completo": doc.get("teor", ""),
                                    "data_deteccao": datetime.now().isoformat(),
                                    "eh_novo": True
                                }).execute()
                                
                                todas_mudancas.append({
                                    "processo": chave,
                                    "tipo": "novo_documento",
                                    "titulo": titulo,
                                    "data": doc["data"],
                                    "teor_preview": doc.get("teor", "")[:200]
                                })
                            else:
                                # Documento existente - atualizar teor se mudou
                                doc_anterior = docs_anteriores[titulo]
                                if doc_anterior.get("teor_completo") != doc.get("teor"):
                                    logger.info(f"   📝 TEOR ATUALIZADO: {titulo}")
                                    
                                    supabase.table("documentos_processo").update({
                                        "teor_completo": doc.get("teor", ""),
                                        "data_atualizacao": datetime.now().isoformat()
                                    }).eq("numero", numero) \
                                     .eq("ano", ano) \
                                     .eq("titulo_documento", titulo) \
                                     .execute()
                                    
                                    todas_mudancas.append({
                                        "processo": chave,
                                        "tipo": "teor_atualizado",
                                        "titulo": titulo,
                                        "teor_preview": doc.get("teor", "")[:200]
                                    })
                
                except Exception as e:
                    logger.error(f"   ❌ Erro ao processar {chave}: {e}")
            
            # Registrar log
            supabase.table("logs").insert({
                "tipo": "scraping_documentos",
                "status": "sucesso",
                "mudancas_detectadas": len(todas_mudancas),
                "data_execucao": datetime.now().isoformat(),
                "descricao": json.dumps({
                    "novos_documentos": len([m for m in todas_mudancas if m["tipo"] == "novo_documento"]),
                    "teores_atualizados": len([m for m in todas_mudancas if m["tipo"] == "teor_atualizado"]),
                    "processos_verificados": len(processos)
                })
            }).execute()
            
            # Responder
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            resposta = {
                "status": "sucesso",
                "processos_verificados": len(processos),
                "mudancas_detectadas": len(todas_mudancas),
                "timestamp": datetime.now().isoformat(),
                "mudancas": todas_mudancas[:10]  # Primeiras 10
            }
            
            self.wfile.write(json.dumps(resposta).encode())
            logger.info(f"✅ Scraping concluído: {len(todas_mudancas)} mudança(s)")
            
        except Exception as e:
            logger.error(f"❌ Erro no scraping: {e}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps({
                "status": "erro",
                "mensagem": str(e)
            }).encode())
    
    def _extrair_documentos_gerais(self, numero, ano):
        """
        Acessa a página real do processo e extrai documentos gerais
        
        URL: https://consultaprocesso-externo.apps.tcema.tc.br/processo/{numero}{ano}
        
        Estrutura esperada (baseada nas screenshots):
        - Seção "Documentos Gerais"
        - Lista de volumes e documentos
        - Cada documento tem: título, data, possível teor
        """
        
        try:
            # Construir URL do processo
            url_processo = f"https://consultaprocesso-externo.apps.tcema.tc.br/processo/{numero}{ano}"
            
            logger.info(f"   Acessando: {url_processo}")
            
            # Fazer requisição
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url_processo, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Fazer parsing com BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            documentos = []
            
            # Estratégia 1: Procurar por "Documentos Gerais"
            # A página usa estrutura com divs e classes
            
            # Encontrar a seção de documentos gerais
            # Baseado nas screenshots, procurar por estrutura de volumes e documentos
            
            # Tentativa 1: Procurar por texto "Documentos Gerais"
            doc_gerais_section = None
            for element in soup.find_all(['h2', 'h3', 'div']):
                if element and 'Documentos Gerais' in element.get_text():
                    doc_gerais_section = element
                    break
            
            if not doc_gerais_section:
                logger.warning(f"   ⚠️  Seção 'Documentos Gerais' não encontrada")
                # Tentar método alternativo
                return self._extrair_documentos_alternativo(soup)
            
            # A partir da seção, procurar por documentos
            # Estrutura esperada: Volume > Documentos com títulos e datas
            
            # Procurar por elementos que parecem ser documentos
            # Na estrutura das screenshots, são listas com:
            # - Ícone de documento
            # - Título (pode ter link)
            # - "Despacho" ou tipo
            # - Data (DD/MM/YYYY HH:MM)
            
            # Procurar padrão: "Documento Processo - XXXXX - YYYY"
            pattern_docs = soup.find_all('div', class_=['documento', 'doc', 'item'])
            
            if not pattern_docs:
                # Tentar padrão alternativo
                pattern_docs = soup.find_all(['li', 'tr'])
            
            # Extrair documentos
            for item in pattern_docs:
                titulo = item.get_text(strip=True)
                
                # Se parecer um documento
                if 'Documento' in titulo or 'Despacho' in titulo:
                    # Extrair data
                    # Formato esperado: DD/MM/YYYY ou DD/MM/YYYY HH:MM
                    import re
                    data_match = re.search(r'\d{2}/\d{2}/\d{4}', titulo)
                    data = data_match.group(0) if data_match else ""
                    
                    # Tentar extrair teor
                    teor = self._extrair_teor_documento(numero, ano, titulo)
                    
                    documentos.append({
                        "titulo": titulo,
                        "data": data,
                        "teor": teor
                    })
            
            logger.info(f"   ✅ Extraídos {len(documentos)} documentos")
            return documentos
            
        except requests.RequestException as e:
            logger.error(f"   ❌ Erro na requisição: {e}")
            return []
        except Exception as e:
            logger.error(f"   ❌ Erro ao extrair documentos: {e}")
            return []
    
    def _extrair_documentos_alternativo(self, soup):
        """
        Método alternativo se a primeira estratégia falhar
        Procura por padrões de documentos em qualquer lugar da página
        """
        
        try:
            documentos = []
            
            # Procurar por qualquer div ou elemento que contenha "Documento"
            for element in soup.find_all(['div', 'li', 'tr']):
                texto = element.get_text(strip=True)
                
                if 'Documento Processo' in texto or 'Despacho' in texto:
                    # Extrair data
                    import re
                    data_match = re.search(r'\d{2}/\d{2}/\d{4}', texto)
                    data = data_match.group(0) if data_match else ""
                    
                    documentos.append({
                        "titulo": texto,
                        "data": data,
                        "teor": ""  # Sem teor neste método
                    })
            
            return documentos
            
        except Exception as e:
            logger.error(f"❌ Erro no método alternativo: {e}")
            return []
    
    def _extrair_teor_documento(self, numero, ano, titulo):
        """
        Tenta clicar no documento e extrair o teor completo
        Se não conseguir, retorna string vazia
        
        Para documentos com links, faz requisição para a página do documento
        """
        
        try:
            # Tentar extrair ID ou link do documento do título
            import re
            
            # Padrão esperado: "Documento Processo - 0001786087 - MPTCE/SEC"
            match = re.search(r'(\d+)', titulo)
            
            if not match:
                return ""
            
            doc_id = match.group(1)
            
            # Tentar acessar página do documento
            # URL possível: /documento/{id} ou similar
            url_doc = f"https://consultaprocesso-externo.apps.tcema.tc.br/documento/{doc_id}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url_doc, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Procurar por conteúdo de texto
                # Pode estar em <p>, <div class="content">, etc
                conteudo = soup.get_text(strip=True)
                
                # Retornar primeiros 500 caracteres
                return conteudo[:500]
            
            return ""
            
        except Exception as e:
            logger.debug(f"Não foi possível extrair teor: {e}")
            return ""


# ============================================================================
# FUNÇÃO AUXILIAR PARA TESTAR LOCALMENTE
# ============================================================================

def testar_scraping_local(numero, ano):
    """
    Função para testar o scraping localmente
    
    Uso:
    python -c "from api_scraping_documentos import testar_scraping_local; testar_scraping_local('3154', '2025')"
    """
    
    scraper = handler(None, None, None)
    documentos = scraper._extrair_documentos_gerais(numero, ano)
    
    print(f"\n📊 RESULTADO DO SCRAPING:")
    print(f"Processos: {numero}/{ano}")
    print(f"Documentos encontrados: {len(documentos)}")
    print()
    
    for doc in documentos:
        print(f"📄 {doc['titulo']}")
        print(f"   Data: {doc['data']}")
        print(f"   Teor: {doc['teor'][:100]}..." if doc['teor'] else "   Teor: [Não extraído]")
        print()

