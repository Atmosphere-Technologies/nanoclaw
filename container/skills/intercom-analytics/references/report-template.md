# Template do Relatório — Intercom Analytics

Use este template para gerar o arquivo `.md` final. Substitua todos os placeholders
`[VALOR]` por dados reais coletados. Nunca deixe placeholders visíveis no relatório final.

---

```markdown
# Relatório de Análise de Atendimento ao Cliente
**Plataforma:** Intercom  
**Período analisado:** [DATA_INICIO] a [DATA_FIM]  
**Gerado em:** [DATA_GERACAO]  
**Total de conversas analisadas:** [TOTAL_CONVERSAS]  
**Total de contatos únicos:** [TOTAL_CONTATOS]

---

## Sumário Executivo

> ≤ 300 palavras. Destaque os 3–5 achados mais críticos. Comece com o mais urgente.
> Use linguagem executiva — sem jargão técnico. Termine com a recomendação mais importante.

[SUMARIO_EXECUTIVO]

**Destaques do período:**
| Indicador | Valor | Status |
|-----------|-------|--------|
| CSAT médio | [VALOR] / 5,0 | [🟢/🟡/🔴] |
| SLA hit rate | [VALOR]% | [🟢/🟡/🔴] |
| Taxa de deflexão do Fin | [VALOR]% | [🟢/🟡/🔴] |
| Tempo médio de resposta | [VALOR] | [🟢/🟡/🔴] |
| Taxa de reabertura | [VALOR]% | [🟢/🟡/🔴] |
| Backlog atual (conversas abertas) | [VALOR] | [🟢/🟡/🔴] |

---

## 1. Performance Operacional e SLA

### 1.1 Conformidade com SLA

| SLA | Conversas | Hit | Missed | Active | Cancelado | Hit Rate |
|-----|-----------|-----|--------|--------|-----------|----------|
| [NOME_SLA] | [N] | [N] | [N] | [N] | [N] | [X]% [🟢/🟡/🔴] |

> Se houver múltiplos SLAs, listar todos. Se nenhum SLA estiver configurado, indicar.

### 1.2 Tempos de Resposta e Resolução

| Métrica | Mediana | Média | P90 | Status |
|---------|---------|-------|-----|--------|
| Tempo até 1ª resposta (`time_to_admin_reply`) | [VALOR] | [VALOR] | [VALOR] | [🟢/🟡/🔴] |
| Mediana de todos os replies (`median_time_to_reply`) | — | [VALOR] | — | [🟢/🟡/🔴] |
| Tempo até 1º fechamento (`time_to_first_close`) | [VALOR] | [VALOR] | [VALOR] | [🟢/🟡/🔴] |
| Handling time | [VALOR] | [VALOR] | — | [🟢/🟡/🔴] |
| Adjusted handling time (ativo) | [VALOR] | [VALOR] | — | [🟢/🟡/🔴] |
| Razão de tempo ocioso | — | [VALOR]% | — | [🟢/🟡/🔴] |

### 1.3 Backlog e Filas

- **Conversas abertas agora:** [N] | Aguardando resposta: [N] | Não lidas: [N]
- **Distribuição por tempo de espera (`waiting_since`):**

| Tempo aguardando | Conversas | % |
|-----------------|-----------|---|
| < 1 hora | [N] | [X]% |
| 1–4 horas | [N] | [X]% |
| 4–24 horas | [N] | [X]% |
| > 24 horas | [N] | [X]% 🔴 |

- **Conversas snoozadas suspeitosamente** (> 7 dias): [N] conversas — [listar IDs se < 5, ou mencionar padrão]

### 1.4 Reabertura

- **Taxa de reabertura geral:** [X]% [🟢/🟡/🔴]
- **Total de reaberturas no período:** [N]
- **Agentes com maior taxa de reabertura:** [LISTA TOP 3]

### 1.5 Distribuição por Prioridade

| Prioridade | Volume | Tempo médio de resposta | CSAT médio |
|-----------|--------|------------------------|-----------|
| Alta (`priority`) | [N] ([X]%) | [VALOR] | [VALOR] |
| Normal (`not_priority`) | [N] ([X]%) | [VALOR] | [VALOR] |

### 1.6 Recomendações — Performance Operacional

[GERAR RECOMENDAÇÕES OBJETIVAS. Use o modelo abaixo para cada uma:]

**Rec. 1.X — [TITULO_CURTO]**  
**Problema:** [o que os dados mostram]  
**Ação:** [o que fazer, em linguagem concreta]  
**Responsável sugerido:** [time/papel]  
**Impacto esperado:** [métrica que vai melhorar e em quanto]

---

## 2. Satisfação do Cliente (CSAT)

### 2.1 Score Geral

- **CSAT médio:** [VALOR] / 5,0 [🟢/🟡/🔴]
- **NPS proxy:** [VALOR] ([X]% promotores − [X]% detratores) [🟢/🟡/🔴]
- **Taxa de resposta ao CSAT:** [X]% ([N] avaliações de [N] elegíveis) [🟢/🟡/🔴]

**Distribuição de notas:**
| Nota | Conversas | % |
|------|-----------|---|
| ⭐⭐⭐⭐⭐ 5 — Excelente | [N] | [X]% |
| ⭐⭐⭐⭐ 4 — Bom | [N] | [X]% |
| ⭐⭐⭐ 3 — Neutro | [N] | [X]% |
| ⭐⭐ 2 — Ruim | [N] | [X]% |
| ⭐ 1 — Péssimo | [N] | [X]% |

### 2.2 Análise de Feedback Qualitativo

**Temas mais frequentes nos comentários (campo `remark`):**

| Tema | Menções | Nota média | Sentimento |
|------|---------|-----------|-----------|
| [TEMA] | [N] | [VALOR] | [positivo/negativo/neutro] |

> Incluir até 5 temas mais relevantes. Citar 2–3 exemplos de comentários reais
> (anonimizados) que ilustram os temas principais.

**Exemplos representativos:**
- Nota 1: *"[COMENTARIO]"*
- Nota 5: *"[COMENTARIO]"*

### 2.3 CSAT por Agente

| Agente | Avaliações | CSAT | Variação vs. média | Status |
|--------|-----------|------|-------------------|--------|
| [NOME] | [N] | [VALOR] | [+/-X] | [🟢/🟡/🔴] |

> Apenas agentes com ≥ 5 avaliações. Ordenar por CSAT crescente (piores primeiro).

### 2.4 CSAT por Canal

| Canal | Avaliações | CSAT | Status |
|-------|-----------|------|--------|
| [CANAL] | [N] | [VALOR] | [🟢/🟡/🔴] |

### 2.5 Correlação CSAT × Tempo de Resposta

| Tempo de resposta | CSAT médio | N conversas |
|------------------|-----------|------------|
| < 1 hora | [VALOR] | [N] |
| 1–4 horas | [VALOR] | [N] |
| 4–24 horas | [VALOR] | [N] |
| > 24 horas | [VALOR] | [N] |

> Comentar se a correlação é forte (queda ≥ 0,5 por bucket) ou fraca.

### 2.6 Fin AI CSAT vs. Humano

| Contexto | CSAT médio | N avaliações |
|---------|-----------|-------------|
| Atendimento 100% humano | [VALOR] | [N] |
| Fin sem escalação | [VALOR] | [N] |
| Fin com escalação humana | [VALOR] | [N] |

### 2.7 Recomendações — CSAT

[RECOMENDAÇÕES NO MESMO FORMATO DA SEÇÃO 1.6]

---

## 3. Fin AI e Automação

### 3.1 Cobertura e Participação

- **Conversas com participação do Fin:** [N] ([X]% do total) [🟢/🟡/🔴]
- **Taxa de deflexão completa (sem toque humano):** [X]% [🟢/🟡/🔴]
- **Taxa de escalação humana pós-Fin:** [X]%

### 3.2 Efetividade do Fin

| Estado de resolução | Conversas | % |
|--------------------|-----------|---|
| `assumed_resolution` — Resolvido pelo Fin | [N] | [X]% [🟢/🟡/🔴] |
| `declines_resolution` — Cliente recusou | [N] | [X]% [🟢/🟡/🔴] |
| `unresolved` — Fin não resolveu | [N] | [X]% [🟢/🟡/🔴] |

### 3.3 Workflows Mais Ativados

| Workflow (`source_title`) | Ativações | Deflexão | CSAT Fin |
|--------------------------|-----------|----------|---------|
| [NOME] | [N] | [X]% | [VALOR] |

### 3.4 Gaps na Base de Conhecimento

- **Respostas do Fin sem artigo de referência:** [N] ([X]%) [🟢/🟡/🔴]

**Tópicos com maior gap (sem fonte de conhecimento):**
1. [TOPICO] — [N] ocorrências
2. [TOPICO] — [N] ocorrências
3. [TOPICO] — [N] ocorrências

> Esses tópicos são candidatos prioritários para criação de novos artigos na base de conhecimento.

### 3.5 Efetividade por Canal

| Canal | Participação Fin | Deflexão | CSAT Fin |
|-------|-----------------|---------|---------|
| [CANAL] | [X]% | [X]% | [VALOR] |

### 3.6 Recomendações — Fin AI

[RECOMENDAÇÕES NO MESMO FORMATO]

---

## 4. Canais e Fontes

### 4.1 Volume por Canal

| Canal | Conversas | % | Tempo resp. médio | CSAT | Deflexão Fin |
|-------|-----------|---|------------------|------|-------------|
| [CANAL] | [N] | [X]% | [VALOR] | [VALOR] | [X]% |

### 4.2 Iniciativa de Contato

- **Iniciado pelo cliente:** [N] ([X]%)
- **Iniciado pelo operador/automação:** [N] ([X]%)

### 4.3 Handoffs Complexos

- **Conversas com 3+ participantes (`teammates`):** [N] ([X]%) [🟢/🟡/🔴]
- **Média de atribuições por conversa:** [VALOR] [🟢/🟡/🔴]

### 4.4 Plataformas e Dispositivos

| Plataforma/OS | Contatos | Tickets por contato | CSAT médio |
|--------------|---------|--------------------|-----------| 
| [PLATAFORMA] | [N] | [VALOR] | [VALOR] |

### 4.5 Top Contas B2B por Volume

| Empresa | Setor | MRR | Tickets | CSAT | Status |
|---------|-------|-----|---------|------|--------|
| [EMPRESA] | [SETOR] | R$ [VALOR] | [N] | [VALOR] | [🟢/🟡/🔴] |

### 4.6 Recomendações — Canais

[RECOMENDAÇÕES NO MESMO FORMATO]

---

## 5. Tickets

### 5.1 Volume e Distribuição

- **Total de tickets no período:** [N]
- **Taxa de conversão conversa → ticket:** [X]% [🟢/🟡/🔴]

| Categoria | Tickets | % | Tempo médio de resolução |
|-----------|---------|---|-------------------------|
| Customer | [N] | [X]% | [VALOR] |
| Back-office | [N] | [X]% | [VALOR] |
| Tracker | [N] | [X]% | [VALOR] |

### 5.2 Estado dos Tickets

| Estado interno | Tickets | % | Média de dias no estado |
|--------------|---------|---|------------------------|
| [ESTADO] | [N] | [X]% | [VALOR] |

> Destacar tickets parados há > 7 dias em `in_progress`.

### 5.3 Tipos Mais Comuns

| Tipo de ticket | Volume | Temas recorrentes nos títulos |
|---------------|--------|-------------------------------|
| [TIPO] | [N] | [TEMAS] |

### 5.4 Recomendações — Tickets

[RECOMENDAÇÕES NO MESMO FORMATO]

---

## 6. Conteúdo e Tópicos (Análise NLP)

### 6.1 Distribuição de Intenção no Primeiro Contato

| Categoria | Conversas | % |
|-----------|-----------|---|
| Cobrança / Faturamento | [N] | [X]% |
| Bug técnico | [N] | [X]% |
| Onboarding / Dúvida de produto | [N] | [X]% |
| Cancelamento / Churn | [N] | [X]% |
| Feature request | [N] | [X]% |
| Elogio | [N] | [X]% |
| Outros | [N] | [X]% |

### 6.2 Sinais de Churn

- **Conversas com linguagem de cancelamento:** [N] ([X]% do total)
- **Valor de MRR em risco (contas com sinal de churn):** R$ [VALOR]

**Contas com maior risco:**
| Empresa | MRR | Conversas de churn | Último contato |
|---------|-----|--------------------|---------------|
| [EMPRESA] | R$ [VALOR] | [N] | [DATA] |

### 6.3 Solicitações de Feature

- **Total identificado:** [N] solicitações de [N] contatos únicos

**Top solicitações:**
1. "[TEMA]" — [N] menções
2. "[TEMA]" — [N] menções
3. "[TEMA]" — [N] menções

### 6.4 Idioma e Localização

- **Clientes com `browser_language` ≠ pt-BR:** [N] ([X]%)
- **Principais idiomas:** [LISTA]
- **Conversas em idioma diferente do configurado:** [N]

### 6.5 Recomendações — Conteúdo e NLP

[RECOMENDAÇÕES NO MESMO FORMATO]

---

## 7. Inteligência de Contatos e Clientes

### 7.1 Distribuição Geográfica (Brasil)

| Estado/Região | Contatos | Tickets | CSAT médio |
|--------------|---------|---------|-----------|
| [ESTADO] | [N] | [N] | [VALOR] |

### 7.2 Saúde de Email

- **Contatos com bounce permanente (`has_hard_bounced`):** [N] ([X]%)
- **Contatos que marcaram como spam:** [N] ([X]%)
- **Contatos desinscrito de emails:** [N] ([X]%)
- **Impacto:** [N]% da base não pode ser contactada por email → dependência de WhatsApp/chat

### 7.3 Engajamento e Suporte

- **Correlação atividade no produto × tickets:** [DESCREVER — correlação positiva/negativa/neutra]
- **Contatos de alto volume (≥ 5 tickets):** [N] contatos — candidatos a suporte proativo

### 7.4 Segmentação por Plano/MRR

| Segmento | Contatos | Tickets/contato | CSAT | SLA hit |
|---------|---------|----------------|------|---------|
| [SEGMENTO] | [N] | [VALOR] | [VALOR] | [X]% |

### 7.5 CSMs com Maior Carga

| CSM (`owner_id`) | Contas | Tickets abertos | Contas em risco |
|-----------------|--------|----------------|-----------------|
| [NOME] | [N] | [N] | [N] |

### 7.6 Recomendações — Contatos

[RECOMENDAÇÕES NO MESMO FORMATO]

---

## 8. Qualidade e Coaching de Agentes

### 8.1 Scorecard Geral da Equipe

| Agente | Conversas | CSAT | SLA hit | Reabertura | Handling time | Score |
|--------|-----------|------|---------|-----------|--------------|-------|
| [NOME] | [N] | [VALOR] | [X]% | [X]% | [VALOR] | [X]/100 [🟢/🟡/🔴] |

> Ordenar por Score crescente. Incluir apenas agentes com ≥ 10 conversas no período.

### 8.2 Fechamento vs. Atribuição

- **Conversas onde o fechador ≠ atribuído (`last_closed_by_id`):** [N] ([X]%)
- **Implicação:** [comentar se é normal ou indica problema de responsabilidade]

### 8.3 Profundidade de Resposta

| Agente | Chars. médios/resposta | Status |
|--------|----------------------|--------|
| [NOME] | [VALOR] | [🟢/🟡/🔴] |

### 8.4 Handoffs e Escalações

- **Agentes que mais escalaram para outros times:** [LISTA TOP 3]
- **Tópicos que mais geram escalação:** [LISTA TOP 3]

### 8.5 Recomendações — Agentes

[RECOMENDAÇÕES NO MESMO FORMATO]

---

## 9. Inteligência Estratégica e de Produto

### 9.1 Saúde das Contas B2B

| Empresa | Setor | MRR | Tickets | CSAT | Score de saúde |
|---------|-------|-----|---------|------|---------------|
| [EMPRESA] | [SETOR] | R$ [VALOR] | [N] | [VALOR] | [SCORE] [🟢/🟡/🔴] |

### 9.2 Custo de Suporte por Segmento

| Segmento | Tickets | Handling time total | Custo estimado |
|---------|---------|--------------------|--------------| 
| [SEGMENTO] | [N] | [HORAS]h | R$ [VALOR] |

### 9.3 Taxonomia de Issues (via Tags)

| Tag | Volume | % | Tendência vs. mês anterior |
|-----|--------|---|---------------------------|
| [TAG] | [N] | [X]% | [↑/↓/→] |

### 9.4 Recomendações — Estratégia e Produto

[RECOMENDAÇÕES NO MESMO FORMATO]

---

## 10. Plano de Ação Consolidado

Lista unificada de todas as recomendações priorizadas por impacto.

| # | Recomendação | Domínio | Responsável | Urgência | Impacto esperado |
|---|-------------|---------|------------|---------|-----------------|
| 1 | [ACAO] | [DOMINIO] | [RESPONSAVEL] | 🔴 Alta | [IMPACTO] |
| 2 | [ACAO] | [DOMINIO] | [RESPONSAVEL] | 🟡 Média | [IMPACTO] |
| 3 | [ACAO] | [DOMINIO] | [RESPONSAVEL] | 🟢 Baixa | [IMPACTO] |

---

## Apêndice — Metodologia

- **Fonte de dados:** Intercom MCP (API v2.15)
- **Total de conversas analisadas:** [N] (bulk metadata via `search_conversations`)
- **Conversas com thread completa analisada:** [N] (amostra via `get_conversation`)
- **Contatos analisados:** [N]
- **Tickets analisados:** [N]
- **Timezone:** Timestamps convertidos para BRT (UTC-3) em análises de volume temporal. Métricas de SLA usam cálculo nativo do Intercom (já exclui fora do horário comercial).
- **Benchmarks:** CS B2B SaaS — Zendesk CX Trends 2024, Intercom Benchmark Report 2024
- **Análise de linguagem:** Classificação de intenção e sentimento via Claude (modelo interno), configurado para Português do Brasil
```
