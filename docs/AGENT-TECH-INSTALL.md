# Guia de Instalação: MCPs do Canal #agent-tech

Pré-requisito: leia `docs/AGENT-TECH-SETUP.md` para entender a arquitetura.
Este guia é **executado no servidor remoto** onde o NanoClaw roda, exceto onde indicado.

---

## Índice

1. [PostgreSQL — Usuários de leitura](#1-postgresql--usuários-de-leitura)
2. [ClickHouse — Usuários de leitura](#2-clickhouse--usuários-de-leitura)
3. [GCP — Service Account](#3-gcp--service-account)
4. [GitHub — Personal Access Token](#4-github--personal-access-token)
5. [Heroku — API Token](#5-heroku--api-token)
6. [Clonar e compilar os MCPs no servidor](#6-clonar-e-compilar-os-mcps-no-servidor)
7. [Atualizar o `.env`](#7-atualizar-o-env)
8. [Verificação final](#8-verificação-final)

---

## 1. PostgreSQL — Usuários de leitura

Execute os comandos abaixo **em cada banco** (staging e produção) como superusuário.

### 1.1 Staging

```sql
-- Conectado ao banco de staging
CREATE USER nanoclaw_ro WITH PASSWORD 'escolha-uma-senha-forte';

-- Permissão para conectar
GRANT CONNECT ON DATABASE <nome_do_banco_staging> TO nanoclaw_ro;

-- Acesso ao schema público
GRANT USAGE ON SCHEMA public TO nanoclaw_ro;

-- SELECT em todas as tabelas existentes
GRANT SELECT ON ALL TABLES IN SCHEMA public TO nanoclaw_ro;

-- SELECT em tabelas futuras (para não precisar repetir)
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO nanoclaw_ro;

-- Se usar outros schemas além de public, repita para cada um:
-- GRANT USAGE ON SCHEMA <schema> TO nanoclaw_ro;
-- GRANT SELECT ON ALL TABLES IN SCHEMA <schema> TO nanoclaw_ro;
```

Anote a connection string:
```
postgresql://nanoclaw_ro:<senha>@<host_staging>:5432/<nome_do_banco_staging>
```

### 1.2 Produção

```sql
-- Conectado ao banco de produção
CREATE USER nanoclaw_ro WITH PASSWORD 'escolha-outra-senha-forte';

GRANT CONNECT ON DATABASE <nome_do_banco_prod> TO nanoclaw_ro;
GRANT USAGE ON SCHEMA public TO nanoclaw_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO nanoclaw_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO nanoclaw_ro;
```

Anote a connection string:
```
postgresql://nanoclaw_ro:<senha>@<host_prod>:5432/<nome_do_banco_prod>
```

> **Segurança:** Se o banco de produção estiver numa VPC privada, verifique que o IP
> do servidor NanoClaw está liberado no security group / firewall antes de testar.

---

## 2. ClickHouse — Usuários de leitura

### 2.1 Staging (self-managed no Compute Engine)

Conecte via SSH na VM do Compute Engine que roda o ClickHouse:

```bash
# Abrir cliente ClickHouse
clickhouse-client --user default --password <senha_admin>
```

```sql
-- Criar usuário somente leitura
CREATE USER nanoclaw_ro IDENTIFIED BY 'escolha-uma-senha-forte';

-- Conceder SELECT em todos os bancos que deseja expor
-- (substitua <database> pelo nome real, ou use *.* para todos)
GRANT SELECT ON <database>.* TO nanoclaw_ro;

-- Se quiser restringir por IP (recomendado em produção):
-- CREATE USER nanoclaw_ro IDENTIFIED BY '...' HOST IP '<ip_do_servidor_nanoclaw>';
```

Variáveis para este servidor:
```
CLICKHOUSE_HOST_STAGING=<ip_ou_hostname_da_vm>
CLICKHOUSE_PORT_STAGING=8123        # HTTP nativo (sem TLS em self-managed)
CLICKHOUSE_USER_STAGING=nanoclaw_ro
CLICKHOUSE_PASSWORD_STAGING=<senha>
CLICKHOUSE_SECURE_STAGING=false
```

> **Firewall:** Abra a porta `8123` (HTTP) ou `9000` (TCP nativo) na regra de firewall
> da VM no GCP Console para o IP do servidor NanoClaw.

### 2.2 Produção (ClickHouse Cloud)

1. Acesse **cloud.clickhouse.com** → seu serviço → **Settings** → **Users**
2. Clique em **Add new user**
3. Nome: `nanoclaw_ro`, escolha uma senha forte
4. Em **Permissions**: marque apenas `READ ONLY`
5. Clique em **Save**

Variáveis para este servidor:
```
CLICKHOUSE_HOST_PROD=<seu-servico>.clickhouse.cloud
CLICKHOUSE_PORT_PROD=8443           # HTTPS (TLS obrigatório no Cloud)
CLICKHOUSE_USER_PROD=nanoclaw_ro
CLICKHOUSE_PASSWORD_PROD=<senha>
CLICKHOUSE_SECURE_PROD=true
```

> O hostname está em **Connect** → **HTTP interface** no painel do ClickHouse Cloud.

---

## 3. GCP — Service Account

### 3.1 Criar a Service Account

No [GCP Console](https://console.cloud.google.com):

1. Menu → **IAM & Admin** → **Service Accounts**
2. Clique em **Create Service Account**
3. Nome: `nanoclaw-agent-tech`
   Descrição: `NanoClaw agent-tech — read-only infra mapping`
4. Clique em **Create and Continue**

### 3.2 Atribuir papéis

> Atribua os papéis **no nível de organização** para ter visão de todos os projetos.
> Se não tiver acesso à org, repita para cada projeto relevante.

Papéis necessários:

| Papel | Para que serve |
|-------|---------------|
| `roles/resourcemanager.organizationViewer` | Ver a organização e seus projetos |
| `roles/resourcemanager.folderViewer` | Ver a hierarquia de folders |
| `roles/viewer` | Viewer genérico em todos os projetos (Cloud Run, SQL, VMs) |
| `roles/cloudasset.viewer` | Cloud Asset Inventory — inventariar todos os recursos |
| `roles/logging.viewer` | Cloud Logging — ver logs de auditoria |
| `roles/monitoring.viewer` | Cloud Monitoring — ver métricas e alertas |

Para adicionar no nível de organização via gcloud (execute na sua máquina com permissão de org admin):

```bash
# Substitua ORG_ID pelo ID numérico da sua organização
# (Menu → IAM & Admin → Settings → Organization ID)
ORG_ID="123456789012"
SA_EMAIL="nanoclaw-agent-tech@<seu-projeto>.iam.gserviceaccount.com"

for role in \
  roles/resourcemanager.organizationViewer \
  roles/resourcemanager.folderViewer \
  roles/viewer \
  roles/cloudasset.viewer \
  roles/logging.viewer \
  roles/monitoring.viewer; do
  gcloud organizations add-iam-policy-binding $ORG_ID \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="$role"
done
```

### 3.3 Gerar a chave JSON

1. Na página da Service Account → aba **Keys**
2. **Add Key** → **Create new key** → **JSON** → **Create**
3. Salve o arquivo como `gcp-nanoclaw-agent-tech.json`

### 3.4 Copiar para o servidor

```bash
# Execute na sua máquina local
scp gcp-nanoclaw-agent-tech.json \
  <usuario>@<servidor>:~/.config/nanoclaw/credentials/gcp-agent-tech.json

# No servidor: restringir permissões
ssh <usuario>@<servidor> "chmod 600 ~/.config/nanoclaw/credentials/gcp-agent-tech.json"
```

### 3.5 Adicionar ao mount-allowlist do NanoClaw

No servidor, edite `~/.config/nanoclaw/mount-allowlist.json` e adicione a entrada:

```json
{
  "allowed": [
    "~/.config/nanoclaw/credentials/gcp-agent-tech.json"
  ]
}
```

> Se o arquivo não existir ainda, crie-o com esse conteúdo.

---

## 4. GitHub — Personal Access Token

Execute na sua máquina ou diretamente no GitHub:

1. github.com → **Settings** (menu do seu perfil)
2. **Developer settings** → **Personal access tokens** → **Fine-grained tokens**
3. Clique em **Generate new token**
4. Nome: `nanoclaw-agent-tech`
5. Expiration: 1 ano (ou conforme política da org)
6. **Resource owner**: selecione a **organização** (não sua conta pessoal)
7. **Repository access**: `All repositories` (ou selecione os repos da org)
8. **Permissions** — marque apenas:
   - `Contents` → Read-only
   - `Metadata` → Read-only (obrigatório)
   - `Pull requests` → Read-only
   - `Issues` → Read-only (opcional)
9. Clique em **Generate token** e copie o valor

> **Aprovação:** Se a organização exigir, um owner da org precisará aprovar o token em
> **org Settings** → **Personal access tokens** → **Pending requests**.

Anote o token: `github_pat_...`

---

## 5. Heroku — API Token

```bash
# Na sua máquina, com Heroku CLI instalado e autenticado
heroku authorizations:create \
  --description "nanoclaw-agent-tech" \
  --expires-in 31536000

# O comando retorna algo como:
# Token: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Anote o token.

> Se não tiver o Heroku CLI local: dashboard.heroku.com → **Account Settings** →
> **API Key** → **Reveal**. Este token não expira, mas pode ser revogado a qualquer hora.

---

## 6. Clonar e compilar os MCPs no servidor

Execute no servidor remoto, numa pasta dedicada (sugerimos `~/mcps/`):

```bash
mkdir -p ~/mcps
cd ~/mcps
```

### 6.1 PostgreSQL MCP

```bash
git clone https://github.com/modelcontextprotocol/servers-archived.git postgres-mcp
cd postgres-mcp
npm install
npm run build
# O binário ficará em dist/ ou o entry point é src/postgres/index.ts
cd ..
```

Teste rápido (opcional):
```bash
node postgres-mcp/dist/postgres/index.js \
  "postgresql://nanoclaw_ro:<senha>@<host_staging>:5432/<banco>" 2>&1 | head -5
```

### 6.2 ClickHouse MCP

O MCP oficial do ClickHouse é **Python**. O container do NanoClaw é Node.js e não
tem Python instalado. Há duas opções:

**Opção A — Instalar Python no container (recomendado)**
Será feito na etapa de código (modificação do `Dockerfile`). Nenhuma ação manual aqui.

**Opção B — Rodar o MCP fora do container como processo separado**
Mais complexo; não recomendado por ora.

Por enquanto, instale no servidor para verificar que funciona:

```bash
# Requer Python 3.10+
python3 --version

pip3 install mcp-clickhouse

# Teste de conectividade com staging
CLICKHOUSE_HOST=<host_staging> \
CLICKHOUSE_PORT=8123 \
CLICKHOUSE_USER=nanoclaw_ro \
CLICKHOUSE_PASSWORD=<senha> \
CLICKHOUSE_SECURE=false \
python3 -m mcp_clickhouse.main --help
```

### 6.3 GitHub MCP (binário oficial Go)

```bash
git clone https://github.com/github/github-mcp-server.git ~/mcps/github-mcp
cd ~/mcps/github-mcp

# Verificar se Go está instalado
go version  # precisa de Go 1.21+

# Compilar
go build -o github-mcp-server ./cmd/github-mcp-server

# Testar
GITHUB_PERSONAL_ACCESS_TOKEN=<seu_token> \
  ./github-mcp-server --help
```

Se Go não estiver instalado no servidor:
```bash
# Ubuntu/Debian
sudo apt install golang-go

# Ou via snap (versão mais recente)
sudo snap install go --classic
```

### 6.4 Heroku MCP

```bash
# Requer Node.js (já disponível no servidor NanoClaw)
npm install -g @heroku/mcp-server

# Verificar versão do Heroku CLI (precisa ser >= 10.8.1)
heroku --version

# Se não tiver o Heroku CLI no servidor:
curl https://cli-assets.heroku.com/install.sh | sh

# Autenticar com o token (sem abrir browser)
heroku auth:login --interactive
# ou via variável de ambiente diretamente (não precisa de login)
```

### 6.5 GCP — não requer instalação local

Os MCPs do GCP são **remotos** (HTTP). Nenhum binário precisa ser clonado. O agente
se conecta diretamente aos endpoints `*.googleapis.com/mcp` usando o token da
Service Account. A configuração é feita inteiramente via código no agent-runner.

---

## 7. Atualizar o `.env`

No servidor, abra o arquivo `.env` na raiz do repositório NanoClaw:

```bash
nano ~/caminho/para/nanoclaw/.env
```

Adicione ao final (após as variáveis existentes):

```bash
# ─── agent-tech: PostgreSQL ────────────────────────────────────────────────
PG_AGENT_TECH_STAGING=postgresql://nanoclaw_ro:<senha>@<host_staging>:5432/<banco_staging>
PG_AGENT_TECH_PROD=postgresql://nanoclaw_ro:<senha>@<host_prod>:5432/<banco_prod>

# ─── agent-tech: ClickHouse ────────────────────────────────────────────────
CLICKHOUSE_HOST_STAGING=<ip_ou_hostname_vm>
CLICKHOUSE_PORT_STAGING=8123
CLICKHOUSE_USER_STAGING=nanoclaw_ro
CLICKHOUSE_PASSWORD_STAGING=<senha>
CLICKHOUSE_SECURE_STAGING=false

CLICKHOUSE_HOST_PROD=<servico>.clickhouse.cloud
CLICKHOUSE_PORT_PROD=8443
CLICKHOUSE_USER_PROD=nanoclaw_ro
CLICKHOUSE_PASSWORD_PROD=<senha>
CLICKHOUSE_SECURE_PROD=true

# ─── agent-tech: GitHub ────────────────────────────────────────────────────
GITHUB_TOKEN_AGENT_TECH=github_pat_<seu_token>

# ─── agent-tech: GCP ───────────────────────────────────────────────────────
GCP_SA_KEY_PATH=/home/<usuario>/.config/nanoclaw/credentials/gcp-agent-tech.json
GOOGLE_CLOUD_PROJECT=<id_do_projeto_principal>

# ─── agent-tech: Heroku ────────────────────────────────────────────────────
HEROKU_API_KEY_AGENT_TECH=<token_heroku>
```

Restrinja as permissões do arquivo:
```bash
chmod 600 ~/caminho/para/nanoclaw/.env
```

---

## 8. Verificação final

Execute este checklist no servidor antes de pedir a implementação do código:

```bash
# 1. PostgreSQL staging
psql "postgresql://nanoclaw_ro:<senha>@<host_staging>:5432/<banco>" \
  -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';"

# 2. PostgreSQL produção
psql "postgresql://nanoclaw_ro:<senha>@<host_prod>:5432/<banco>" \
  -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';"

# 3. ClickHouse staging
curl -s "http://<host_staging>:8123/?query=SELECT+version()" \
  --user nanoclaw_ro:<senha>

# 4. ClickHouse Cloud (produção)
curl -s "https://<servico>.clickhouse.cloud:8443/?query=SELECT+version()" \
  --user nanoclaw_ro:<senha>

# 5. GitHub token (substituir <org> pelo nome da sua organização)
curl -s -H "Authorization: Bearer github_pat_<token>" \
  https://api.github.com/orgs/<org>/repos?per_page=1 | jq '.[0].name'

# 6. GCP Service Account
gcloud auth activate-service-account \
  --key-file=~/.config/nanoclaw/credentials/gcp-agent-tech.json
gcloud projects list --limit=5

# 7. Heroku token
curl -s -H "Authorization: Bearer <token_heroku>" \
  https://api.heroku.com/apps \
  -H "Accept: application/vnd.heroku+json; version=3" | jq '.[0].name'

# 8. Binários MCP compilados
~/mcps/github-mcp/github-mcp-server --version
node ~/mcps/postgres-mcp/dist/index.js --version 2>/dev/null || echo "OK (sem --version)"
```

---

## Próximo passo

Com todas as verificações passando, volte aqui e peça:

> "Todas as credenciais estão prontas, pode implementar o `#agent-tech`."

As mudanças de código serão:
1. `container/Dockerfile` — adicionar Python 3.10 + `mcp-clickhouse`
2. `container/agent-runner/src/index.ts` — bloco de MCPs condicional para `agent-tech`
3. `groups/agent-tech/CLAUDE.md` — instruções e contexto do grupo
4. `src/container-runner.ts` — injeção das variáveis de ambiente para o grupo `agent-tech`
