from app.model.user import User
from app.model.gambar import Gambar

from app import response, app, db, uploadconfig
from flask import request
import os
import uuid
from werkzeug.utils import secure_filename

from datetime import timedelta
from flask_jwt_extended import *


# membuat user superadmin
def create_user_admin():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        level = 1
        
        users = User(name=name, email=email, level=level)
        users.set_password(password)
        db.session.add(users)
        db.session.commit()
        
        return response.success('', 'Success Create Data User Admin')
    except Exception as e:
        print(e)
        

def singleObject(data):
    data = {
        'id' : data.id,
        'name' : data.name,
        'email' : data.email,
        'level' : data.level
    }
    
    return data


# Login dan generate Token JWT
def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return response.badRequest([], 'Email tidak terdaftar')
        
        if not user.check_password(password):
            return response.badRequest([], 'Kombinasi password salah')

        
        data = singleObject(user)

        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        acces_token = create_access_token(data, fresh=True, expires_delta= expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            "data" : data,
            "access_token" : acces_token,
            "refresh_token" : refresh_token,
        }, "Sukses Login!")
        
    except Exception as e:
        print(e)
        

# proses upload foto
def upload():
    try:
        judul = request.form.get('judul')
        
        if 'file' not in request.files:
            return response.badRequest([], 'File tidak ada')
        
        file = request.files['file']
        
        if file.filename == '':
            return response.badRequest([], 'File tidak ada')
        
        if file and uploadconfig.allowed_file(file.filename):
            uid = uuid.uuid4()
            filename = secure_filename(file.filename)
            renamefile = "Flask-"+str(uid)+filename
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], renamefile))
            
            uploads = Gambar(judul=judul, pathname=renamefile)
            db.session.add(uploads)
            db.session.commit()
            
            return response.success(
                {
                    'judul': judul,
                    'pathname' : renamefile
                },
                "Sukses mengupload file"
            )
        else:
            return response.badRequest([],"Extension File tidak diizinkan")
            
    except Exception as e:
        print(e)