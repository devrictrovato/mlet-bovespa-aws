import time
import json
import requests
import datetime
import boto3
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Lê as variáveis do ambiente
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")
aws_region = os.getenv("AWS_REGION", "us-east-1")
delivery_stream_name = os.getenv("DELIVERY_STREAM_NAME")

def get_crypto_price(coin):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=brl'
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()[coin]["brl"]
    return None


# Inicializa o cliente do AWS Firehose usando variáveis de ambiente
firehose_client = boto3.client(
    "firehose",
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)


# Loop infinito para pegar o preço e enviar ao Firehose
while True:
    coin = 'bitcoin'
    price = get_crypto_price(coin)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if price:
        data = {
            "collect": timestamp,
            "coin": coin,
            "price": price
        }

        try:
            # Envia para o Firehose
            response = firehose_client.put_record(
                DeliveryStreamName=delivery_stream_name,
                Record={
                    'Data': json.dumps(data)
                }
            )
            print(f"[{time.strftime('%H:%M:%S')}] Enviado: {data}")
        except Exception as e:
            print(f"Erro ao enviar para Firehose: {e}")
    else:
        print("Erro ao obter o preço.")

    time.sleep(60)  # Espera 60 segundos antes de buscar novamente
