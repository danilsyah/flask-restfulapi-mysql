from app import app, response
from app.controller import DosenController
from app.controller import UserController
from app.controller import MahasiswaContorller
from flask import request
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

@app.route('/')
def index():
    return 'Hello Flask App'


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return response.success(current_user, 'Sukses')


@app.route('/createadmin', methods=['POST'])
def admins():
    return UserController.create_user_admin()

# endpoint login
@app.route('/login', methods=['POST'])
def logins():
    return UserController.login()

# endpoint upload file
@app.route('/uploads', methods=['POST'])
@jwt_required()
def uploads():
    return UserController.upload()


# ========= route endpoint dosen =======================

# endpoint view all dosen dan endpoint Insert Data Dosen
@app.route('/dosens', methods=['GET','POST'])
# @jwt_required()
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()


# endpoint view dosen mahasiswa detail, ubah data dosen dan hapus data dosen
@app.route('/dosens/<id>', methods=['GET','PUT', 'DELETE'])
def dosensDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    elif request.method == 'PUT':
        return DosenController.ubah(id)
    elif request.method == 'DELETE':
        return DosenController.hapus(id)

# endpoint paging
@app.route('/api/dosens/page', methods=['GET'])
def pagination():
    return DosenController.paginate()


# ======================= route endpoint mahasiswa =====================
@app.route('/mahasiswas', methods=['GET','POST'])
def mhs_index():
    if request.method == 'GET':
        return MahasiswaContorller.index()
    elif request.method == 'POST':
        return MahasiswaContorller.save()
    

# endpoint update mahasiswa
@app.route('/mahasiswas/<id>', methods=['PUT','DELETE'])
def mhs_update(id):
    if request.method == 'PUT':
        return MahasiswaContorller.ubah(id)
    elif request.method == 'DELETE':
        return MahasiswaContorller.hapus(id)