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