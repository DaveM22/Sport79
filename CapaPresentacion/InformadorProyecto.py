from flask import Flask,render_template,request,flash,url_for,redirect,abort,g
from CapaDatos.modelos import db
from werkzeug.routing import Rule
from CapaDatos import config
from flask_login import LoginManager,login_required,login_user,logout_user,current_user
from CapaDatos.modelos import Usuario,Articulo, MovimientoStock,DetalleArticulo
from CapaNegocio.Logica import ControladorLocal
from datetime import date
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
    return render_template('index.html',pagina='inicio.html')

@app.route('/Prueba')
@login_required
def prueba():
    return render_template('index.html',pagina='informes.html')



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
    if usuario_registrado is False:
            flash('Usuario o contraseña invalidos','error')
            return render_template('index.html',pagina='login.html',error='Credenciales invalidas')
    login_user(usuario_registrado)
    flash('bien logueado')
    return redirect(request.args.get("next") or url_for('index'))


@app.route('/Logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/Stock')
def stock():
    articulos = ControladorLocal().getall_articulos()
    return render_template('index.html',pagina='stock.html',articulos=articulos)


@app.route('/FormularioArticulo')
def formularioarticulos():
    ID = request.args.get('ID')
    if ID is None:
        return render_template('index.html', pagina='FormularioArticulos.html', modificar=None, titulo='Nuevo Articulo',modo='Nuevo')
    else:
        art = Articulo.query.get(ID)
        return render_template('index.html', pagina='FormularioArticulos.html', modificar=art, titulo='Modificar Articulo',modo='Modificar')


@app.route('/registrar_articulo', methods=['POST'])
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
def eliminararticulo():
    id = request.args.get('ID')
    ControladorLocal().eliminar_articulo(id)
    return redirect(url_for('stock'))

@app.route('/Personal')
def personal():
    personal = Usuario.query.all()
    return render_template('index.html', pagina='personal.html', personal=personal)


@app.route('/registrar_personal', methods=['GET', 'POST'])
def registrar_personal():
    nombre = request.form['usuario']
    clave = '123'
    habilitado = True
    if not current_user.is_authenticated:
        tipo = 1
    else:
        tipo = request.form['tipo']
    ControladorLocal().setUsuario(Usuario(nombre,clave,habilitado,tipo))
    return redirect(url_for('personal'))


@app.route('/Ventas')
def ventas():
    detalles = MovimientoStock.query.all()
    return render_template('index.html', pagina='ventas.html', detalles=detalles)

@app.route('/FormularioVentas',methods=['GET','POST'])
def formularioventas():
        articulos = ControladorLocal().getall_articulos()
        detalles = ControladorLocal().getAllDetallesSinConfirmar()
        montototal = ControladorLocal().sumAllDetallesSinConfimrar()
        return render_template('index.html',pagina='FormularioVentas.html',montototal=montototal,articulos=articulos,detalles=detalles,modificar=None,titulo='Nueva Venta')

@app.route('/RegistrarStock',methods=['GET','POST'])
def registrar_stock():
    detalles = ControladorLocal().getAllDetallesSinConfirmar()
    montototal = ControladorLocal().sumAllDetallesSinConfimrar()
    fecha = date.today()
    movstock = MovimientoStock(fecha, montototal)
    id_generado = ControladorLocal().SetMovimientoStock(movstock)
    ControladorLocal().asignarIDDetallesPendientes(id_generado)
    return redirect(url_for('formularioventas'))


@app.route('/AgregarDetalle',methods=['GET','POST'])
def agregardetalle():
    id = request.form['id']
    cantidad = float(request.form['cantidad'])
    print(cantidad)
    precio = Articulo.query.get(id).precio_unitario
    detalle = DetalleArticulo(0,id,precio * cantidad)
    db.session.add(detalle)
    db.session.commit()
    return redirect(url_for('formularioventas'))


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)
