
#Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    mydb = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="0987654321",
        database = "crud_flask_python"
        )
    if mydb:
        print ("Conexion exitosa a BD")
        return mydb
    else:
        print("Error en la conexion a BD")
    

    
    
    