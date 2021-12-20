from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

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
def root():
    return{'Sistema': 'Bagricola Flotas'}

# RETORNAR TODAS LAS FLOTAS REGISTRADAS
@app.get("/api/ObtenerFlotas")
def obtenerFlotas():
    try:
        datos = []
        conexion = sqlite3.connect("BagriFlotas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID, Numero, Nombre FROM RegistroFlotas ORDER BY Nombre ASC")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos.append({"Id":i[0],"Numero":i[1], "Nombre":i[2]})
        return datos
    except TypeError:
        return "ERROR AL CONECTAR CON LA BASE DE DATOS"  

# INICIO DE SESION
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
            "SELECT ID, Nombre, Usuario, Clave from IniciarSesion where Usuario ='"+correo+"' and Clave = '"+clave+"'")
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
        return "ERROR AL CONECTAR CON LA BASE DE DATOS"

# RETORNA LA CANTIDAD TOTAL DE FLOTAS REGISTRADAS
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
        return "ERROR AL CONECTAR CON LA BASE DE DATOS"

# RETORNA LA CANTIDAD TOTAL DE FLOTAS DISPONIBLES
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
        return "ERROR AL CONECTAR CON LA BASE DE DATOS"

# AGREGAR FLOTAS
@app.post("/api/RegistroFlota/{numero}/{nombre}")
def RegistroFlota(numero: str, nombre: str):
    try:
        idu = ""
        conexion = sqlite3.connect("BagriFlotas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT Numero FROM RegistroFlotas WHERE ID = '"+numero+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            idu = i[0]
        if numero == idu:
            return {"Ok": False}
        else: 
            datos = (numero, nombre)
            sql='''INSERT INTO RegistroFlotas(Numero,Nombre) VALUES(?,?)'''
            cursor.execute(sql,datos)
            conexion.commit()
            return  {"Ok":True}
    except TypeError:
        return "ERROR AL CONECTAR CON LA BASE DE DATOS"

# ELIMINAR FLOTAS
@app.delete("/api/EliminarFlota/{codigo}")
def EliminarFlota(codigo: str):
    conexion = sqlite3.connect("BagriFlotas.db")
    cursor = conexion.cursor()
    conexion.commit()
    cursor.execute("DELETE FROM RegistroFlotas WHERE ID = '"+codigo+"'")
    #conexion.commit()
    return  {"Ok":codigo}

# ACTUALIZAR FLOTAS
@app.put("/api/ActualizarFlota/{id}/{numero}/{nombre}")
def ActualizarFlota(id: str, numero:str, nombre:str):
    conexion = sqlite3.connect("BagriFlotas.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE RegistroFlotas SET Numero='"+numero+"',Nombre='"+nombre+"' WHERE ID = '"+id+"'")
    conexion.commit()
    return  {"Ok":True}