from pydantic import BaseModel


# Modelo para scraping
class ScrapeInput(BaseModel):
    url: str


# Modelo para procesamiento de texto
class TextInput(BaseModel):
    text: str
