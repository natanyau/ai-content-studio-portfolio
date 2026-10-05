import { describe, expect, test } from 'claude-code/testing'
import { bashWrites, isProtected } from '../hooks/paths'

const CWD = '/home/user/ai-content-studio-portfolio'

describe('comandos de shell', () => {
  const barrados = [
    'rm assets/media/who.mp4',
    'rm -rf ./assets',
    'mv assets/media/cha.jpg /tmp/',
    'cp .watermark/out/who.mp4 assets/media/who.mp4',
    'cp -t assets/media .watermark/out/who.jpg',
    'ffmpeg -i in.mp4 -c:v libx264 assets/media/cover.mp4',
    'echo oi > assets/media/x.txt',
    'cat a >> /home/user/ai-content-studio-portfolio/assets/media/x',
    'sed -i s/a/b/ assets/media/x.svg',
    'git checkout -- assets/media/who.mp4',
    'git rm assets/media/old.jpg',
    'find assets -name "*.tmp" -delete',
    'cd assets/media && rm who.mp4',
    'cd scripts; cp x.jpg ../assets/media/',
    'curl -o assets/media/new.jpg https://example.com/a.jpg',
    'bash -c "rm assets/media/who.mp4"',
    'sudo touch assets/media/x',
  ]
  for (const cmd of barrados) {
    test(`barra: ${cmd}`, () => {
      expect(bashWrites(CWD, cmd)).toBeDefined()
    })
  }

  const liberados = [
    'ls -la assets/media',
    'du -h assets/media/*.mp4',
    'ffprobe assets/media/who.mp4',
    'cat assets/media/x.txt > /tmp/copia',
    'cp assets/media/who.jpg .watermark/out/',
    'bash scripts/watermark.sh assets/media/who.mp4',
    'bash scripts/check.sh 2>/dev/null',
    'git diff assets/',
    'git add assets/media/who.mp4',
    'sed -n 1p assets/media/x.txt',
    'ffmpeg -i assets/media/who.mp4 .watermark/out/who.mp4',
    'rm -rf .preview/assets',
    'grep -rn "assets/media" index.html',
  ]
  for (const cmd of liberados) {
    test(`libera: ${cmd}`, () => {
      expect(bashWrites(CWD, cmd)).toBeUndefined()
    })
  }
})

describe('caminhos de Edit e Write', () => {
  test('assets/ na raiz do repositório é protegido', () => {
    expect(isProtected(CWD, 'assets/media/who.jpg')).toBe(true)
    expect(isProtected(CWD, `${CWD}/assets/media/who.jpg`)).toBe(true)
    expect(isProtected(`${CWD}/scripts`, '../assets/media/who.jpg')).toBe(true)
  })
  test('outros lugares não são', () => {
    expect(isProtected(CWD, 'index.html')).toBe(false)
    expect(isProtected(CWD, 'assets-notes.md')).toBe(false)
    expect(isProtected(CWD, '.watermark/out/who.mp4')).toBe(false)
    expect(isProtected(CWD, 'assets/../index.html')).toBe(false)
  })
})

test('limitação conhecida: o que entra pelo pipe no xargs não é visto', () => {
  expect(bashWrites(CWD, 'ls assets | xargs rm')).toBeUndefined()
})

describe('dentro do engine', () => {
  test('sem a pasta da sessão, assets/ relativo continua barrado', async ($, on) => {
    on('tool.call', () => ({ result: {} }) as never)
    const r = await $.tool.call({ tool: 'Edit', file_path: 'assets/media/x.txt', old_string: 'a', new_string: 'b' })
    expect(r.deny).toContain('regra 4')
  })

  test('Edit em assets/ volta como erro e não chega à ferramenta', async ($, on) => {
    on('session.cwd', () => ({ value: CWD }))
    let chegou = 0
    on('tool.call', () => {
      chegou++
      return { result: {} } as never
    })
    const cwd = CWD
    const r = await $.tool.call({ tool: 'Write', file_path: `${cwd}/assets/media/x.txt`, content: 'x' })
    expect(r.deny).toContain('regra 4')
    expect(chegou).toBe(0)
  })

  test('Edit fora de assets/ segue normalmente', async ($, on) => {
    on('session.cwd', () => ({ value: CWD }))
    let chegou = 0
    on('tool.call', () => {
      chegou++
      return { result: {} } as never
    })
    const cwd = CWD
    await $.tool.call({ tool: 'Write', file_path: `${cwd}/index.html`, content: 'x' })
    expect(chegou).toBe(1)
  })

  test('Bash que copia para assets/ é barrado', async ($, on) => {
    on('session.cwd', () => ({ value: CWD }))
    let chegou = 0
    on('tool.call', () => {
      chegou++
      return { result: {} } as never
    })
    on('ui.toast', () => undefined as never)
    const r = await $.tool.call({ tool: 'Bash', command: 'cp .watermark/out/who.mp4 assets/media/who.mp4' })
    expect(r.deny).toContain('regra 4')
    expect(chegou).toBe(0)
  })
})
