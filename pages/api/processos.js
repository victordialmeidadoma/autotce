// pages/api/processos.js

import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
)

export default async function handler(req, res) {
  try {
    // GET: Retornar processos ativos
    if (req.method === 'GET') {
      const { data, error } = await supabase
        .from('processos_ativos')
        .select('*')
        .order('data_atualizacao', { ascending: false })
        .limit(100)
      
      if (error) {
        return res.status(500).json({ erro: error.message })
      }
      
      return res.status(200).json({
        sucesso: true,
        total: data.length,
        processos: data,
        novos: data.filter(p => p.eh_novo).length
      })
    }
    
    // POST: Adicionar novo processo
    if (req.method === 'POST') {
      const { numero, ano, ente, descricao } = req.body
      
      const { data, error } = await supabase
        .from('processos_monitorados')
        .insert([{
          numero,
          ano,
          ente,
          descricao,
          data_adicao: new Date().toISOString(),
          status: 'Ativo'
        }])
      
      if (error) {
        return res.status(500).json({ erro: error.message })
      }
      
      return res.status(201).json({
        sucesso: true,
        mensagem: 'Processo adicionado com sucesso'
      })
    }
    
    res.status(405).json({ erro: 'Método não permitido' })
    
  } catch (erro) {
    console.error('Erro:', erro)
    res.status(500).json({ erro: erro.message })
  }
}
