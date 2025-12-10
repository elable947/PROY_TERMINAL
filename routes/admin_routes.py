from flask import Blueprint, request, jsonify
from models import db
from sqlalchemy import text

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    try:
        sql = text("""
            DECLARE @NewId INT;
            EXEC sp_CrearEmpresa 
                @nombreEmpresa=:nombreEmpresa, 
                @razonSocial=:razonSocial, 
                @ruc=:ruc, 
                @telefonoEmpresa=:telefonoEmpresa,
                @NewId=@NewId OUTPUT;
            SELECT @NewId;
        """)
        result = db.session.execute(sql, {
            'nombreEmpresa': data['nombreEmpresa'],
            'razonSocial': data.get('razonSocial'),
            'ruc': data['ruc'],
            'telefonoEmpresa': data.get('telefonoEmpresa')
        })
        new_id = result.scalar()
        db.session.commit()
        return jsonify({'message': 'Empresa creada exitosamente', 'idEmpresa': new_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/pending', methods=['GET'])
def get_pending_users():
    try:
        sql = text("EXEC sp_ListarUsuariosPendientes")
        result = db.session.execute(sql)
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/approve', methods=['POST'])
def approve_user():
    data = request.get_json()
    try:
        sql = text("EXEC sp_AprobarUsuario @idUsuario=:idUsuario")
        db.session.execute(sql, {'idUsuario': data['idUsuario']})
        db.session.commit()
        return jsonify({'message': 'Usuario aprobado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/assign-company', methods=['POST'])
def assign_company():
    data = request.get_json()
    try:
        sql = text("EXEC sp_AsignarEmpresaUsuario @idUsuario=:idUsuario, @idEmpresaTransporte=:idEmpresa")
        db.session.execute(sql, {
            'idUsuario': data['idUsuario'],
            'idEmpresa': data['idEmpresa']
        })
        db.session.commit()
        return jsonify({'message': 'Empresa asignada correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/search', methods=['GET'])
def search_user():
    dni = request.args.get('dni')
    if not dni:
        return jsonify({'error': 'DNI es requerido'}), 400
    try:
        sql = text("EXEC sp_BuscarUsuarioPorDNI @dni=:dni")
        result = db.session.execute(sql, {'dni': dni})
        row = result.mappings().first()
        if row:
            return jsonify(dict(row)), 200
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/companies/<int:id>', methods=['GET'])
def get_company_details(id):
    try:
        sql = text("EXEC sp_ObtenerDetalleEmpresaAdmin @idEmpresaTransporte=:id")
        result = db.session.execute(sql, {'id': id})
        row = result.mappings().first()
        if row:
            return jsonify(dict(row)), 200
        else:
            return jsonify({'error': 'Empresa no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
