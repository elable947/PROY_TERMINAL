from flask import Blueprint, jsonify
from models import db
from sqlalchemy import text

data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/destinos', methods=['GET'])
def get_destinos():
    try:
        sql = text("EXEC sp_ListarDestinos")
        result = db.session.execute(sql)
        # Use fetchall to get all rows, then convert mappings to dicts
        rows = result.fetchall()
        destinos = [dict(row._mapping) for row in rows]
        return jsonify(destinos), 200
    except Exception as e:
        print(f"Error getting destinos: {e}") # Log error for debug
        return jsonify({'error': str(e)}), 500

@data_bp.route('/empresas', methods=['GET'])
def get_empresas():
    try:
        sql = text("EXEC sp_ListarEmpresas")
        result = db.session.execute(sql)
        rows = result.fetchall()
        empresas = [dict(row._mapping) for row in rows]
        return jsonify(empresas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/paises', methods=['GET'])
def get_paises():
    try:
        sql = text("EXEC sp_ListarPaises")
        result = db.session.execute(sql)
        rows = result.fetchall()
        paises = [dict(row._mapping) for row in rows]
        return jsonify(paises), 200
    except Exception as e:
        print(f"Error getting paises: {e}")
        return jsonify({'error': str(e)}), 500
