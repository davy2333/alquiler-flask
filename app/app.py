from flask import Flask, render_template, request, redirect, url_for, jsonify
from controller.controllerCarro import *



import os
from werkzeug.utils import secure_filename 



app = Flask(__name__)
application = app

msg  =''
tipo =''



@app.route('/', methods=['GET','POST'])
def inicio():
    return render_template('public/layout.html', miData = listaCarros())



@app.route('/registrar-carro', methods=['GET','POST'])
def addCarro():
    return render_template('public/acciones/add.html')


 

@app.route('/carro', methods=['POST'])
def formAddCarro():
    if request.method == 'POST':
        marca               = request.form['marca']
        modelo              = request.form['modelo']
        year                = request.form['year']
        color               = request.form['color']
        puertas             = request.form['puertas']
        favorito            = request.form['favorito']
        
        
        if(request.files['foto'] !=''):
            file     = request.files['foto'] 
            nuevoNombreFile = recibeFoto(file) 
            resultData = registrarCarro(marca, modelo, year, color, puertas, favorito, nuevoNombreFile)
            if(resultData ==1):
                return render_template('public/layout.html', miData = listaCarros(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layout.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('public/layout.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-carro/<string:id>', methods=['GET','POST'])
def formViewUpdate(id):
    if request.method == 'GET':
        resultData = updateCarro(id)
        if resultData:
            return render_template('public/acciones/update.html',  dataInfo = resultData)
        else:
            return render_template('public/layout.html', miData = listaCarros(), msg='No existe el carro', tipo= 1)
    else:
        return render_template('public/layout.html', miData = listaCarros(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalles-del-carro/<int:idCarro>', methods=['GET', 'POST'])
def viewDetalleCarro(idCarro):
    msg =''
    if request.method == 'GET':
        resultData = detallesdelCarro(idCarro) 
        
        if resultData:
            return render_template('public/acciones/view.html', infoCarro = resultData, msg='Detalles del Carro', tipo=1)
        else:
            return render_template('public/acciones/layout.html', msg='No existe el Carro', tipo=1)
    return redirect(url_for('inicio'))
    

@app.route('/actualizar-carro/<string:idCarro>', methods=['POST'])
def  formActualizarCarro(idCarro):
    if request.method == 'POST':
        marca           = request.form['marca']
        modelo          = request.form['modelo']
        year            = request.form['year']
        color           = request.form['color']
        puertas         = request.form['puertas']
        favorito        = request.form['favorito']
        
        
        if(request.files['foto']):
            file     = request.files['foto']
            fotoForm = recibeFoto(file)
            resultData = recibeActualizarCarro(marca, modelo, year, color, puertas, favorito, fotoForm, idCarro)
        else:
            fotoCarro  ='sin_foto.jpg'
            resultData = recibeActualizarCarro(marca, modelo, year, color, puertas, favorito, fotoCarro, idCarro)

        if(resultData ==1):
            return render_template('public/layout.html', miData = listaCarros(), msg='Datos del carro actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/layout.html', miData = listaCarros(), msg='No se pudo actualizar', tipo=1)



@app.route('/borrar-carro', methods=['GET', 'POST'])
def formViewBorrarCarro():
    if request.method == 'POST':
        idCarro         = request.form['id']
        nombreFoto      = request.form['nombreFoto']
        resultData      = eliminarCarro(idCarro, nombreFoto)

        if resultData ==1:
            
            return jsonify([1])
            
        else: 
            return jsonify([0])




def eliminarCarro(idCarro='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() 
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM carros WHERE id=%s', (idCarro,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount 
    
    
    basepath = os.path.dirname (__file__) 
    url_File = os.path.join (basepath, 'static/assets/fotos_carros', nombreFoto)
    os.remove(url_File) 
    
    

    return resultado_eliminar



def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) 
    filename = secure_filename(file.filename) 

    
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    
        
    upload_path = os.path.join (basepath, 'static/assets/fotos_carros', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile

       
  
  

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    
    
    
    
if __name__ == "__main__":
    app.run(debug=True, port=8000)