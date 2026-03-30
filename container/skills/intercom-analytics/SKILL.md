---
name: intercom-analytics
description: >
  Comprehensive Intercom customer service analytics skill. Use this skill whenever the user asks
  to analyze Intercom data, generate a customer service report, understand support performance,
  evaluate Fin AI effectiveness, measure CSAT, investigate ticket trends, or extract any insight
  from Intercom conversations and contacts. Also triggers for phrases like "relatório do Intercom",
  "análise do suporte", "desempenho da equipe de CS", "efetividade do Fin", or any request to
  understand what is happening in customer service operations. Always use this skill when Intercom
  MCP is connected and the user wants insights from support data — even if they phrase it casually
  like "o que está acontecendo no suporte?" or "me dê um panorama do atendimento".
compatibility:
  mcp_servers:
    - name: Intercom
      url: https://mcp.intercom.com/mcp
      required: true
---

# Intercom Analytics Expert

Você é um especialista em análise de dados de atendimento ao cliente com profundo conhecimento
do ecossistema Intercom. Seu objetivo é coletar dados via Intercom MCP, realizar análises
abrangentes em todas as dimensões disponíveis e produzir um relatório executivo completo em
**Português do Brasil**, com achados concretos e recomendações objetivas e acionáveis.

---

## Fluxo de Execução

Siga estas etapas em ordem. Não pule etapas. Informe o usuário sobre o progresso a cada fase.

### Fase 1 — Coleta de Parâmetros

Antes de iniciar qualquer coleta, confirme com o usuário:

1. **Período de análise** — padrão: últimos 30 dias. Aceita: "última semana", "último trimestre",
   datas específicas, ou "tudo disponível".
2. **Filtros opcionais** — time específico, canal (WhatsApp/email/chat), tag, segmento de cliente.
3. **Foco prioritário** — se o usuário quer ênfase em algum domínio (ex: "foca no Fin AI" ou
   "quero entender o CSAT").

Se o usuário disser "pode ir" ou similar, use os defaults (30 dias, sem filtros, todos os domínios).

---

### Fase 2 — Coleta de Dados

Execute as coletas abaixo em paralelo onde possível. Para cada ferramenta MCP, pagine
completamente usando `starting_after` até que não haja mais resultados. **Limite máximo por
query: 150 resultados por página.**

Consulte `references/mcp-queries.md` para os parâmetros exatos de cada query MCP.
Consulte `references/field-catalog.md` para o mapeamento completo de campos por objeto.

#### 2A — Conversas (bulk metadata)
Coletar via `search_conversations` com os seguintes filtros temporais e de estado:
- Estado `open` — backlog atual
- Estado `closed` — resolvidas no período
- Estado `snoozed` — em espera
- Incluir campos de `statistics` para todos

#### 2B — Conversas com detalhes completos (amostra)
Para análises de conteúdo (NLP, tópicos, qualidade de resposta), usar `get_conversation`
em uma amostra representativa. Priorizar:
- Conversas com `conversation_rating` preenchido (100% de cobertura se viável)
- Conversas onde `ai_agent_participated = true`
- Conversas com `count_reopens > 0`
- Conversas com `sla_applied.sla_status = "missed"`
- Amostra aleatória das demais (mínimo 50, ideal 200)

#### 2C — Contatos
Usar `search_contacts` para obter perfis dos contatos mais ativos no período.
Enriquecer com `get_contact` para campos de localização, dispositivo e atividade.

#### 2D — Tickets
Usar `search` com `object_type:tickets` para coletar tickets vinculados a conversas do período.

---

### Fase 3 — Processamento e Análise

Execute todas as análises abaixo. Para cada domínio, calcule as métricas especificadas e
registre os achados. Consulte `references/analysis-specs.md` para fórmulas e critérios de
classificação detalhados.

**Regra geral de análise:** Sempre que uma métrica estiver fora dos benchmarks de referência
(listados em `references/benchmarks.md`), marque como achado relevante e gere uma recomendação.

#### Domínio 1 — Performance Operacional e SLA
- Taxa de SLA hit/missed/cancelled por `sla_applied.sla_name`
- Distribuição de `statistics.time_to_admin_reply` (mediana, média, p90)
- `statistics.median_time_to_reply` — responsividade contínua
- `statistics.handling_time` vs `statistics.adjusted_handling_time` — razão de tempo ocioso
- `statistics.count_reopens` — taxa de reabertura por agente e canal
- Backlog ativo: conversas abertas com `waiting_since` há mais de X horas
- Conversas não lidas (`read = false`) por time
- Distribuição `priority` vs `not_priority` e seus tempos médios de resposta
- Conversas "snoozed" com `snoozed_until` > 7 dias (possível abuso de snooze)

#### Domínio 2 — Satisfação do Cliente (CSAT)
- Distribuição de `conversation_rating.rating` (1–5) — porcentagem por nota
- NPS proxy: % nota 4–5 (promotores) vs % nota 1–2 (detratores)
- Análise qualitativa de `conversation_rating.remark` — clustering de temas em PT-BR
- Correlação: `rating` vs `statistics.time_to_admin_reply`
- Correlação: `rating` vs `statistics.count_reopens`
- CSAT por agente via `conversation_rating.teammate`
- CSAT por canal via `source.type`
- CSAT do Fin AI: `ai_agent.rating` vs CSAT humano — comparativo

#### Domínio 3 — Fin AI e Automação
- Taxa de participação do Fin: % conversas com `ai_agent_participated = true`
- Taxa de deflexão total: Fin participou + fechado sem `count_assignments > 0`
- Breakdown de `ai_agent.resolution_state`:
  - `assumed_resolution` — Fin assumiu resolução
  - `declines_resolution` — cliente recusou resolução do Fin
  - `unresolved` — Fin não resolveu
- `ai_agent.last_answer_type` — proporção de respostas geradas por IA vs outras
- `ai_agent.source_title` — quais workflows disparam o Fin com mais frequência
- `ai_agent.content_sources` — artigos mais utilizados pelo Fin; tópicos sem fonte = gap de conhecimento
- Taxa de escalação humana pós-Fin: conversas onde Fin participou mas `first_assignment_at` existe
- Deflexão por canal: taxa de resolução autônoma do Fin por `source.type`

#### Domínio 4 — Canais e Fontes
- Volume por `source.type` (WhatsApp, email, chat, etc.)
- `source.delivered_as` — iniciado pelo operador vs pelo cliente
- Tempo médio de resolução por canal
- CSAT médio por canal
- Conversas com `teammates` > 2 participantes — conversas de handoff complexo
- Dispositivos: `contact.os`, `contact.android_device`, `contact.ios_device` — plataformas gerando mais tickets
- Análise de `source.author.email` domain / `company.name` — contas B2B com maior volume

#### Domínio 5 — Tickets
- Volume por `ticket.category` (Customer, Back-office, Tracker)
- Distribuição de `ticket.ticket_state.internal_label` — onde os tickets empacam
- Taxa de conversão conversa → ticket: % conversas com `linked_objects` apontando para ticket
- `ticket.ticket_type.name` — tipos de ticket mais comuns
- Padrões em `ticket.ticket_attributes._default_title_` — títulos recorrentes = problemas sistêmicos

#### Domínio 6 — Conteúdo e NLP (Português)
- Intenção via `first_contact_reply` — classificar por tema sem buscar thread completa
- Clustering de tópicos: analisar `source.body` e `conversation_parts[].body`
  Categorias sugeridas: cobrança/faturamento, bug técnico, onboarding, cancelamento,
  dúvida de produto, elogio, solicitação de feature, outros
- Palavras-chave mais frequentes em mensagens de clientes
- Detecção de `contact.browser_language` ≠ `pt-BR` — clientes em outro idioma
- Pico de sentimento negativo: volume de mensagens com frustração por semana
- Frases de churn: "quero cancelar", "vou cancelar", "pensando em sair", "muito caro"
- Frases de feature request: "seria ótimo se", "falta", "vocês poderiam", "quando vai ter"

#### Domínio 7 — Inteligência de Contatos e Clientes
- Distribuição geográfica: `contact.location.region` — estados brasileiros
- `contact.has_hard_bounced` / `marked_email_as_spam` — contatos com email quebrado
- Correlação: `contact.last_seen_at` vs volume de tickets — usuários ativos geram mais suporte?
- Segmentação por `contact.custom_attributes` — plano, MRR, indústria
- `contact.owner_id` — CSMs com maior volume de clientes com tickets abertos
- Contatos de alto volume (5+ tickets no período) — candidatos a suporte proativo
- Contatos dormentes: `last_replied_at` > 90 dias com tickets históricos

#### Domínio 8 — Qualidade e Coaching de Agentes
- Scorecard por agente: CSAT + taxa de reabertura + handling_time + SLA hit rate
  Normalizar por `statistics.count_conversation_parts` (complexidade)
- `statistics.last_closed_by_id` vs `admin_assignee_id` — quem realmente fecha vs quem está atribuído
- `statistics.count_assignments` alto — conversas com muitos handoffs
- `statistics.assigned_team_first_response_time_by_team` — tempo de resposta pós-reatribuição
- Profundidade de resposta: comprimento médio de `conversation_parts[].body` por agente
- Padrões de escalação por agente: temas que cada agente escala com mais frequência

#### Domínio 9 — Inteligência Estratégica e de Produto
- `company.industry` + `company.monthly_spend` + volume de tickets — custo de suporte por segmento
- Tags mais usadas: `tags.tags[].name` — taxonomia de issues aplicada pelo time
- Sinais de churn: conversas com linguagem de cancelamento vinculadas a contas de alto MRR
- `company.plan` vs CSAT — planos premium recebem melhor atendimento?
- `linked_objects` — conversas que viraram tickets: quais temas exigem escalação formal
- Comparação entre `company.size` e `statistics.time_to_admin_reply` — PMEs vs enterprises

---

### Fase 4 — Geração do Relatório

Produza um arquivo `.md` completo com a estrutura abaixo. O relatório deve ser escrito em
**Português do Brasil**, em tom executivo mas acessível. Use dados reais coletados — nunca
invente números.

Consulte `references/report-template.md` para o template completo com instruções de formatação.

**Regras de qualidade do relatório:**
- Todo achado numérico deve citar o campo de origem (ex: `statistics.time_to_admin_reply`)
- Toda recomendação deve ser numerada, objetiva e ter um responsável sugerido (time/papel)
- Usar tabelas para comparações com 3+ itens
- Usar emojis de semáforo (🟢 🟡 🔴) para sinalizar status de cada métrica vs benchmark
- O sumário executivo deve caber em ≤ 300 palavras e destacar os 3–5 achados mais críticos
- Seções sem dados suficientes devem ser indicadas como "Dados insuficientes para análise"
  em vez de omitidas

---

## Notas de Implementação

### Paginação
Sempre paginar completamente. Padrão:
```
while has_more:
    results = search_conversations(starting_after=cursor)
    cursor = results.pages.next.starting_after
    all_results.extend(results.conversations)
```

### Limites práticos
- `get_conversation` busca a thread completa (até 500 parts). Para amostras grandes,
  priorize conversas com CSAT, reabertura ou participação do Fin.
- `statistics` está disponível no resultado de `search_conversations` — não é necessário
  fazer `get_conversation` apenas para métricas de tempo.

### Tratamento de campos nulos
- `conversation_rating` é nulo para conversas sem avaliação — calcule taxas sobre o universo
  de conversas que receberam solicitação de rating quando possível.
- `adjusted_handling_time` pode ser nulo — use `handling_time` como fallback.
- `company` pode ser nulo para contatos sem empresa associada.

### Timezone
- Todos os timestamps da API estão em UTC Unix.
- Para análises temporais (heatmap de horário, pico de volume), converter para BRT (UTC-3).
- Para métricas de SLA já calculadas pelo Intercom (`time_to_admin_reply` etc.), o Intercom
  já subtrai fora do horário comercial — não reconverter.

---

## Referências

- `references/mcp-queries.md` — Parâmetros exatos de cada query MCP
- `references/field-catalog.md` — Catálogo completo de campos por objeto
- `references/analysis-specs.md` — Fórmulas, critérios e classificações por análise
- `references/benchmarks.md` — Benchmarks de referência do setor para CS B2B SaaS
- `references/report-template.md` — Template completo do relatório com formatação
