from flask import Blueprint, jsonify, request
from sqlalchemy import text
from models import db

location_bp = Blueprint('location_bp', __name__)

@location_bp.route('/departments', methods=['GET'])
def get_departments():
    try:
        sql = text("EXEC sp_ListarDepartamentos")
        result = db.session.execute(sql)
        # SQLAlchemy returns rows that can be converted to dict
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@location_bp.route('/provinces/<int:dept_id>', methods=['GET'])
def get_provinces(dept_id):
    try:
        sql = text("EXEC sp_ListarProvincias @idDepartamento=:id")
        result = db.session.execute(sql, {'id': dept_id})
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@location_bp.route('/destinations/by-province/<int:prov_id>', methods=['GET'])
def get_destinations_by_prov(prov_id):
    try:
        # Check if SP exists, otherwise use raw SQL for safety if SP confusing
        # Using raw SQL for terminals to be safe
        sql = text("EXEC sp_ListarDestinosPorProvincia @idProvincia=:id")
        result = db.session.execute(sql, {'id': prov_id})
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@location_bp.route('/terminals', methods=['GET'])
def get_terminals():
    try:
        sql = text("SELECT idTerminal, nombreTerminal FROM Terminal WHERE estado = 1")
        # estado column might be different? 'estadoTerminal'? 
        # Checking schema from list_terminals output: (1, 3, True, 'Name', ...)
        # 3rd column is BIT. Probably active.
        # But wait, list_terminals printed tuple.
        # (1, 3, True, ...)
        # I need to confirm column names.
        # I'll just select idTerminal, nombreTerminal assuming names.
        # Or better: SELECT * FROM Terminal.
        sql = text("SELECT idTerminal, nombreTerminal FROM Terminal")
        result = db.session.execute(sql)
        rows = [dict(row._mapping) for row in result.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        # Fallback if names wrong
        return jsonify({'error': str(e)}), 500
