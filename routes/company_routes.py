from flask import Blueprint, request, jsonify, current_app, send_from_directory
from sqlalchemy import text
from models import db
import os
from werkzeug.utils import secure_filename

company_bp = Blueprint('company_bp', __name__)

# --- DRIVERS ---
@company_bp.route('/drivers', methods=['GET'])
def get_drivers():
    id_empresa = request.args.get('idEmpresaTransporte')
    if not id_empresa:
        return jsonify({'error': 'idEmpresaTransporte is required'}), 400
    try:
        sql = text("EXEC sp_ListarConductoresEmpresa @idEmpresaTransporte=:id")
        result = db.session.execute(sql, {'id': id_empresa})
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/users/search', methods=['GET'])
def search_user():
    dni = request.args.get('dni')
    if not dni:
        return jsonify({'error': 'DNI required'}), 400
    try:
        sql = text("EXEC sp_BuscarUsuarioPorDNI @dni=:dni")
        result = db.session.execute(sql, {'dni': dni})
        user = result.fetchone()
        if user:
            return jsonify(dict(user._mapping)), 200
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/drivers/assign', methods=['POST'])
def assign_driver():
    data = request.json
    try:
        sql = text("""
            EXEC sp_AsignarConductor 
                @idUsuario=:uid, 
                @idEmpresaTransporte=:eid,
                @licencia=:lic
        """)
        db.session.execute(sql, {
            'uid': data['idUsuario'],
            'eid': data['idEmpresaTransporte'],
            'lic': data['licencia']
        })
        db.session.commit()
        return jsonify({'message': 'Conductor asignado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@company_bp.route('/drivers/<int:id_conductor>', methods=['PUT'])
def update_driver(id_conductor):
    data = request.json
    try:
        sql = text("""
            EXEC sp_EditarConductor 
                @idConductorEmpresa=:cid, 
                @idEmpresaTransporte=:eid,
                @licencia=:lic,
                @estado=:est
        """)
        db.session.execute(sql, {
            'cid': id_conductor,
            'eid': data['idEmpresaTransporte'],
            'lic': data['licencia'],
            'est': data.get('estado', 1) # Default to active if missing
        })
        db.session.commit()
        return jsonify({'message': 'Conductor actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@company_bp.route('/drivers/<int:id_conductor>', methods=['DELETE'])
def delete_driver(id_conductor):
    id_empresa = request.args.get('idEmpresaTransporte')
    if not id_empresa:
        return jsonify({'error': 'idEmpresaTransporte required'}), 400
    try:
        sql = text("EXEC sp_EliminarConductor @idConductorEmpresa=:cid, @idEmpresaTransporte=:eid")
        db.session.execute(sql, {'cid': id_conductor, 'eid': id_empresa})
        db.session.commit()
        return jsonify({'message': 'Conductor eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@company_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    id_empresa = request.args.get('idEmpresaTransporte')
    if not id_empresa:
        return jsonify({'error': 'Missing idEmpresaTransporte'}), 400
    try:
        sql = text("EXEC sp_ListarVehiculosEmpresa @idEmpresaTransporte=:id")
        result = db.session.execute(sql, {'id': id_empresa})
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/vehicle-types', methods=['GET'])
def get_vehicle_types():
    try:
        sql = text("EXEC sp_ListarTiposVehiculo")
        result = db.session.execute(sql)
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/vehicles/<int:id_vehiculo>', methods=['PUT'])
def edit_vehicle(id_vehiculo):
    data = request.json
    try:
        sql = text("""
            EXEC sp_EditarVehiculo
                @idVehiculo=:vid,
                @idEmpresaTransporte=:eid,
                @placa=:placa,
                @capacidadAsientos=:capacidad,
                @idTipoVehiculo=:tipo
        """)
        db.session.execute(sql, {
            'vid': id_vehiculo,
            'eid': data['idEmpresaTransporte'],
            'placa': data['placa'],
            'capacidad': data['capacidadAsientos'],
            'tipo': data['idTipoVehiculo']
        })
        db.session.commit()
        return jsonify({'message': 'Vehículo actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@company_bp.route('/vehicles/<int:id_vehiculo>', methods=['DELETE'])
def delete_vehicle(id_vehiculo):
    id_empresa = request.args.get('idEmpresaTransporte')
    if not id_empresa:
         return jsonify({'error': 'idEmpresaTransporte required'}), 400
    try:
        sql = text("EXEC sp_EliminarVehiculo @idVehiculo=:vid, @idEmpresaTransporte=:eid")
        db.session.execute(sql, {'vid': id_vehiculo, 'eid': id_empresa})
        db.session.commit()
        return jsonify({'message': 'Vehículo eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@company_bp.route('/vehicles', methods=['POST'])
def register_vehicle():
    data = request.json
    try:
        sql = text("""
            EXEC sp_RegistrarVehiculo
                @idEmpresaTransporte=:eid,
                @placa=:placa,
                @modelo=:modelo,
                @capacidadAsientos=:capacidad,
                @idTipoVehiculo=:tipo
        """)
        db.session.execute(sql, {
            'eid': data['idEmpresaTransporte'],
            'placa': data['placa'],
            'modelo': data.get('modelo', ''),
            'capacidad': data['capacidadAsientos'],
            'tipo': data['idTipoVehiculo']
        })
        db.session.commit()
        return jsonify({'message': 'Vehículo registrado'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- TRIPS ---
@company_bp.route('/trips', methods=['GET'])
def get_trips():
    id_empresa = request.args.get('idEmpresaTransporte')
    if not id_empresa:
        return jsonify({'error': 'Missing idEmpresaTransporte'}), 400
    try:
        sql = text("EXEC sp_ListarViajesEmpresa @idEmpresaTransporte=:id")
        result = db.session.execute(sql, {'id': id_empresa})
        rows = []
        for row in result.fetchall():
            d = dict(row._mapping)
            if d.get('fechaSalida'):
                d['fechaSalida'] = str(d['fechaSalida'])
            rows.append(d)
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/trips', methods=['POST'])
def create_trip():
    data = request.json
    try:
        sql = text("""
            EXEC sp_CrearViaje
                @idEmpresaTransporte=:eid,
                @idVehiculo=:vid,
                @idConductorEmpresa=:cid,
                @idRuta=:rid,
                @fechaSalida=:fecha,
                @precio=:precio
        """)
        db.session.execute(sql, {
            'eid': data['idEmpresaTransporte'],
            'vid': data['idVehiculo'],
            'cid': data['idConductorEmpresa'],
            'rid': data['idRuta'],
            'fecha': data['fechaSalida'].replace('T', ' ') if data.get('fechaSalida') else None,
            'precio': data['precio']
        })
        db.session.commit()
        return jsonify({'message': 'Viaje creado'}), 201
    except Exception as e:
        print(f"ERROR creating trip: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- PROMOS ---
@company_bp.route('/promos', methods=['GET'])
def get_promos():
    try:
        sql = text("EXEC sp_ListarPromociones")
        result = db.session.execute(sql)
        rows = []
        for row in result.fetchall():
            d = dict(row._mapping)
            if d.get('fechaInicio'): d['fechaInicio'] = str(d['fechaInicio'])
            if d.get('fechaFin'): d['fechaFin'] = str(d['fechaFin'])
            rows.append(d)
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/promos', methods=['POST'])
def create_promo():
    data = request.json
    try:
        sql = text("""
            EXEC sp_CrearPromocion
                @nombre=:nombre,
                @descripcion=:desc,
                @valor=:valor,
                @fechaInicio=:inicio,
                @fechaFin=:fin
        """)
        db.session.execute(sql, {
            'nombre': data['nombrePromocion'],
            'desc': data['descripcionPromocion'],
            'valor': data['valorDescuento'],
            'inicio': data['fechaInicio'],
            'fin': data['fechaFin']
        })
        db.session.commit()
        return jsonify({'message': 'Promoción creada'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- RUTAS ---
@company_bp.route('/routes', methods=['GET'])
def get_routes():
    try:
        sql = text("EXEC sp_ListarRutas")
        result = db.session.execute(sql)
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/driver/trips', methods=['GET'])
def get_driver_trips():
    id_usuario = request.args.get('idUsuario')
    if not id_usuario:
        return jsonify({'error': 'idUsuario required'}), 400
    try:
        sql = text("EXEC sp_ListarViajesConductor @idUsuario=:uid")
        result = db.session.execute(sql, {'uid': id_usuario})
        rows = []
        for row in result.fetchall():
            d = dict(row._mapping)
            if d.get('fechaSalida'): d['fechaSalida'] = str(d['fechaSalida'])
            rows.append(d)
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/routes', methods=['POST'])
def create_route():
    data = request.json
    try:
        sql = text("EXEC sp_CrearRuta @idOrigen=:orig, @idDestino=:dest, @duracion=:dur, @distanciakm=:dist")
        db.session.execute(sql, {
            'orig': data['idOrigen'],
            'dest': data['idDestino'],
            'dur': data['duracionAprox'],
            'dist': data['distanciakm']
        })
        db.session.commit()
        return jsonify({'message': 'Ruta creada exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@company_bp.route('/destinations', methods=['POST'])
def create_destination():
    data = request.json
    try:
        sql = text("""
            DECLARE @out int;
            EXEC sp_CrearDestino @idProvincia=:prov, @nombreDestino=:nom, @newId=@out OUTPUT;
            SELECT @out AS idDestino;
        """)
        result = db.session.execute(sql, {
            'prov': data['idProvincia'],
            'nom': data['nombreDestino']
        })
        row = result.fetchone()
        new_id = row.idDestino if row else None
        db.session.commit()
        return jsonify({'idDestino': new_id, 'message': 'Destino creado'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- COMPANY INFO & BANNER ---
@company_bp.route('/my-company/<int:id>', methods=['GET'])
def get_company_details(id):
    try:
        sql = text("SELECT * FROM EmpresaTransporte WHERE idEmpresaTransporte = :id")
        result = db.session.execute(sql, {'id': id}).mappings().first()
        if result:
            return jsonify(dict(result)), 200
        return jsonify({'error': 'Empresa not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/banner', methods=['POST'])
def upload_banner():
    if 'banner' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['banner']
    id_empresa = request.form.get('idEmpresaTransporte')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and id_empresa:
        filename = secure_filename(f"banner_{id_empresa}_{file.filename}")
        
        # Save to 'uploads/banners' folder in root
        upload_folder = os.path.join(os.getcwd(), 'uploads', 'banners')
        os.makedirs(upload_folder, exist_ok=True)
        
        file.save(os.path.join(upload_folder, filename))
        
        # Update DB - Use URL path relative to API static serving or new route
        # Using /uploads/banners/filename assuming we add a route for it
        banner_url = f"/uploads/banners/{filename}"
        
        try:
            sql = text("UPDATE EmpresaTransporte SET bannerUrl = :url WHERE idEmpresaTransporte = :id")
            db.session.execute(sql, {'url': banner_url, 'id': id_empresa})
            db.session.commit()
            return jsonify({'message': 'Banner uploaded', 'url': banner_url}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
        
    return jsonify({'error': 'Invalid request'}), 400

# --- SOCIAL NETWORKS ---
@company_bp.route('/socials', methods=['GET'])
def get_socials():
    id_empresa = request.args.get('idEmpresaTransporte')
    if not id_empresa:
        return jsonify({'error': 'idEmpresaTransporte required'}), 400
    try:
        sql = text("EXEC sp_ListarRedesSociales @idEmpresa=:id")
        result = db.session.execute(sql, {'id': id_empresa}).mappings().all()
        return jsonify([dict(row) for row in result]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/socials', methods=['POST'])
def add_social():
    data = request.json
    try:
        sql = text("""
            DECLARE @out INT;
            EXEC @out = sp_AgregarRedSocial @idEmpresa=:id, @red=:red, @url=:url;
            SELECT @out as idRedSocial;
        """)
        # Note: Depending on SP implementation, might need to fetch Scope_Identity differently
        # But for now assuming simple insert or selecting scope_identity 
        # Modifying SP approach slightly if needed, but let's try direct EXEC
        
        # Actually simple insert in SP selects id, so fetchone should work
        result = db.session.execute(text("EXEC sp_AgregarRedSocial @idEmpresa=:id, @red=:red, @url=:url"), {
            'id': data['idEmpresaTransporte'],
            'red': data['red'],
            'url': data['url']
        })
        row = result.fetchone()
        new_id = row[0] if row else None
        db.session.commit()
        return jsonify({'message': 'Red social agregada', 'idRedSocial': new_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@company_bp.route('/socials/<int:id>', methods=['DELETE'])
def delete_social(id):
    id_empresa = request.args.get('idEmpresaTransporte') # Security
    if not id_empresa:
         return jsonify({'error': 'idEmpresaTransporte required'}), 400
    try:
        sql = text("EXEC sp_EliminarRedSocial @idRedSocial=:id, @idEmpresa=:eid")
        db.session.execute(sql, {'id': id, 'eid': id_empresa})
        db.session.commit()
        return jsonify({'message': 'Red social eliminada'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

