from flask import Flask,render_template,request,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from modelo.dao import Usuario, db,Categoria,Producto
from flask_login import login_required,login_user,logout_user,current_user,login_manager

app = Flask(__name__)

Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopit3sz.123@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

#_______________RUTAS RELACIONADAS CON LOS USUARIOS_______________#
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

#CRUD
#CONSULTA GENERAL
@app.route('/usuarios')
def consultaUsuarios():
    us=Usuario()
    return render_template('usuarios/ConsultaGeneral.html',usuarios=us.consultaGeneral())

# #REDIRECCIONA A LA PAGINA DE AGREGAR USUARIOS
@app.route('/usuarios/nuevo')
def nuevoUsuario():
    return render_template('usuarios/agregar.html')

# #AGREGAR USUARIOS
@app.route('/usuarios/agregar',methods=['post'])
def agregarUsuario():
    try:
        usuario=Usuario()
        usuario.nombreCompleto=request.form['nombreCompleto']
        usuario.direccion=request.form['direccion']
        usuario.telefono=request.form['telefono']        
        usuario.email=request.form['email']
        usuario.password=request.form['password']
        usuario.tipo=request.form['tipo']
        usuario.estatus=request.form['estatus']
        usuario.agregar()
        flash('¡ Usuario registrado con exito')
    except:
        flash('¡ Error al agregar al usuario !')
    return redirect(url_for('consultaUsuarios'))

# #CONSULTAR CATEGORIA ESPECIFICA
# @app.route('/Categorias/<int:id>')
# def consultarCategoria(id):
#     cat=Categoria()
#     return render_template('categorias/editar.html',cat=cat.consultaIndividuall(id))

# #EDITAR CATEGORIAS
# @app.route('/Categorias/editar',methods=['POST'])
# def editarCategoria():
#     try:
#         cat=Categoria()
#         cat.idCategoria=request.form['id']
#         cat.nombre=request.form['nombre']
#         imagen=request.files['imagen'].stream.read()
#         if imagen:
#             cat.imagen=imagen
#         cat.estatus=request.values.get("estatus","Inactiva")
#         cat.editar()
#         flash('¡ Categoria editada con exito !')
#     except:
#         flash('¡ Error al editar la categoria !')

#     return redirect(url_for('consultaCategorias'))

# #ELIMINAR CATEGORIA
# @app.route('/Categorias/eliminar/<int:id>')
# def eliminarCategoria(id):
#     try:
#         categoria=Categoria()
#         #categoria.eliminar(id)
#         categoria.eliminacionLogica(id)
#         flash('Categoria eliminada con exito')
#     except:
#         flash('Error al eliminar la categoria')
#     return redirect(url_for('consultaCategorias'))


#_______________RUTAS RELACIONADAS CON LOS PRODUCTOS_______________#
#REDIRECCIONA A LA PAGINA DE CONSULTA GENERAL DE PRODUCTOS
@app.route('/productos')
def productos():
    return render_template('productos/productos_general.html')


#_______________RUTAS RELACIONADAS CON LOS PEDIDOS_______________#
#REDIRECCIONA A EL PEDIDO DEL CLIENTE
@app.route('/usuarios/pedido')
def usuarioPedido():
    return render_template('pedidos/compra.html')

#REDIRECCIONA A LAS COMPRAS HECHAS POR EL USUARIO
@app.route('/usuarios/compras')
def usuarioCompras():
    return render_template('pedidos/pedidos.html')

#REDIRECCIONA A LA PAGINA DE SEGUIMIENTO DEL PEDIDO
@app.route('/usuarios/pedidos/seguimiento')
def usuarioSegPedido():
    return render_template('pedidos/seguimiento.html')


#_______________RUTAS RELACIONADAS CON LA CESTA_______________#
#REDIRECCIONA A LA CESTA DEL CLIENTE
@app.route('/usuarios/cesta')
def cesta():
    return render_template('cesta/cesta.html')


#_______________RUTAS RELACIONADAS CON LAS TARJETAS_______________#
#REDIRECCIONA A LA PAGINA PARA AGREGAR TARJETAS
@app.route('/usuarios/tarjetas')
def tarjetas():
    return render_template('tarjetas/Altatarjeta.html')


#_______________RUTAS RELACIONADAS CON LAS CATEGORIAS_______________#
#CONSULTA GENERAL
@app.route('/Categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('categorias/ConsultaGeneral.html',categorias=cat.consultaGeneral())

#CONSULTA IMAGEN
@app.route('/Categorias/consultarImagen/<int:id>')
def consultarImagenCategoria(id):
    cat=Categoria()
    return cat.consultarImagen(id)

#REDIRECCIONA A LA PAGINA DE AGREGAR CATEGORIAS
@app.route('/Categorias/nueva')
def nuevaCategoria():
    return render_template('categorias/agregar.html')

#AGREGAR CATEGORIAS
@app.route('/Categorias/agregar',methods=['post'])
def agregarCategoria():
    try:
        cat=Categoria()
        cat.nombre=request.form['nombre']
        cat.imagen=request.files['imagen'].stream.read()
        cat.estatus='A'
        cat.agregar()
        flash('¡ Categoria agregada con exito !')
    except:
        flash('¡ Error al agregar la categoria !')
    return redirect(url_for('consultaCategorias'))

#CONSULTAR CATEGORIA ESPECIFICA
@app.route('/Categorias/<int:id>')
def consultarCategoria(id):
    cat=Categoria()
    return render_template('categorias/editar.html',cat=cat.consultaIndividuall(id))

#EDITAR CATEGORIAS
@app.route('/Categorias/editar',methods=['POST'])
def editarCategoria():
    try:
        cat=Categoria()
        cat.idCategoria=request.form['id']
        cat.nombre=request.form['nombre']
        imagen=request.files['imagen'].stream.read()
        if imagen:
            cat.imagen=imagen
        cat.estatus=request.values.get("estatus","Inactiva")
        cat.editar()
        flash('¡ Categoria editada con exito !')
    except:
        flash('¡ Error al editar la categoria !')

    return redirect(url_for('consultaCategorias'))

#ELIMINAR CATEGORIA
@app.route('/Categorias/eliminar/<int:id>')
def eliminarCategoria(id):
    try:
        categoria=Categoria()
        #categoria.eliminar(id)
        categoria.eliminacionLogica(id)
        flash('Categoria eliminada con exito')
    except:
        flash('Error al eliminar la categoria')
    return redirect(url_for('consultaCategorias'))

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)