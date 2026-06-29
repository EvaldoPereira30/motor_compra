import pandas as pd


def gerar_motor_compra(
    base_produto: pd.DataFrame,
    dias_alvo: int = 90,
    media_base: str = "Media_Utilizada"
) -> pd.DataFrame:

    motor = base_produto.copy()

    motor["Media_Base_Usada"] = media_base
    motor["Valor_Media_Base"] = motor[media_base]

    motor["Dias_Alvo"] = dias_alvo

    motor["Dias_Estoque_Atual"] = (
        motor["Estoque_Total"] / motor["Valor_Media_Base"]
    ).replace([float("inf")], 9999)

    motor["Dias_Estoque_Atual"] = motor["Dias_Estoque_Atual"] * 30
    motor["Dias_Estoque_Atual"] = motor["Dias_Estoque_Atual"].fillna(9999)

    motor["Estoque_Alvo"] = motor["Valor_Media_Base"] * (dias_alvo / 30)

    motor["Necessidade_Compra"] = (
        motor["Estoque_Alvo"] - motor["Estoque_Total"]
    )

    motor.loc[
        motor["Necessidade_Compra"] < 0,
        "Necessidade_Compra"
    ] = 0

    motor.loc[
        motor["Elegivel_Compra"] == "NÃO",
        "Necessidade_Compra"
    ] = 0

    motor["Necessidade_Compra"] = (
        motor["Necessidade_Compra"]
        .round(0)
        .astype(int)
    )

    colunas = [
        "CodProduto",
        "Descricao",
        "Fabricante",
        "Linha",
        "StatusProduto",
        "Elegivel_Compra",
        "Motivo_Nao_Compra",
        "Estoque_Lojas",
        "Estoque_CD",
        "Estoque_Total",
        "Media_Base_Usada",
        "Valor_Media_Base",
        "Dias_Estoque_Atual",
        "Dias_Alvo",
        "Estoque_Alvo",
        "Necessidade_Compra",
    ]

    return motor[colunas]