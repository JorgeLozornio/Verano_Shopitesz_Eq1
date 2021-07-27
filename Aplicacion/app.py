from flask import Flask,render_template,request,redirect,url_for,flash, session, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from modelo.dao import Usuario, db,Categoria,Producto, Tarjetas, Pedidos, Carrito
from flask_login import login_required,login_user,logout_user,current_user,login_manager, LoginManager
from datetime import timedelta
import json

app = Flask(__name__)

Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopit3sz.123@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

#_______________RUTAS RELACIONADAS CON LOS USUARIOS_______________#
#REDIRECCIONA AL LOGIN
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

# Urls defininas para el control de usuario
@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)


@app.route('/usuarios/iniciarSesion')
def mostrar_login():
    if current_user.is_authenticated:
        return render_template('productos/Productos_General.html')
    else:
        return render_template('usuarios/login.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

@app.route('/usuarios/nuevo')
def nuevoUsuario():
    if current_user.is_authenticated and not current_user.is_admin():
        return render_template('productos/Productos_General.html')
    else: 
        return render_template('usuarios/agregar.html')

@app.route("/usuarios/validarSesion",methods=['POST'])
def login():
    correo=request.form['correo']
    password=request.form['password']
    usuario=Usuario()
    user=usuario.validar(correo,password)
    if user!=None:
        login_user(user)
        return render_template('productos/Productos_General.html')
    else:
        flash('Nombre de usuario o contraseña incorrectos')
        print('Error de inicio de sesión')
        return render_template('usuarios/login.html')

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('mostrar_login'))


#_______________RUTAS RELACIONADAS CON LOS USUARIOS_______________#
#REDIRECCIONA AL LOGIN

@app.route("/")
def inicio():
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

# # #REDIRECCIONA A LA PAGINA DE AGREGAR USUARIOS
# @app.route('/usuarios/nuevo')
# def nuevoUsuario():
#     return render_template('usuarios/agregar.html')

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
        usuario.tipo=request.form.get('tipo')
        usuario.estatus=request.form.get('estatus')
        print(usuario.nombreCompleto)
        print(usuario.direccion)
        print(usuario.telefono)
        print(usuario.email)
        print(usuario.tipo)
        print(usuario.estatus)
        usuario.agregar()
        flash('¡ Usuario registrado con exito')
    except:
        print('No paso')
        flash('¡ Error al agregar al usuario !')
    return redirect(url_for('consultaUsuarios'))

#CONSULTAR USUARIO ESPECIFICO
@app.route('/usuarios/<int:id>')
def consultarUsuario(id):
    us=Usuario()
    return render_template('usuarios/editar.html',us=us.consultaIndividual(id))

#EDITAR USUARIOS
@app.route('/usuarios/editar',methods=['POST'])
def editarUsuario():
    try:
        us=Usuario()
        us.idUsuario=request.form['id']
        us.nombreCompleto=request.form['nombreCompleto']
        us.direccion=request.form['direccion']
        us.telefono=request.form['telefono']        
        us.email=request.form['email']
        us.password=request.form['password']
        us.tipo=request.form.get('tipo')
        us.estatus=request.form.get('estatus')
        print(us.nombreCompleto)
        print(us.direccion)
        print(us.telefono)
        print(us.email)
        print(us.tipo)
        print(us.estatus)
        us.editar()
        flash('¡ Usuario editado con exito !')
    except:
        flash('¡ Error al editar el usuario !')

    return redirect(url_for('consultaUsuarios'))

#ELIMINAR USUARIO
@app.route('/usuarios/eliminar/<int:id>')
def eliminarUsuario(id):
    try:
        us=Usuario()
        #categoria.eliminar(id)
        us.eliminacionLogica(id)
        flash('Usuario eliminado con exito')
    except:
        flash('Error al eliminar el usuario')
    return redirect(url_for('consultaUsuarios'))


#_______________RUTAS RELACIONADAS CON LOS PRODUCTOS_______________#
#REDIRECCIONA A LA PAGINA DE CONSULTA GENERAL DE PRODUCTOS
@app.route('/productos')
def productos():
    return render_template('productos/productos_general.html')

@app.route('/Productos/consultarFoto/<int:id>')
def consultarFotoProductos(id):
    pro=productos()
    return pro.consultarfoto(id)

@app.route('/Productos/consultarEspecificaciones/<int:id>')
def consultarEspecificacionesProductos(id):
    pro=productos()
    return pro.consultarEspecificaciones(id)

#REDIRECCIONA A LA PAGINA DE AGREGAR PRODUOCTOS
@app.route('/Productos/AltaProductos')
def nuevoProducto():
    return render_template('Productos/altaProductos.html')

#REDIRECCIONA A LA PAGINA PARA AGREGAR Productos
@app.route('/Productos/AltaProductos',methods=['post'])
def agregarProducto():
    try:
        pro=Producto()
        pro.idCategoria = request.form['idCategoria']
        pro.nombre = request.form['nombre']
        pro.descripcion = request.form['descripcion']
        pro.precioVenta = request.form['precioventa']
        pro.existencia = request.form['existencia']
        imagen=request.files['imagen'].stream.read()
        if imagen:
            pro.foto=imagen
        esp=request.files['especificaciones'].stream.read()
        if esp:
            pro.especificaciones=esp
        
        pro.estatus = 'A'
        pro.agregar()
        flash('¡ Producto agregado con exito !')
    except:
        flash('¡ Error al agregar el Producto !')
    return redirect(url_for('consultaProductos'))

#REDIRECCIONA A LA PAGINA PARA CONSULTAR Productos
@app.route('/Productos/Productos_General')
def consultaProductos():
    pro=Producto()
    return render_template('Productos/consultaProducto.html', productos = pro.consultaGeneral())

#REDIRECCIONA A LA PAGINA PARA EDITAR Productos
@app.route('/Productos/editarProductos',methods=['POST'])
def editarTProducto():
    try:
        pro=Producto()
        pro.idProducto = request.form['idProducto']
        pro.idCategoria = request.form['idCategoria']
        pro.nombre = request.form['nombre']
        pro.descripcion = request.form['descripcion']
        pro.precioVenta = request.form['precioventa']
        pro.existencia = request.form['existencia']
        imagen=request.files['imagen'].stream.read()
        Especificacion=request.files['Especificacion'].stream.read()
        if imagen:
            pro.foto=imagen
        if Especificacion:
            pro.especificaciones = request.form['especificaciones']
        
        pro.estatus = 'A'
        pro.editar()
        flash('¡ Producto editado con exito !')
    except:
        flash('¡ Error al editar el producto !')

    return redirect(url_for('consultaProducto'))

#ELIMINAR Productos
@app.route('/Productos/eliminar/<int:id>')
def eliminarProducto(id):
    try:
        pro=Producto()
        pro.eliminacionLogica(id)
        flash('Producto eliminado con exito')
    except:
        flash('Error al eliminar el Producto')
    return redirect(url_for('consultaProductos'))
#CONSULTA IMAGEN
@app.route('/Productos/consultarImagen/<int:id>')
def consultarImagenProductos(id):
    pro=Productos()
    return pro.consultarImagen(id)
#CONSULTAR Producto ESPECIFICA
@app.route('/Productos/<int:id>')
def consultarProductos(id):
    pro = Producto()
    ur = Usuario()
    return render_template('Productos/editarProducto.html', pro = pro.consultaIndividuall(id))



#_______________RUTAS RELACIONADAS CON LOS PEDIDOS_______________#
#REDIRECCIONA A EL PEDIDO DEL CLIENTE
@app.route('/pedidos/pedido')
def usuarioPedido():
    return render_template('pedidos/pedidos.html')

#REDIRECCIONA A LAS COMPRAS HECHAS POR EL USUARIO
@app.route('/usuarios/compras')
def usuarioCompras():
    return render_template('pedidos/compra.html')

#REDIRECCIONA A LA PAGINA DE SEGUIMIENTO DEL PEDIDO
@app.route('/usuarios/pedidos/seguimiento')
def usuarioSegPedido():
    return render_template('pedidos/seguimiento.html')


#_______________RUTAS RELACIONADAS CON LA CESTA_______________#
# Seccion para el carrito
@app.route('/carrito/agregar/<data>', methods = ['get'])
def agregarProductoCarrito(data):
    msg = ''
    if current_user.is_authenticated and current_user.is_comprador():
        datos = json.loads(data)
        carrito = Carrito()
        carrito.idProducto = datos['idProducto']
        carrito.idUsuario = current_user.idUsuario
        carrito.cantidad = datos['cantidad']
        carrito.agregar()
        msg={'estatus':'ok','mensaje':'Producto agregado a la cesta.'}
    return json.dumps(msg)

@app.route("/Cesta")
@login_required
def cesta():
    if current_user.is_authenticated:
        carrito = Carrito()
        return render_template('Cesta/Cesta.html', cesta = carrito.consultaGeneral(current_user.idUsuario))
# fin de la seccion del carrito


#_______________RUTAS RELACIONADAS CON LAS TARJETAS_______________#
#REDIRECCIONA A LA PAGINA DE AGREGAR TARJETAS
@app.route('/usuarios/nuevaTarjeta')
def nuevaTarjeta():
    return render_template('Tarjetas/AltaTarjeta.html')

#REDIRECCIONA A LA PAGINA PARA AGREGAR TARJETAS
@app.route('/usuarios/AltaTarjeta',methods=['post'])
def agregarTarjeta():
    try:
        tar=Tarjetas()
        tar.idUsuario = request.form['idUsuario']
        tar.noTarjeta = request.form['noTarjeta']
        tar.saldo = request.form['saldo']
        tar.banco = request.form['banco']
        tar.estatus = 'A'
        tar.agregar()
        flash('¡ Tarjeta agregada con exito !')
    except:
        flash('¡ Error al agregar la Tarjeta !')
    return redirect(url_for('consultaTarjetas'))

#REDIRECCIONA A LA PAGINA PARA CONSULTAR TARJETAS
@app.route('/usuarios/Tarjetas')
def consultaTarjetas():
    tar=Tarjetas()
    return render_template('Tarjetas/ConsultaTarjetas.html', Tarjetas = tar.consultaGeneral())

#REDIRECCIONA A LA PAGINA PARA EDITAR TARJETAS
@app.route('/usuarios/EditarTarjeta',methods=['POST'])
def editarTarjeta():
    try:
        tar=Tarjetas()
        tar.idTarjeta = request.form['idTarjeta']
        tar.idUsuario = request.form['idUsuario']
        tar.noTarjeta = request.form['noTarjeta']
        tar.saldo = request.form['saldo']
        tar.banco = request.form['banco']
        tar.estatus = request.values.get("estatus","Inactiva")
        tar.editar()
        flash('¡ Tarjeta editada con exito !')
    except:
        flash('¡ Error al editar la Tarjeta !')

    return redirect(url_for('consultaTarjetas'))

#ELIMINAR TARJETAS
@app.route('/tarjetas/eliminar/<int:id>')
def eliminarTarjeta(id):
    try:
        tar=Tarjetas()
        #tarjeta.eliminar(id)
        tar.eliminacionLogica(id)
        flash('Tarjeta eliminada con exito')
    except:
        flash('Error al eliminar la Tarjeta')
    return redirect(url_for('consultaTarjetas'))

#CONSULTAR TARJETA ESPECIFICA
@app.route('/Tarjetas/<int:id>')
def consultarTarjeta(id):
    tar = Tarjetas()
    ur = Usuario()
    return render_template('Tarjetas/EditarTarjeta.html', tar = tar.consultaIndividuall(id))


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


#__RUTAS RELACIONADAS CON LOS PEDIDOS__#

#REDIRECCIONA A LA PAGINA PARA AGREGAR PEDIDOS
@app.route('/Pedidos/Compra',methods=['post'])
def agregarPedido():
    try:
        ped=Pedidos()
        ped.idPedido=request.form['idPedido']
        ped.idComprador=request.form['idComprador']
        ped.idVendedor=request.form['idVendedor']
        ped.idTarjeta=request.form['idTarjeta']
        ped.fechaRegistro=request.form['fechaRegistro']
        ped.fechaAtencion=request.form['fechaAtencion']
        ped.fechaRecepcion=request.form['fechaRecepcion']
        ped.fechaCierre=request.form['fechaCierre']
        ped.total=request.form['total']
        ped.estatus=request.form.get('estatus')
        print(ped.idPedido)
        print(ped.idComprador)
        print(ped.idVendedor)
        print(ped.idTarjeta)
        print(ped.fechaRegistro)
        print(ped.fechaAtencion)
        print(ped.fechaRecepcion)
        print(ped.fechaCierre)
        print(ped.total)
        print(ped.estatus)
        ped.agregar()
        flash('¡ Pedido agregada con exito !')
    except:
        flash('¡ Error al agregar la Pedido !')
    return redirect(url_for('consultaPedidos'))

#REDIRECCIONA A LA PAGINA PARA CONSULTAR PEDIDOS
@app.route('/Pedidos/Pedidos')
def consultaPedidos():
    ped=Pedidos()
    return render_template('Pedidos/Pedidos.html',Pedidos=ped.consultaGeneral())

#REDIRECCIONA A LA PAGINA PARA EDITAR PEDIDOS
@app.route('/Pedidos/EditarPedido',methods=['POST'])
def editarPedido():
    try:
        ped=Pedidos()
        ped.idPedido=request.form['idPedido']
        ped.idComprador=request.form['idComprador']
        ped.idVendedor=request.form['idVendedor']
        ped.idTarjeta=request.form['idTarjeta']
        ped.fechaRegistro=request.form['fechaRegistro']
        ped.fechaAtencion=request.form['fechaAtencion']
        ped.fechaRecepcion=request.form['fechaRecepcion']
        ped.fechaCierre=request.form['fechaCierre']
        ped.total=request.form['total']
        ped.estatus=request.form.get('estatus')
        print(ped.idPedido)
        print(ped.idComprador)
        print(ped.idVendedor)
        print(ped.idTarjeta)
        print(ped.fechaRegistro)
        print(ped.fechaAtencion)
        print(ped.fechaRecepcion)
        print(ped.fechaCierre)
        print(ped.total)
        print(ped.estatus)
        ped.editar()
        flash('¡ Pedido editada con exito !')
    except:
        flash('¡ Error al editar el Pedido !')

    return redirect(url_for('consultaPedidos'))

#ELIMINAR PEDIDOS
@app.route('/Pedidos/eliminar/<int:id>')
def eliminarPedido(id):
    try:
        ped=Pedidos()
        #pedido.eliminar(id)
        ped.eliminacionLogica(id)
        flash('Pedido eliminado con exito')
    except:
        flash('Error al eliminar el Pedido')
    return redirect(url_for('consultaPedidos'))

#CONSULTAR PEDIDO ESPECIFICO
@app.route('/Pedidos/<int:id>')
def consultarPedido(id):
    ped=Pedidos()
    return render_template('Pedidos/EditarPedido.html',ped = ped.consultaIndividuall(id))


if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)


#_______________RUTAS RELACIONADAS CON LAS PAQUETERIAS_______________#
#CONSULTA GENERAL
@app.route('/Paqueteria')
def consultaPaqueteria():
    paq=Paqueteria()
    return render_template('paqueteria/ConsultaGeneral.html',paqueteria=paq.consultaGeneral())

#REDIRECCIONA A LA PAGINA DE AGREGAR CATEGORIAS
@app.route('/Paqueteria/nueva')
def nuevaPaqueteria():
    return render_template('paqueteria/agregar.html')

#AGREGAR Paqueterias
@app.route('/Paqueteria/agregar',methods=['post'])
def agregarPaqueteria():
    try:
        paq=Paqueteria()
        paq.nombre=request.form['nombre']
        paq.paginaweb=request.form['paginaweb']
        paq.precio=request.form['precio']
        paq.telefono=request.form['telefono']
        paq.estatus='A'
        paq.agregar()
        flash('¡ Paqueteria agregada con exito !')
    except:
        flash('¡ Error al agregar la paqueteria !')
    return redirect(url_for('consultaPaqueteria'))

#CONSULTAR PAQUETERIA ESPECIFICA
@app.route('/Paqueteria/<int:id>')
def consultarPaqueteria(id):
    paq=Paqueteria()
    return render_template('paqueteria/editar.html',paq=paq.consultaIndividuall(id))

#EDITAR PAQUETERIA
@app.route('/Paqueteria/editar',methods=['POST'])
def editarPaqueteria():
    try:
        paq=Paqueteria()
        paq.nombre=request.form['nombre']
        paq.paginaweb=request.form['paginaweb']
        paq.precio=request.form['precio']
        paq.telefono=request.form['telefono']
        paq.estatus=request.values.get("estatus","Inactiva")
        paq.editar()
        flash('¡ Paqueteria editada con exito !')
    except:
        flash('¡ Error al editar la paqueteria !')

    return redirect(url_for('consultaPaqueteria'))

#ELIMINAR PAQUETERIA
@app.route('/Paqueteria/eliminar/<int:id>')
def eliminarPaqueteria(id):
    try:
        Paqueteria=Paqueteria()
        paqueteria.eliminacionLogica(id)
        flash('paqueteria eliminada con exito')
    except:
        flash('Error al eliminar la paqueteria')
    return redirect(url_for('consultaPaqueteria'))

