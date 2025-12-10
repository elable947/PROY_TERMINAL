from flask import Blueprint, request, jsonify
from sqlalchemy import text
from models import db
from routes.auth_routes import token_required

client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/trips/<int:id_viaje>/seats', methods=['GET'])
# Publicly accessible to view seats? Or token required?
# Usually viewing seats is public to encourage buying.
def get_seats(id_viaje):
    try:
        sql = text("EXEC sp_ObtenerAsientosViaje @idViaje=:idViaje")
        result = db.session.execute(sql, {'idViaje': id_viaje}).mappings().all()
        # Commit needed because sp_GenerarAsientos inserts rows!
        db.session.commit()
        return jsonify([dict(row) for row in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/payment-methods', methods=['GET'])
def get_payment_methods():
    try:
        sql = text("SELECT * FROM MetodoPago")
        result = db.session.execute(sql).mappings().all()
        return jsonify([dict(row) for row in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/purchase', methods=['POST'])
@token_required
def purchase_ticket(current_user):
    data = request.json
    id_viaje = data.get('idViaje')
    id_asiento = data.get('idAsiento')
    id_metodo = data.get('idMetodoPago', 1) 
    
    print(f"DEBUG: Purchase Request - User: {current_user.idUsuario}, Viaje: {id_viaje}, Asiento: {id_asiento}, Metodo: {id_metodo}")
    
    if not id_viaje or not id_asiento:
        print("DEBUG: Missing data")
        return jsonify({'error': 'Faltan datos'}), 400

    try:
        # Pass idMetodoPago
        sql = text("EXEC sp_ComprarBoleto @idUsuario=:idUsuario, @idViaje=:idViaje, @idAsiento=:idAsiento, @idMetodoPago=:idMetodoPago")
        params = {
            'idUsuario': current_user.idUsuario,
            'idViaje': id_viaje,
            'idAsiento': id_asiento,
            'idMetodoPago': id_metodo
        }
        
        result = db.session.execute(sql, params).mappings().fetchone()
        db.session.commit()
        print(f"DEBUG: Purchase Success - Boleto: {result}")
        
        return jsonify({'message': 'Compra exitosa', 'boleto': dict(result)})
        
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Purchase Error: {e}")
        return jsonify({'error': str(e)}), 500

@client_bp.route('/reserve', methods=['POST'])
@token_required
def reserve_ticket(current_user):
    data = request.json
    id_viaje = data.get('idViaje')
    id_asiento = data.get('idAsiento')
    
    if not id_viaje or not id_asiento:
        return jsonify({'error': 'Faltan datos'}), 400

    try:
        sql = text("EXEC sp_ReservarBoleto @idUsuario=:idUsuario, @idViaje=:idViaje, @idAsiento=:idAsiento")
        params = {
            'idUsuario': current_user.idUsuario,
            'idViaje': id_viaje,
            'idAsiento': id_asiento
        }
        
        result = db.session.execute(sql, params).mappings().fetchone()
        db.session.commit()
        
        return jsonify({'message': 'Reserva exitosa', 'boleto': dict(result)})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@client_bp.route('/history', methods=['GET'])
@token_required
def get_history(current_user):
    try:
        sql = text("EXEC sp_ObtenerHistorialUsuario @idUsuario=:idUsuario")
        result = db.session.execute(sql, {'idUsuario': current_user.idUsuario}).mappings().all()
        return jsonify([dict(row) for row in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/ticket/<int:id_boleto>', methods=['GET'])
@token_required
def get_ticket_detail(current_user, id_boleto):
    try:
        sql = text("EXEC sp_ObtenerDetalleBoleta @idBoleto=:idBoleto")
        result = db.session.execute(sql, {'idBoleto': id_boleto}).mappings().fetchone()
        if result:
            return jsonify(dict(result))
        else:
            return jsonify({'error': 'Boleta no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/cancel-reservation', methods=['POST'])
@token_required
def cancel_reservation(current_user):
    data = request.get_json()
    try:
        sql = text("EXEC sp_CancelarReserva @idBoleto=:idBoleto, @idUsuario=:idUsuario")
        result = db.session.execute(sql, {
            'idBoleto': data['idBoleto'],
            'idUsuario': current_user.idUsuario
        })
        row = result.mappings().first()
        db.session.commit()
        
        if row and row['success']:
            return jsonify({'message': row['message']}), 200
        else:
            return jsonify({'error': row['message'] if row else 'Error al cancelar'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
