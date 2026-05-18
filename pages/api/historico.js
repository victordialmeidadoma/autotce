// pages/api/historico.js

import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
)

export default async function handler(req, res) {
  try {
    // GET: Retornar histórico de movimentações
    if (req.method === 'GET') {
      const { numero, ano, limite = 50 } = req.query
      
      let query = supabase
        .from('historico_movimentacoes')
        .select('*')
        .order('data_deteccao', { ascending: false })
        .limit(parseInt(limite))
      
      // Filtrar por número e ano se fornecido
      if (numero && ano) {
        query = query.eq('numero', numero).eq('ano', parseInt(ano))
      }
      
      const { data, error } = await query
      
      if (error) {
        return res.status(500).json({ erro: error.message })
      }
      
      return res.status(200).json({
        sucesso: true,
        total: data.length,
        historico: data
      })
    }
    
    res.status(405).json({ erro: 'Método não permitido' })
    
  } catch (erro) {
    console.error('Erro:', erro)
    res.status(500).json({ erro: erro.message })
  }
}
