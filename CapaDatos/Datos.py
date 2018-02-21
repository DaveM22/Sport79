from CapaDatos.modelos import Articulo,MovimientoStock,DetalleArticulo,Usuario,db

class CatalogoArticulos():

    def getall_articulos(self):
        return Articulo.query.all()

    def insert_articulo(self,articulo):
        db.session.add(articulo)
        db.session.commit()

    def actualizar_articulo(self,articulo):
        art = Articulo.query.get(articulo.getId())
        art.setDescripcion(articulo.getDescripcion())
        art.setPrecio(articulo.getPrecio())
        art.setStock(articulo.getStock())
        db.session.commit()

    def eliminar_articulo(self,ideliminar):
        Articulo.query.filter_by(id = ideliminar).delete()
        db.session.commit()

class CatalogoStocks():

    def getAllMovimientosStock(self):
        return MovimientoStock.query.all()

    def setMovimientoStock(self, movstock):
        db.session.add(movstock)
        db.session.commit()
        return movstock.id

class CatalogoDetalles():
    def getAllDetallesSinConfirmar(self):
        return DetalleArticulo.query.filter_by(id_movimientostock=0).all()

    def sumDetallesSinConfimrar(self):
        return db.session.query(db.func.sum(DetalleArticulo.monto)).select_from(DetalleArticulo).scalar()

    def asignarIDdetallesPendientes(self,id):
        detalles = self.getAllDetallesSinConfirmar()
        for det in detalles:
            det.id_movimientostock = id
        db.session.commit()

    def eliminarDetallesPendientes(self,id):
        DetalleArticulo.query.filter_by(id_movimientostock=0).delete()
        db.session.commit()

class CatalogoUsuarios():

    def nuevo_usuario(self,usr):
        db.session.add(usr)
        db.session.commit()

    def validar_login(self,usr,clave):
        usr = Usuario.query.filter_by(nombre=usr, clave=clave).first()
        if usr is None:
            return None
        else:
            return usr

    def modificar_usuario(self,usr):
        usrmod = Usuario.query.get(usr.getId())
        usrmod.setNombre(usr.getNombre())
        usrmod.setClave(usr.getClave())
        usrmod.setHabilitado(usr.getHabilitado())
        db.session.commit()

    def eliminar_usuario(self,idpersonal):
        Usuario.query.filter_by(id=idpersonal).delete()
        db.session.commit()