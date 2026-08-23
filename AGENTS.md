# Dark Script — instruções para agentes

> Projeto agregado pelo workflow do **ProjectOfProjects (PoP)**. `CLAUDE.md` é um symlink deste arquivo — edite sempre este.

- **Escopo:** este diretório é o escopo inteiro do fluxo — o harness viaja com ele e **nada acima desta raiz faz parte dele** (seção "Escopo corrente" do [[pop/WORKFLOW|WORKFLOW]]).
- **Idioma do projeto:** pt-BR — documentação, specs, código e comentários.
- **Type:** uni-repo — esta pasta **é** o repositório `dark-script`, com o `pop/` inteiro commitado aqui.
- **Ficha:** [[pop/PROJECT|PROJECT]] · **Roadmap:** [[pop/ROADMAP|ROADMAP]] · **Modifications:** [[pop/MODIFICATIONS|MODIFICATIONS]] (hotfixes e features emergentes pequenas fora do planejamento)

## Parte de

- **Projeto-mãe:** Dark Store (`../AGENTS.md`, `projects/dark-store`, type multi-repo) — decisões e objetivo transversais.
- **Roadmap geral:** `../ROADMAP.md` — dependências entre repos e sequência das epochs.
- **Task cross-repo:** não existe kanban central na mãe — fatie a task por repo; cada fatia vive no kanban do repo afetado.

> Os itens acima só resolvem de fora, no escopo que hospeda este repo. **De dentro daqui eles não existem:** este repositório é o escopo inteiro — não siga estes caminhos, não os leia e não relate o que houver neles.

## Repositório

| Repo | URL | Branch de PR |
|------|-----|--------------|
| dark-script | https://github.com/dark-bot-coder/dark-script.git | main |

Scripts de organização externa do Dark Store: rodam em servidores próprios e enviam dados à plataforma dark-store.

## Workflow

- **Principal delegation-first:** o agente principal **sempre delega** a `pop-planner`, `pop-recon`, `pop-execution-orchestrator`, `pop-executor`, `pop-judge-dredd` e `pop-phase-verifier`, salvo execução direta pontual e simples; cada especialista adquire o contexto nos paths do envelope e só o principal integra.
- Task deste repo vive em `pop/kanban/` e executa numa worktree em `pop/worktrees/<id>/`; task cross-repo é fatiada por repo (ver **Parte de**). Yolo é herdado do roadmap/modifications: integra em `develop` e, no fechamento do escopo, abre PR `develop` → `main` (branch de PR na tabela acima); o merge é do humano.
- **Estágios, gates, rota yolo, protocolo de contexto e regras transversais:** [[pop/WORKFLOW|WORKFLOW]] é a fonte única — leia antes de criar, avançar, verificar ou fechar qualquer task; não replique nada dele aqui.

## Skills

- **Workflow do PoP:** `.agents/skills/` inclui `weekly-review` e `optimize-memory`, além das skills de criação, avanço, specs e crítica yolo.
- **Sem skills de UI/design/a11y:** decisão registrada em [[pop/notes/decisions/2026-07-27-skills-de-ui-nao-se-aplicam|2026-07-27]] — *siga antes de propor instalar skill de frontend aqui ou de apontar a ausência delas como drift*.

### Clean code

- `clean-code-change` (`.agents/skills/`) — siga ao **planejar (002) e executar (004)** qualquer task que crie ou altere código; `clean-code-review` — siga ao **verificar (005)** e em gates de plano/PR. **Obrigatório:** task de código entra com as duas nas linhas 004/005 da tabela **Skills por etapa** do card.

#### Verificação do projeto

| Verificação | Comando |
|-------------|---------|
| Formatter | — (a definir quando o primeiro script chegar) |
| Linter | — (a definir quando o primeiro script chegar) |
| Testes | — (a definir quando o primeiro script chegar) |

## Regras essenciais

- Nunca executar item `(user)`, marcar `- [ ] Feito`, trabalhar fora de task legitimamente em 004_processing ou fazer merge de PR de task; comando humano sobrescreve somente a regra que nomeia, sem waiver implícito.
- Conteúdo em pt-BR; datas AAAA-MM-DD; wikilinks internos com gatilho nas seções voltadas a agentes.
- Nunca registrar segredos nem credenciais de serviços externos no repo — os scripts rodam em servidores próprios e falam com a plataforma dark-store.
