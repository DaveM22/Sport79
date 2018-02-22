from flask_login import UserMixin



from flask_sqlalchemy import SQLAlchemy

# create a new SQLAlchemy object
db = SQLAlchemy()
#asd
#cambio desde david
# Base model that for other models to inherit from
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String,nullable=False)
    clave = db.Column(db.String,nullable=False)
    habilitado = db.Column(db.Boolean,nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'), nullable=False)
    usuario_tipo_rel = db.relationship('Tipo_usuario', foreign_keys=tipo_id)

    def __init__(self,nombre,habilitado,tipo_id,clave=None,id=None):
        self.nombre = nombre
        self.clave = clave
        self.habilitado = habilitado
        self.tipo_id = tipo_id
        self.id = id

    def setPassFalsa(self,clave):
        self.clave = clave

    def setNombre(self,nombre):
        self.nombre = nombre

    def setClave(self,clave):
         self.clave = clave

    def setHabilitado(self,habilitado):
        self.habilitado = habilitado

    def setTipo(self,idtipo):
        self.tipo_id = idtipo

    def getNombre(self):
        return self.nombre

    def getClave(self):
        return self.clave

    def getHabilitado(self):
        return self.habilitado

    def getId(self):
        return self.id

class Tipo_usuario(db.Model):
    __tablename__='tipo_usuario'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    descripcion = db.Column(db.String,nullable=False)

    def __init__(self,descripcion):
        self.descripcion = descripcion



class Articulo(db.Model):
    __tablename__='articulos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String, nullable=False, unique=True)
    precio_unitario = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self,descripcion, precio_unitario, cant_stock,id=None):
        self.id = id
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.stock = cant_stock

    def getId(self):
        return self.id

    def getDescripcion(self):
        return self.descripcion

    def getPrecio(self):
        return self.precio_unitario

    def getStock(self):
        return self.stock

    def setDescripcion(self,descripcion):
        self.descripcion = descripcion

    def setPrecio(self,precio):
        self.precio_unitario = precio

    def setStock(self,stock):
        self.stock = stock


class MovimientoStock(db.Model):
    __tablename__= 'movimientostock'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False)
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuarios.id'),nullable=False)
    movimiento_usuario_rel = db.relationship('Usuario',foreign_keys=id_usuario)
    monto_total = db.Column(db.Float, nullable=False)

    def __init__(self,fecha,monto_total,id_usuario):
        self.fecha = fecha
        self.monto_total = monto_total
        self.id_usuario = id_usuario

    def getFecha(self):
        return self.fecha

    def getMontototal(self):
        return self.monto_total

class DetalleArticulo(db.Model):
    __tablename__ = 'detallearticulo'
    id = db.Column(db.Integer,nullable=False, primary_key=True, autoincrement=True)
    id_movimientostock = db.Column(db.Integer, db.ForeignKey('movimientostock.id'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulos.id'))
    detalle_usuario_rel = db.relationship('Usuario', foreign_keys=id_usuario,backref='usuarios', lazy=True)
    detalle_articulo_rel = db.relationship('Articulo', foreign_keys=id_articulo,backref='articulos', lazy=True)
    detalle_movimientostock_rel = db.relationship('MovimientoStock', foreign_keys=id_movimientostock, backref='movimientos', lazy=True)
    monto = db.Column(db.Float, nullable=False)


    def __init__(self, id_movimientostock, id_articulo, monto):
        self.id_movimientostock = id_movimientostock
        self.id_articulo = id_articulo
        self.monto = monto

