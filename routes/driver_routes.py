from flask import Blueprint, request, jsonify
from models import db
from sqlalchemy import text

driver_bp = Blueprint('driver', __name__)

@driver_bp.route('/current-trip', methods=['GET'])
def get_current_trip():
    idUsuario = request.args.get('idUsuario')
    try:
        sql = text("EXEC sp_ObtenerViajeActualConductor @idUsuario=:idUsuario")
        result = db.session.execute(sql, {'idUsuario': idUsuario})
        row = result.mappings().first()
        
        if row and row['idViaje']:
             # Return trip data
             return jsonify(dict(row)), 200
        else:
             # No active trip, return null but 200 OK
             return jsonify(None), 200
             
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@driver_bp.route('/trip/start', methods=['POST'])
def start_trip():
    data = request.get_json()
    try:
        sql = text("EXEC sp_IniciarViaje @idViaje=:idViaje, @idUsuario=:idUsuario")
        result = db.session.execute(sql, {
            'idViaje': data['idViaje'],
            'idUsuario': data['idUsuario']
        })
        row = result.mappings().first()
        db.session.commit()
        
        if row and row['success']:
            return jsonify({'message': row['message']}), 200
        else:
            return jsonify({'error': row['message'] if row else 'Error desconocido'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@driver_bp.route('/trip/end', methods=['POST'])
def end_trip():
    data = request.get_json()
    try:
        sql = text("EXEC sp_FinalizarViaje @idViaje=:idViaje, @idUsuario=:idUsuario")
        result = db.session.execute(sql, {
            'idViaje': data['idViaje'],
            'idUsuario': data['idUsuario']
        })
        row = result.mappings().first()
        db.session.commit()
        
        if row and row['success']:
            return jsonify({'message': row['message']}), 200
        else:
            return jsonify({'error': row['message'] if row else 'Error desconocido'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@driver_bp.route('/history', methods=['GET'])
def get_trip_history():
    idUsuario = request.args.get('idUsuario')
    try:
        sql = text("EXEC sp_ObtenerHistorialViajesConductor @idUsuario=:idUsuario")
        result = db.session.execute(sql, {'idUsuario': idUsuario})
        rows = [dict(row._mapping) for row in result.fetchall()]
        
        # Serialize dates if needed
        for r in rows:
            if r.get('fechaSalida'):
                 r['fechaSalida'] = str(r['fechaSalida'])
                 
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@driver_bp.route('/trip/passengers', methods=['GET'])
def get_trip_passengers():
    idViaje = request.args.get('idViaje')
    idUsuario = request.args.get('idUsuario')
    try:
        sql = text("EXEC sp_ListarPasajerosViaje @idViaje=:idViaje, @idUsuarioConductor=:idUsuario")
        result = db.session.execute(sql, {
            'idViaje': idViaje,
            'idUsuario': idUsuario
        })
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
