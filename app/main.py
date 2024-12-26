import uvicorn
from fastapi import FastAPI

from app.routes import router

# Crear la instancia de la aplicación
app = FastAPI()

# Incluir las rutas
app.include_router(router)


# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "API iniciada correctamente"}


# Iniciar el servidor al ejecutar el archivo directamente
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
