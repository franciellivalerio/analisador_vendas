import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Leitura e preparação dos dados
# ==============================
df = pd.read_csv("data/vendas.csv", parse_dates=["data"])
df.dropna(subset=["produto", "quantidade", "preco_unitario"], inplace=True)

if "valor_total" not in df.columns:
    df["valor_total"] = df["quantidade"] * df["preco_unitario"]

# Estatísticas
print("\n📊 Estatísticas gerais:")
print(df.describe())

receita_total = df["valor_total"].sum()
print(f"\n💰 Receita Total: R$ {receita_total:,.2f}")

receita_media = df["valor_total"].mean()
print(f"📈 Receita Média por venda: R$ {receita_media:,.2f}")

top_produtos = (
    df.groupby("produto")["quantidade"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
print("\n🏆 Top 5 produtos mais vendidos (em quantidade):")
print(top_produtos)

# ==============================
# Análises temporais
# ==============================
df["mes"] = df["data"].dt.to_period("M")
receita_mensal = df.groupby("mes")["valor_total"].sum()
qtd_mensal = df.groupby("mes")["quantidade"].sum()

plt.style.use("seaborn-v0_8")

# ==============================
# Gráfico 1: Receita mensal
# ==============================
fig, ax = plt.subplots(figsize=(12,6))
receita_mensal.plot(kind="line", marker="o", color="blue", ax=ax)

for x, y in zip(receita_mensal.index.astype(str), receita_mensal.values):
    ax.annotate(f"{y/1e6:.2f}M", 
                (x, y),
                textcoords="offset points", 
                xytext=(0,10),
                ha="center", 
                va="bottom",
                fontsize=9,
                color="black",
                rotation=30)

ax.set_title("Receita Mensal")
ax.set_xlabel("Mês")
ax.set_ylabel("Receita (em milhões de R$)")

# Mostra apenas 0.5 e 1.0 no eixo Y
ax.set_yticks([0.5e6, 1.0e6])  
ax.set_yticklabels(["0.5M", "1.0M"])  

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("img/receita_mensal.png")
plt.show()

# ==============================
# Gráfico 2: Quantidade de vendas por mês
# ==============================
fig, ax = plt.subplots(figsize=(12,6))
barras = qtd_mensal.plot(kind="bar", color="green", ax=ax)

ax.set_title("Quantidade de Vendas por Mês")
ax.set_xlabel("Mês")
ax.set_ylabel("Quantidade")

ax.bar_label(barras.containers[0], fmt="%.0f", fontsize=9)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("img/quantidade_mensal.png")
plt.show()

# ==============================
# Gráfico 3: Top 5 produtos mais vendidos
# ==============================
fig, ax = plt.subplots(figsize=(8,5))
barras = top_produtos.plot(kind="barh", color="orange", ax=ax)

ax.set_title("Top 5 Produtos Mais Vendidos")
ax.set_xlabel("Quantidade")
ax.set_ylabel("Produto")

ax.bar_label(barras.containers[0], fmt="%.0f", fontsize=9)
plt.tight_layout()
plt.savefig("img/top_produtos.png")
plt.show()
