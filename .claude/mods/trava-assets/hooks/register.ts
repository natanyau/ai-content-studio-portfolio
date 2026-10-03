import type { Register } from 'claude-code'
import { bashWrites, isProtected } from './paths'

const MOTIVO =
  'assets/ guarda os arquivos de produção do site e só é alterado à mão (regra 4 do CLAUDE.md). ' +
  'Gere o arquivo novo fora de assets/ (por exemplo em .watermark/out/) e deixe a cópia para a pessoa.'

// Se a pasta da sessão não vier, assume "/": um assets/ relativo continua
// protegido e o hook não falha. Hook que falha é pulado, e a ação passaria.
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
  )

  on('tool.call', { tool: 'Write' }, async ($, e, next) =>
    isProtected(await cwdOf(() => $.session.cwd()), e.file_path) ? { deny: `${MOTIVO} Arquivo: ${e.file_path}` } : next(e),
  )

  on('tool.call', { tool: 'NotebookEdit' }, async ($, e, next) =>
    isProtected(await cwdOf(() => $.session.cwd()), e.notebook_path) ? { deny: `${MOTIVO} Arquivo: ${e.notebook_path}` } : next(e),
  )

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const hit = bashWrites(await cwdOf(() => $.session.cwd()), e.command)
    if (hit === undefined) return next(e)
    $.ui.toast(`trava-assets barrou: ${hit.slice(0, 60)}`)
    return { deny: `${MOTIVO} Trecho barrado: ${hit}` }
  })
}
