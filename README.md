<div align="center">

# ✈️ TURISMODATA BR

### Estimativas de chegadas de turistas internacionais ao Brasil

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-data%20analysis-E70013?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![MySQL](https://img.shields.io/badge/MySQL-database-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

*Do dado bruto ao banco relacional — um pipeline de ETL completo em Python*

</div>

---

## 📌 Sobre o projeto

O **TurismoData BR** transforma uma planilha bruta com as chegadas de turistas estrangeiros ao Brasil em um banco relacional pronto para análise. O dados passam por auditoria de qualidade, padronização e modelagem em **esquema estrela**, terminando em um MySQL com relatórios analíticos consultáveis por um menu interativo.

## ✨ Destaques

- 🔍 **Auditoria de dados** — nulos, duplicatas, valores inválidos e inconsistências detectados automaticamente
- 🧹 **Padronização** — nomes de países normalizados (ex.: *Holanda → Países Baixos*, *Cingapura → Singapura*)
- 🏗️ **Star schema** — 4 dimensões + 1 tabela fato com chaves surrogate
- 💾 **Carga transacional** — inserção em massa no MySQL com commit/rollback
- 📊 **Consultas analíticas** — menu interativo com 6 relatórios prontos (países, UFs, vias, meses…)

## 🗂️ Modelo de dados

```
        dim_pais ◄──┐
        dim_uf   ◄──┤
 dim_via  ◄──┼── fato_chegadas
        dim_mes  ◄──┘
```

| Tabela | Registros | Conteúdo |
|:---:|:---:|:---|
| `dim_pais` | 202 | Países de origem |
| `dim_uf` | 27 | Destinos com sigla e região |
| `dim_via` | 4 | Aérea, Terrestre, Marítima, Fluvial |
| `dim_mes` | 12 | Meses do ano |
| `fato_chegadas` | ~19.7 mil | Chegadas agregadas por combinação |

## 🚀 Começo rápido

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python tratamento.py   # limpa e modela os dados
python banco.py        # carrega no MySQL
python consultas.py    # menu de consultas 📊
```

> 💡 Requer um MySQL local rodando e o arquivo `chegadas-2025.csv` na raiz do projeto (não versionado).

## 📄 Licença

Distribuído sob a licença [MIT](LICENSE) — © 2026 João Victor Feliciano dos Santos.
