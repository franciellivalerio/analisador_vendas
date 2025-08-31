import pandas as pd
import matplotlib.pyplot as plt

# Carregar dataset
df = pd.read_csv("data/vendas.csv", parse_dates=["data"])

# Estatísticas básicas
print("📊 Estatísticas gerais:")
print(df.describe())

# Receita total
receita_total = df["valor_total"].sum()
print(f"\n💰 Receita Total: R$ {receita_total:,.2f}")

# Top 5 produtos mais vendidos em quantidade
top_produtos = df.groupby("produto")["quantidade"].sum().sort_values(ascending=False).head(5)
print("\n🏆 Top 5 produtos mais vendidos:")
print(top_produtos)

# Receita mensal
df["mes"] = df["data"].dt.to_period("M")
receita_mensal = df.groupby("mes")["valor_total"].sum()

# Gráfico de receita mensal
plt.figure(figsize=(10,5))
receita_mensal.plot(kind="line", marker="o")
plt.title("Receita Mensal")
plt.xlabel("Mês")
plt.ylabel("Receita (R$)")
plt.grid(True)
plt.show()
