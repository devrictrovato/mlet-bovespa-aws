# 📈 mlet-bovespa-aws

> Pipeline para scraping e processamento de dados do pregão da B3, utilizando apenas os arquivos presentes no repositório.

## 🗂 Estrutura do repositório

```bash
mlet-bovespa-aws/
├── scraping/ # Script(s) para coletar dados da B3 (web scraping)
├── glue/ # Projeto visual do job de ETL (visual, formato exportado)
├── lambda/ # Código da função local que iniciaria o job (exemplo)
├── s3/ # Estrutura de pastas esperada: raw/, refined/
└── README.md # Este arquivo
```


## 🔧 Funcionalidades sem AWS

- O diretório `scraping/` contém script(s) que fazem o download dos dados do pregão da B3.
- Dentro de `glue/`, há o job de transformação com lógica visual (agrupamento, renomeação e cálculo de datas).
- A pasta `lambda/` mostra um exemplo de função que acionaria esse job.
- A pasta `s3/` ilustra como os dados seriam organizados localmente com as pastas `raw/` (dados brutos) e `refined/` (dados processados), ambos em formato Parquet, particionados por data e ticker.

## 🧪 Como executar localmente

1. Execute o script de scraping para obter arquivos `.parquet` no diretório `s3/raw/YYYY/MM/DD/`.
2. Simule a lógica visual do Glue com ferramentas como Pandas ou PySpark:
   - Execute agregações e sumarizações (ex.: soma de volumes).
   - Renomeie pelo menos duas colunas.
   - Realize um cálculo envolvendo campos de data (ex.: diferença entre data de pregão e data de registro).
3. Salve os dados transformados no diretório `s3/refined/YYYY/MM/DD/`, no formato Parquet.

## ✅ Requisitos contemplados (sem AWS)

| Requisito       | Descrição |
|----------------|-----------|
| Scraping       | Extração de dados da B3 via script. |
| Formato Parquet | Armazenamento em Parquet local. |
| Partição por data | Organização em subpastas por data. |
| Transformações | Agregação, renomeação e cálculo envolvido datas. |
| Saída refinada | Arquivos refinados em `s3/refined/...`. |

## ⚠️ Observações

- Este repositório exemplifica a lógica do pipeline sem utilizar serviços de nuvem.
- Para uso em produção ou escalabilidade, considere adaptar os scripts para execução em data lakes, Spark, PostgreSQL, etc.
- Os códigos demonstram o fluxo esperado, mas não são auto‑executáveis sem ambiente local configurado, sendo executado sobdemanda.

---
