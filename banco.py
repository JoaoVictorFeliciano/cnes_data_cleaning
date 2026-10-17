import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

PASTA_DADOS = "dados_tratados"

CONFIGURACAO = {
    "host": "localhost",
    "user": "root",
    "password": "davi140714",
    "database": "turismo_dados"
}

def conectar():
    return mysql.connector.connect(**CONFIGURACAO)

def carregar_csv(nome_arquivo):
    caminho = os.path.join(PASTA_DADOS, nome_arquivo)

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    return pd.read_csv(caminho, sep=";", encoding="utf-8")


def inserir_dados(conexao, tabela, df, colunas):
    df = df[colunas].copy()
    df = df.astype(object).where(pd.notna(df), None)

    nomes_colunas = ", ".join(colunas)
    marcadores = ", ".join(["%s"] * len(colunas))

    comando = (f"INSERT INTO {tabela} ({nomes_colunas}) " f"VALUES ({marcadores})")

    cursor = conexao.cursor()

    try:
        registros = list(df.itertuples(index=False, name=None))

        if registros:
            cursor.executemany(comando, registros)

        conexao.commit()
        print(f"{tabela}: {len(registros)} registros inseridos.")

    except Error:
        conexao.rollback()
        raise

    finally:
        cursor.close()


def popular_banco(conexao):

    pais = carregar_csv("dim_pais.csv")
    uf = carregar_csv("dim_uf.csv")
    via = carregar_csv("dim_via.csv")
    mes = carregar_csv("dim_mes.csv")
    fato = carregar_csv("fato_chegadas.csv")

    inserir_dados(conexao, "dim_pais", pais,["id_pais", "nome_pais"])

    inserir_dados(conexao, "dim_uf", uf,["id_uf", "nome_uf", "sigla_uf", "regiao"])

    inserir_dados(conexao, "dim_via", via,["id_via", "via_acesso"])

    inserir_dados(conexao, "dim_mes", mes,["id_mes", "nome_mes", "numero_mes"])

    inserir_dados(conexao, "fato_chegadas", fato,[    "id_chegada", "id_pais", "id_uf",    "id_via", "id_mes", "ano", "quantidade" ])

def main():
    
    conexao = None

    try:
        conexao = conectar()
        print("Conexão com o MySQL estabelecida.")

        popular_banco(conexao)
        print("\nBanco populado com sucesso!")

    except (Error, FileNotFoundError, KeyError, ValueError) as erro:
        print(f"\nErro ao popular o banco: {erro}")

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()
            print("Conexão encerrada.")


if __name__ == "__main__":
    main()