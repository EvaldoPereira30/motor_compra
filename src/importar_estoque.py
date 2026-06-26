import pandas as pd


def importar_estoque(caminho_arquivo: str) -> pd.DataFrame:
    df = pd.read_csv(
        caminho_arquivo,
        sep=",",
        encoding="latin1",
        skiprows=2,
        dtype=str
    )

    # Remove linhas sem produto
    df = df.dropna(subset=["CodProduto"])

    # Remove rodapés/logs que venham no campo CodFilial
    df = df[~df["CodFilial"].astype(str).str.contains("Usuário|H:", na=False)]

    # Preenche filial para baixo
    df["CodFilial"] = df["CodFilial"].ffill()

    # Limpa códigos
    df["CodFilial"] = df["CodFilial"].astype(str).str.strip()
    df["CodProduto"] = df["CodProduto"].astype(str).str.replace(".0", "", regex=False).str.strip()

    # Converte colunas numéricas com vírgula decimal
    for coluna in ["MediaF", "QtEstoqueComercial", "Faceamento"]:
        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0)

    # Média utilizada: maior entre MediaF e Faceamento
    df["Media_Utilizada"] = df[["MediaF", "Faceamento"]].max(axis=1)

    return df


if __name__ == "__main__":
    arquivo = r"entrada\Estoque Opella.txt"
    estoque = importar_estoque(arquivo)

    print("\n=== COLUNAS ===")
    print(estoque.columns.tolist())

    print("\n=== PRIMEIRAS 5 LINHAS LIMPAS ===")
    print(estoque.head())

    print(f"\nTotal de registros limpos: {len(estoque)}")

    print("\n=== CD 900 EXISTE? ===")
    print((estoque["CodFilial"] == "900").any())

    print("\n=== TOTAL DE FILIAIS ===")
    print(estoque["CodFilial"].nunique())

    print("\n=== TESTE MEDIA UTILIZADA ===")
    print(estoque[["CodFilial", "CodProduto", "MediaF", "Faceamento", "Media_Utilizada"]].head(10))