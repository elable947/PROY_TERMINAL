from . import db
from sqlalchemy.orm import relationship

class Paises(db.Model):
    __tablename__ = 'Paises'
    idPais = db.Column(db.Integer, primary_key=True)
    nombrePais = db.Column(db.String, nullable=False)
    codTelefonico = db.Column(db.String, nullable=False)
    usuarios = relationship('Usuario', backref='pais', lazy=True)

class TipoUsuario(db.Model):
    __tablename__ = 'TipoUsuario'
    idTipoUsuario = db.Column(db.Integer, primary_key=True)
    nombreTipoUsuario = db.Column(db.String)
    usuarios = relationship('Usuario', backref='tipo_usuario', lazy=True)

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    idTipoUsuario = db.Column(db.Integer, db.ForeignKey('TipoUsuario.idTipoUsuario'), nullable=False)
    idPais = db.Column(db.Integer, db.ForeignKey('Paises.idPais'), nullable=False)
    nombre_usuario = db.Column(db.String, nullable=False)
    apPaterno = db.Column(db.String, nullable=False)
    apMaterno = db.Column(db.String, nullable=False)
    correo = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    telefono = db.Column(db.String, nullable=False)
    edad = db.Column(db.Integer)
    dni = db.Column(db.String)
    esActivo = db.Column(db.Boolean)
    
    registro_login = relationship('RegistroLogin', backref='usuario', lazy=True)
    notificaciones = relationship('Notificaciones', backref='usuario', lazy=True)
    usuario_empresa = relationship('UsuarioEmpresa', backref='usuario', lazy=True)
    boletos = relationship('Boleto', backref='usuario', lazy=True)

class RegistroLogin(db.Model):
    __tablename__ = 'RegistroLogin'
    idLogin = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'))
    fecharegistro = db.Column(db.DateTime)
    ip = db.Column(db.String)

class Departamento(db.Model):
    __tablename__ = 'Departamento'
    idDepartamento = db.Column(db.Integer, primary_key=True)
    nombreDepartamento = db.Column(db.String)
    provincias = relationship('Provincia', backref='departamento', lazy=True)

class Provincia(db.Model):
    __tablename__ = 'Provincia'
    idProvincia = db.Column(db.Integer, primary_key=True)
    idDepartamento = db.Column(db.Integer, db.ForeignKey('Departamento.idDepartamento'))
    nombreProvincia = db.Column(db.String)
    destinos = relationship('Destino', backref='provincia', lazy=True)

class Destino(db.Model):
    __tablename__ = 'Destino'
    idDestino = db.Column(db.Integer, primary_key=True)
    idProvincia = db.Column(db.Integer, db.ForeignKey('Provincia.idProvincia'), nullable=False)
    nombreDestino = db.Column(db.String, nullable=False)
    rutas = relationship('Ruta', backref='destino', lazy=True)

class Terminal(db.Model):
    __tablename__ = 'Terminal'
    idTerminal = db.Column(db.Integer, primary_key=True)
    idProvincia = db.Column(db.Integer) # Missing FK in schema info, keeping as is
    esPrincipal = db.Column(db.Boolean)
    nombreTerminal = db.Column(db.String)
    direccion = db.Column(db.String)
    rutas_origen = relationship('Ruta', backref='terminal_origen', lazy=True)

class EmpresaTransporte(db.Model):
    __tablename__ = 'EmpresaTransporte'
    idEmpresaTransporte = db.Column(db.Integer, primary_key=True)
    nombreEmpresa = db.Column(db.String, nullable=False)
    razonSocial = db.Column(db.String, nullable=False)
    ruc = db.Column(db.String, nullable=False)
    telefonoEmpresa = db.Column(db.String, nullable=False)
    bannerUrl = db.Column(db.String)
    
    redes_sociales = relationship('RedSocial', backref='empresa', lazy=True)
    vehiculos = relationship('Vehiculo', backref='empresa', lazy=True)
    conductores = relationship('ConductorEmpresa', backref='empresa', lazy=True)
    viajes = relationship('Viaje', backref='empresa', lazy=True)
    usuarios_empresa = relationship('UsuarioEmpresa', backref='empresa', lazy=True)

class RedSocial(db.Model):
    __tablename__ = 'RedSocial'
    idRedSocial = db.Column(db.Integer, primary_key=True)
    idEmpresaTransporte = db.Column(db.Integer, db.ForeignKey('EmpresaTransporte.idEmpresaTransporte'))
    red = db.Column(db.String)
    url = db.Column(db.String)

class UsuarioEmpresa(db.Model):
    __tablename__ = 'UsuarioEmpresa'
    idUsuarioEmpresa = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'))
    idEmpresaTransporte = db.Column(db.Integer, db.ForeignKey('EmpresaTransporte.idEmpresaTransporte'))

class TipoVehiculo(db.Model):
    __tablename__ = 'TipoVehiculo'
    idTipoVehiculo = db.Column(db.Integer, primary_key=True)
    nombreTipoVehiculo = db.Column(db.String)
    vehiculos = relationship('Vehiculo', backref='tipo_vehiculo', lazy=True)

class Vehiculo(db.Model):
    __tablename__ = 'Vehiculo'
    idVehiculo = db.Column(db.Integer, primary_key=True)
    idEmpresaTransporte = db.Column(db.Integer, db.ForeignKey('EmpresaTransporte.idEmpresaTransporte'), nullable=False)
    idTipoVehiculo = db.Column(db.Integer, db.ForeignKey('TipoVehiculo.idTipoVehiculo'), nullable=False)
    placa = db.Column(db.String, nullable=False)
    capacidadAsientos = db.Column(db.Integer, nullable=False)
    estadoVehiculo = db.Column(db.Boolean, nullable=False)
    viajes = relationship('Viaje', backref='vehiculo', lazy=True)

class ConductorEmpresa(db.Model):
    __tablename__ = 'ConductorEmpresa'
    idConductorEmpresa = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'))
    idEmpresaTransporte = db.Column(db.Integer, db.ForeignKey('EmpresaTransporte.idEmpresaTransporte'))
    licencia = db.Column(db.String)
    fechaingreso = db.Column(db.Date)
    estadoConductorEmpresa = db.Column(db.Boolean)
    viajes = relationship('Viaje', backref='conductor', lazy=True)

class Ruta(db.Model):
    __tablename__ = 'Ruta'
    idRuta = db.Column(db.Integer, primary_key=True)
    idOrigen = db.Column(db.Integer, db.ForeignKey('Terminal.idTerminal'))
    idDestino = db.Column(db.Integer, db.ForeignKey('Destino.idDestino'))
    duracionAprox = db.Column(db.String)
    distanciakm = db.Column(db.Numeric)
    estadoRuta = db.Column(db.Boolean)
    
    viajes = relationship('Viaje', backref='ruta', lazy=True)
    promociones = relationship('PromocionRuta', backref='ruta', lazy=True)

class Horario(db.Model):
    __tablename__ = 'Horario'
    idHorario = db.Column(db.Integer, primary_key=True)
    horaSalida = db.Column(db.Time, nullable=False)
    horaLlegadaAprox = db.Column(db.Time)
    viajes = relationship('Viaje', backref='horario', lazy=True)

class EstadoViaje(db.Model):
    __tablename__ = 'EstadoViaje'
    idEstadoViaje = db.Column(db.Integer, primary_key=True)
    nombreEstadoViaje = db.Column(db.String)
    viajes = relationship('Viaje', backref='estado_viaje', lazy=True)

class Viaje(db.Model):
    __tablename__ = 'Viaje'
    idViaje = db.Column(db.Integer, primary_key=True)
    idEmpresaTransporte = db.Column(db.Integer, db.ForeignKey('EmpresaTransporte.idEmpresaTransporte'), nullable=False)
    idVehiculo = db.Column(db.Integer, db.ForeignKey('Vehiculo.idVehiculo'), nullable=False)
    idConductorEmpresa = db.Column(db.Integer, db.ForeignKey('ConductorEmpresa.idConductorEmpresa'), nullable=False)
    idRuta = db.Column(db.Integer, db.ForeignKey('Ruta.idRuta'), nullable=False)
    fechaSalida = db.Column(db.DateTime)
    idHorario = db.Column(db.Integer, db.ForeignKey('Horario.idHorario'))
    precio = db.Column(db.Numeric)
    asientosDisponibles = db.Column(db.Integer)
    idEstadoViaje = db.Column(db.Integer, db.ForeignKey('EstadoViaje.idEstadoViaje'))
    
    asientos = relationship('Asiento', backref='viaje', lazy=True)
    boletos = relationship('Boleto', backref='viaje', lazy=True)

class EstadoBoleto(db.Model):
    __tablename__ = 'EstadoBoleto'
    idEstadoBoleto = db.Column(db.Integer, primary_key=True)
    nombreEstadoBoleto = db.Column(db.String)
    boletos = relationship('Boleto', backref='estado_boleto', lazy=True)

class Asiento(db.Model):
    __tablename__ = 'Asiento'
    idAsiento = db.Column(db.Integer, primary_key=True)
    idViaje = db.Column(db.Integer, db.ForeignKey('Viaje.idViaje'), nullable=False)
    numeroAsiento = db.Column(db.Integer)
    disponible = db.Column(db.Boolean)
    boletos = relationship('Boleto', backref='asiento', lazy=True)

class Boleto(db.Model):
    __tablename__ = 'Boleto'
    idBoleto = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'), nullable=False)
    idViaje = db.Column(db.Integer, db.ForeignKey('Viaje.idViaje'), nullable=False)
    idAsiento = db.Column(db.Integer, db.ForeignKey('Asiento.idAsiento'), nullable=False)
    idEstadoBoleto = db.Column(db.Integer, db.ForeignKey('EstadoBoleto.idEstadoBoleto'))
    fechaCompra = db.Column(db.DateTime)
    
    pagos = relationship('Pago', backref='boleto', lazy=True)

class MetodoPago(db.Model):
    __tablename__ = 'MetodoPago'
    idMetodoPago = db.Column(db.Integer, primary_key=True)
    nombreMetodoPago = db.Column(db.String)
    pagos = relationship('Pago', backref='metodo_pago', lazy=True)

class Pago(db.Model):
    __tablename__ = 'Pago'
    idPago = db.Column(db.Integer, primary_key=True)
    idBoleto = db.Column(db.Integer, db.ForeignKey('Boleto.idBoleto'))
    monto = db.Column(db.Numeric)
    idMetodoPago = db.Column(db.Integer, db.ForeignKey('MetodoPago.idMetodoPago'))
    fechaPago = db.Column(db.DateTime)
    confirmado = db.Column(db.Boolean)

class Notificaciones(db.Model):
    __tablename__ = 'Notificaciones'
    idNotificacion = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'))
    mensaje = db.Column(db.String)
    fechaEnvio = db.Column(db.DateTime)
    leido = db.Column(db.Boolean)

class TipoDescuento(db.Model):
    __tablename__ = 'TipoDescuento'
    idTipoDescuento = db.Column(db.Integer, primary_key=True)
    nombreTipoDescuento = db.Column(db.String)
    promociones = relationship('Promocion', backref='tipo_descuento', lazy=True)

class Promocion(db.Model):
    __tablename__ = 'Promocion'
    idPromocion = db.Column(db.Integer, primary_key=True)
    nombrePromocion = db.Column(db.String)
    descripcionPromocion = db.Column(db.String)
    idTipoDescuento = db.Column(db.Integer, db.ForeignKey('TipoDescuento.idTipoDescuento'))
    valorDescuento = db.Column(db.Numeric)
    fechaInicio = db.Column(db.DateTime)
    fechaFin = db.Column(db.DateTime)
    estadoPromocion = db.Column(db.Boolean)
    rutas = relationship('PromocionRuta', backref='promocion', lazy=True)

class PromocionRuta(db.Model):
    __tablename__ = 'PromocionRuta'
    idPromocionRuta = db.Column(db.Integer, primary_key=True)
    idPromocion = db.Column(db.Integer, db.ForeignKey('Promocion.idPromocion'))
    idRuta = db.Column(db.Integer, db.ForeignKey('Ruta.idRuta'))
    estadoPromocionRuta = db.Column(db.Boolean)
