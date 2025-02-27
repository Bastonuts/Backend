from fastapi import FastAPI
from pydantic import BaseModel

class sensor(BaseModel):
	lon: int 
	lat: int 
	pos: int 
	ult: int

app = FastAPI()

@app.post("/data")
async def insert_data(data_sensor: sensor):
	"""
	Inserta los datos a la base de datos
	"""
	return sensor
	
if __name__ == "__main__":
	port = int(os.getenv("PORT", 8080))  # 🚀 Usa el puerto que asigna Railway
	uvicorn.run(app, host="0.0.0.0", port=port)