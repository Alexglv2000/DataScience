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
    
    if isinstance(product["RatingOpinion"], list):
        good = next((opinion["Amount"] for opinion in product["RatingOpinion"] if opinion["Rating"] == "Good"), 0)
        bad = next((opinion["Amount"] for opinion in product["RatingOpinion"] if opinion["Rating"] == "Bad"), 0)
        regular = next((opinion["Amount"] for opinion in product["RatingOpinion"] if opinion["Rating"] == "Regular"), 0)
    else:
        good = product["RatingOpinion"]["Amount"] if product["RatingOpinion"]["Rating"] == "Good" else 0
        bad = product["RatingOpinion"]["Amount"] if product["RatingOpinion"]["Rating"] == "Bad" else 0
        regular = product["RatingOpinion"]["Amount"] if product["RatingOpinion"]["Rating"] == "Regular" else 0
    
    data.append({"Title": title, "Price": price, "Good": good, "Bad": bad, "Regular": regular})


# Convertir los datos en un DataFrame
data = pd.DataFrame(data)

# Generar colores aleatorios para cada producto
categories = data["Title"].apply(lambda x: str(hash(x)))[-6:]
colors = random.choices(list(mcolors.CSS4_COLORS.values()), k=len(categories))

# Crear una figura con dos subplots
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), gridspec_kw={"width_ratios": [3, 1]})

# Configurar el primer subplot con el gráfico de línea
ax1.plot(data.index, data["Good"], marker="o", linewidth=2, markersize=8, color='green', label='Good')
ax1.plot(data.index, data["Bad"], marker="o", linewidth=2, markersize=8, color='red', label='Bad')
ax1.plot(data.index, data["Regular"], marker="o", linewidth=2, markersize=8, color='blue', label='Regular')

# Agregar las sombras para cada línea
ax1.fill_between(data.index, data["Good"], alpha=0.2, color='green')
ax1.fill_between(data.index, data["Bad"], alpha=0.2, color='red')
ax1.fill_between(data.index, data["Regular"], alpha=0.2, color='blue')

ax1.set_ylim(bottom=0)
ax1.set_title("Popularidad de los Productos")
ax1.set_xlabel("Productos")
ax1.set_ylabel("Cantidad de Opiniones")
# Agregar los colores junto a las líneas del gráfico
for i in range(len(data)):
    ax1.plot(i, data.loc[i, "Good"], marker="o", markersize=8, color='green')
    ax1.plot(i, data.loc[i, "Bad"], marker="o", markersize=8, color='red')
    ax1.plot(i, data.loc[i, "Regular"], marker="o", markersize=8, color='blue')
    ax1.text(i + 0.1, data.loc[i, "Good"], ".", color='green', fontsize=12, ha="center", va="center")
    ax1.text(i + 0.1, data.loc[i, "Bad"], ".", color='red', fontsize=12, ha="center", va="center")
    ax1.text(i + 0.1, data.loc[i, "Regular"], ".", color='blue', fontsize=12, ha="center", va="center")

# Obtener los nombres de los puntos asociados a los colores
legend_labels = data["Title"].tolist()

# Crear la guía de colores en el segundo subplot
ax2.axis("off")
legend_handles = [ax2.plot(0, 0, marker="o", markersize=8, color=color)[0] for color in colors]
ax2.legend(legend_handles, legend_labels, loc="center", fontsize=8)

# Calcular la cantidad mínima y máxima de opiniones
min_opinions = data[["Good", "Bad", "Regular"]].min().min()
max_opinions = data[["Good", "Bad", "Regular"]].max().max()

# Agregar el texto con la cantidad mínima y máxima al gráfico
ax1.text(len(data), min_opinions, f"Min: {min_opinions}", ha="left", va="bottom", fontsize=10)
ax1.text(len(data), max_opinions, f"Max: {max_opinions}", ha="left", va="top", fontsize=10)

# Mostrar la figura
plt.show()


