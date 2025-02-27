import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
	host=os.getenv("MYSQL_HOST"),
	user=os.getenv("MYSQL_USER"),
	password=os.getenv("MYSQL_PASSWORD"),
	database=os.getenv("MYSQL_DATABASE"),
	port=int(os.getenv("MYSQL_PORT", 3306))
)

class sensor(BaseModel):
	lon: float
	lat: float
	pos: str
	ult: float
app = FastAPI()

@app.post("/data")
async def insert_data(data_sensor: sensor):
	"""
	Inserta los datos a la base de datos
	"""
	cursor = db.cursor()
	query = """
		INSERT INTO datos_baston (latitud, longitud, posicion, fecha, alerta)
		VALUES (%s, %s, %s, %s, %s)
    """
	values = (data.lat, data.lon, data.pos, datetime.now(), data.ult)
	try:
		with db.cursor() as cursor:
			cursor.execute(query, values)
			db.commit()
		return {"message": "Datos almacenados correctamente"}
	except Exception as e:
		db.rollback()
		return {"error": str(e)}
	finally:
		cursor.close()
	
if __name__ == "__main__":
	port = int(os.getenv("PORT", 8080))  # 🚀 Usa el puerto que asigna Railway
	uvicorn.run(app, host="0.0.0.0", port=port)