import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")

if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE_ID, ZAPI_TOKEN]):
    logging.error("Erro: Verifique se todas as variáveis no arquivo .env foram preenchidas.")
    exit(1)

def buscar_contatos(limite: int = 3) -> list:
    """Busca os contatos cadastrados no Supabase limitando a quantidade."""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        resposta = supabase.table("contatos").select("nome, telefone").limit(limite).execute()
        return resposta.data
    except Exception as e:
        logging.error(f"Erro ao conectar ou buscar dados no Supabase: {e}")
        return []

def enviar_mensagem_zapi(nome: str, telefone: str):
    """Envia a mensagem personalizada utilizando a API da Z-API."""
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    
    mensagem = f"Olá, {nome} tudo bem com você?"
    
    payload = {
        "phone": telefone,
        "message": mensagem
    }
    
    try:
        resposta = requests.post(url, json=payload, timeout=10)
        if resposta.status_code in [200, 201]:
            logging.info(f"Mensagem enviada com sucesso para {nome} ({telefone}).")
        else:
            logging.warning(f"Falha ao enviar para {nome}. Status Code: {resposta.status_code} - Resposta: {resposta.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de rede ao tentar enviar mensagem para {nome}: {e}")

def main():
    logging.info("Iniciando o processo de envio de mensagens...")
    
    # 1. Busca contatos no banco (Máximo 3)
    contatos = buscar_contatos(limite=3)
    
    if not contatos:
        logging.info("Nenhum contato encontrado para processar.")
        return

    logging.info(f"Encontrado(s) {len(contatos)} contato(s). Iniciando envios...")

    # 2. Iterar e enviar as mensagens
    for contato in contatos:
        nome = contato.get("nome")
        telefone = contato.get("telefone")
        
        if nome and telefone:
            enviar_mensagem_zapi(nome, telefone)
        else:
            logging.warning(f"Contato com dados incompletos ignorado: {contato}")

if __name__ == "__main__":
    main()