# Guia de Configuração: Canal #agent-tech com MCPs de Infraestrutura

## Visão Geral da Arquitetura

A solução usa o mecanismo de **grupos isolados** do NanoClaw: o canal `#agent-tech` no Slack
será registrado como um grupo dedicado. Todo container desse grupo carregará MCPs extras
(PostgreSQL, ClickHouse, GCP, GitHub, Heroku) que **não ficam disponíveis nos demais grupos**.

```
#agent-tech (Slack) → grupo "agent-tech" → container isolado
                                                 ├── MCP: nanoclaw (padrão)
                                                 ├── MCP: postgres
                                                 ├── MCP: clickhouse
                                                 ├── MCP: github
                                                 ├── MCP: gcp
                                                 └── MCP: heroku
```

Os outros canais (WhatsApp, Telegram, demais Slack) continuam rodando seus próprios
containers **sem acesso** a esses MCPs.

---

## Etapa 1 — Credenciais e Configurações Externas

Colete as seguintes credenciais antes de iniciar. Elas serão injetadas via variáveis de
ambiente no container do grupo `agent-tech`.

### 1.1 PostgreSQL

| Item | Onde obter |
|------|-----------|
| `PG_CONNECTION_STRING` | String de conexão no formato `postgresql://user:pass@host:5432/db` |
| Acesso de leitura | Crie um usuário **somente leitura** para segurança (`GRANT SELECT ON ALL TABLES`) |

> **Recomendação de segurança:** nunca use o usuário `postgres` ou um usuário com `WRITE`.
> O MCP de banco deve ser somente leitura para evitar mutações acidentais pelo agente.

### 1.2 ClickHouse

| Item | Onde obter |
|------|-----------|
| `CLICKHOUSE_HOST` | Hostname/IP do servidor |
| `CLICKHOUSE_PORT` | Porta HTTP (padrão: `8123`) |
| `CLICKHOUSE_USER` | Usuário com `SELECT` |
| `CLICKHOUSE_PASSWORD` | Senha |
| `CLICKHOUSE_DATABASE` | Database padrão (opcional) |

> Se usar ClickHouse Cloud, habilite o acesso por IP do servidor onde o NanoClaw roda.

### 1.3 GitHub (GitHub MCP Server oficial)

O GitHub tem um MCP Server oficial: `github.com/github/github-mcp-server`

| Item | Onde obter |
|------|-----------|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | github.com → Settings → Developer settings → Personal access tokens → Fine-grained |
| Permissões necessárias | `repo:read`, `org:read`, `read:packages` (ajuste conforme necessidade) |
| Escopo | Configure para a **organização** desejada, não para todos os repos pessoais |

> Para listagem de repositórios da org, o token precisa ser aprovado pelo owner da org
> em Settings → Personal access tokens.

### 1.4 Google Cloud Platform (GCP)

O MCP para GCP usa Application Default Credentials (ADC). Há duas opções:

**Opção A — Service Account (recomendado para servidor)**
1. No GCP Console: IAM & Admin → Service Accounts → Create
2. Papéis mínimos sugeridos:
   - `Viewer` (visão geral de recursos)
   - `BigQuery Data Viewer` (se quiser consultar BQ)
   - `Cloud Run Viewer`, `Cloud SQL Viewer`, etc. conforme necessidade
3. Gerar chave JSON: Service Account → Keys → Add Key → JSON
4. Guardar o arquivo como `gcp-service-account.json`
5. Este arquivo será montado no container (via `additionalMounts`)

**Opção B — Token de usuário (para desenvolvimento)**
```bash
gcloud auth application-default login
# Gera ~/.config/gcloud/application_default_credentials.json
```

| Variável de ambiente | Valor |
|---------------------|-------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Caminho para o JSON dentro do container |
| `GOOGLE_CLOUD_PROJECT` | ID do projeto GCP padrão |

### 1.5 Heroku

| Item | Onde obter |
|------|-----------|
| `HEROKU_API_KEY` | dashboard.heroku.com → Account Settings → API Key |
| Escopo | O token dá acesso a **todos os apps da conta** — considere criar uma conta de serviço separada ou usar `heroku authorizations:create --description "nanoclaw" --short` |

```bash
# Gerar token com expiração (recomendado)
heroku authorizations:create --description "nanoclaw-agent-tech" --expires-in 31536000
```

---

## Etapa 2 — MCPs a Instalar no Container

Os MCPs rodam **dentro do container Docker**. Eles precisam ser instalados na imagem ou
invocados via `npx` (sem instalação prévia). A tabela abaixo lista as opções:

| Serviço | Pacote / Repositório | Modo de execução |
|---------|---------------------|-----------------|
| PostgreSQL | `@modelcontextprotocol/server-postgres` (npm) | `npx -y` |
| ClickHouse | `clickhouse-mcp` (npm) ou `mcp-clickhouse` | `npx -y` |
| GitHub | `@github/github-mcp-server` (GitHub Releases — binário Go) | binário pré-compilado |
| GCP | `@cloudmcp/gcp` ou `gcp-mcp` (npm) | `npx -y` |
| Heroku | Sem MCP oficial — usar `heroku-mcp-server` (community) ou wrapper Bash | `npx -y` / custom |

> **Nota sobre GitHub MCP:** O servidor oficial (`github/github-mcp-server`) é um binário Go.
> A alternativa é usar `@modelcontextprotocol/server-github` (npm) que é mais simples de instalar.
> Para uso em org, o binário oficial tem mais funcionalidades.

### Verificação prévia de MCPs

Antes de implementar, teste cada MCP na sua máquina local:

```bash
# PostgreSQL
npx -y @modelcontextprotocol/server-postgres "postgresql://user:pass@host/db"

# GitHub (npm)
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx npx -y @modelcontextprotocol/server-github

# ClickHouse (verificar qual pacote está ativo)
npx -y mcp-clickhouse --help
```

---

## Etapa 3 — Estrutura de Arquivos a Criar no Repositório

Após coletar as credenciais, os seguintes arquivos serão criados/modificados:

```
nanoclaw/
├── groups/
│   └── agent-tech/
│       └── CLAUDE.md          # Instruções e contexto do grupo (criado por você)
│
└── container/
    └── agent-runner/
        └── src/
            └── index.ts       # Modificado: MCPs injetados condicionalmente por grupo
```

**Opção alternativa (mais limpa):** usar o mecanismo de **per-group agent-runner** — o
NanoClaw copia o `agent-runner` para `{DATA_DIR}/sessions/agent-tech/agent-runner-src/`
na primeira execução. Modificamos apenas essa cópia, sem alterar o agent-runner global.

---

## Etapa 4 — Variáveis de Ambiente no Servidor Remoto

No servidor onde o NanoClaw roda, edite o arquivo de ambiente do serviço:

**Linux (systemd):**
```bash
# Editar override do serviço
systemctl --user edit nanoclaw

# Adicionar no arquivo override.conf:
[Service]
Environment="PG_AGENT_TECH=postgresql://readonly:pass@pg-host:5432/mydb"
Environment="CLICKHOUSE_HOST=ch-host"
Environment="CLICKHOUSE_PORT=8123"
Environment="CLICKHOUSE_USER=readonly"
Environment="CLICKHOUSE_PASSWORD=pass"
Environment="CLICKHOUSE_DATABASE=mydb"
Environment="GITHUB_TOKEN_AGENT_TECH=ghp_xxxxx"
Environment="GOOGLE_CLOUD_PROJECT=my-project-id"
Environment="HEROKU_API_KEY=xxxxx"
```

> Use nomes de variáveis com sufixo `_AGENT_TECH` para diferenciar de possíveis
> variáveis globais e evitar vazamento para outros grupos.

**Arquivo de credenciais GCP no servidor:**
```bash
# Criar diretório para credenciais do NanoClaw
mkdir -p ~/.config/nanoclaw/credentials

# Copiar o JSON da service account
scp gcp-service-account.json server:~/.config/nanoclaw/credentials/gcp-agent-tech.json

# Permissões restritas
chmod 600 ~/.config/nanoclaw/credentials/gcp-agent-tech.json
```

Este arquivo será montado no container via `additionalMounts` na configuração do grupo.

---

## Etapa 5 — Registrar o Grupo no NanoClaw

Após implementar as mudanças de código (etapa futura), no canal **#agent-tech** do Slack,
envie ao bot:

```
@bot registrar grupo agent-tech
```

Ou pelo canal principal (main), via comando de registro de grupo com a configuração
de mounts adicionais para o GCP JSON.

---

## Etapa 6 — Conteúdo do `groups/agent-tech/CLAUDE.md`

Crie um CLAUDE.md descrevendo o contexto do grupo. Exemplo de estrutura:

```markdown
# Agent Tech

Você é um assistente de engenharia com acesso a ferramentas de infraestrutura.

## Ferramentas Disponíveis

- **PostgreSQL**: banco transacional principal (somente leitura)
- **ClickHouse**: data warehouse analítico (somente leitura)
- **GitHub**: repositórios da organização [NOME_DA_ORG]
- **GCP**: projeto [NOME_DO_PROJETO] — recursos de Cloud Run, BigQuery, etc.
- **Heroku**: pipelines e dynos dos apps da organização

## Diretrizes

- Nunca execute queries de escrita (INSERT, UPDATE, DELETE, DROP) nos bancos.
- Para explorar schemas, prefira queries de metadados (information_schema).
- Ao listar repos do GitHub, filtre pela organização — não liste repos pessoais.
- Mantenha segredo sobre strings de conexão e tokens.
```

---

## Checklist de Pré-Implementação

Antes de pedir para fazer as mudanças de código, confirme:

- [ ] String de conexão PostgreSQL (usuário readonly criado)
- [ ] Credenciais ClickHouse (usuário readonly criado)
- [ ] GitHub Personal Access Token (aprovado pela org se necessário)
- [ ] Service Account JSON do GCP baixado e copiado para o servidor
- [ ] Heroku API key gerada
- [ ] Variáveis de ambiente configuradas no systemd do servidor
- [ ] `~/.config/nanoclaw/credentials/gcp-agent-tech.json` no servidor
- [ ] `~/.config/nanoclaw/mount-allowlist.json` atualizado para permitir o mount do JSON GCP
- [ ] Canal `#agent-tech` criado no Slack (e bot adicionado ao canal)
- [ ] ID do canal `#agent-tech` anotado (formato: `C...`) para confirmar o JID correto

---

## Próximos Passos (Implementação de Código)

Quando o setup externo estiver pronto, as mudanças de código serão:

1. **`container/agent-runner/src/index.ts`**: adicionar bloco `mcpServers` extra quando
   `containerInput.groupFolder === 'agent-tech'`
2. **`groups/agent-tech/CLAUDE.md`**: criar com contexto do grupo
3. **`container/Dockerfile`** (opcional): pré-instalar binários MCP pesados (GitHub MCP Go binary)
   para evitar download em runtime
4. **Configuração de mount**: adicionar o JSON do GCP nos mounts permitidos do grupo

Nenhum outro arquivo precisa ser modificado — o isolamento é garantido pela checagem de
`groupFolder` no agent-runner, que já é o mecanismo usado para permissões de `isMain`.


---
1. Local (repositório clonado) vs npm/npx — qual a diferença?
npx -y @pacote/nome (execução direta via npm)
O comando baixa o pacote do registro npm e executa na hora, sem instalação permanente.

Vantagens:
- Zero setup: nenhum arquivo extra no repositório
- Sempre usa a versão mais recente (ou a que você fixar com @1.2.3)
- Funciona imediatamente dentro do container se npx estiver disponível

Desvantagens:
- Requer acesso à internet no momento em que o container sobe — se o npm estiver lento ou bloqueado, o MCP não inicia
- Em servidores de produção isso é um risco real (cold start lento, falha silenciosa)
- Não dá controle sobre o código que está sendo executado (supply chain risk)

Clonar o repositório localmente (código-fonte)
Você faz git clone do MCP server, compila (npm install && npm run build), e aponta o
container para o binário local via mount.

Vantagens:
- Determinístico: você sabe exatamente qual código está rodando, fixado num commit
- Offline: funciona sem internet após o build inicial
- Auditável: pode inspecionar e modificar o código
- Mais rápido para subir o container (sem download)

Desvantagens:
- Você precisa manter os repositórios e rebuildar quando quiser atualizar
- Mais arquivos para gerenciar
Pré-instalar na imagem Docker (Dockerfile)
Terceira opção: adicionar RUN npm install -g @pacote/nome no Dockerfile do container.

Vantagens:
- Zero latência no startup
- Determinístico (fixado na build da imagem)
- Não depende de internet em runtime
Desvantagens:
- Precisa rebuildar a imagem (./container/build.sh) a cada atualização de MCP

---
Recomendação para o seu caso

┌──────────────────────────────────────────────────────────────────────┬──────────────────────────────────┐
│                               Cenário                                │           Opção ideal            │
├──────────────────────────────────────────────────────────────────────┼──────────────────────────────────┤
│ MCPs npm maduros e estáveis (PostgreSQL, GitHub)                     │ Pré-instalar no Dockerfile       │
├──────────────────────────────────────────────────────────────────────┼──────────────────────────────────┤
│ MCPs em desenvolvimento ativo que você quer atualizar com frequência │ Clone local + mount no container │
├──────────────────────────────────────────────────────────────────────┼──────────────────────────────────┤
│ Protótipo/teste inicial                                              │ npx                              │
└──────────────────────────────────────────────────────────────────────┴──────────────────────────────────┘

Para o #agent-tech em produção: Dockerfile para os MCPs npm consolidados, e clone local com mount para o GCP (que é via
endpoint remoto HTTP, diferente dos outros).

---
2. MCPs do GCP para mapear sua infraestrutura
A Google lançou MCPs remotos — eles rodam na infraestrutura deles, não no seu servidor. Você aponta o cliente MCP para um
endpoint HTTPS e autentica via Application Default Credentials / Service Account. Isso simplifica muito o setup.
Para o objetivo de explorar projetos, listar serviços e gerar um mapa da infra, os MCPs prioritários são:

Camada 1 — Essenciais (visão geral da org)
┌────────────────┬─────────────────────────────────────────────────┬──────────────────────────────────────────────────────┐
│      MCP       │                    Endpoint                     │                    Para que serve                    │
├────────────────┼─────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ Resource       │                                                 │ Lista organizations, folders e projetos. É o ponto   │
│ Manager        │ https://cloudresourcemanager.googleapis.com/mcp │ de partida — sem isso você não sabe quais projetos   │
│                │                                                 │ existem                                              │
├────────────────┼─────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ Cloud Asset    │ (via API)                                       │ Inventário completo de todos os recursos em todos os │
│ Inventory      │                                                 │  projetos — VMs, buckets, DBs, tudo                  │
├────────────────┼─────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ Cloud          │ https://monitoring.googleapis.com/mcp           │ Visão de métricas e alertas por projeto; indica      │
│ Monitoring     │                                                 │ quais recursos estão ativos                          │
├────────────────┼─────────────────────────────────────────────────┼──────────────────────────────────────────────────────┤
│ Cloud Logging  │ https://logging.googleapis.com/mcp              │ Logs de auditoria (quem criou o quê, quando) — útil  │
│                │                                                 │ para entender o histórico da infra                   │
└────────────────┴─────────────────────────────────────────────────┴──────────────────────────────────────────────────────┘

Camada 2 — Por tipo de recurso (mapear o que você tem)
┌────────────────┬──────────────────────────────────────┬──────────────────────────────────────┐
│      MCP       │               Endpoint               │            Para que serve            │
├────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ Compute Engine │ https://compute.googleapis.com/mcp   │ Lista VMs, discos, redes, IPs        │
├────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ Cloud Run      │ https://run.googleapis.com/mcp       │ Lista serviços serverless por região │
├────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ GKE            │ https://container.googleapis.com/mcp │ Lista clusters Kubernetes            │
├────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ Cloud SQL      │ https://sqladmin.googleapis.com/mcp  │ Lista instâncias de banco gerenciado │
├────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ BigQuery       │ https://bigquery.googleapis.com/mcp  │ Lista datasets e tabelas             │
└────────────────┴──────────────────────────────────────┴──────────────────────────────────────┘

Camada 3 — Adicionar depois (conforme necessidade)
┌────────────────────────────────┬──────────────────────────────────┐
│              MCP               │               Uso                │
├────────────────────────────────┼──────────────────────────────────┤
│ Vertex AI                      │ Se usar ML/modelos               │
├────────────────────────────────┼──────────────────────────────────┤
│ Pub/Sub                        │ Se tiver pipelines de mensageria │
├────────────────────────────────┼──────────────────────────────────┤
│ Firestore / Spanner / Bigtable │ Conforme os bancos que você usa  │
└────────────────────────────────┴──────────────────────────────────┘

---
Como esses MCPs remotos se autenticam
Os endpoints GCP MCP usam OAuth 2.0 via Application Default Credentials. No container do #agent-tech, você precisa:
1. Montar o JSON da Service Account
2. Definir GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/sa.json
A Service Account precisa dos seguintes papéis no nível de organização (não apenas por projeto) para ter visão completa:
roles/resourcemanager.organizationViewer   ← ver a org
roles/resourcemanager.folderViewer         ← ver folders
roles/viewer                               ← viewer em todos os projetos
roles/cloudasset.viewer                    ← Cloud Asset Inventory
▎ Se não tiver acesso à organização inteira, aplique roles/viewer em cada projeto individualmente.

---
Ordem de execução para gerar o "mapa"
Quando o agente entrar no #agent-tech, o fluxo ideal seria:
1. Resource Manager  →  listar todos os projetos da org
2. Cloud Asset Inventory  →  para cada projeto, inventariar todos os recursos
3. Compute/CloudRun/GKE/SQL  →  detalhes por tipo de recurso
4. Cloud Monitoring  →  quais recursos têm tráfego/alertas ativos (os "vivos")
5. Cloud Logging (audit)  →  quem criou o quê (para documentação histórica)
