# Especificações de Análise

Fórmulas, critérios de classificação e regras de cálculo para cada análise do skill.

---

## Domínio 1 — Performance Operacional e SLA

### Taxa de SLA
```
sla_hit_rate = count(sla_status == "hit") / count(sla_status IN ["hit","missed"]) * 100
sla_miss_rate = count(sla_status == "missed") / count(sla_status IN ["hit","missed"]) * 100
```
Excluir `cancelled` do denominador (SLA foi removido manualmente — não conta).
Separar por `sla_name` quando houver múltiplos SLAs.

### Tempos de resposta (em segundos → converter para exibição)
Converter segundos para formato legível:
- < 3600s → exibir em minutos (ex: "47 min")
- >= 3600s → exibir em horas e minutos (ex: "2h 15min")
- >= 86400s → exibir em dias e horas (ex: "1d 3h")

Calcular por conjunto de conversas:
```
mediana = percentile(50, time_to_admin_reply values)
media   = mean(time_to_admin_reply values)
p90     = percentile(90, time_to_admin_reply values)  # 90% das conversas respondidas em X
```

### Taxa de tempo ocioso
```
idle_ratio = (handling_time - adjusted_handling_time) / handling_time * 100
```
Se `adjusted_handling_time` for null, pular o cálculo para essa conversa.
`idle_ratio > 40%` = sinal de alerta (agente distraído ou conversa abandonada).

### Taxa de reabertura
```
reopen_rate = count(count_reopens > 0) / total_closed * 100
```
Por agente: filtrar conversas por `last_closed_by_id`.

### Backlog de espera atual
```
waiting_queue = conversas onde state == "open" AND waiting_since != null
waiting_hours = (now() - waiting_since) / 3600
```
Buckets: < 1h | 1–4h | 4–24h | > 24h

### Abuso de snooze
```
snooze_abuse = conversas onde snoozed_until > (now() + 7*86400)
```

---

## Domínio 2 — CSAT

### Score CSAT padrão
```
csat_score = mean(conversation_rating.rating para todas conversas avaliadas)
```

### NPS proxy
```
promoters    = count(rating IN [4,5]) / total_rated * 100
detractors   = count(rating IN [1,2]) / total_rated * 100
nps_proxy    = promoters - detractors
```

### Taxa de resposta ao CSAT
```
csat_response_rate = count(conversation_rating != null) / total_closed * 100
```
Taxa < 15% indica que a solicitação de avaliação não está sendo enviada corretamente.

### Correlação tempo de resposta × CSAT
Agrupar conversas em buckets de `time_to_admin_reply`:
- Bucket 1: < 1h
- Bucket 2: 1–4h
- Bucket 3: 4–24h
- Bucket 4: > 24h

Calcular CSAT médio por bucket. Queda de ≥ 0.5 pontos entre buckets consecutivos = correlação forte.

### CSAT por agente
```
agent_csat = mean(rating) filtrado por conversation_rating.teammate.id == admin_id
agent_volume = count(conversas avaliadas) por admin
```
Apenas incluir agentes com ≥ 5 avaliações (volume mínimo para significância).

### Comparativo Fin AI vs humano
```
fin_csat   = mean(ai_agent.rating) para conversas com ai_agent_participated == true E ai_agent.rating != null
human_csat = mean(conversation_rating.rating) para conversas sem participação do Fin
mixed_csat = mean(conversation_rating.rating) para conversas com Fin + handoff humano
```

---

## Domínio 3 — Fin AI e Automação

### Taxa de participação
```
fin_participation_rate = count(ai_agent_participated == true) / total_conversations * 100
```

### Taxa de deflexão completa (sem toque humano)
```
full_deflection = conversas onde:
  ai_agent_participated == true
  AND count_assignments == 0
  AND state == "closed"

deflection_rate = full_deflection / count(ai_agent_participated == true) * 100
```

### Breakdown de resolution_state (do Fin)
```
assumed_res_rate = count(ai_agent.resolution_state == "assumed_resolution") / fin_conversations * 100
declined_res_rate = count(ai_agent.resolution_state == "declines_resolution") / fin_conversations * 100
unresolved_rate = count(ai_agent.resolution_state == "unresolved") / fin_conversations * 100
```

### Gap de conhecimento na base de artigos
```
no_source_answers = conversas onde:
  ai_agent.last_answer_type == "ai_answer"
  AND (ai_agent.content_sources == null OR ai_agent.content_sources.sources == [])
```
Esses são tópicos que o Fin respondeu sem embasamento em artigos → risco de alucinação.
Extrair keywords do `source.body` dessas conversas para identificar gaps temáticos.

### Taxa de escalação pós-Fin
```
escalation_rate = conversas onde:
  ai_agent_participated == true
  AND statistics.first_assignment_at != null

rate = escalation_rate / count(ai_agent_participated == true) * 100
```

---

## Domínio 4 — Canais e Fontes

### Volume por canal
```
channel_volume[channel] = count(source.type == channel)
channel_share[channel] = channel_volume[channel] / total * 100
```

### Performance por canal
Para cada `source.type`, calcular:
- `mean(time_to_admin_reply)`
- `mean(time_to_first_close)`
- `mean(handling_time)`
- `mean(conversation_rating.rating)` (onde disponível)
- `count_reopens_rate`
- `fin_deflection_rate`

### Índice de complexidade de handoff
```
complex_handoff = conversas onde len(teammates) > 2
complexity_rate = complex_handoff / total * 100
```

---

## Domínio 6 — Conteúdo e NLP

### Classificação de intenção
Para classificar intenção de `first_contact_reply` e `source.body`, use este prompt ao chamar Claude:

```
Classifique a mensagem abaixo em uma das categorias:
- cobrança_faturamento
- bug_tecnico
- onboarding_duvida
- cancelamento_churn
- feature_request
- elogio
- outros

Mensagem: [BODY]

Responda apenas com o nome da categoria.
```

Acumule as classificações e calcule distribuição percentual.

### Detecção de churn intent
Termos a buscar (case-insensitive, português):
```python
churn_terms = [
  "quero cancelar", "vou cancelar", "cancelamento", "cancela minha conta",
  "pensando em sair", "não quero mais", "vou embora", "trocar de plataforma",
  "muito caro", "não vale a pena", "decepcionado", "pessimo", "péssimo"
]
```

### Detecção de feature request
```python
feature_terms = [
  "seria ótimo se", "faltando", "vocês poderiam", "quando vai ter",
  "precisamos de", "gostaríamos que", "por que não tem", "sugestão",
  "melhoria", "funcionalidade nova"
]
```

---

## Domínio 8 — Qualidade de Agentes

### Scorecard composto por agente
Normalizar cada métrica para escala 0–100, depois calcular média ponderada:

| Métrica | Peso | Cálculo |
|---------|------|---------|
| CSAT médio | 35% | (agent_csat - 1) / 4 * 100 |
| Taxa de SLA hit | 25% | agent_sla_hit_rate |
| Taxa de reabertura inversa | 20% | (1 - reopen_rate) * 100 |
| Velocidade de resposta | 20% | normalizar `time_to_admin_reply` inversamente |

```
composite_score = 0.35 * csat_norm + 0.25 * sla_norm + 0.20 * reopen_norm + 0.20 * speed_norm
```

Para normalizar velocidade: `speed_norm = max(0, 100 - (time_to_admin_reply / target_time * 100))`
onde `target_time` é o SLA definido (padrão: 3600s = 1h).

Apenas incluir agentes com ≥ 10 conversas no período.

### Índice de profundidade de resposta
```
depth_index = mean(len(body) para parts de admin) por agente
```
`len` em caracteres. Benchmark: > 200 chars = resposta elaborada.
Agentes com `depth_index < 80` + CSAT baixo = prioridade de coaching.

---

## Domínio 9 — Inteligência Estratégica

### Custo de suporte por segmento (estimado)
```
# Assumindo custo médio por minuto de agente
cost_per_minute = [definido pelo usuário ou usar R$ 1,50 como padrão]
segment_cost = sum(adjusted_handling_time / 60 * cost_per_minute) por company.industry
```

### Health score de conta B2B
Para cada empresa (agrupada por `company.id`):
```
ticket_volume_score = normalizar(count(conversas)) invertido  # menos tickets = melhor
csat_score_norm     = (mean(rating) - 1) / 4 * 100
reopen_score        = (1 - reopen_rate) * 100
churn_risk          = 1 se tem conversa com churn_intent, 0 se não

account_health = 0.30 * csat_score_norm
               + 0.25 * ticket_volume_score
               + 0.20 * reopen_score
               + 0.25 * (1 - churn_risk) * 100
```

Classificação:
- 80–100: 🟢 Saudável
- 60–79:  🟡 Atenção
- 0–59:   🔴 Em risco
