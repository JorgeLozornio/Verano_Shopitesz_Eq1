from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,BLOB,ForeignKey,Float, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import datetime

db = SQLAlchemy()

#TABLA DE CATEGORIAS
class Categoria(db.Model):
    __tablename__='Categorias' 
    idCategoria = Column( Integer, primary_key = True )
    nombre = Column( String, unique = True )
    imagen = Column( BLOB )
    estatus = Column( String, nullable = True)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividuall(self,id):
        return Categoria.query.get(id)

    def consultarImagen(self,id):
        return self.consultaIndividuall(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        cat=self.consultaIndividuall(id)
        db.session.delete(cat)
        db.session.commit()

    def eliminacionLogica(self,id):
        cat = self.consultaIndividuall(id)
        cat.estatus='Inactiva'
        cat.editar()


#TABLA DE PRODUCTOS
class Producto(db.Model):
    __tablename__='Productos'
    idProducto=Column(Integer,primary_key=True)
    idCategoria=Column(Integer,ForeignKey('Categorias.idCategoria'))
    nombre=Column(String,nullable=False)
    descripcion=Column(String,nullable=True)
    precioVenta=Column(Float,nullable=False)
    existencia=Column(Integer,nullable=False)
    foto=Column(BLOB)
    especificaciones=Column(BLOB)
    estatus=Column(String,nullable=False)
    categoria=relationship('Categoria',backref='productos',lazy='select')

    def consultaGeneral(self):
        return self.query.all()
    
    def consultaIndividuall(self,id):
        return Producto.query.get(id)
        
    def consultarFoto(self,id):
        return self.consultaIndividuall(id).foto
    
    def consultarEspecificaciones(self,id):
        return self.consultaIndividuall(id).especificaciones    

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        tar=self.consultaIndividuall(id)
        db.session.delete(tar)
        db.session.commit()

    def eliminacionLogica(self,id):
        tar = self.consultaIndividuall(id)
        tar.estatus='Inactiva'
        tar.editar()



#TABLA DE USUARIOS    
class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombreCompleto=Column(String,nullable=False)
    direccion=Column(String,nullable=False)
    telefono=Column(String,nullable=False)
    email=Column(String,unique=True)
    password_hash=Column(String(128),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)

    @property #Implementa el metodo Get (para acceder a un valor)
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')

    @password.setter #Definir el metodo set para el atributo password_hash
    def password(self,password):#Se informa el password en formato plano para hacer el cifrado
        self.password_hash=generate_password_hash(password)

    def validarPassword(self,password):
        print(self.password_hash)
        print(password)
        return check_password_hash(self.password_hash,password)
    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus=='A':
            return True
        else:
            return False
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def is_admin(self):
        if self.tipo=='Admin':
            return True
        else:
            return False
    def is_vendedor(self):
        if self.tipo=='Vendedor':
            return True
        else:
            return False
    def is_comprador(self):
        if self.tipo=='Comprador':
            return True
        else:
            return False
    #Definir el método para la autenticacion
    def validar(self,email,password):
        usuario=Usuario.query.filter(Usuario.email==email).first()
        if usuario!=None and usuario.validarPassword(password) and usuario.is_active():
            return usuario
        else:
            return None

    #Método para agregar una cuenta de usuario
    def agregar(self):
        pws = generate_password_hash(self.password_hash)
        self.password_hash = pws
        db.session.add(self)
        db.session.commit()

    #Consulta general
    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self,id):
        return Usuario.query.get(id)

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminacionLogica(self,id):
        cat = self.consultaIndividual(id)
        cat.estatus='I'
        cat.editar()
    
#TABLA DE TARJETAS
class Tarjetas(db.Model):
    __tablename__='Tarjetas'
    idTarjeta = Column( Integer, primary_key = True )
    idUsuario = Column( Integer,ForeignKey('Usuarios.idUsuario') )
    noTarjeta = Column( String, unique = True )
    saldo = Column( String, nullable = False )
    banco = Column( String, nullable = False )
    estatus = Column( String, nullable = False )

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Tarjetas.estatus=='Activa').all()

    def consultaIndividuall(self,id):
        return Tarjetas.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        tar=self.consultaIndividuall(id)
        db.session.delete(tar)
        db.session.commit()

    def eliminacionLogica(self,id):
        tar = self.consultaIndividuall(id)
        tar.estatus='Inactiva'
        tar.editar()

#TABLA DE PEDIDOS
class Pedidos(db.Model):
    tablename='Pedidos'
    idPedido = Column( Integer, primary_key = True )
    idComprador = Column( Integer, ForeignKey('Usuarios.idUsuario') )
    idVendedor = Column( Integer, ForeignKey('Usuarios.idUsuario') )
    idTarjeta = Column( Integer, ForeignKey('Tarjetas.idTarjeta') )
    fechaRegistro = Column( String, nullable = False )
    fechaAtencion = Column( String, nullable = False )
    fechaRecepcion = Column( String, nullable = False )
    fechaCierre = Column( String, nullable = False )
    total = Column( Float, nullable = False )
    estatus = Column( String, nullable = False )

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Pedidos.estatus=='Activa').all()

    def consultaIndividuall(self,id):
        return Pedidos.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        ped=self.consultaIndividuall(id)
        db.session.delete(ped)
        db.session.commit()

    def eliminacionLogica(self,id):
        ped = self.consultaIndividuall(id)
        ped.estatus='Inactiva'
        ped.editar()

 #TABLA DE CARRITO
class Carrito(db.Model):
    __tablename__='Carrito'
    idCarrito = Column(Integer, primary_key = True)
    idUsuario = Column(Integer, ForeignKey('Usuarios.idUsuario'))
    idProducto = Column(Integer, ForeignKey('Productos.idProducto'))
    fecha = Column(Date, default = datetime.date.today())
    cantidad = Column(Integer, nullable = False, default = 1)
    estatus = Column(String, nullable = False, default = 'Pendiente')
    producto = relationship('Producto', backref = 'carrito', lazy = 'select')
    usuario = relationship('Usuario', backref = 'carrito', lazy = 'select')

    def agregar(self):
        db.session.add(self)
        db.session.commit()
        
    def consultaGeneral(self,idUsuario):
        return self.query.filter(Carrito.idUsuario == idUsuario).all()

#TABLA DE PAQUETERIAS
class PAQUETERIA(db.Model):
    __tablename__='Paqueteria' 
    idPaqueteria = Column( Integer, primary_key = True )
    nombre = Column( String, unique = True )
    paginaweb = Column( String, unique = True )
    precio = Column( String, unique = True )
    telefono = Column( String, unique = True )
    estatus = Column( String, nullable = True)

    def consultaGeneral(self):
        return self.query.all()
        
    def consultaIndividuall(self,id):
        return Paqueteria.query.get(id)

    def consultarImagen(self,id):
        return self.consultaIndividuall(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        cat=self.consultaIndividuall(id)
        db.session.delete(cat)
        db.session.commit()

    def eliminacionLogica(self,id):
        cat = self.consultaIndividuall(id)
        cat.estatus='Inactiva'
        cat.editar()

