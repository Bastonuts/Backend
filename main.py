import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
	host=os.getenv("MYSQLHOST"),
	user=os.getenv("MYSQL_USER"),
	password=os.getenv("MYSQL_ROOT_PASSWORD"),
	database=os.getenv("MYSQL_DATABASE"),
	port=int(os.getenv("MYSQL_PORT", 3306))
)

class sensor(BaseModel):
	lon: float
	lat: float
	pos: str
	alarm: int
app = FastAPI()

@app.post("/data")
async def insert_data(data_sensor: sensor):
	#"""
	#Inserta los datos a la base de datos
	#"""
	try:
		cursor = db.cursor()
		nombre_tabla = "datos_baston"

		# Crear la tabla si no existe
		crear_tabla_sql = f"""
			CREATE TABLE IF NOT EXISTS {nombre_tabla} (
				id INT AUTO_INCREMENT PRIMARY KEY,
				latitud DECIMAL(9,7) NOT NULL,
				longitud DECIMAL(9,7) NOT NULL,
				posicion VARCHAR(16) DEFAULT NULL,
				fecha DATETIME NOT NULL,
				alerta INT NOT NULL
			)
			"""

		cursor.execute(crear_tabla_sql)

		query = """
			INSERT INTO datos_baston (latitud, longitud, posicion, fecha, alerta)
			VALUES (%s, %s, %s, %s, %s)
		"""
		values = (data_sensor.lon, data_sensor.lat, data_sensor.pos, datetime.now(), data_sensor.alarm)
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
	except Exception as e:
		return {"error": str(e)}
	#return sensor

@app.delete("/delete_table")
async def delete_tabla(name_table:str):
	"""Elimina una tabla si existe"""
	try:
		cursor = db.cursor()
		query = "DROP TABLE IF EXISTS `{}`".format(name_table)
		cursor.execute(query)
		db.commit()
		return {"message": f"Tabla '{name_table}' eliminada correctamente"}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		cursor.close()

@app.post("/modifique_table")
async def delete_tabla(name_table:str):
	"""Modifica la estructura de la tabla"""
	try:
		cursor = db.cursor()
		query = "ALTER TABLE `{}` MODIFY COLUMN posicion VARCHAR(16)".format(name_table)
		cursor.execute(query)
		db.commit()
		return {"message": f"Tabla '{name_table}' modificada correctamente"}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		cursor.close()

if __name__ == "__main__":
	port = int(os.getenv("PORT", 8080))  # 🚀 Usa el puerto que asigna Railway
	uvicorn.run(app, host="0.0.0.0", port=port)
