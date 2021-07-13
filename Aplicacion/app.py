from flask import Flask, render_template
app = Flask(__name__)

#_______________RUTAS RELACIONADAS CON LOS CLIEMTES_______________#
#REDIRECCIONA AL LOGIN
@app.route("/")
def login():
    return render_template('usuarios/login.html')

#REDIRECCION AL REGISTRO UTILIZADO POR LOS CLIENTES
@app.route('/registro/clientes')
def registroClientes():
    return render_template('usuarios/registro.html')

#REDIRECCIONA AL PERFIL DEL USUARIO
@app.route('/usuarios/perfil')
def perfil():
    return render_template('usuarios/perfil.html')


#_______________RUTAS RELACIONADAS CON LOS PRODUCTOS_______________#
#REDIRECCIONA A LA PAGINA DE CONSULTA GENERAL DE PRODUCTOS
@app.route('/productos')
def productos():
    return render_template('productos/productos_general.html')

if __name__=='__main__':
    app.run(debug=True)