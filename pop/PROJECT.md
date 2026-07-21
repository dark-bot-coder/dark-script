# Dark Script

- **Categoria:** applications
- **Status:** planejando
- **Prioridade:** alta
- **Criado em:** 2026-07-21
- **Roadmap:** [[ROADMAP|Roadmap]]

## Objetivo

Reunir os scripts de organização externa do Dark Store — utilitários que rodam em servidores próprios e enviam dados à plataforma dark-store — com contratos, operação e envio documentados.

## Contexto

A plataforma Dark Store recebe dados de servidores externos operados por scripts hoje não versionados. Este repo nasce para versioná-los e padronizar como eles se autenticam e enviam dados ao dark-store.

## Harness

- **Branch de PR:** main.
- **Worktree por task:** obrigatória.
- **Tasks críticas:** integrações com pagamentos, dados de clientes e qualquer script que opere contra produção.
- **Stack:** a definir na chegada do primeiro script — registrar então os comandos de verificação no AGENTS.md.

## Decisões

- **2026-07-21:** repo adicionado ao projeto full-multi-repo Dark Store com harness included próprio, ainda sem código além do README.
