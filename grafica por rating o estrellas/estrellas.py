import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

# Cargar el JSON desde un archivo
with open("../offers.json", "r") as file:
    json_data = json.load(file)

# Obtener la lista de productos del JSON
products = json_data["products"]

# Crear una lista para almacenar los datos de los productos
data = []

# Iterar sobre los productos y extraer los datos relevantes
for product in products:
    title = product["Title"]
    price = product.get("DiscountPrice", product["OriginalPrice"])
    rating = float(product["Rating"]["Rating"])
    rating_amount_str = product["Rating"]["Amount"].replace("+", "")
    
    # Omitir los casos en los que Rating es 0 o Amount está vacío
    if rating != 0 and rating_amount_str:
        # Eliminar palabras no numéricas de Amount
        rating_amount_str = ''.join(filter(str.isdigit, rating_amount_str))
        
        # Verificar si rating_amount_str es un número válido
        if rating_amount_str.isdigit():
            rating_amount = int(rating_amount_str)
        else:
            rating_amount = 0
        
        data.append({"Title": title, "Price": price, "Rating": rating, "RatingAmount": rating_amount})

# Convertir los datos en un DataFrame
data = pd.DataFrame(data)

# Obtener el número de productos
num_products = len(data)

# Generar una lista de colores únicos para cada producto
colors = random.choices(list(mcolors.CSS4_COLORS.values()), k=num_products)

# Obtener los nombres truncados de los puntos asociados a los colores
legend_labels = [title[:20] + '...' if len(title) > 20 else title for title in data["Title"].tolist()]

# Obtener el producto con el mejor Rating
best_rating_product = data.loc[data["Rating"].idxmax()]

# Obtener el producto con el peor Rating
worst_rating_product = data.loc[data["Rating"].idxmin()]

# Crear una lista de colores correspondientes a cada producto
product_colors = [colors[legend_labels.index(title)] for title in legend_labels]

# Crear una figura con dos subplots
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), gridspec_kw={"width_ratios": [3, 1]})

# Configurar el primer subplot con el gráfico de línea
ax1.plot(data.index, data["Price"], marker="o", linewidth=2, markersize=8)
ax1.fill_between(data.index, data["Price"], alpha=0.2)
ax1.set_ylim(bottom=0)
ax1.set_title("Precios y Ratings de los Productos")
ax1.set_xlabel("Productos")
ax1.set_ylabel("Precio")

# Agregar los colores junto a la línea del gráfico
for i in range(len(data)):
    ax1.plot(i, data.loc[i, "Price"], marker="o", markersize=8, color=product_colors[i])
    ax1.text(i + 0.1, data.loc[i, "Price"], ".", color=product_colors[i], fontsize=12, ha="center", va="center")

# Crear la guía de colores en el segundo subplot
ax2.axis("off")
legend_handles = [ax2.plot(0, 0, marker="o", markersize=8, color=color)[0] for color in product_colors]
legend_labels.append(f"Best Rating: {best_rating_product['Rating']} ({best_rating_product['RatingAmount']} personas)")
legend_labels.append(f"Worst Rating: {worst_rating_product['Rating']} ({worst_rating_product['RatingAmount']} personas)")
legend_handles.append(ax2.plot(0, 0, marker="o", markersize=8, color="white")[0])  # Espacio en blanco para separar los puntos
legend_handles.append(ax2.plot(0, 0, marker="o", markersize=8, color="white")[0])  # Espacio en blanco para separar los puntos
ax2.legend(legend_handles, legend_labels, loc="center", fontsize=8)

# Mostrar la gráfica
plt.tight_layout()
plt.show()
