import json
import pandas as pd
import matplotlib.pyplot as plt
import random

# Cargar el JSON desde un archivo
with open("../registros.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

# Obtener la lista de productos del JSON
products = json_data["products"]

# Crear listas para almacenar los datos de los productos
titles = []
opinions_bad = []

# Iterar sobre los productos y extraer los datos relevantes
for product in products:
    title = product["Title"]
    rating_opinion = product["RatingOpinion"]
    if isinstance(rating_opinion, dict):  # Caso de un solo rating opinion
        amount = rating_opinion["Amount"]
    elif isinstance(rating_opinion, list):  # Caso de múltiples rating opinion
        amount = sum(opinion["Amount"] for opinion in rating_opinion if opinion["Rating"] == "Bad")
    else:
        amount = 0
    titles.append(title)
    opinions_bad.append(amount)

# Crear un DataFrame con los datos
data = pd.DataFrame({"Título": titles, "Opiniones Bad": opinions_bad})

# Ordenar los datos por cantidad de opiniones Bad en orden descendente
data_sorted = data.sort_values(by="Opiniones Bad", ascending=False)

# Obtener el máximo y mínimo de opiniones Bad y sus títulos correspondientes
max_opinions = data_sorted.iloc[0]
min_opinions = data_sorted.iloc[-1]

# Generar colores aleatorios para las barras
colors = [random.choice(["#"+''.join(random.choices('0123456789ABCDEF', k=6))]) for _ in range(len(data_sorted))]

# Crear el gráfico de barras
plt.bar(data_sorted.index, data_sorted["Opiniones Bad"], color=colors)

# Configurar los ejes y etiquetas
plt.title("Opiniones Bad por Producto")
plt.xlabel("Producto")
plt.ylabel("Opiniones Bad")
plt.xticks([])  # Eliminar las etiquetas del eje x

# Imprimir el máximo y mínimo de opiniones Bad en la parte inferior del gráfico
plt.text(len(data_sorted) / 2, -200, f"Máximo: {max_opinions['Título']}",
         ha="center", va="top", bbox=dict(facecolor="white", alpha=0.5))
plt.text(len(data_sorted) / 2, -400, f"Mínimo: {min_opinions['Título']}",
         ha="center", va="top", bbox=dict(facecolor="white", alpha=0.5))

# Crear una guía de colores en un recuadro en la esquina superior derecha
color_patches = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
legend = plt.legend(color_patches, data_sorted["Título"], loc="upper right", bbox_to_anchor=(1.2, 1))
plt.gca().add_artist(legend)

# Mostrar el gráfico de barras con la guía de colores
plt.show()
