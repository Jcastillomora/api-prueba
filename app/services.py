import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Inicializar modelo de IA desde HuggingFace
analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f",  # Versión específica
)


# Función para scraping
def scrape_(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Asegura que la respuesta sea 200 OK

        # Analizar contenido HTML
        soup = BeautifulSoup(response.content, "html.parser")
        books = []

        # Extraer datos de cada producto
        for article in soup.find_all("article", class_="product_pod"):
            # Obtener título
            title = article.h3.a["title"]

            # Obtener precio
            price = article.find("p", class_="price_color").text.strip()

            # Obtener disponibilidad
            availability = article.find("p", class_="instock availability").text.strip()

            # Agregar datos al listado
            books.append(
                {
                    "scraped_text": [
                        f"{title} , {price}, {availability}"
                    ],  # Título como lista
                    # 'analysis': [f"{price} - {availability}"]  # Precio y disponibilidad
                }
            )

        # Depurar resultado #quizas falta agregar mas campos
        print(f"Scraped data: {books}")
        return books

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error de conexión: {e}")
    except Exception as e:
        raise Exception(f"Error inesperado: {e}")


# Función para scraping
def scrape_content(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Asegura que la respuesta sea 200 OK

        # Analizar contenido HTML
        soup = BeautifulSoup(response.content, "html.parser")
        books = []

        # Extraer datos de cada producto
        for article in soup.find_all("article", class_="product_pod"):
            # Obtener título
            title = article.h3.a["title"]

            # Obtener precio
            price = article.find("p", class_="price_color").text.strip()

            # Obtener disponibilidad
            availability = article.find("p", class_="instock availability").text.strip()

            # Combinar texto para análisis de sentimiento
            combined_text = f"{title}. {price} - {availability}"

            # Realizar análisis de sentimiento
            sentiment = analyzer(combined_text)[0]  # Obtener el primer resultado
            sentiment_label = sentiment["label"]
            sentiment_score = sentiment["score"]

            # Agregar datos al listado
            books.append(
                {
                    "scraped_text": [title],  # Título como lista
                    "analysis": f"Sentimento: {sentiment_label}, Score: {sentiment_score:.2f}",  # Precio y disponibilidad
                }
            )

        # Depurar resultado #quizas falta agregar mas campos
        print(f"Scraped data: {books}")
        return books

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error de conexión: {e}")
    except Exception as e:
        raise Exception(f"Error inesperado: {e}")


# Función para procesar texto con IA
def process_text(text: str):
    try:
        # Limitar longitud del texto
        if len(text) > 500:
            text = text[:500]

        # Procesar texto con el modelo de análisis de sentimiento
        result = analyzer(text)
        return result
    except Exception as e:
        print(f"Error al procesar texto: {e}")
        return []
