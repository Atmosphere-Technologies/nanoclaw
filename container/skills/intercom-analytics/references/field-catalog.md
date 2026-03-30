# Catálogo de Campos — Objetos Intercom

Referência completa de todos os campos disponíveis por objeto, com tipo, descrição e
indicação de disponibilidade (search vs. fetch).

---

## Objeto: Conversation

Disponível em `search_conversations` (S) e `get_conversation` (G).

| Campo | Tipo | Disponível | Descrição |
|-------|------|-----------|-----------|
| `id` | string | S+G | ID único da conversa |
| `title` | string\|null | S+G | Título da conversa |
| `created_at` | unix timestamp | S+G | Criação da conversa (UTC) |
| `updated_at` | unix timestamp | S+G | Última atualização (UTC) |
| `waiting_since` | unix timestamp\|null | S+G | Quando o cliente começou a esperar resposta. Null se último reply foi de admin |
| `snoozed_until` | unix timestamp\|null | S+G | Até quando está snoozada |
| `open` | boolean | S+G | true = aberta, false = fechada |
| `state` | enum | S+G | `open` \| `closed` \| `snoozed` |
| `read` | boolean | S+G | Se foi lida por algum admin |
| `priority` | enum | S+G | `priority` \| `not_priority` |
| `admin_assignee_id` | integer\|null | S+G | ID do admin responsável |
| `team_assignee_id` | string\|null | S+G | ID do time responsável |
| `ai_agent_participated` | boolean | S+G | Fin AI participou? |
| `custom_attributes` | object | S+G | Atributos customizados da conversa |

### Sub-objeto: company (diretamente na conversa)
| Campo | Disponível | Descrição |
|-------|-----------|-----------|
| `company.id` | S+G | ID da empresa |
| `company.name` | S+G | Nome da empresa |
| `company.industry` | S+G | Setor |
| `company.monthly_spend` | S+G | MRR da empresa |
| `company.plan.name` | S+G | Plano contratado |
| `company.size` | S+G | Número de funcionários |
| `company.user_count` | S+G | Usuários na plataforma |

### Sub-objeto: source
| Campo | Disponível | Descrição |
|-------|-----------|-----------|
| `source.type` | S+G | Canal: `email` \| `chat` \| `twitter` \| `facebook` \| `api` \| `push` \| `ios` \| `android` \| `web` \| `whatsapp` |
| `source.delivered_as` | S+G | `operator_initiated` \| `customer_initiated` \| `campaigns` |
| `source.subject` | S+G | Assunto (para email) |
| `source.body` | S+G | Corpo da primeira mensagem |
| `source.author.id` | S+G | ID do autor |
| `source.author.name` | S+G | Nome do autor |
| `source.author.email` | S+G | Email do autor |
| `source.url` | S+G | URL de origem |
| `source.redacted` | S+G | Se o conteúdo foi removido |

### Sub-objeto: statistics
| Campo | Disponível | Descrição |
|-------|-----------|-----------|
| `statistics.time_to_assignment` | S+G | Segundos até primeira atribuição (exclui fora do horário) |
| `statistics.time_to_admin_reply` | S+G | Segundos até primeira resposta de admin (exclui fora do horário) |
| `statistics.time_to_first_close` | S+G | Segundos até primeiro fechamento (exclui fora do horário) |
| `statistics.time_to_last_close` | S+G | Segundos até último fechamento (exclui fora do horário) |
| `statistics.median_time_to_reply` | S+G | Mediana de todos os tempos de resposta de admin |
| `statistics.handling_time` | S+G | Tempo da atribuição ao fechamento em segundos |
| `statistics.adjusted_handling_time` | S+G | Tempo ativo (exclui períodos ociosos). Pode ser null |
| `statistics.first_contact_reply_at` | S+G | Timestamp da primeira mensagem do cliente |
| `statistics.first_assignment_at` | S+G | Timestamp da primeira atribuição |
| `statistics.first_admin_reply_at` | S+G | Timestamp da primeira resposta de admin |
| `statistics.first_close_at` | S+G | Timestamp do primeiro fechamento |
| `statistics.last_assignment_at` | S+G | Timestamp da última atribuição |
| `statistics.last_assignment_admin_reply_at` | S+G | Primeiro reply após a atribuição mais recente |
| `statistics.last_contact_reply_at` | S+G | Última mensagem do cliente |
| `statistics.last_admin_reply_at` | S+G | Última resposta de admin |
| `statistics.last_close_at` | S+G | Timestamp do último fechamento |
| `statistics.last_closed_by_id` | S+G | ID do admin que fechou por último |
| `statistics.count_reopens` | S+G | Número de reaberturas |
| `statistics.count_assignments` | S+G | Número total de atribuições |
| `statistics.count_conversation_parts` | S+G | Total de partes na conversa (proxy de complexidade) |
| `statistics.assigned_team_first_response_time_by_team` | G | Array: tempo de resposta por time (para conversas multi-time) |
| `statistics.assigned_team_first_response_time_in_office_hours` | G | Idem, apenas horário comercial |

### Sub-objeto: conversation_rating
Disponível apenas em `get_conversation` para conversas avaliadas.
| Campo | Descrição |
|-------|-----------|
| `conversation_rating.rating` | Nota 1–5 |
| `conversation_rating.remark` | Texto livre do feedback |
| `conversation_rating.created_at` | Quando a avaliação foi feita |
| `conversation_rating.contact.id` | Quem avaliou |
| `conversation_rating.teammate.id` | Qual admin foi avaliado |

### Sub-objeto: ai_agent
Disponível apenas em `get_conversation` quando `ai_agent_participated = true`.
| Campo | Descrição |
|-------|-----------|
| `ai_agent.source_type` | Tipo de fonte: `workflow` ou outros |
| `ai_agent.source_title` | Nome do workflow que ativou o Fin |
| `ai_agent.last_answer_type` | `ai_answer` \| outros |
| `ai_agent.resolution_state` | `assumed_resolution` \| `declines_resolution` \| `unresolved` |
| `ai_agent.rating` | Nota 1–5 dada especificamente ao Fin |
| `ai_agent.rating_remark` | Texto do feedback sobre o Fin |
| `ai_agent.content_sources` | Artigos da base de conhecimento usados pelo Fin |
| `ai_agent.created_at` | Quando o Fin entrou na conversa |
| `ai_agent.updated_at` | Última atualização do registro do Fin |

### Sub-objeto: sla_applied
| Campo | Descrição |
|-------|-----------|
| `sla_applied.sla_name` | Nome do SLA aplicado |
| `sla_applied.sla_status` | `hit` \| `missed` \| `cancelled` \| `active` |

### Sub-objeto: first_contact_reply
| Campo | Descrição |
|-------|-----------|
| `first_contact_reply.created_at` | Timestamp do primeiro contato |
| `first_contact_reply.type` | Tipo do primeiro contato |
| `first_contact_reply.url` | URL de origem |

### Sub-objetos: tags, teammates, linked_objects
| Campo | Descrição |
|-------|-----------|
| `tags.tags[].name` | Nomes das tags aplicadas |
| `tags.tags[].id` | IDs das tags |
| `teammates[].id` | IDs de todos os admins que participaram |
| `teammates[].name` | Nomes dos participantes |
| `linked_objects.data[].id` | IDs de tickets vinculados |
| `linked_objects.data[].type` | `ticket` \| `conversation` |

### conversation_parts (apenas get_conversation)
| Campo | Descrição |
|-------|-----------|
| `conversation_parts[].id` | ID da parte |
| `conversation_parts[].part_type` | Tipo: `comment` \| `note` \| `activity` \| outros |
| `conversation_parts[].body` | Texto da mensagem |
| `conversation_parts[].created_at` | Timestamp |
| `conversation_parts[].author.id` | ID do autor |
| `conversation_parts[].author.type` | `admin` \| `user` \| `bot` |
| `conversation_parts[].author.name` | Nome do autor |
| `conversation_parts[].author.from_ai_agent` | Parte enviada pelo AI Agent? |
| `conversation_parts[].author.is_ai_answer` | Resposta gerada pelo AI? |

---

## Objeto: Contact

Disponível em `search_contacts` (S) e `get_contact` (G).

| Campo | Disponível | Descrição |
|-------|-----------|-----------|
| `id` | S+G | ID único |
| `external_id` | S+G | ID no sistema do cliente |
| `role` | S+G | `user` \| `lead` |
| `email` | S+G | Email |
| `email_domain` | S+G | Domínio do email |
| `phone` | S+G | Telefone |
| `name` | S+G | Nome |
| `owner_id` | S+G | ID do CSM/admin responsável |
| `has_hard_bounced` | S+G | Email com bounce permanente? |
| `marked_email_as_spam` | S+G | Marcou email como spam? |
| `unsubscribed_from_emails` | S+G | Desinscrito de emails? |
| `created_at` | S+G | Criação do contato |
| `signed_up_at` | S+G | Cadastro na plataforma |
| `last_seen_at` | S+G | Última vez visto no produto |
| `last_replied_at` | S+G | Última mensagem enviada ao suporte |
| `last_contacted_at` | S+G | Última vez que recebeu mensagem |
| `last_email_opened_at` | S+G | Último email aberto |
| `last_email_clicked_at` | S+G | Último clique em email |
| `language_override` | S+G | Idioma preferido configurado |
| `browser` | S+G | Navegador |
| `browser_version` | S+G | Versão do navegador |
| `browser_language` | S+G | Idioma do navegador (ex: `pt-BR`) |
| `os` | S+G | Sistema operacional |
| `android_app_name` | S+G | Nome do app Android |
| `android_app_version` | S+G | Versão do app Android |
| `android_device` | S+G | Dispositivo Android |
| `android_os_version` | S+G | Versão do Android |
| `android_last_seen_at` | S+G | Último uso no Android |
| `ios_app_name` | S+G | Nome do app iOS |
| `ios_app_version` | S+G | Versão do app iOS |
| `ios_device` | S+G | Dispositivo iOS |
| `ios_os_version` | S+G | Versão do iOS |
| `ios_last_seen_at` | S+G | Último uso no iOS |
| `custom_attributes` | S+G | Atributos customizados (plano, MRR, etc.) |
| `location.country` | G | País |
| `location.region` | G | Estado/região |
| `location.city` | G | Cidade |
| `tags.data[].name` | G | Tags aplicadas ao contato |
| `companies.data[].id` | G | Empresas vinculadas |
| `social_profiles.data` | G | Perfis em redes sociais |

---

## Objeto: Ticket

Disponível via `search` DSL.

| Campo | Descrição |
|-------|-----------|
| `id` | ID único |
| `ticket_id` | ID exibido no Inbox |
| `category` | `Customer` \| `Back-office` \| `Tracker` |
| `ticket_attributes._default_title_` | Título do ticket |
| `ticket_attributes._default_description_` | Descrição |
| `ticket_state.category` | Estado: `submitted` \| `in_progress` \| `waiting_on_customer` \| `resolved` |
| `ticket_state.internal_label` | Label interno (ex: "Com time de Dev") |
| `ticket_state.external_label` | Label visível ao cliente |
| `ticket_type.name` | Tipo (ex: "Bug", "Solicitação") |
| `admin_assignee_id` | Admin responsável |
| `team_assignee_id` | Time responsável |
| `created_at` | Criação |
| `updated_at` | Última atualização |
| `open` | Aberto? |
| `snoozed_until` | Snoozado até |
| `linked_objects.data` | Conversas vinculadas |
| `is_shared` | Visível ao cliente? |
