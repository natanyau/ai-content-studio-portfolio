import type { Register } from 'claude-code'
import { bashWrites, isProtected } from './paths'

const MOTIVO =
  'assets/ guarda os arquivos de produção do site e só é alterado à mão (regra 4 do CLAUDE.md). ' +
  'Gere o arquivo novo fora de assets/ (por exemplo em .watermark/out/) e deixe a cópia para a pessoa.'

// Se a checagem falhar antes de decidir, recusa: na dúvida, assets/ fica intacto.
const FALHOU = `${MOTIVO} A checagem da trava falhou antes de decidir; tente de novo.`

// Se a pasta da sessão não vier, assume "/": um assets/ relativo continua
// protegido e o hook não falha.
async function cwdOf(cwd: () => Promise<string>): Promise<string> {
  try {
    return await cwd()
  } catch {
    return '/'
  }
}

export const register: Register = on => {
  on('tool.call', { tool: 'Edit' }, async ($, e, next) =>
    isProtected(await cwdOf(() => $.session.cwd()), e.file_path) ? { deny: `${MOTIVO} Arquivo: ${e.file_path}` } : next(e),
  ).catch(($, e, next) => (next.called ? next(e) : { deny: FALHOU }))

  on('tool.call', { tool: 'Write' }, async ($, e, next) =>
    isProtected(await cwdOf(() => $.session.cwd()), e.file_path) ? { deny: `${MOTIVO} Arquivo: ${e.file_path}` } : next(e),
  ).catch(($, e, next) => (next.called ? next(e) : { deny: FALHOU }))

  on('tool.call', { tool: 'NotebookEdit' }, async ($, e, next) =>
    isProtected(await cwdOf(() => $.session.cwd()), e.notebook_path) ? { deny: `${MOTIVO} Arquivo: ${e.notebook_path}` } : next(e),
  ).catch(($, e, next) => (next.called ? next(e) : { deny: FALHOU }))

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const hit = bashWrites(await cwdOf(() => $.session.cwd()), e.command)
    if (hit === undefined) return next(e)
    $.ui.toast(`timasmotion barrou: ${hit.slice(0, 60)}`)
    return { deny: `${MOTIVO} Trecho barrado: ${hit}` }
  }).catch(($, e, next) => (next.called ? next(e) : { deny: FALHOU }))
}
