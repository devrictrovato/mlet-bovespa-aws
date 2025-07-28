import boto3
import datetime
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# 4. Faz upload do arquivo Parquet para S3 com partição diária
def upload_parquet_to_s3(parquet_bytes: bytes, date: datetime.date = None):
    """
    Envia um arquivo Parquet (em bytes) para o S3 com caminho particionado por data.
    Lê configurações do ambiente (.env ou variáveis de ambiente), incluindo session token.
    """

    # Lê variáveis de ambiente
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.environ.get("AWS_SESSION_TOKEN")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    bucket = os.environ.get("S3_BUCKET")
    base_path = os.environ.get("S3_BASE_PATH", "raw")

    # Usa data e hora atual se nenhuma for passada
    if date is None:
        now = datetime.datetime.now()
    else:
        # Se o usuário passar apenas uma data (sem hora), combine com meia-noite
        now = datetime.datetime.combine(date, datetime.datetime.min.time())

    year = str(now.year)
    month = f"{now.month:02d}"
    day = f"{now.day:02d}"
    hour = f"{now.hour:02d}"
    minute = f"{now.minute:02d}"
    second = f"{now.second:02d}"

    filename = f"ibov_{year}-{month}-{day}_{hour}-{minute}-{second}.parquet"

    # Monta o caminho S3
    MONTH_MAP = {
        "01": "jan", "02": "fev", "03": "mar", "04": "abr",
        "05": "mai", "06": "jun", "07": "jul", "08": "ago",
        "09": "set", "10": "out", "11": "nov", "12": "dez"
    }
    month = MONTH_MAP[month]
    s3_key = f"{base_path}/{year}/{month}/{day}/{filename}"

    # Inicializa cliente S3 com ou sem token temporário
    s3_args = {
        "aws_access_key_id": aws_access_key,
        "aws_secret_access_key": aws_secret_key,
        "region_name": aws_region
    }
    if aws_session_token:
        s3_args["aws_session_token"] = aws_session_token

    s3 = boto3.client("s3", **s3_args)

    # Testa conexão com S3
    try:
        response = s3.list_buckets()
        print("🟢 Conexão com S3 estabelecida com sucesso.")
        print("Buckets disponíveis:", [b['Name'] for b in response['Buckets']])
    except Exception as e:
        print("🔴 Falha na conexão com S3:", e)
        raise

    # Envia o arquivo
    s3.put_object(Bucket=bucket, Key=s3_key, Body=parquet_bytes)
    print(f"✅ Upload realizado com sucesso: s3://{bucket}/{s3_key}")
