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

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)

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

@app.get("/api/ObtenerUsuario/{codigo}")
def obtenerFlotas(codigo: str):
    try:
        datos = []
        conexion = sqlite3.connect("BagriFlotas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID, Nombre, Correo FROM IniciarSesion WHERE ID = '"+codigo+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos.append({"Id":i[0],"Nombre":i[1], "Correo":i[2]})
        return datos
    except TypeError:
        return "ERROR AL CONECTAR CON LA BASE DE DATOS"  

@app.get("/api/signin/{correo}/{clave}")
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