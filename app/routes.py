import json

from fastapi import APIRouter, HTTPException

from app.database import save_combined_result, save_process_result, save_scrape_result
from app.models import ScrapeInput, TextInput
from app.services import process_text, scrape_content, scrape_

router = APIRouter()


# Endpoint para scraping
@router.post("/scrape/")
async def scrape(scrape_input: ScrapeInput):
    try:
        results = scrape_(scrape_input.url)

        # Validar resultados
        if not isinstance(results, list) or len(results) == 0:
            raise HTTPException(status_code=404, detail="No se encontraron resultados.")

        # Procesar cada resultado
        combined_data = []
        for result in results:
            # Extraer texto scrapeado
            scraped_text = " ".join(
                [
                    " ".join(item) if isinstance(item, list) else item
                    for item in result["scraped_text"]
                ]
            )

            # Guardar resultado en la base de datos
            save_scrape_result(scrape_input.url, scraped_text)

            # Agregar resultado al JSON de respuesta
            combined_data.append(
                {
                    "scraped_text": scraped_text,
                }
            )

        # Responder con datos combinados
        return {"combined_data": combined_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint para procesamiento de texto
@router.post("/process/")
async def process(input_text: TextInput):
    try:
        # Procesar texto
        result = process_text(input_text.text)

        # Guardar en base de datos
        save_process_result(input_text.text, result)

        # Respuesta
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint combinado
@router.post("/combined/")
async def combined(scrape_input: ScrapeInput):
    try:
        # Realizar scraping
        results = scrape_content(scrape_input.url)

        # Validar resultados
        if not isinstance(results, list) or len(results) == 0:
            raise HTTPException(status_code=404, detail="No se encontraron resultados.")

        # Procesar cada resultado
        combined_data = []
        for result in results:
            # Extraer texto scrapeado
            scraped_text = ", ".join(result["scraped_text"])  # Convertir lista a cadena

            # Extraer datos para análisis
            analysis_data = ", ".join(result["analysis"])  # Convertir lista a cadena

            # Crear texto combinado para análisis de IA
            text_to_process = f"{scraped_text}. {analysis_data}"

            # Realizar análisis de sentimiento
            analysis = process_text(text_to_process)

            # Guardar resultado en la base de datos
            save_combined_result(
                scrape_input.url,
                text_to_process,
                json.dumps(analysis),  # Convertir análisis a JSON para la base de datos
            )

            # Agregar resultado al JSON de respuesta
            combined_data.append(
                {
                    "scraped_text": scraped_text,
                    "analysis_data": analysis_data,
                    "analysis_result": analysis,
                }
            )

        # Responder con datos combinados
        return {"combined_data": combined_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
