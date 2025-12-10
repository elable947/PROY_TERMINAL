from flask import Blueprint, request, jsonify
from sqlalchemy import text
from models import db
from datetime import datetime

public_bp = Blueprint('public_bp', __name__)

@public_bp.route('/companies', methods=['GET'])
def get_public_companies():
    try:
        sql = text("EXEC sp_ListarEmpresas")
        result = db.session.execute(sql).mappings().all()
        companies = [dict(row) for row in result]
        
        # Enrich with social networks
        for company in companies:
            social_sql = text("SELECT * FROM RedSocial WHERE idEmpresaTransporte = :id")
            socials_res = db.session.execute(social_sql, {'id': company['idEmpresaTransporte']}).mappings().all()
            company['redesSociales'] = [dict(s) for s in socials_res]
            
        return jsonify(companies)
    except Exception as e:
        print(f"Error listing public companies: {e}")
        return jsonify({'error': str(e)}), 500

@public_bp.route('/trips', methods=['GET'])
def get_public_trips():
    id_destino = request.args.get('idDestino')
    id_empresa = request.args.get('idEmpresa')
    
    try:
        sql = text("EXEC sp_ListarViajesPublico @idDestino=:idDestino, @idEmpresa=:idEmpresa")
        params = {
            'idDestino': id_destino if id_destino else None,
            'idEmpresa': id_empresa if id_empresa else None
        }
        result = db.session.execute(sql, params).mappings().all()
        
        trips = []
        for row in result:
            trip = dict(row)
            # Serialize dates
            if isinstance(trip.get('fechaSalida'), datetime):
                trip['fechaSalida'] = trip['fechaSalida'].isoformat()
            trips.append(trip)
            
        return jsonify(trips)
    except Exception as e:
        print(f"Error listing public trips: {e}")
        return jsonify({'error': str(e)}), 500

@public_bp.route('/destinations', methods=['GET'])
def get_public_destinations():
    try:
        sql = text("EXEC sp_ListarDestinos") # Reusing existing SP
        result = db.session.execute(sql).mappings().all()
        return jsonify([dict(row) for row in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
