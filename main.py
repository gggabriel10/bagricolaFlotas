from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import uvicorn

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class config:
    orm_mode = True

@app.get("/")
async def root():
    return{'Sistema': 'Bagricola Flotas'}

@app.get("/api/ObtenerFlotas")
async def obtenerFlotas():
    try:
        datos = []
        conexion = sqlite3.connect("BagriFlotas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID, Numero, Nombre FROM RegistroFlotas ORDER BY Nombre")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos.append({"Id":i[0],"Numero":i[1], "Nombre":i[2]})
        return datos
    except TypeError:
        return "ERROR AL CONECTAR CON LA BASE DE DATOS"  

@app.get("/api/IniciarSesion/{correo}/{clave}")
def iniciar(correo: str,clave:str):
    try:
        passw = ""
        user = ""
        nombre = ""
        id = ""
        conexion = sqlite3.connect("BagriFlotas.db")
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT ID, Nombre, Correo, Clave from IniciarSesion where Correo ='"+correo+"' and Clave = '"+clave+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            id = i[0]
            nombre = i[1]
            user = i[2]
            passw = i[3]
        if correo == user and clave==passw:
            return {"Usuario": nombre}
        else:
            return {"Response": False}
    except TypeError:
        return "Error al extraer los datos"


@app.get("/api/TotalFlotas")
def TotalFlotas():
    try:
        datos=""
        conexion = sqlite3.connect("BagriFlotas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT count(ID) as Cantidad FROM RegistroFlotas")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = i[0]
        return datos
    except TypeError:
        return "Error al conectar a la base de datos"

@app.get("/api/FlotasDisponibles")
def FlotasDisponibles():
    try:
        texto = "DISPONIBLE"
        datos = ""
        conexion = sqlite3.connect("BagriFlotas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT count(Nombre) as Cantidad FROM RegistroFlotas WHERE Nombre='"+texto+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = i[0]
        return datos
    except TypeError:
        return "Error al conectar a la base de datos"