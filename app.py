#--------------------------------------------------------------------
# Importamos el framework Flask
from flask import Flask 

# Importamos la función que nos permit el render de los templates,
# recibir datos del form, redireccionar, etc.
from flask import render_template, request,redirect, send_from_directory, flash

# Importamos el módulo que permite conectarnos a la BS
from flaskext.mysql import MySQL

# Importamos las funciones relativas a fecha y hora
from datetime import datetime

# Importamos paquetes de interfaz con el sistema operativo.
import os
#--------------------------------------------------------------------


# Creamos la aplicación
app = Flask(__name__) 

#--------------------------------------------------------------------
# Creamos la conexión con la base de datos:
mysql = MySQL()
# Creamos la referencia al host, para que se conecte a la base
# de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_HOST']='localhost' 
# Indicamos el usuario, por defecto es user
app.config['MYSQL_DATABASE_USER']='root' 
# Sin contraseña, se puede omitir
app.config['MYSQL_DATABASE_PASSWORD']='' 
# Nombre de nuestra BD
app.config['MYSQL_DATABASE_BD']='sistema' 
# Creamos la conexión con los datos
mysql.init_app(app) 

'''  
#--------------------------------------------------------------------
# Guardamos la ruta de la carpeta "uploads" en nuestra app
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#--------------------------------------------------------------------
# Generamos el acceso a la carpeta uploads. 
# El método uploads que creamos nos dirige a la carpeta (variable CARPETA)
# y nos muestra la foto guardada en la variable nombreFoto.
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)
    
'''

#--------------------------------------------------------------------
# Proporcionamos la ruta a la raiz del sitio
@app.route('/') 
def index():
    # Creamos una variable que va a contener la consulta sql:
    sql = "SELECT * FROM `sistema`.`empleados`;"    
    # Nos conectamos a la base de datos 
    conn = mysql.connect()    
    # Sobre el cursor vamos a realizar las operaciones
    cursor = conn.cursor()     
    # Ejecutamos la sentencia SQL sobre el cursor
    cursor.execute(sql)     
    # Copiamos el contenido del cursor a una variable
    db_empleados = cursor.fetchall()
    # "Commiteamos" (Cerramos la conexión)
    conn.commit()     
    # Devolvemos código HTML para ser renderizado
    return render_template('empleados/index.html', empleados = db_empleados)

#--------------------------------------------------------------------
# Función para eliminar un registro
@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `sistema`.`empleados` WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

#--------------------------------------------------------------------
# Función para editar un registro
@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `sistema`.`empleados` WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

# Función para editar un registro
@app.route('/menu')
def menu():
    return render_template('empleados/Menu.html')    

@app.route('/contactanos')
def contactanos():
    return render_template('empleados/Contactanos.html')        

@app.route('/donde_estamos')
def contactanos():
    return render_template('empleados/Donde estamos.html') 

@app.route('/formulario_contacto')
def contactanos():
    return render_template('empleados/FormularioContacto.html') 

@app.route('/mostrar_datos')
def contactanos():
    return render_template('empleados/mostrar_datos.html') 

@app.route('/pedidos')
def contactanos():
    return render_template('empleados/Pedidos.html') 

@app.route('/pedidos2')
def contactanos():
    return render_template('empleados/Pedidos2.html') 
#--------------------------------------------------------------------
# Función para actualizar los datos de un registro
@app.route('/update', methods=['POST'])
def update():
    # Recibimos los valores del formulario y los pasamos a variables locales:
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
   # _foto = request.files['txtFoto']    
    id = request.form['txtID']
    
    # Armamos la sentencia SQL que va a actualizar los datos en la DB:
    sql = "UPDATE `sistema`.`empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s;"
    # Y la tupa correspondiente
    datos = (_nombre,_correo,id)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Guardamos en now los datos de fecha y hora
    now = datetime.now()
    
    # Y en tiempo almacenamos una cadena con esos datos
    tiempo= now.strftime("%Y%H%M%S")

    ''' 
    #Si el nombre de la foto ha sido proporcionado en el form...
    if _foto.filename != '':
        # Creamos el nombre de la foto y la guardamos.
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)
        
        # Buscamos el registro y buscamos el nombre de la foto vieja:
        cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s", id)
        fila= cursor.fetchall()
        
        # Y la borramos de la carpeta:
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        
        # Finalmente, actualizamos la DB con el nuevo nombre del archivo:
        cursor.execute("UPDATE `sistema`.`empleados` SET foto=%s WHERE id=%s;", (nuevoNombreFoto, id))
        conn.commit()
        '''
        
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')


#--------------------------------------------------------------------
# Función para crear un registro nuevo.
@app.route('/create')
def create():
    return render_template('empleados/create.html')

#--------------------------------------------------------------------
#Función para almacenar los datos de un usuario.
@app.route('/store', methods=['POST'])
def storage():
    # Recibimos los valores del formulario y los pasamos a variables locales:
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
   # _foto = request.files['txtFoto']
    
    # Guardamos en now los datos de fecha y hora
    now = datetime.now()
    
    # Y en tiempo almacenamos una cadena con esos datos
    tiempo = now.strftime("%Y%H%M%S") 
    
    ''' 
    #Si el nombre de la foto ha sido proporcionado en el form...
    if _foto.filename!='':
        #...le cambiamos el nombre.
        nuevoNombreFoto=tiempo+_foto.filename 
        # Guardamos la foto en la carpeta uploads.
        _foto.save("uploads/"+nuevoNombreFoto)
    
    # Y armamos una tupla con esos valores:
    datos = (_nombre,_correo, nuevoNombreFoto)
        
    # Armamos la sentencia SQL que va a almacenar estos datos en la DB:
    sql = "INSERT INTO `sistema`.`empleados` \
          (`id`, `nombre`, `correo`, `foto`) \
          VALUES (NULL, %s, %s, %s);"
          
    '''
    
    # Y armamos una tupla con esos valores:
    datos = (_nombre,_correo)
        
    # Armamos la sentencia SQL que va a almacenar estos datos en la DB:
    sql = "INSERT INTO `sistema`.`empleados` \
          (`id`, `nombre`, `correo`) \
          VALUES (NULL, %s, %s);"
    

    conn = mysql.connect()     # Nos conectamos a la base de datos 
    cursor = conn.cursor()     # En cursor vamos a realizar las operaciones
    cursor.execute(sql, datos) # Ejecutamos la sentencia SQL en el cursor
    conn.commit()              # Hacemos el commit
    return redirect('/')       # Volvemos a index.html


#--------------------------------------------------------------------
# Estas líneas de código las requiere python para que 
# se pueda empezar a trabajar con la aplicación
if __name__=='__main__':
    #Corremos la aplicación en modo debug
    app.run(debug=True) 
#--------------------------------------------------------------------