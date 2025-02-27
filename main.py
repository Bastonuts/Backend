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
	