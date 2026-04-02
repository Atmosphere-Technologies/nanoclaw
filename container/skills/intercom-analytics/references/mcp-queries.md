# MCP Queries Reference

Parâmetros exatos para cada chamada ao Intercom MCP. Use como cookbook durante a Fase 2.

---

## search_conversations

### Conversas fechadas no período (bulk stats)
```json
{
  "state": "closed",
  "per_page": 150,
  "statistics_time_to_admin_reply": ">= 0"
}
```
Paginar com `starting_after` até `pages.next` ausente.

### Conversas abertas (backlog atual)
```json
{
  "state": "open",
  "per_page": 150
}
```

### Conversas snoozed
```json
{
  "state": "snoozed",
  "per_page": 150
}
```

### Conversas com SLA missed
```json
{
  "state": "closed",
  "per_page": 150
}
```
Filtrar em pós-processamento por `sla_applied.sla_status == "missed"`.

### Conversas por time específico
```json
{
  "team_assignee_id": "TEAM_ID",
  "state": "closed",
  "per_page": 150
}
```

### Conversas por agente específico
```json
{
  "admin_assignee_id": 12345,
  "state": "closed",
  "per_page": 150
}
```

### Conversas com alto tempo de resposta (triagem)
```json
{
  "statistics_time_to_admin_reply": ">= 14400",
  "state": "closed",
  "per_page": 150
}
```
`14400` = 4 horas em segundos. Ajuste conforme SLA configurado.

---

## get_conversation

### Conversa completa com todas as parts
```
fetch conversation_{id}
```
Retorna: objeto completo incluindo `conversation_parts`, `ai_agent`, `conversation_rating`,
`statistics`, `sla_applied`, `linked_objects`, `teammates`, `tags`, `company`.

---

## search (DSL universal)

### Conversas por canal
```
object_type:conversations source_type:whatsapp
object_type:conversations source_type:email
object_type:conversations source_type:chat
```

### Conversas com participação do Fin
```
object_type:conversations ai_agent_participated:true
```

### Conversas com avaliação preenchida
```
object_type:conversations conversation_rating_rating:>0
```

### Conversas com churn intent (por palavra-chave)
```
object_type:conversations source_body:contains:"quero cancelar" limit:150
object_type:conversations source_body:contains:"vou cancelar" limit:150
object_type:conversations source_body:contains:"muito caro" limit:150
object_type:conversations source_body:contains:"pensando em sair" limit:150
```

### Conversas com feature request
```
object_type:conversations source_body:contains:"seria ótimo" limit:150
object_type:conversations source_body:contains:"faltando" limit:150
object_type:conversations source_body:contains:"vocês poderiam" limit:150
```

### Conversas com bug report
```
object_type:conversations source_body:contains:"não funciona" limit:150
object_type:conversations source_body:contains:"erro" limit:150
object_type:conversations source_body:contains:"bug" limit:150
```

### Conversas por empresa (domínio de email)
```
object_type:conversations source_author_email:"@empresa.com.br"
```

### Contatos por domínio de email
```
object_type:contacts email_domain:"empresa.com.br"
```

### Conversas não lidas
```
object_type:conversations read:false state:open
```

### Conversas de alta prioridade
```
object_type:conversations priority:priority state:open
```

---

## search_contacts

### Contatos com localização no Brasil
```json
{
  "location": { "country": "Brazil" },
  "per_page": 150
}
```

### Contatos por atributo customizado (ex: plano)
```json
{
  "custom_attributes": { "plan": "enterprise" },
  "per_page": 150
}
```

### Contatos com email com bounce
```json
{
  "has_hard_bounced": true,
  "per_page": 150
}
```

---

## Tickets

### Todos os tickets do período
```
object_type:tickets limit:150
```
Paginar normalmente.

### Tickets por categoria
```
object_type:tickets category:Customer limit:150
object_type:tickets category:Back-office limit:150
object_type:tickets category:Tracker limit:150
```
