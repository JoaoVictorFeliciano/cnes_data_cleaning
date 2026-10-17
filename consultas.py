from banco import conectar

def executar_consulta(sql):
    #Executa uma consulta SQL e retorna os resultados
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql)

        resultados = cursor.fetchall()
        return resultados

    except Exception as erro:
        print(f"Erro ao executar consulta: {erro}")
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()


def consultar_paises():
    #Retorna os 10 países com mais chegadas ao brasil
    sql = """
        SELECT
            p.nome_pais,
            SUM(f.quantidade) AS total_chegadas
        FROM fato_chegadas f
        JOIN dim_pais p ON f.id_pais = p.id_pais
        GROUP BY p.id_pais, p.nome_pais
        ORDER BY total_chegadas DESC
        LIMIT 10;
    """

    return executar_consulta(sql)


def consultar_vias():
    #Retorna o total de chegadas por via de acesso
    sql = """
        SELECT
            v.via_acesso,
            SUM(f.quantidade) AS total_chegadas
        FROM fato_chegadas f
        JOIN dim_via v ON f.id_via = v.id_via
        GROUP BY v.id_via, v.via_acesso
        ORDER BY total_chegadas DESC;
    """

    return executar_consulta(sql)


def consultar_estados():
    #Retorna os 10 estados com mais chegadas
    sql = """
        SELECT
            u.nome_uf,
            u.sigla_uf,
            SUM(f.quantidade) AS total_chegadas
        FROM fato_chegadas f
        JOIN dim_uf u ON f.id_uf = u.id_uf
        GROUP BY u.id_uf, u.nome_uf, u.sigla_uf
        ORDER BY total_chegadas DESC
        LIMIT 10;
    """

    return executar_consulta(sql)


def consultar_mes():
    #Retorna o mês com mais chegadas
    sql = """
        SELECT
            m.nome_mes,
            SUM(f.quantidade) AS total_chegadas
        FROM fato_chegadas f
        JOIN dim_mes m ON f.id_mes = m.id_mes
        GROUP BY m.id_mes, m.nome_mes, m.numero_mes
        ORDER BY total_chegadas DESC
        LIMIT 1;
    """

    return executar_consulta(sql)


def consultar_total():
    #Retorna a soma total de chegadas registradas
    sql = """
        SELECT SUM(quantidade) AS total_chegadas
        FROM fato_chegadas;
    """

    return executar_consulta(sql)


def consultar_paises_por_via():
    #Retorna os 15 maiores totais por país e via de acesso
    sql = """
        SELECT
            p.nome_pais,
            v.via_acesso,
            SUM(f.quantidade) AS total_chegadas
        FROM fato_chegadas f
        JOIN dim_pais p ON f.id_pais = p.id_pais
        JOIN dim_via v ON f.id_via = v.id_via
        GROUP BY
            p.id_pais,
            p.nome_pais,
            v.id_via,
            v.via_acesso
        ORDER BY total_chegadas DESC
        LIMIT 15;
    """

    return executar_consulta(sql)


def exibir_resultados(resultados):
    #Exibe os resultados de uma consulta no terminal
    if not resultados:
        print("Nenhum resultado encontrado.")
        return

    for registro in resultados:
        print(" | ".join(f"{coluna}: {valor}" for coluna, valor in registro.items()))


def main():
    while True:
        print("TURISMODATA BR:")
        print("1 - Países com mais chegadas")
        print("2 - Chegadas por via de acesso")
        print("3 - Estados com mais chegadas")
        print("4 - Mês com mais chegadas")
        print("5 - Total de chegadas")
        print("6 - Países e vias de acesso")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            resultados = consultar_paises()
        elif opcao == "2":
            resultados = consultar_vias()
        elif opcao == "3":
            resultados = consultar_estados()
        elif opcao == "4":
            resultados = consultar_mes()
        elif opcao == "5":
            resultados = consultar_total()
        elif opcao == "6":
            resultados = consultar_paises_por_via()
        elif opcao == "0":
            print("Encerrando TurismoData BR")
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue

        print()
        exibir_resultados(resultados)


if __name__ == "__main__":
    main()
