"""
API: GET /api/monitoramento_diario

Função serverless para verificar movimentações diárias.
Agendado para rodar todo dia às 08:00 e 18:00
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Executa monitoramento diário"""
        try:
            print("🔍 Iniciando monitoramento diário...")
            
            # Conectar ao Supabase
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            # Obter processos monitorados
            response = supabase.table("processos_monitorados").select("*").execute()
            processos_monitorados = response.data
            
            alteracoes = []
            
            for processo in processos_monitorados:
                numero = processo["numero"]
                ano = processo["ano"]
                
                print(f"   Verificando: {numero}/{ano}")
                
                # Obter movimentação atual (simulada)
                mov_atual = self._obter_movimentacao(numero, ano)
                
                if mov_atual:
                    # Comparar com anterior
                    mov_anterior = processo.get("ultima_movimentacao")
                    
                    if mov_anterior != mov_atual:
                        # Houve mudança!
                        alteracoes.append({
                            "numero": numero,
                            "ano": ano,
                            "anterior": mov_anterior,
                            "atual": mov_atual,
                            "ente": processo.get("ente")
                        })
                        
                        # Atualizar no banco
                        supabase.table("processos_monitorados").update({
                            "ultima_movimentacao": json.dumps(mov_atual),
                            "ultima_atualizacao": datetime.now().isoformat()
                        }).eq("numero", numero).eq("ano", ano).execute()
                        
                        # Salvar no histórico
                        supabase.table("historico_movimentacoes").insert({
                            "numero": numero,
                            "ano": ano,
                            "movimentacao_descricao": mov_atual.get("descricao"),
                            "movimentacao_data": mov_atual.get("data"),
                            "movimentacao_status": mov_atual.get("status"),
                            "data_deteccao": datetime.now().isoformat()
                        }).execute()
                        
                        print(f"   ✅ MUDANÇA DETECTADA: {mov_atual.get('descricao')}")
            
            # Registrar log
            supabase.table("logs").insert({
                "tipo": "monitoramento_diario",
                "status": "sucesso",
                "alteracoes_detectadas": len(alteracoes),
                "data_execucao": datetime.now().isoformat(),
                "descricao": json.dumps({
                    "processos_verificados": len(processos_monitorados),
                    "alteracoes": [f"{a['numero']}/{a['ano']}" for a in alteracoes]
                })
            }).execute()
            
            # Responder
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            resposta = {
                "status": "sucesso",
                "processos_verificados": len(processos_monitorados),
                "alteracoes_detectadas": len(alteracoes),
                "timestamp": datetime.now().isoformat(),
                "alteracoes": alteracoes[:5]  # Primeiras 5
            }
            
            self.wfile.write(json.dumps(resposta).encode())
            print(f"✅ Monitoramento concluído: {len(alteracoes)} alteração(ões)")
            
        except Exception as e:
            print(f"❌ Erro no monitoramento: {e}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps({
                "status": "erro",
                "mensagem": str(e)
            }).encode())
    
    def _obter_movimentacao(self, numero, ano):
        """Simula obtenção de movimentação (adaptar para API real do TCE-MA)"""
        # Em produção, fazer requisição real ao TCE-MA
        return {
            "data": datetime.now().strftime("%Y-%m-%d"),
            "descricao": "Movimentação simulada",
            "status": "Processando"
        }
