# 🚀 Automação Supabase + Z-API (WhatsApp)

Este projeto consiste em uma automação em Python desenvolvida como um desafio técnico. O objetivo é ler contatos cadastrados em um banco de dados **Supabase (PostgreSQL)** e disparar mensagens personalizadas via WhatsApp utilizando a infraestrutura da **Z-API**.

O fluxo respeita a regra de negócio de disparar mensagens para no máximo 3 contatos por execução, utilizando o formato exato exigido: `"Olá, <nome_contato> tudo bem com você?"`.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.12+**
* **Supabase** (Banco de dados PostgreSQL)
* **Z-API** (Gateway de integração com WhatsApp)
* **Bibliotecas Python:** `supabase`, `requests`, `python-dotenv`, `websockets`

---

## 📊 1. Setup da Tabela no Supabase

Para preparar o banco de dados, acesse o **SQL Editor** no painel do seu Supabase, crie uma nova consulta (New Query), cole o código abaixo e clique em **Run**:

```sql
-- Criação da tabela de contatos
create table contatos (
  id bigint generated always as identity primary key,
  nome text not null,
  telefone text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Inserção de dados fictícios para teste
-- NOTA: O formato do telefone deve ser DDI + DDD + Número (Apenas números).
-- Dica: Caso o WhatsApp não entregue com o 9º dígito devido às regras locais da Meta, tente cadastrar sem o 9 (Ex: 55117402XXXX).
insert into contatos (nome, telefone) values 
('Joao', '5511999999999'),
('Maria', '5511988888888'),
('Pedro', '5511977777777');
```

---

## 2. Variáveis de Ambiente (.env)

O projeto utiliza variáveis de ambiente para garantir a segurança das credenciais, evitando a exposição de chaves no repositório público.

Na raiz do projeto, você encontrará o arquivo .env.example.

Duplique ou renomeie este arquivo para .env:

```sql
Bash
cp .env.example .env
```
Abra o arquivo .env e preencha com as suas chaves reais:

```sql
--# Configurações do Supabase (Project Settings > API)
SUPABASE_URL=[https://seu-projeto.supabase.co](https://seu-projeto.supabase.co)
SUPABASE_KEY=sua_anon_public_key_aqui

--# Configurações da Z-API (Painel da Instância)
ZAPI_INSTANCE_ID=SUA_ID_DA_INSTANCIA
ZAPI_TOKEN=SEU_TOKEN_DA_ZAPI
```
---

## 🏃 3. Como Instalar e Rodar Localmente (Passo a Passo)
Siga os passos abaixo no seu terminal para isolar o ambiente e executar a automação:

Passo 1: Clonar o repositório

```sql
Bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

Passo 2: Criar o Ambiente Virtual (venv)
Crie uma "bolha" isolada para que as bibliotecas deste projeto não conflitem com outras do seu computador:

```sql
Bash
python -m venv venv
```

Passo 3: Ativar o Ambiente Virtual
Ative o ambiente virtual para que o terminal utilize o Python isolado do projeto:

No Windows (Prompt de Comando / CMD):

```sql
DOS
venv\Scripts\activate
```

No Mac ou Linux:

```sql
Bash
source venv/bin/activate
```

(Você notará o prefixo (venv) aparecendo no início da linha do terminal indicando que a ativação deu certo).

Passo 4: Instalar as dependências do projeto
Instale todas as bibliotecas necessárias listadas no arquivo requirements.txt:

```sql
Bash
pip install -r requirements.txt
```

Passo 5: Conectar o WhatsApp na Z-API
Antes de executar o script, acesse o painel da Z-API, gere o QR Code na sua instância e escaneie com o aplicativo do WhatsApp no seu celular (como se fosse conectar no WhatsApp Web). Certifique-se de que o status da instância mudou para "Connected".

Passo 6: Executar a automação
Agora basta rodar o arquivo principal para ler os dados do Supabase e disparar as mensagens:

```sql
Bash
python main.py
```

🔍 Logs de Execução Esperados
O script conta com um sistema de logs estruturado para monitoramento e diagnóstico de falhas. Uma execução bem-sucedida gerará saídas semelhantes a esta:

```sql
2026-06-17 19:51:36,836 - INFO - Iniciando o processo de envio de mensagens...
2026-06-17 19:51:38,215 - INFO - HTTP Request: GET [https://xxxx.supabase.co/rest/v1/contatos?select=nome%2Ctelefone&limit=3](https://xxxx.supabase.co/rest/v1/contatos?select=nome%2Ctelefone&limit=3) "HTTP/2 200 OK"
2026-06-17 19:51:38,228 - INFO - Encontrado(s) 3 contato(s). Iniciando envios...
2026-06-17 19:51:38,726 - INFO - Mensagem enviada com sucesso para Joao (551199999XXXX).
2026-06-17 19:51:39,207 - INFO - Mensagem enviada com sucesso para Maria (551198888XXXX).
2026-06-17 19:51:39,692 - INFO - Mensagem enviada com sucesso para Pedro (551197777XXXX).