// Decide se um caminho ou um comando de shell altera algo dentro de assets/.
// É uma barreira contra engano, não uma sandbox: um script Python que escreve
// em assets/ passa, porque o comando em si não diz para onde ele escreve.

const REPO = 'ai-content-studio-portfolio'

function normalize(path: string): string {
  const out: string[] = []
  for (const part of path.split('/')) {
    if (part === '' || part === '.') continue
    if (part === '..') out.pop()
    else out.push(part)
  }
  return '/' + out.join('/')
}

function resolve(base: string, path: string): string {
  return normalize(path.startsWith('/') ? path : `${base}/${path}`)
}

// assets/ da pasta da sessão, ou o assets/ de qualquer clone deste repositório
// (cobre o caso de o shell ter feito cd para um subdiretório).
export function isProtected(cwd: string, path: string): boolean {
  if (path === '' || path.startsWith('~') || path.startsWith('-')) return false
  const abs = resolve(cwd, path)
  const root = normalize(`${cwd}/assets`)
  if (abs === root || abs.startsWith(root + '/')) return true
  return abs.endsWith(`/${REPO}/assets`) || abs.includes(`/${REPO}/assets/`)
}

// Comandos que alteram qualquer caminho que recebem.
const WRITES_ANY = new Set([
  'rm', 'rmdir', 'mv', 'touch', 'truncate', 'shred', 'chmod', 'chown',
  'ln', 'mkdir', 'unlink', 'tee',
])
// Comandos cujo último argumento é o destino.
const WRITES_LAST = new Set(['cp', 'rsync', 'install', 'scp', 'ffmpeg', 'convert', 'magick'])
// Subcomandos do git que reescrevem arquivos do disco.
const GIT_WRITES = new Set(['rm', 'mv', 'checkout', 'restore', 'clean'])
// Opções cujo valor seguinte é um arquivo de saída (curl -o, wget -O, sort -o, cp -t...).
const OUTPUT_FLAGS = new Set(['-o', '-O', '--output', '-t', '--target-directory'])
// Prefixos que não mudam qual é o comando de verdade.
const PREFIXES = new Set(['sudo', 'env', 'time', 'nohup', 'command', 'exec', 'xargs'])

const REDIRECT = /(?:\d|&)?>>?\|?\s*([^\s;&|<>]+)/g

function words(segment: string): string[] {
  return segment
    .replace(REDIRECT, ' ')
    .split(/\s+/)
    .map(w => w.replace(/^['"]+|['"]+$/g, ''))
    .filter(w => w !== '')
}

// Devolve o trecho do comando que alteraria assets/, ou undefined.
export function bashWrites(cwd: string, command: string): string | undefined {
  let base = cwd
  for (const raw of command.split(/&&|\|\||[;|\n]/)) {
    const segment = raw.trim()
    if (segment === '') continue

    for (const m of segment.matchAll(REDIRECT)) {
      if (m[1] !== undefined && isProtected(base, m[1].replace(/^['"]|['"]$/g, ''))) return segment
    }

    const w = words(segment)
    while (w.length > 0 && (PREFIXES.has(w[0]!) || /^[A-Za-z_]\w*=/.test(w[0]!) || w[0]!.startsWith('-'))) {
      w.shift()
    }
    const verb = w[0]
    if (verb === undefined) continue
    const args = w.slice(1)
    const hits = (list: string[]) => list.some(a => isProtected(base, a.replace(/^of=/, '')))

    if (verb === 'cd' || verb === 'pushd') {
      const target = args[0]
      if (target !== undefined && !target.startsWith('~') && target !== '-') base = resolve(base, target)
      continue
    }
    if ((verb === 'bash' || verb === 'sh' || verb === 'zsh') && args[0] === '-c') {
      const inner = bashWrites(base, args.slice(1).join(' '))
      if (inner !== undefined) return inner
      continue
    }

    const paths = args.filter(a => !a.startsWith('-'))
    let writes = false
    if (WRITES_ANY.has(verb)) writes = hits(paths)
    else if (WRITES_LAST.has(verb)) writes = paths.length > 0 && hits(paths.slice(-1))
    else if (verb === 'sed') writes = args.some(a => /^-[a-zA-Z]*i|^--in-place/.test(a)) && hits(paths)
    else if (verb === 'perl') writes = args.some(a => /^-[a-zA-Z]*i/.test(a)) && hits(paths)
    else if (verb === 'git') writes = GIT_WRITES.has(args[0] ?? '') && hits(args.slice(1))
    else if (verb === 'find') {
      const exec = args.findIndex(a => a === '-exec' || a === '-execdir')
      const execVerb = exec >= 0 ? args[exec + 1] : undefined
      const destroys = args.includes('-delete') || (execVerb !== undefined && WRITES_ANY.has(execVerb))
      writes = destroys && hits(paths)
    } else if (verb === 'dd') writes = hits(args.filter(a => a.startsWith('of=')))
    if (writes) return segment

    for (let i = 0; i < args.length - 1; i++) {
      if (OUTPUT_FLAGS.has(args[i]!) && isProtected(base, args[i + 1]!)) return segment
    }
  }
  return undefined
}
