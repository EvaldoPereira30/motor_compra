import pandas as pd


MESES_2026_2025 = [
    "junho/2026",
    "maio/2026",
    "abril/2026",
    "março/2026",
    "fevereiro/2026",
    "janeiro/2026",
    "dezembro/2025",
    "novembro/2025",
    "outubro/2025",
    "setembro/2025",
    "agosto/2025",
    "julho/2025",
    "junho/2025",
    "maio/2025",
    "abril/2025",
    "março/2025",
    "fevereiro/2025",
    "janeiro/2025",
]


def importar_vendas(caminho_arquivo: str) -> pd.DataFrame:
    df = pd.read_csv(
        caminho_arquivo,
        sep=",",
        encoding="latin1",
        skiprows=9,
        dtype=str
    )

    # Mantém somente: 6 fixas + 18 meses
    df = df.iloc[:, :24]

    colunas_fixas = [
        "CodFilial",
        "CodProduto",
        "EAN",
        "DescricaoProduto",
        "Fabricante",
        "Linha",
    ]

    df.columns = colunas_fixas + MESES_2026_2025

    # Remove linhas sem produto
    df = df.dropna(subset=["CodProduto"])

    # Limpa filial ANTES do preenchimento
    df["CodFilial"] = df["CodFilial"].astype(str).str.strip()

    # Transforma valores inválidos em vazio real
    df.loc[
        df["CodFilial"].isin(["", "nan", "NaN", "None", "<NA>"]),
        "CodFilial"
    ] = pd.NA

    # Remove rodapés/logs
    df = df[~df["CodFilial"].astype(str).str.contains("Usuário|H:", na=False)]

    # Preenche filial para baixo
    df["CodFilial"] = df["CodFilial"].ffill()

    # Remove linhas que continuaram sem filial
    df = df.dropna(subset=["CodFilial"])

    # Limpa códigos
    df["CodFilial"] = df["CodFilial"].astype(str).str.strip()

    df["CodProduto"] = (
        df["CodProduto"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    # Converte meses para número
    for coluna in MESES_2026_2025:
        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0)

    return df


if __name__ == "__main__":
    vendas = importar_vendas(r"entrada\Vendas Opella.txt")

    print("\n=== COLUNAS VENDAS ===")
    print(vendas.columns.tolist())

    print("\n=== PRIMEIRAS 5 LINHAS LIMPAS ===")
    print(vendas.head())

    print(f"\nTotal de registros limpos: {len(vendas)}")