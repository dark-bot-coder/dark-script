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

Toda alteração percorre pop/kanban/001_initial_task → … → 006_done, conforme [[WORKFLOW|WORKFLOW]]. Tasks deste repo usam seu kanban e uma worktree em pop/worktrees/<id>/.

Pedido de alteração sem card aciona `new-task` → `advance-task`; “iniciar o fluxo em yolo” materializa/libera a task e percorre a rota yolo inteira, nunca execução direta.

O 002 pertence a planejador separado. Em 004, frente coesa recebe executor direto; DAG, múltiplas skills ou write sets recebem suborquestrador. Em yolo, o 003 só existe para `critical: true` (crítico strong) — as demais tasks yolo transitam 002 → 004 direto; o 005 é o gate único de qualidade (strong, sessão limpa) e verifica primeiro se o pedido original do card foi atendido. Cada gate aceita duas devoluções e ativa circuit breaker na 3ª falha. Tasks independentes avançam em waves de até três; dependência ou overlap serializa. O 006 integra em `develop` e, no fechamento do escopo marcado (task, phase/epoch ou modification), abre automaticamente o PR final para `main`.

## Skills

- **Workflow PoP:** `.agents/skills/` inclui `weekly-review` e `optimize-memory`, além das skills de criação, avanço, specs e crítica yolo.

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

- Nunca executar item (user), trabalhar fora de uma task que chegou legitimamente a `004_processing` (003 aprovado ou yolo não crítico 002→004) ou fazer merge de PR de task.
- Comando humano sobrescreve somente a regra/gate que nomeia; “aplique”, “execute”, “urgente”, “até finalizar” ou “em yolo” não dispensam o fluxo. Só dispensa literal ativa o protocolo de desvio do [[WORKFLOW|WORKFLOW]], sempre com memory e avaliação de specs/DOX.
- Nunca registrar segredos nem credenciais de serviços externos no repo.
- Toda task concluída gera memory/<id>.md e sincroniza specs afetadas.
- Frentes paralelas usam worktrees/branches isoladas; somente o orquestrador valida ownership e integra seus diffs.
