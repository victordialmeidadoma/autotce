"""
API: GET /api/busca_semanal

Função serverless para executar busca semanal de processos.
Agendado para rodar todo segundo-feira às 09:00
"""

from http.server import BaseHTTPRequestHandler
import json
import requests
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, ENTIDADES_MONITORADAS, EXERCICIOS_MONITORADOS, PALAVRAS_PREVIDENCIA
from supabase import create_client, Client

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Executa a busca semanal"""
        try:
            print("🔍 Iniciando busca semanal...")
            
            # Conectar ao Supabase
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            todos_processos = []
            
            # Para cada ente
            for ente, codigo in ENTIDADES_MONITORADAS.items():
                for exercicio in EXERCICIOS_MONITORADOS:
                    print(f"   Buscando: {ente} ({exercicio})")
                    
                    # Fazer requisição (simulado)
                    processos = self._buscar_processos(ente, exercicio)
                    
                    # Filtrar previdência
                    processos_filtrados = self._filtrar_previdencia(processos)
                    
                    # Adicionar informações
                    for p in processos_filtrados:
                        p["ente"] = ente
                        p["exercicio"] = exercicio
                        p["data_atualizacao"] = datetime.now().isoformat()
                    
                    todos_processos.extend(processos_filtrados)
            
            # Carregar processos anteriores
            try:
                response = supabase.table("processos_ativos").select("*").execute()
                processos_anteriores = {p["numero"]: p for p in response.data}
            except:
                processos_anteriores = {}
            
            # Detectar novos
            novos = []
            for p in todos_processos:
                chave = f"{p['numero']}/{p['exercicio']}"
                if chave not in processos_anteriores:
                    novos.append(p)
                    p["eh_novo"] = True
                else:
                    p["eh_novo"] = False
            
            # Salvar no banco de dados
            for p in todos_processos:
                try:
                    supabase.table("processos_ativos").upsert({
                        "numero": p["numero"],
                        "exercicio": p["exercicio"],
                        "ente": p["ente"],
                        "natureza": p.get("natureza", ""),
                        "status": p.get("status", ""),
                        "data_atualizacao": datetime.now().isoformat(),
                        "eh_novo": p.get("eh_novo", False)
                    }).execute()
                except Exception as e:
                    print(f"   Erro ao salvar {p['numero']}: {e}")
            
            # Registrar log
            supabase.table("logs").insert({
                "tipo": "busca_semanal",
                "status": "sucesso",
                "processos_encontrados": len(todos_processos),
                "novos_processos": len(novos),
                "data_execucao": datetime.now().isoformat(),
                "descricao": json.dumps({
                    "novos": [f"{p['numero']}/{p['exercicio']}" for p in novos]
                })
            }).execute()
            
            # Responder
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            resposta = {
                "status": "sucesso",
                "processos_encontrados": len(todos_processos),
                "novos_processos": len(novos),
                "timestamp": datetime.now().isoformat(),
                "novos": [{"numero": p["numero"], "exercicio": p["exercicio"], "ente": p["ente"]} for p in novos[:5]]
            }
            
            self.wfile.write(json.dumps(resposta).encode())
            print(f"✅ Busca concluída: {len(todos_processos)} processos, {len(novos)} novos")
            
        except Exception as e:
            print(f"❌ Erro na busca semanal: {e}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps({
                "status": "erro",
                "mensagem": str(e)
            }).encode())
    
    def _buscar_processos(self, ente, exercicio):
        """Simula busca de processos (adaptar para API real do TCE-MA)"""
        # Em produção, fazer requisição real ao TCE-MA
        # Por agora, retornar dados simulados
        return [
            {"numero": "10001", "natureza": "Auditoria", "status": "Em andamento"},
            {"numero": "10002", "natureza": "Fiscalização", "status": "Em andamento"},
            {"numero": "10003", "natureza": "Previdência", "status": "Em andamento"},
        ]
    
    def _filtrar_previdencia(self, processos):
        """Remove processos de previdência"""
        filtrados = []
        
        for p in processos:
            natureza = p.get("natureza", "").lower()
            
            # Verificar palavras-chave de previdência
            eh_previdencia = any(
                palavra.lower() in natureza 
                for palavra in PALAVRAS_PREVIDENCIA
            )
            
            if not eh_previdencia:
                filtrados.append(p)
        
        return filtrados
