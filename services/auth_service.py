from models import db
from models.entities import Usuario, TipoUsuario
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

class AuthService:
    @staticmethod
    def register_user(data):
        try:
            hashed_password = generate_password_hash(data['password'])
            
            # Use Stored Procedure for registration
            sql = text("""
                DECLARE @NewId INT;
                EXEC sp_RegistrarUsuario 
                    @idTipoUsuario=:idTipoUsuario, 
                    @idPais=:idPais, 
                    @nombre_usuario=:nombre_usuario, 
                    @apPaterno=:apPaterno, 
                    @apMaterno=:apMaterno, 
                    @correo=:correo, 
                    @password=:password, 
                    @telefono=:telefono,
                    @edad=:edad,
                    @dni=:dni,
                    @idEmpresaTransporte=:idEmpresaTransporte,
                    @licencia=:licencia,
                    @NewIdUsuario=@NewId OUTPUT;
                SELECT @NewId;
            """)
            
            result = db.session.execute(sql, {
                'idTipoUsuario': data['idTipoUsuario'],
                'idPais': data.get('idPais', 135),
                'nombre_usuario': data['nombre_usuario'],
                'apPaterno': data['apPaterno'],
                'apMaterno': data['apMaterno'],
                'correo': data['correo'],
                'password': hashed_password,
                'telefono': data['telefono'],
                'edad': data.get('edad'),
                'dni': data.get('dni'),
                'idEmpresaTransporte': data.get('idEmpresaTransporte'),
                'licencia': data.get('licencia')
            })
            
            new_id = result.scalar()
            db.session.commit()
            
            return {'message': 'User registered successfully', 'idUsuario': new_id}, 201
            
        except Exception as e:
            db.session.rollback()
            # Handle SP thrown errors (51000)
            error_msg = str(e)
            if '51000' in error_msg:
                 # Extract custom message if possible, or generic
                 return {'error': 'El usuario o correo ya existe (SP Error)'}, 400
            return {'error': str(e)}, 500

    @staticmethod
    def login_user(data):
        try:
            # Use Stored Procedure for login
            sql = text("EXEC sp_ValidarLogin @Usuario=:username")
            result = db.session.execute(sql, {'username': data['username']})
            user_row = result.mappings().first()
            
            print(f"DEBUG: Login attempt for {data['username']}")
            
            if not user_row:
                print("DEBUG: User not found in DB")
                return {'error': 'Invalid credentials (User not found)'}, 401
                
            stored_hash = user_row['password']
            if stored_hash:
                stored_hash = str(stored_hash).strip()
                
            print(f"DEBUG: Stored hash (stripped): '{stored_hash}'")
            print(f"DEBUG: Input password: '{data['password']}'")
            
            # Compatibility: check if plain text matches (for legacy/seed data)
            password_matches = False
            
            if stored_hash == data['password']:
                print("DEBUG: Password matched via PLAIN TEXT comparison")
                password_matches = True
            elif stored_hash and check_password_hash(stored_hash, data['password']):
                print("DEBUG: Password matched via HASH comparison")
                password_matches = True
            
            if password_matches:
                # Generate Token
                import datetime
                import jwt
                from flask import current_app
                
                token = jwt.encode({
                    'idUsuario': user_row['idUsuario'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, current_app.config['SECRET_KEY'], algorithm="HS256")
                
                return {
                    'message': 'Login successful',
                    'token': token,
                    'user': {
                        'idUsuario': user_row['idUsuario'],
                        'nombre_usuario': user_row['nombre_usuario'],
                        'idTipoUsuario': user_row['idTipoUsuario'],
                        'tipo': user_row['nombreTipoUsuario'] or 'Unknown',
                        'apPaterno': user_row['apPaterno'],
                        'apMaterno': user_row['apMaterno'],
                        'correo': user_row['correo'],
                        'telefono': user_row['telefono'],
                        'edad': user_row['edad'],
                        'dni': user_row['dni'],
                        'idEmpresaTransporte': user_row['idEmpresaTransporte'],
                        'nombreEmpresa': user_row['nombreEmpresa']
                    }
                }, 200
            else:
                print("DEBUG: Password mismatch")
                return {'error': 'Invalid credentials (Password mismatch)'}, 401
                
        except Exception as e:
            print(f"DEBUG: Exception in login: {e}")
            return {'error': str(e)}, 500

    @staticmethod
    def update_profile_data(data):
        try:
            sql = text("""
                EXEC sp_EditarUsuario
                    @idUsuario=:idUsuario,
                    @nombre_usuario=:nombre_usuario,
                    @apPaterno=:apPaterno,
                    @apMaterno=:apMaterno,
                    @correo=:correo,
                    @telefono=:telefono,
                    @edad=:edad,
                    @dni=:dni,
                    @idPais=:idPais
            """)
            
            db.session.execute(sql, {
                'idUsuario': data['idUsuario'],
                'nombre_usuario': data['nombre_usuario'],
                'apPaterno': data['apPaterno'],
                'apMaterno': data['apMaterno'],
                'correo': data['correo'],
                'telefono': data['telefono'],
                'edad': data['edad'],
                'dni': data.get('dni'),
                'idPais': data.get('idPais', 135) # Default Peru (135) if missing
            })
            db.session.commit()
            
            # Return full updated user object to refresh frontend
            return {'message': 'Perfil actualizado', 'user': data}, 200 
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
