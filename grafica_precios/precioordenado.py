import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

# Cargar el JSON desde un archivo
with open("../registros.json", "r") as file:
    json_data = json.load(file)

# Obtener la lista de productos del JSON
products = json_data["products"]

# Crear una lista para almacenar los datos de los productos
data = []

# Iterar sobre los productos y extraer los datos relevantes
for product in products:
    title = product["Title"]
    price = product.get("DiscountPrice", product["OriginalPrice"])
    data.append({"Title": title, "Price": price})

# Ordenar los productos por precio de forma ascendente
data.sort(key=lambda x: x["Price"])

# Convertir los datos en un DataFrame
data = pd.DataFrame(data)

# Generar colores aleatorios para cada producto
colors = random.sample(list(mcolors.CSS4_COLORS.values()), k=len(data))

# Crear una figura con un subplot
fig, ax = plt.subplots(figsize=(10, 6))

# Configurar el gráfico de línea
ax.plot(data.index, data["Price"], marker="o", linewidth=2, markersize=8, color="blue")
ax.fill_between(data.index, data["Price"], alpha=0.2, color="blue")
ax.set_ylim(bottom=0)
ax.set_title("Precios de los Productos (Ordenados de menor a mayor)")
ax.set_xlabel("Productos")
ax.set_ylabel("Precio")

# Agregar los puntos con los colores correspondientes
for i in range(len(data)):
    ax.plot(i, data.loc[i, "Price"], marker="o", markersize=8, color=colors[i % len(colors)])
    ax.text(i + 0.1, data.loc[i, "Price"], ".", color=colors[i % len(colors)], fontsize=12, ha="center", va="center")

# Obtener los nombres de los puntos asociados a los colores
legend_labels = data["Title"].tolist()

# Crear la guía de colores en el gráfico
legend_handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=colors[i % len(colors)], markersize=8) for i in range(len(data))]
ax.legend(legend_handles, legend_labels, loc="upper left", fontsize=8)

# Calcular el precio mínimo y máximo
min_price = data["Price"].min()
max_price = data["Price"].max()

# Agregar el texto con el precio mínimo y máximo al gráfico
ax.text(len(data) - 1, min_price, f"Min: ${min_price}", ha="left", va="bottom", fontsize=10)
ax.text(len(data) - 1, max_price, f"Max: ${max_price}", ha="left", va="top", fontsize=10)

# Mostrar la figura
plt.show()
