# API-Prueba

# Instructivo para Uso de la API

## **Requisitos Previos**
1. **Python 3.9 o superior**
2. **Crear un entorno virtual:**
```bash
python -m venv venv
```

3. **Activar el entorno virtual:**
```bash
# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

5. **Base de datos SQLite:**
La base de datos se genera automáticamente al iniciar la aplicación. No requiere configuración manual.

---

## **Iniciar el Servidor**

1. Ejecutar el servidor:
```bash
uvicorn app.main:app --reload
```

2. Abrir el navegador o Postman para probar los endpoints en:
```
http://127.0.0.1:8000
```

3. Documentación automática en Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## **Endpoints Disponibles**

### **1. Endpoint: /scrape/**
**Descripción:** Realiza scraping en una URL dada y almacena los datos en la base de datos.

**Método:** POST

**URL:**
```
http://127.0.0.1:8000/scrape/
```

**Ejemplo de Solicitud:**
```json
{
  "url": "https://books.toscrape.com/"
}
```

**Respuesta esperada:**
```json
{
  "combined_data": [
    {
      "scraped_text": "Book Title, £19.99, In stock",
      "analysis": "Sentiment: POSITIVE, Score: 0.95"
    }
  ]
}
```

---

### **2. Endpoint: /process/**
**Descripción:** Analiza un texto utilizando un modelo de IA para determinar el sentimiento.

**Método:** POST

**URL:**
```
http://127.0.0.1:8000/process/
```

**Ejemplo de Solicitud:**
```json
{
  "text": "FastAPI es un excelente framework."
}
```

**Respuesta esperada:**
```json
{
  "analysis": [
    {
      "label": "POSITIVE",
      "score": 0.98
    }
  ]
}
```

---

### **3. Endpoint: /combined/**
**Descripción:** Combina el scraping y el análisis de IA para devolver resultados procesados.

**Método:** POST

**URL:**
```
http://127.0.0.1:8000/combined/
```

**Ejemplo de Solicitud:**
```json
{
  "url": "https://books.toscrape.com/"
}
```

**Respuesta esperada:**
```json
{
  "combined_data": [
    {
      "scraped_text": "Book Title, £19.99, In stock",
      "analysis": "Sentiment: POSITIVE, Score: 0.95"
    }
  ]
}
```

---

## **Base de Datos**
Se almacenan los resultados en un archivo SQLite llamado `data.db` en el directorio raíz del proyecto.

### **Estructura de Tablas:**
```sql
-- Tabla scrape_results
CREATE TABLE scrape_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    scraped_text TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabla process_results
CREATE TABLE process_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT,
    result TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabla combined_results
CREATE TABLE combined_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    scraped_text TEXT,
    analysis TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## **Notas Finales**
- La API utiliza el modelo de HuggingFace `distilbert-base-uncased-finetuned-sst-2-english` para el análisis de sentimientos.
- El scraping está diseñado para funcionar con estructuras HTML estándar.
** http://books.toscrape.com/index.html
** http://books.toscrape.com/catalogue/page-2.html
** http://books.toscrape.com/catalogue/page-3.html

---

## **Autor**
- **Nombre:** Jorge Castillo
- **Correo Electrónico:** j.castillomora01@gmail.com

