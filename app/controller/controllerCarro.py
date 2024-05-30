from random import sample
from conexionBD import *  




def listaCarros():
    conexion_MySQLdb = connectionBD() 
    cur      = conexion_MySQLdb.cursor(dictionary=True)

    querySQL = "SELECT * FROM carros ORDER BY id DESC"
    cur.execute(querySQL) 
    resultadoBusqueda = cur.fetchall() 
    totalBusqueda = len(resultadoBusqueda) 
    
    cur.close() 
    conexion_MySQLdb.close()  
    return resultadoBusqueda



def updateCarro(id=''):
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM carros WHERE id = %s LIMIT 1", [id])
        resultQueryData = cursor.fetchone() 
        return resultQueryData
    
    
    
def registrarCarro(marca='', modelo='', year='', color='', puertas='', favorito='', nuevoNombreFile=''):       
        conexion_MySQLdb = connectionBD()
        cursor           = conexion_MySQLdb.cursor(dictionary=True)
            
        sql         = ("INSERT INTO carros(marca, modelo, year, color, puertas, favorito, foto) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        valores     = (marca, modelo, year, color, puertas, favorito, nuevoNombreFile)
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()
        cursor.close() 
        conexion_MySQLdb.close() 
        
        resultado_insert = cursor.rowcount 
        ultimo_id        = cursor.lastrowid 
        return resultado_insert
  

def detallesdelCarro(idCarro):
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM carros WHERE id ='%s'" % (idCarro,))
        resultadoQuery = cursor.fetchone()
        cursor.close() 
        conexion_MySQLdb.close() 
        
        return resultadoQuery
    
    

def  recibeActualizarCarro(marca, modelo, year, color, puertas, favorito, nuevoNombreFile, idCarro):
        conexion_MySQLdb = connectionBD()
        cur = conexion_MySQLdb.cursor(dictionary=True)
        cur.execute("""
            UPDATE carros
            SET 
                marca   = %s,
                modelo  = %s,
                year    = %s,
                color   = %s,
                puertas = %s,
                favorito= %s,
                foto    = %s
            WHERE id=%s
            """, (marca,modelo, year, color, puertas, favorito, nuevoNombreFile,  idCarro))
        conexion_MySQLdb.commit()
        
        cur.close() 
        conexion_MySQLdb.close() 
        resultado_update = cur.rowcount 
        return resultado_update
 


def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio