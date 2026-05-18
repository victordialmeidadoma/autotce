// pages/index.jsx

import { useEffect, useState } from 'react'
import axios from 'axios'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { Plus, Trash2, RefreshCw, AlertCircle, Clock } from 'lucide-react'

const COLORS = ['#3b82f6', '#10b981', '#f59e0b']

export default function Home() {
  const [abaAtiva, setAbaAtiva] = useState('visao-geral')
  const [processosAtivos, setProcessosAtivos] = useState([])
  const [processosMonitorados, setProcessosMonitorados] = useState([])
  const [historico, setHistorico] = useState([])
  const [loading, setLoading] = useState(false)
  
  const [novoProcesso, setNovoProcesso] = useState({
    numero: '',
    ano: new Date().getFullYear(),
    ente: 'São Luís',
    descricao: ''
  })

  // Carregar dados ao montar componente
  useEffect(() => {
    carregarDados()
  }, [])

  const carregarDados = async () => {
    setLoading(true)
    try {
      // Carregar processos ativos
      const resAtivos = await axios.get('/api/processos')
      setProcessosAtivos(resAtivos.data.processos || [])
      
      // Carregar processos monitorados
      const resMonitorados = await axios.get('/api/monitorados')
      setProcessosMonitorados(resMonitorados.data.monitorados || [])
      
      // Carregar histórico
      const resHistorico = await axios.get('/api/historico')
      setHistorico(resHistorico.data.historico || [])
    } catch (erro) {
      console.error('Erro ao carregar dados:', erro)
    }
    setLoading(false)
  }

  const adicionarProcesso = async () => {
    if (!novoProcesso.numero || !novoProcesso.ano) {
      alert('Preencha número e ano')
      return
    }
    
    try {
      await axios.post('/api/processos', novoProcesso)
      setNovoProcesso({ numero: '', ano: new Date().getFullYear(), ente: 'São Luís', descricao: '' })
      await carregarDados()
      alert('Processo adicionado com sucesso!')
    } catch (erro) {
      alert('Erro ao adicionar processo: ' + erro.message)
    }
  }

  const removerProcesso = async (numero, ano) => {
    if (confirm('Remover este processo do monitoramento?')) {
      try {
        await axios.delete('/api/monitorados', { data: { numero, ano } })
        await carregarDados()
      } catch (erro) {
        alert('Erro ao remover: ' + erro.message)
      }
    }
  }

  const estatisticas = {
    totalAtivos: processosAtivos.length,
    totalMonitorados: processosMonitorados.length,
    novos: processosAtivos.filter(p => p.eh_novo).length,
  }

  const dadosGrafico = [
    { ente: 'São Luís', quantidade: 12 },
    { ente: 'Paço do Lumiar', quantidade: 8 },
    { ente: 'Outras', quantidade: 5 }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* HEADER */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-8 px-6">
        <h1 className="text-4xl font-bold">📋 TCE-MA Acompanhamento</h1>
        <p className="text-blue-100 mt-2">Sistema Automatizado de Processos</p>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        {/* ABAS */}
        <div className="flex flex-wrap gap-2 mb-8">
          {[
            { id: 'visao-geral', label: '📊 Visão Geral' },
            { id: 'ativos', label: '✅ Processos Ativos' },
            { id: 'monitorados', label: '🔍 Monitorados' },
            { id: 'novo', label: '➕ Adicionar' },
          ].map(aba => (
            <button
              key={aba.id}
              onClick={() => setAbaAtiva(aba.id)}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                abaAtiva === aba.id
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {aba.label}
            </button>
          ))}
        </div>

        {/* ABAS - CONTEÚDO */}
        
        {/* VISÃO GERAL */}
        {abaAtiva === 'visao-geral' && (
          <div className="space-y-6">
            {/* CARDS */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">Processos Ativos</p>
                <p className="text-4xl font-bold mt-2">{estatisticas.totalAtivos}</p>
              </div>
              <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">Monitorando</p>
                <p className="text-4xl font-bold mt-2">{estatisticas.totalMonitorados}</p>
              </div>
              <div className="bg-gradient-to-br from-amber-500 to-amber-600 rounded-lg p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">Novos (semana)</p>
                <p className="text-4xl font-bold mt-2">{estatisticas.novos}</p>
              </div>
            </div>

            {/* GRÁFICO */}
            <div className="bg-slate-700 rounded-lg p-6">
              <h3 className="text-lg font-bold text-slate-100 mb-4">Processos por Ente</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={dadosGrafico}
                    dataKey="quantidade"
                    nameKey="ente"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  >
                    {dadosGrafico.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* PROCESSOS ATIVOS */}
        {abaAtiva === 'ativos' && (
          <div className="bg-slate-700 rounded-lg overflow-hidden">
            <button
              onClick={carregarDados}
              className="m-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" /> Atualizar
            </button>
            
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-slate-100">
                <thead className="bg-slate-600">
                  <tr>
                    <th className="px-6 py-3 text-left">Processo</th>
                    <th className="px-6 py-3 text-left">Ente</th>
                    <th className="px-6 py-3 text-left">Natureza</th>
                    <th className="px-6 py-3 text-left">Status</th>
                    <th className="px-6 py-3 text-center">Novo?</th>
                  </tr>
                </thead>
                <tbody>
                  {processosAtivos.slice(0, 20).map(p => (
                    <tr key={`${p.numero}/${p.exercicio}`} className="border-t border-slate-600 hover:bg-slate-600">
                      <td className="px-6 py-3 font-mono text-blue-400">{p.numero}/{p.exercicio}</td>
                      <td className="px-6 py-3">{p.ente}</td>
                      <td className="px-6 py-3">{p.natureza}</td>
                      <td className="px-6 py-3">{p.status}</td>
                      <td className="px-6 py-3 text-center">{p.eh_novo ? '✅' : '⭕'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* PROCESSOS MONITORADOS */}
        {abaAtiva === 'monitorados' && (
          <div className="bg-slate-700 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-slate-100">
                <thead className="bg-slate-600">
                  <tr>
                    <th className="px-6 py-3 text-left">Processo</th>
                    <th className="px-6 py-3 text-left">Ente</th>
                    <th className="px-6 py-3 text-left">Descrição</th>
                    <th className="px-6 py-3 text-left">Status</th>
                    <th className="px-6 py-3 text-center">Ação</th>
                  </tr>
                </thead>
                <tbody>
                  {processosMonitorados.map(p => (
                    <tr key={`${p.numero}/${p.ano}`} className="border-t border-slate-600 hover:bg-slate-600">
                      <td className="px-6 py-3 font-mono text-blue-400">{p.numero}/{p.ano}</td>
                      <td className="px-6 py-3">{p.ente}</td>
                      <td className="px-6 py-3 truncate">{p.descricao}</td>
                      <td className="px-6 py-3">{p.status}</td>
                      <td className="px-6 py-3 text-center">
                        <button
                          onClick={() => removerProcesso(p.numero, p.ano)}
                          className="text-red-400 hover:text-red-300"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ADICIONAR PROCESSO */}
        {abaAtiva === 'novo' && (
          <div className="max-w-2xl mx-auto bg-slate-700 rounded-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-slate-100">➕ Adicionar Processo</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Número</label>
                <input
                  type="text"
                  placeholder="Ex: 12345"
                  value={novoProcesso.numero}
                  onChange={(e) => setNovoProcesso({...novoProcesso, numero: e.target.value})}
                  className="w-full px-4 py-2 bg-slate-600 border border-slate-500 rounded text-slate-100 placeholder-slate-400"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Ano</label>
                  <input
                    type="number"
                    value={novoProcesso.ano}
                    onChange={(e) => setNovoProcesso({...novoProcesso, ano: parseInt(e.target.value)})}
                    className="w-full px-4 py-2 bg-slate-600 border border-slate-500 rounded text-slate-100"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Ente</label>
                  <input
                    type="text"
                    value={novoProcesso.ente}
                    onChange={(e) => setNovoProcesso({...novoProcesso, ente: e.target.value})}
                    className="w-full px-4 py-2 bg-slate-600 border border-slate-500 rounded text-slate-100"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Descrição</label>
                <textarea
                  value={novoProcesso.descricao}
                  onChange={(e) => setNovoProcesso({...novoProcesso, descricao: e.target.value})}
                  rows="4"
                  className="w-full px-4 py-2 bg-slate-600 border border-slate-500 rounded text-slate-100"
                />
              </div>

              <button
                onClick={adicionarProcesso}
                disabled={loading}
                className="w-full mt-6 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 disabled:opacity-50"
              >
                {loading ? 'Adicionando...' : 'Adicionar à Monitoramento'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
