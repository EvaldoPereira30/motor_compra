from importar_estoque import importar_estoque
from importar_vendas import importar_vendas
from importar_industria import importar_industria
from gerar_produtos_cotacao import gerar_produtos_cotacao
from gerar_base_decisao_produto import gerar_base_decisao_produto
from gerar_base_decisao_lojas import gerar_base_decisao_lojas
from gerar_motor_compra import gerar_motor_compra

estoque = importar_estoque(r"entrada\Estoque Opella.txt")
vendas = importar_vendas(r"entrada\Vendas Opella.txt")
industria = importar_industria(r"entrada\Industria Opella.xlsx")

print("\n=== RESUMO ===")
print(f"Estoque: {len(estoque)} registros")
print(f"Vendas: {len(vendas)} registros")
print(f"Indústria: {len(industria)} registros")

produtos_estoque = set(estoque["CodProduto"])
produtos_vendas = set(vendas["CodProduto"])
produtos_industria = set(industria["CodProduto"])

print("\n=== VALIDAÇÃO ===")
print(f"Produtos Estoque: {len(produtos_estoque)}")
print(f"Produtos Vendas: {len(produtos_vendas)}")
print(f"Produtos Indústria: {len(produtos_industria)}")

print(
    f"Produtos Estoque x Indústria: "
    f"{len(produtos_estoque.intersection(produtos_industria))}"
)

print(
    f"Produtos Vendas x Indústria: "
    f"{len(produtos_vendas.intersection(produtos_industria))}"
)

cruzamento = produtos_estoque.intersection(produtos_industria)

print("\n=== PRIMEIROS 20 PRODUTOS CRUZADOS ===")
print(sorted(list(cruzamento))[:20])

print("\n=== PRODUTOS DA INDÚSTRIA NÃO ENCONTRADOS NO ESTOQUE ===")
nao_encontrados = produtos_industria - produtos_estoque
print(sorted(list(nao_encontrados))[:20])
print(f"Total: {len(nao_encontrados)}")

produtos_cotacao = gerar_produtos_cotacao(
    estoque,
    vendas,
    industria
)

produtos_cotacao.to_excel(
    r"saida\produtos_cotacao.xlsx",
    index=False
)

print("\n=== PRODUTOS COTAÇÃO ===")
print(f"Produtos gerados: {len(produtos_cotacao)}")

print("\nArquivo criado:")
print(r"saida\produtos_cotacao.xlsx")


base_decisao_produto = gerar_base_decisao_produto(
    estoque,
    vendas,
    industria
)

base_decisao_produto.to_excel(
    r"saida\Base_Decisao_Produto.xlsx",
    index=False
)

print("\n=== BASE DECISÃO PRODUTO ===")
print(f"Produtos gerados: {len(base_decisao_produto)}")
print(r"Arquivo criado: saida\Base_Decisao_Produto.xlsx")

base_decisao_lojas = gerar_base_decisao_lojas(
    estoque,
    vendas,
    industria
)

base_decisao_lojas.to_excel(
    r"saida\Base_Decisao_Lojas.xlsx",
    index=False
)

print("\n=== BASE DECISÃO LOJAS ===")
print(f"Registros gerados: {len(base_decisao_lojas)}")
print(r"Arquivo criado: saida\Base_Decisao_Lojas.xlsx")

motor_compra = gerar_motor_compra(
    base_decisao_produto,
    dias_alvo=90,
    media_base="Media_Utilizada"
)

motor_compra.to_excel(
    r"saida\Motor_Compra.xlsx",
    index=False
)

print("\n=== MOTOR COMPRA ===")
print(f"Produtos analisados: {len(motor_compra)}")
print(r"Arquivo criado: saida\Motor_Compra.xlsx")