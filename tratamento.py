import os
import pandas as pd
from analise import carregar_dados

PASTA_SAIDA = "dados_tratados"

VIAS_VALIDAS = ["Aérea", "Terrestre", "Marítima", "Fluvial"]

MESES = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3,
    "Abril": 4, "Maio": 5, "Junho": 6,
    "Julho": 7, "Agosto": 8, "Setembro": 9,
    "Outubro": 10, "Novembro": 11, "Dezembro": 12
}

UF_INFO = {
    "Acre": ("AC", "Norte"),
    "Alagoas": ("AL", "Nordeste"),
    "Amapá": ("AP", "Norte"),
    "Amazonas": ("AM", "Norte"),
    "Bahia": ("BA", "Nordeste"),
    "Ceará": ("CE", "Nordeste"),
    "Distrito Federal": ("DF", "Centro-Oeste"),
    "Espírito Santo": ("ES", "Sudeste"),
    "Goiás": ("GO", "Centro-Oeste"),
    "Maranhão": ("MA", "Nordeste"),
    "Mato Grosso": ("MT", "Centro-Oeste"),
    "Mato Grosso do Sul": ("MS", "Centro-Oeste"),
    "Minas Gerais": ("MG", "Sudeste"),
    "Pará": ("PA", "Norte"),
    "Paraíba": ("PB", "Nordeste"),
    "Paraná": ("PR", "Sul"),
    "Pernambuco": ("PE", "Nordeste"),
    "Piauí": ("PI", "Nordeste"),
    "Rio de Janeiro": ("RJ", "Sudeste"),
    "Rio Grande do Norte": ("RN", "Nordeste"),
    "Rio Grande do Sul": ("RS", "Sul"),
    "Rondônia": ("RO", "Norte"),
    "Roraima": ("RR", "Norte"),
    "Santa Catarina": ("SC", "Sul"),
    "São Paulo": ("SP", "Sudeste"),
    "Sergipe": ("SE", "Nordeste"),
    "Tocantins": ("TO", "Norte")
}

SINONIMOS_PAISES = {
    "Barein": "Bahrein",
    "Casaquistão": "Cazaquistão",
    "Cingapura": "Singapura",
    "Mianma": "Mianmar",
    "Seichelles": "Seicheles",
    "Suazilândia": "Essuatíni",
    "Macedônia": "Macedônia do Norte",
    "República Tcheca": "Chéquia",
    "República da Coreia": "Coreia do Sul",
    "Holanda": "Países Baixos",
    "Vaticano": "Santa Sé",
    "Timor Leste": "Timor-Leste"
}


def identificar_nulos(df):
    print("\n=== VALORES NULOS ===")
    print(df.isna().sum())
    print(f"Total de valores nulos: {df.isna().sum().sum()}")


def identificar_duplicadas(df):
    print("\n=== DUPLICATAS ===")

    duplicadas = df[df.duplicated(keep=False)]

    print(f"Linhas totalmente duplicadas: {df.duplicated().sum()}")

    if not duplicadas.empty:
        print("\nExemplos:")
        print(duplicadas.head(5).to_string(index=False))

    return duplicadas


def identificar_inconsistencias(df):
    print("\n=== INCONSISTÊNCIAS ===")

    meses_invalidos = df[~df["mes"].isin(MESES)]
    vias_invalidas = df[~df["Via_de_acesso"].isin(VIAS_VALIDAS)]
    chegadas_invalidas = df[df["Chegadas"] <= 0]

    print(f"Meses inválidos: {len(meses_invalidos)}")
    print(f"Vias inválidas: {len(vias_invalidas)}")
    print(f"Chegadas menores ou iguais a zero: {len(chegadas_invalidas)}")

    if not meses_invalidos.empty:
        print(meses_invalidos.head().to_string(index=False))

    if not vias_invalidas.empty:
        print(vias_invalidas.head().to_string(index=False))

    if not chegadas_invalidas.empty:
        print(chegadas_invalidas.head().to_string(index=False))

    ufs_desconhecidas = sorted(set(df["UF"]) - set(UF_INFO))
    print(f"UFs sem correspondência no cadastro: {ufs_desconhecidas}")

    return meses_invalidos, vias_invalidas, chegadas_invalidas


def identificar_sinonimos(df):
    print("\n=== SINÔNIMOS DE PAÍSES ===")

    paises = df["nome_pais_correto"]
    encontrados = {
        nome: sinonimo
        for nome, sinonimo in SINONIMOS_PAISES.items()
        if nome in paises.values
    }

    for nome, sinonimo in encontrados.items():
        print(f"{nome} -> {sinonimo}")

    if not encontrados:
        print("Nenhuma variante cadastrada foi encontrada.")

    depois = paises.replace(SINONIMOS_PAISES)

    print(f"Países distintos antes: {paises.nunique()}")
    print(f"Países distintos após padronização: {depois.nunique()}")

    return encontrados


def padronizar(df):
    df = df.copy()

    colunas_texto = [
        "Via_de_acesso", "UF", "nome_pais_correto", "mes"
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    df["nome_pais_correto"] = df["nome_pais_correto"].replace(
        SINONIMOS_PAISES
    )

    return df


def montar_dimensoes(df):
    dim_pais = pd.DataFrame({
        "id_pais": range(1, df["nome_pais_correto"].nunique() + 1),
        "nome_pais": sorted(df["nome_pais_correto"].unique())
    })

    dim_uf = pd.DataFrame([
        {
            "id_uf": i,
            "nome_uf": nome,
            "sigla_uf": dados[0],
            "regiao": dados[1]
        }
        for i, (nome, dados) in enumerate(UF_INFO.items(), start=1)
    ])

    dim_via = pd.DataFrame({
        "id_via": range(1, len(VIAS_VALIDAS) + 1),
        "via_acesso": VIAS_VALIDAS
    })

    dim_mes = pd.DataFrame({
        "id_mes": range(1, 13),
        "nome_mes": list(MESES.keys()),
        "numero_mes": list(MESES.values())
    })

    return dim_pais, dim_uf, dim_via, dim_mes


def montar_fato(df, dimensoes):
    dim_pais, dim_uf, dim_via, dim_mes = dimensoes

    fato = df.groupby(
        ["nome_pais_correto", "UF", "Via_de_acesso", "mes", "ano"],
        as_index=False
    )["Chegadas"].sum()

    fato = fato.merge(
        dim_pais, left_on="nome_pais_correto",
        right_on="nome_pais"
    )
    fato = fato.merge(
        dim_uf, left_on="UF", right_on="nome_uf"
    )
    fato = fato.merge(
        dim_via, left_on="Via_de_acesso",
        right_on="via_acesso"
    )
    fato = fato.merge(
        dim_mes, left_on="mes", right_on="nome_mes"
    )

    fato = fato[[
        "id_pais", "id_uf", "id_via",
        "id_mes", "ano", "Chegadas"
    ]]

    fato = fato.rename(columns={"Chegadas": "quantidade"})
    fato.insert(0, "id_chegada", range(1, len(fato) + 1))

    return fato


def salvar_tabelas(tabelas):
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    for nome, tabela in tabelas.items():
        caminho = os.path.join(PASTA_SAIDA, f"{nome}.csv")
        tabela.to_csv(
            caminho, sep=";", index=False, encoding="utf-8"
        )
        print(f"Arquivo salvo: {caminho} ({len(tabela)} registros)")


def tratar():
    df = carregar_dados()

    print(f"Registros originais: {len(df)}")

    identificar_nulos(df)
    identificar_duplicadas(df)
    identificar_inconsistencias(df)
    identificar_sinonimos(df)

    df = padronizar(df)

    dimensoes = montar_dimensoes(df)
    fato = montar_fato(df, dimensoes)

    tabelas = {
        "dim_pais": dimensoes[0],
        "dim_uf": dimensoes[1],
        "dim_via": dimensoes[2],
        "dim_mes": dimensoes[3],
        "fato_chegadas": fato
    }

    salvar_tabelas(tabelas)

    print("\n=== RESUMO ===")
    print(f"Registros originais: {len(df)}")
    print(f"Registros na tabela de chegadas: {len(fato)}")

    return tabelas


def main():
    tratar()


if __name__ == "__main__":
    main()
