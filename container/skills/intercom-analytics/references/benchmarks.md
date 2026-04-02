# Benchmarks de Referência — CS B2B SaaS

Use estes benchmarks para contextualizar as métricas do cliente e determinar status
(🟢 bom / 🟡 atenção / 🔴 crítico).

Fontes: Zendesk CX Trends, Intercom Customer Support Benchmark Report, HubSpot State of
Customer Service. Valores ajustados para mercado brasileiro onde disponível.

---

## Tempos de Resposta

| Métrica | 🟢 Bom | 🟡 Atenção | 🔴 Crítico |
|---------|--------|-----------|-----------|
| Primeiro reply (chat/WhatsApp) | < 5 min | 5–30 min | > 30 min |
| Primeiro reply (email) | < 4h | 4–24h | > 24h |
| `time_to_admin_reply` geral | < 3.600s (1h) | 3.600–14.400s (1–4h) | > 14.400s |
| `median_time_to_reply` | < 1.800s (30min) | 1.800–7.200s (30min–2h) | > 7.200s |
| `time_to_first_close` | < 86.400s (24h) | 86.400–259.200s (1–3d) | > 259.200s |

---

## Qualidade e Satisfação

| Métrica | 🟢 Bom | 🟡 Atenção | 🔴 Crítico |
|---------|--------|-----------|-----------|
| CSAT médio (1–5) | ≥ 4,3 | 3,8–4,2 | < 3,8 |
| NPS proxy | ≥ +40 | +10 a +39 | < +10 |
| Taxa de resposta ao CSAT | > 25% | 15–25% | < 15% |
| Taxa de reabertura | < 5% | 5–10% | > 10% |
| SLA hit rate | > 90% | 75–90% | < 75% |

---

## Eficiência Operacional

| Métrica | 🟢 Bom | 🟡 Atenção | 🔴 Crítico |
|---------|--------|-----------|-----------|
| Handling time médio | < 1.800s (30min) | 1.800–3.600s (30min–1h) | > 3.600s |
| Razão de tempo ocioso (`idle_ratio`) | < 20% | 20–40% | > 40% |
| Conversas não lidas (backlog) | < 2% do total open | 2–5% | > 5% |
| Média de atribuições por conversa | < 1,5 | 1,5–2,5 | > 2,5 |
| Conversas com 3+ participantes | < 8% | 8–15% | > 15% |

---

## Fin AI e Automação

| Métrica | 🟢 Bom | 🟡 Atenção | 🔴 Crítico |
|---------|--------|-----------|-----------|
| Taxa de deflexão do Fin | > 40% | 20–40% | < 20% |
| `assumed_resolution` rate | > 60% | 40–60% | < 40% |
| `declines_resolution` rate | < 15% | 15–30% | > 30% |
| `unresolved` rate | < 25% | 25–40% | > 40% |
| Fin CSAT vs humano | ≥ humano − 0,3 | humano − 0,3 a − 0,7 | < humano − 0,7 |
| Gaps de conhecimento (sem source) | < 10% respostas | 10–25% | > 25% |

---

## Canais

| Canal | Primeiro reply esperado | CSAT mínimo |
|-------|------------------------|-------------|
| WhatsApp | < 10 min | ≥ 4,2 |
| Chat ao vivo | < 5 min | ≥ 4,3 |
| Email | < 4h | ≥ 4,0 |

---

## Tickets

| Métrica | 🟢 Bom | 🟡 Atenção | 🔴 Crítico |
|---------|--------|-----------|-----------|
| Taxa conversa → ticket | < 5% | 5–15% | > 15% |
| Tickets em `in_progress` > 7 dias | < 10% | 10–20% | > 20% |

---

## Agentes

| Métrica | 🟢 Bom | 🟡 Atenção | 🔴 Crítico |
|---------|--------|-----------|-----------|
| Composite score (0–100) | ≥ 75 | 55–74 | < 55 |
| Índice de profundidade de resposta | > 200 chars | 80–200 chars | < 80 chars |
| Conversas/agente/dia | < 35 | 35–60 | > 60 |

---

## Notas

- Benchmarks de tempo já assumem **horário comercial** (como os campos do Intercom).
- Para mercado brasileiro, considere que WhatsApp tem expectativa de resposta muito mais
  rápida do que email — usuários BR têm baixa tolerância a delays em mensageria instantânea.
- Empresas com plano enterprise/high-MRR devem ter SLAs mais agressivos — idealmente < 1h
  para qualquer canal.
