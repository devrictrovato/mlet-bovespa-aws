import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import io


# 3. Converte DataFrame em Parquet em memória (bytes)
def convert_df_to_parquet_bytes(df: pd.DataFrame) -> bytes:
    """
    Converte um DataFrame pandas para o formato Parquet em memória.
    Retorna os dados como bytes (útil para salvar em arquivo ou enviar ao S3).
    """
    # Converte DataFrame para objeto Table do pyarrow
    table = pa.Table.from_pandas(df)

    # Cria um buffer de memória em bytes
    buffer = io.BytesIO()

    # Escreve o conteúdo do table no buffer no formato Parquet
    pq.write_table(table, buffer)

    # Retorna o conteúdo binário do Parquet
    return buffer.getvalue()