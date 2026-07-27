# Dark Script — instruções para agentes

> Projeto gerido pelo workflow do ProjectOfProjects. CLAUDE.md é um symlink deste arquivo — edite sempre este.

- **Type:** included.
- **Idioma do projeto:** pt-BR em documentação, specs, código e comentários.
- **Ficha:** [[PROJECT|PROJECT]]
- **Roadmap:** [[ROADMAP|ROADMAP]] · **Modifications:** [[MODIFICATIONS|MODIFICATIONS]] (criado sob demanda — hotfixes e features emergentes pequenas fora do planejamento)

## Parte de

- **Projeto-mãe:** Dark Store (`categories/applications/dark-store/pop/PROJECT.md` no vault PoP) — siga para decisões e objetivo transversais.
- **Roadmap geral:** `categories/applications/dark-store/pop/ROADMAP.md` no vault PoP — siga para dependências entre repos e sequência das epochs.
- **Kanban cross-repo:** categories/applications/dark-store/pop/kanban/ — use somente quando a task afetar mais de um repo.

> Os três itens acima só resolvem com o repo clonado dentro do vault PoP; num clone standalone, ignore esta seção.

## Repositório

| Repo | URL | Branch de PR |
|------|-----|--------------|
| dark-script | https://github.com/dark-bot-coder/dark-script.git | main |

Scripts de organização externa do Dark Store: rodam em servidores próprios e enviam dados à plataforma dark-store.

## Workflow

Fonte única dos estágios, gates, yolo e papéis: [[WORKFLOW|WORKFLOW]] — *leia antes de criar, avançar ou fechar qualquer task deste repo*. Específico daqui:

- Task de um único repo vive no kanban deste repo (`pop/kanban/`), com uma worktree em `pop/worktrees/<id>/`; task cross-repo vive no kanban da mãe (ver **Parte de**).
- Yolo é herdado do roadmap/modifications: integra em `develop` e, no fechamento do escopo, abre PR `develop` → `main` (branch de PR na tabela **Repositório**).

## Skills

- **Workflow PoP:** `.agents/skills/` inclui `weekly-review` e `optimize-memory`, além das skills de criação, avanço, specs e crítica yolo.
- **Sem skills de UI/design/a11y:** decisão registrada em [[notes/decisions/2026-07-27-skills-de-ui-nao-se-aplicam|2026-07-27]] — *siga antes de propor instalar skill de frontend aqui ou de apontar a ausência delas como drift*.

### Clean code

- `clean-code-change` (`.agents/skills/`) — siga ao **planejar (002) e executar (004)** qualquer task que crie ou altere código.
- `clean-code-review` (`.agents/skills/`) — siga ao **verificar (005)** task de código e como critério de leitura em gate de plano ou PR.
- **Obrigatório:** em 002, toda task que cria/altera código entra com `clean-code-change` na linha **004** e `clean-code-review` na linha **005** da tabela **Skills por etapa** do card.

#### Verificação do projeto

| Verificação | Comando |
|-------------|---------|
| Formatter | — (a definir quando o primeiro script chegar) |
| Linter | — (a definir quando o primeiro script chegar) |
| Testes | — (a definir quando o primeiro script chegar) |

## Regras essenciais

- Regras transversais do vault (itens `(user)`, merge humano, nada fora de 004, comando explícito, desvio sem kanban, memory e specs antes de fechar, ownership de frentes) valem sem cópia aqui: seção **Regras transversais** do [[WORKFLOW|WORKFLOW]] — *siga ao decidir se pode agir sem gate*.
- Conteúdo em pt-BR; datas AAAA-MM-DD; wikilinks internos com gatilho nas seções voltadas a agentes.
- Nunca registrar segredos nem credenciais de serviços externos no repo — os scripts rodam em servidores próprios e falam com a plataforma dark-store.
