import pandas as pd
from scripts.conversor import convert_df_to_parquet_bytes
from scripts.get_data import get_html_with_selenium, parse_table_with_bs4
from scripts.upload_file import upload_parquet_to_s3


# 🚀 Execução
if __name__ == "__main__":
    url = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br"
    html = get_html_with_selenium(url, True)
    headers, rows = parse_table_with_bs4(html)
    df = pd.DataFrame(rows[:-2], columns=headers)
    print(df)
    parquet_bytes = convert_df_to_parquet_bytes(df)
    upload_parquet_to_s3(parquet_bytes)


