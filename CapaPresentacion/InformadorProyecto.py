from flask import Flask,render_template,request,flash,url_for,redirect,abort,g
from CapaDatos.modelos import db
from werkzeug.routing import Rule
from CapaDatos import config
from flask_login import LoginManager,login_required,login_user,logout_user,current_user
from CapaDatos.modelos import Usuario,Articulo, MovimientoStock,DetalleArticulo,Tipo_usuario, Informe
from CapaNegocio.Logica import ControladorLocal
from datetime import datetime,date
import os

app = Flask(__name__)
app.debug = True
app.url_map.add(Rule('/FormularioArticulos',endpoint='FormularioArticulos'))
app.config.from_object(config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db.init_app(app)
db.create_all(app=app)

@app.route('/')
def index():
    db.session.add(Tipo_usuario('Administrador'))
    db.session.commit()
    db.session.add(Usuario(nombre='admin',clave='admin',habilitado=True,tipo_id=1))
    db.session.commit()
    return render_template('index.html',pagina='inicio.html')

@app.route('/Informes')
@login_required
def informes():
    informes=ControladorLocal().getall_informes()
    return render_template('index.html',pagina='informes.html', informes=informes)

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.route('/Login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
            return render_template('index.html',pagina='login.html')
    usuario = request.form['usuario']
    clave = request.form['clave']
    usuario_registrado = ControladorLocal().validarLogin(usuario,clave)
    if usuario_registrado is None:
            flash('Usuario o contraseña invalidos','error')
            return render_template('index.html',pagina='login.html',error='Credenciales invalidas')
    usuario_registrado.setPassFalsa('####')
    login_user(usuario_registrado)
    flash('bien logueado')
    return redirect(request.args.get("next") or url_for('index'))

@app.route('/Logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/Stock')
@login_required
def stock():
    articulos = ControladorLocal().getall_articulos()
    return render_template('index.html',pagina='stock.html',articulos=articulos)

@app.route('/FormularioPersonal')
@login_required
def formulariopersonal():
    ID = request.args.get('ID')
    if ID is None:
        return render_template('index.html', pagina='FormularioPersonal.html', modificar=None, titulo='Nuevo Usuario',modo='Nuevo')
    else:
        usr = Usuario.query.get(ID)
        return render_template('index.html', pagina='FormularioPersonal.html', modificar=usr, titulo='Modificar Usuario', modo='Modificar')


@app.route('/eliminar_personal',methods=['GET'])
@login_required
def eliminarpersonal():
    id = request.args.get('ID')
    ControladorLocal().eliminarUsuario(id)
    return redirect(url_for('personal'))

@app.route('/FormularioArticulo')
@login_required
def formularioarticulos():
    ID = request.args.get('ID')
    if ID is None:
        return render_template('index.html', pagina='FormularioArticulos.html', modificar=None, titulo='Nuevo Articulo',modo='Nuevo')
    else:
        art = Articulo.query.get(ID)
        return render_template('index.html', pagina='FormularioArticulos.html', modificar=art, titulo='Modificar Articulo',modo='Modificar')

@app.route('/registrar_articulo', methods=['POST'])
@login_required
def registrar_articulo():
    modo = request.form['modo']
    descripcion = request.form['descripcion']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    if modo == 'Nuevo':
        ControladorLocal().nuevo_articulo(Articulo(descripcion, precio, stock))
    else:
        id = request.form['id']
        artmod = Articulo(descripcion, precio, stock, id)
        ControladorLocal().modificar_articulo(artmod)
    return redirect(url_for('stock'))

@app.route('/eliminar_articulo',methods=['GET'])
@login_required
def eliminararticulo():
    id = request.args.get('ID')
    ControladorLocal().eliminar_articulo(id)
    return redirect(url_for('stock'))

@app.route('/eliminar_detalle',methods=['GET'])
@login_required
def eliminar_detalle():
    id = request.args.get('ID')
    ControladorLocal().eliminar_detalle(id)
    return redirect(url_for('formularioventas'))

@app.route('/Personal')
@login_required
def personal():
    personal = Usuario.query.all()
    return render_template('index.html', pagina='personal.html', personal=personal)


@app.route('/registrar_personal', methods=['GET', 'POST'])
@login_required
def registrar_personal():
    modo = request.form['modo']
    nombre = request.form['usuario']
    clave = request.form['clave']
    check = request.form.getlist('habilitado')
    if len(check)== 0:
        habilitado = False
    else:
        habilitado = True
    if modo == 'Nuevo':
        ControladorLocal().setUsuario(Usuario(nombre=nombre,clave=clave,habilitado=habilitado,tipo_id=1))
    else:
        ID = request.form['id']
        ControladorLocal().modificarUsuario(Usuario(tipo_id=1,nombre=nombre,clave=clave,habilitado=habilitado,id=ID))
    return redirect(url_for('personal'))


@app.route('/Ventas')
@login_required
def ventas():
    detalles = ControladorLocal().getAllMovimientosStock()

    montos = ControladorLocal().sumVentasMontoTotales()
    return render_template('index.html', pagina='ventas.html', detalles=detalles , montos=montos)

@app.route('/FormularioVentas',methods=['GET','POST'])
def formularioventas():
        articulos = ControladorLocal().getall_articulos()
        detalles = ControladorLocal().getAllDetallesSinConfirmar()
        montototal = ControladorLocal().sumAllDetallesSinConfimrar()
        return render_template('index.html',pagina='FormularioVentas.html',montototal=montototal,articulos=articulos,detalles=detalles,modificar=None,titulo='Nueva Venta')

@app.route('/RegistrarStock',methods=['GET','POST'])
@login_required
def registrar_stock():
    detalles = ControladorLocal().getAllDetallesSinConfirmar()
    ControladorLocal().AjustarStock()
    montototal = ControladorLocal().sumAllDetallesSinConfimrar()
    fecha = date.today()
    usuario = request.form['idusuario']
    movstock = MovimientoStock(fecha, montototal,id_usuario=usuario)
    id_generado = ControladorLocal().SetMovimientoStock(movstock)
    ControladorLocal().asignarIDDetallesPendientes(id_generado)
    return redirect(url_for('formularioventas'))

@app.route('/RegistrarInforme',methods=['GET','POST'])
@login_required
def registrar_informe():
    monto_total=ControladorLocal().sumVentasMontoTotales()
    fecha_hora = datetime.today()
    inf = Informe(current_user.id, fecha_hora, monto_total)
    ControladorLocal().insertar_informes(inf)
    return redirect(url_for('informes'))


@app.route('/Caja')
@login_required
def caja():
    fecha = date
    horario = datetime.now().strftime("%H:%M")
    monto = ControladorLocal().sumVentasMontoTotales()
    return render_template('index.html',pagina='caja.html',fecha=fecha,monto=monto,horario = horario)

@app.route('/AgregarDetalle',methods=['GET','POST'])
@login_required
def agregardetalle():
    id = request.form['id']
    cantidad = float(request.form['cantidad'])
    print(cantidad)
    precio = Articulo.query.get(id).precio_unitario
    detalle = DetalleArticulo(0,id,precio * cantidad,cantidad)
    db.session.add(detalle)
    db.session.commit()
    return redirect(url_for('formularioventas'))

@app.route('/CancelarVenta',methods=['GET','POST'])
@login_required
def cancelarventa():
    ControladorLocal().eliminarDetallesPendientes()
    return redirect(url_for('ventas'))

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)
