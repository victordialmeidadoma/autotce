// pages/api/monitorados.js

import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
)

export default async function handler(req, res) {
  try {
    // GET: Retornar processos monitorados
    if (req.method === 'GET') {
      const { data, error } = await supabase
        .from('processos_monitorados')
        .select('*')
        .order('data_adicao', { ascending: false })
      
      if (error) {
        return res.status(500).json({ erro: error.message })
      }
      
      return res.status(200).json({
        sucesso: true,
        total: data.length,
        monitorados: data
      })
    }
    
    // DELETE: Remover processo do monitoramento
    if (req.method === 'DELETE') {
      const { numero, ano } = req.body
      
      const { error } = await supabase
        .from('processos_monitorados')
        .delete()
        .eq('numero', numero)
        .eq('ano', ano)
      
      if (error) {
        return res.status(500).json({ erro: error.message })
      }
      
      return res.status(200).json({
        sucesso: true,
        mensagem: 'Processo removido do monitoramento'
      })
    }
    
    res.status(405).json({ erro: 'Método não permitido' })
    
  } catch (erro) {
    console.error('Erro:', erro)
    res.status(500).json({ erro: erro.message })
  }
}
