import pandas as pd

CAMINHO_ARQUIVO = "chegadas-2025.csv"

def carregar_dados():

    df = pd.read_csv(CAMINHO_ARQUIVO, sep=";", encoding="latin1")
    return df


def analisar_estrutura(df):
    print("\nESQUEMA ORIGINAL:")

    print(f"\nQuantidade de linhas: {df.shape[0]}")
    print(f"Quantidade de colunas: {df.shape[1]}")

    print("\nColunas:")
    print(df.columns.tolist())

    print("\nTipos de dados:")
    print(df.dtypes)

    print("\nPrimeiras linhas:")
    print(df.head().to_string(index=False))


def main():

    df = carregar_dados()
    analisar_estrutura(df)
    
    

if __name__ == "__main__":
    main()
