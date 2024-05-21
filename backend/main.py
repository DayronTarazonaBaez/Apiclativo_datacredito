from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class ConsultaRequest(BaseModel):
    documento: str

class ConsultaResponse(BaseModel):
    # Define aquí los campos de respuesta según la API de Datacrédito
    # Ejemplo:
    nombre: str
    score_crediticio: int
    deuda_total: float

API_URL = "URL_DE_LA_API_DE_DATACREDITO"
API_KEY = "TU_API_KEY"

@app.post("/consulta-datacredito", response_model=ConsultaResponse)
async def consulta_datacredito(request: ConsultaRequest):
    try:
        response = requests.post(API_URL, json={"documento": request.documento}, headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        data = response.json()
        # Mapear los datos de la API de Datacrédito a los campos del modelo de respuesta
        consulta_response = ConsultaResponse(
            nombre=data.get("nombre"),
            score_crediticio=data.get("score_crediticio"),
            deuda_total=data.get("deuda_total")
        )
        return consulta_response
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
