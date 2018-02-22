from CapaDatos.Datos import CatalogoArticulos,CatalogoDetalles,CatalogoStocks,CatalogoUsuarios, CatalogoInformes

class ControladorLocal():

    def __init__(self):
        self.articulosdata = CatalogoArticulos()
        self.detallesdata = CatalogoDetalles()
        self.movstockdata = CatalogoStocks()
        self.catusuarios = CatalogoUsuarios()
        self.catinformes = CatalogoInformes()

    def getall_informes(self):
        return self.catinformes.getall_informes()

    def insertar_informes(self,informe):
        self.catinformes.insertar_informes(informe)

    def getall_articulos(self):
        return self.articulosdata.getall_articulos()

    def nuevo_articulo(self,articulo):
        self.articulosdata.insert_articulo(articulo)

    def modificar_articulo(self,articulo):
        self.articulosdata.actualizar_articulo(articulo)

    def eliminar_articulo(self,ideliminar):
        self.articulosdata.eliminar_articulo(ideliminar)

    def eliminar_detalle(self,ideliminar):
        self.detallesdata.eliminar_detalle(ideliminar)

    def getAllDetallesSinConfirmar(self):
        return self.detallesdata.getAllDetallesSinConfirmar()

    def sumAllDetallesSinConfimrar(self):
        return self.detallesdata.sumDetallesSinConfimrar()

    def asignarIDDetallesPendientes(self,id):
        self.detallesdata.asignarIDdetallesPendientes(id)

    def SetMovimientoStock(self,movstock):
        return self.movstockdata.setMovimientoStock(movstock)

    def setUsuario(self,usr):
        self.catusuarios.nuevo_usuario(usr)

    def modificarUsuario(self,usr):
        self.catusuarios.modificar_usuario(usr)

    def eliminarUsuario(self,ideliminar):
        self.catusuarios.eliminar_usuario(ideliminar)

    def validarLogin(self,usr,clave):
        return self.catusuarios.validar_login(usr,clave)

    def eliminarDetallesPendientes(self):
        self.detallesdata.eliminarDetallesPendientes()

    def sumVentasMontoTotales(self):
        return self.movstockdata.sumVentasMontoTotales()

    def getAllMovimientosStock(self):
        return self.movstockdata.getAllMovimientosStock()

    def AjustarStock(self):
        detalles = self.detallesdata.getAllDetallesSinConfirmar()
        for det in detalles:
            self.articulosdata.descontar_stock(det)







