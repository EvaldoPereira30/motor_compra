import pandas as pd


MESES_3M = [
    "junho/2026",
    "maio/2026",
    "abril/2026",
]

MESES_6M = [
    "junho/2026",
    "maio/2026",
    "abril/2026",
    "março/2026",
    "fevereiro/2026",
    "janeiro/2026",
]

MESES_12M = [
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
]


def gerar_base_decisao_lojas(
    estoque: pd.DataFrame,
    vendas: pd.DataFrame,
    industria: pd.DataFrame
) -> pd.DataFrame:

    produtos_industria = set(industria["CodProduto"])

    estoque_base = estoque[
        estoque["CodProduto"].isin(produtos_industria)
    ].copy()

    vendas_base = vendas[
        vendas["CodProduto"].isin(produtos_industria)
    ].copy()

    vendas_base["Venda_3M"] = vendas_base[MESES_3M].sum(axis=1)
    vendas_base["Venda_6M"] = vendas_base[MESES_6M].sum(axis=1)
    vendas_base["Venda_12M"] = vendas_base[MESES_12M].sum(axis=1)

    vendas_base = vendas_base[
        [
            "CodFilial",
            "CodProduto",
            "Venda_3M",
            "Venda_6M",
            "Venda_12M",
        ]
    ]

    base = estoque_base.merge(
        vendas_base,
        on=["CodFilial", "CodProduto"],
        how="left"
    )

    base[["Venda_3M", "Venda_6M", "Venda_12M"]] = base[
        ["Venda_3M", "Venda_6M", "Venda_12M"]
    ].fillna(0)

    base["Media_3M"] = base["Venda_3M"] / 3
    base["Media_6M"] = base["Venda_6M"] / 6
    base["Media_12M"] = base["Venda_12M"] / 12

    base["Dias_Estoque_3M"] = (
        base["QtEstoqueComercial"] / base["Media_3M"]
    ).replace([float("inf")], 9999)

    base["Dias_Estoque_6M"] = (
        base["QtEstoqueComercial"] / base["Media_6M"]
    ).replace([float("inf")], 9999)

    base["Dias_Estoque_12M"] = (
        base["QtEstoqueComercial"] / base["Media_12M"]
    ).replace([float("inf")], 9999)

    base["Dias_Estoque_3M"] *= 30
    base["Dias_Estoque_6M"] *= 30
    base["Dias_Estoque_12M"] *= 30

    base["Dias_Estoque_3M"] = base["Dias_Estoque_3M"].fillna(9999)
    base["Dias_Estoque_6M"] = base["Dias_Estoque_6M"].fillna(9999)
    base["Dias_Estoque_12M"] = base["Dias_Estoque_12M"].fillna(9999)

    base["Elegivel_Compra"] = "NÃO"

    base.loc[
        base["StatusProduto"] == "ATIVO",
        "Elegivel_Compra"
    ] = "SIM"

    base["Motivo_Nao_Compra"] = ""

    base.loc[
        base["Elegivel_Compra"] == "NÃO",
        "Motivo_Nao_Compra"
    ] = "Status: " + base["StatusProduto"].astype(str)

    base["Loja_Zerada_Com_Demanda"] = "NÃO"

    base.loc[
        (base["QtEstoqueComercial"] == 0) &
        (base["MediaF"] > 0.1),
        "Loja_Zerada_Com_Demanda"
    ] = "SIM"

    def classificar_cobertura(dias):
        if dias == 0:
            return "Ruptura"
        elif dias >= 9999:
            return "Sem venda"
        elif dias <= 30:
            return "Crítico"
        elif dias <= 60:
            return "Baixo"
        elif dias <= 90:
            return "Adequado"
        else:
            return "Excesso"

    base["Faixa_Cobertura_3M"] = base["Dias_Estoque_3M"].apply(classificar_cobertura)

    return base