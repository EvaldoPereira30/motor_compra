import pandas as pd


def importar_industria(caminho_arquivo: str) -> pd.DataFrame:
    df = pd.read_excel(
        caminho_arquivo,
        header=None,
        dtype=str
    )

    # Remove linhas acima do cabeçalho real
    df = df.iloc[5:].copy()

    # Mantém apenas as 18 colunas esperadas
    df = df.iloc[:, :18]

    df.columns = [
        "EAN",
        "CodProduto",
        "DescricaoIndustria",

        "Default_Faixa2_Min",
        "Default_Faixa2_Desc",
        "Default_Faixa2_Preco",

        "Default_Faixa1_Min",
        "Default_Faixa1_Desc",
        "Default_Faixa1_Preco",

        "Default_Desc",
        "Default_Preco",
        "Preco_Fabrica",

        "Campanha_Faixa2_Min",
        "Campanha_Faixa2_Desc",
        "Campanha_Faixa2_Preco",

        "Campanha_Faixa1_Min",
        "Campanha_Faixa1_Desc",
        "Campanha_Faixa1_Preco",
    ]

    # Remove linhas sem produto
    df = df.dropna(subset=["CodProduto"])

    # Limpa código
    df["CodProduto"] = (
        df["CodProduto"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    # Remove produto com código 0, se existir
    df = df[df["CodProduto"] != "0"]

    # Converte campos numéricos
    colunas_numericas = [
        "Default_Faixa2_Min",
        "Default_Faixa2_Desc",
        "Default_Faixa2_Preco",
        "Default_Faixa1_Min",
        "Default_Faixa1_Desc",
        "Default_Faixa1_Preco",
        "Default_Desc",
        "Default_Preco",
        "Preco_Fabrica",
        "Campanha_Faixa2_Min",
        "Campanha_Faixa2_Desc",
        "Campanha_Faixa2_Preco",
        "Campanha_Faixa1_Min",
        "Campanha_Faixa1_Desc",
        "Campanha_Faixa1_Preco",
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0)

    return df


if __name__ == "__main__":
    industria = importar_industria(r"entrada\Industria Opella.xlsx")

    print("\n=== COLUNAS INDÚSTRIA ===")
    print(industria.columns.tolist())

    print("\n=== PRIMEIRAS 5 LINHAS LIMPAS ===")
    print(industria.head())

    print(f"\nTotal de registros limpos: {len(industria)}")