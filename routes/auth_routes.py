from functools import wraps
import jwt
from flask import Blueprint, request, jsonify, current_app
from services.auth_service import AuthService
from models.entities import Usuario
from models import db

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.session.query(Usuario).filter_by(idUsuario=data['idUsuario']).first()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response, status = AuthService.register_user(data)
    return jsonify(response), status

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status = AuthService.login_user(data)
    return jsonify(response), status

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    response, status = AuthService.update_profile_data(data)
    return jsonify(response), status
