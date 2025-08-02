import boto3

print('Função Lambda carregada com sucesso!')

# Cliente do AWS Glue
glue = boto3.client('glue')

def lambda_handler(event, context):
    gluejobname = "BovespaParquetRefined"

    try:
        # Inicia o Glue Job
        run_response = glue.start_job_run(JobName=gluejobname)
        print(f"Job '{gluejobname}' iniciado com sucesso! RunId: {run_response['JobRunId']}")

        # Importante: Não tente verificar o status imediatamente.
        # O job pode levar alguns minutos para iniciar/executar.
        # Caso queira monitorar, utilize Step Functions ou agende uma outra Lambda.
        
        return {
            "statusCode": 200,
            "body": f"Glue job iniciado com sucesso. RunId: {run_response['JobRunId']}"
        }

    except Exception as e:
        print(f"Erro ao iniciar o job '{gluejobname}': {str(e)}")
        raise e  # Mantém o erro para que o CloudWatch registre a falha corretamente
