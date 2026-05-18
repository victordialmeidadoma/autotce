// components/DocumentosProcesso.jsx

import { useState, useEffect } from 'react'
import { ChevronDown, ChevronUp, FileText, AlertCircle } from 'lucide-react'
import axios from 'axios'

export default function DocumentosProcesso({ numero, ano }) {
  const [documentos, setDocumentos] = useState([])
  const [expandidos, setExpandidos] = useState({})
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState(null)

  useEffect(() => {
    carregarDocumentos()
  }, [numero, ano])

  const carregarDocumentos = async () => {
    if (!numero || !ano) return
    
    setLoading(true)
    setErro(null)
    
    try {
      const response = await axios.get('/api/documentos', {
        params: { numero, ano }
      })
      
      setDocumentos(response.data.documentos || [])
    } catch (err) {
      setErro('Erro ao carregar documentos: ' + err.message)
    }
    
    setLoading(false)
  }

  const toggleExpandido = (id) => {
    setExpandidos(prev => ({
      ...prev,
      [id]: !prev[id]
    }))
  }

  if (loading) {
    return <div className="text-slate-400">Carregando documentos...</div>
  }

  if (erro) {
    return (
      <div className="bg-red-500/20 border border-red-500 rounded p-4 text-red-400">
        <AlertCircle className="w-4 h-4 inline mr-2" />
        {erro}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="bg-slate-700 rounded-lg p-4">
        <h3 className="text-lg font-bold text-slate-100 mb-4">
          📄 Documentos Gerais ({documentos.length})
        </h3>

        {documentos.length === 0 ? (
          <p className="text-slate-400">Nenhum documento encontrado</p>
        ) : (
          <div className="space-y-3">
            {documentos.map((doc, idx) => (
              <div key={idx} className="bg-slate-600 rounded border border-slate-500">
                {/* HEADER - Clicável */}
                <button
                  onClick={() => toggleExpandido(idx)}
                  className="w-full px-4 py-3 flex items-center justify-between hover:bg-slate-500 transition-colors text-left"
                >
                  <div className="flex items-center gap-3 flex-1">
                    <FileText className="w-5 h-5 text-blue-400 flex-shrink-0" />
                    
                    <div className="flex-1 min-w-0">
                      <p className="font-semibold text-slate-100 truncate">
                        {doc.titulo_documento}
                      </p>
                      <p className="text-sm text-slate-400">
                        {doc.data_documento}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 ml-2">
                    {doc.eh_novo && (
                      <span className="px-3 py-1 bg-green-500/30 text-green-400 text-xs font-semibold rounded-full">
                        NOVO
                      </span>
                    )}
                    
                    {expandidos[idx] ? (
                      <ChevronUp className="w-5 h-5 text-slate-400" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-slate-400" />
                    )}
                  </div>
                </button>

                {/* CONTEÚDO - Expandível */}
                {expandidos[idx] && (
                  <div className="px-4 py-4 border-t border-slate-500 bg-slate-700/50">
                    {doc.teor_completo ? (
                      <div>
                        <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
                          {doc.teor_completo}
                        </p>
                        <p className="text-xs text-slate-500 mt-3">
                          Última atualização: {new Date(doc.data_atualizacao || doc.data_deteccao).toLocaleString('pt-BR')}
                        </p>
                      </div>
                    ) : (
                      <p className="text-slate-400 italic">
                        [Teor não disponível]
                      </p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* BOTÃO PARA ATUALIZAR */}
      <button
        onClick={carregarDocumentos}
        className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
      >
        🔄 Atualizar Documentos
      </button>
    </div>
  )
}
