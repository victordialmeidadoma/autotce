// pages/api/documentos.js

import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
)

export default async function handler(req, res) {
  try {
    // GET: Retornar documentos de um processo
    if (req.method === 'GET') {
      const { numero, ano } = req.query
      
      if (!numero || !ano) {
        return res.status(400).json({ erro: 'Número e ano são obrigatórios' })
      }
      
      const { data, error } = await supabase
        .from('documentos_processo')
        .select('*')
        .eq('numero', numero)
        .eq('ano', parseInt(ano))
        .order('data_deteccao', { ascending: false })
      
      if (error) {
        return res.status(500).json({ erro: error.message })
      }
      
      return res.status(200).json({
        sucesso: true,
        processo: `${numero}/${ano}`,
        total_documentos: data.length,
        novos: data.filter(d => d.eh_novo).length,
        documentos: data,
        resumo: {
          total: data.length,
          novos: data.filter(d => d.eh_novo).length,
          ultima_atualizacao: data.length > 0 ? data[0].data_deteccao : null
        }
      })
    }
    
    res.status(405).json({ erro: 'Método não permitido' })
    
  } catch (erro) {
    console.error('Erro:', erro)
    res.status(500).json({ erro: erro.message })
  }
}
