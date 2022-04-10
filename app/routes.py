from flask import request
from app import app
from app.controller import DosenController
from app.controller import UserController

@app.route('/')
def index():
    return 'Hello Flask App'

@app.route('/createadmin', methods=['POST'])
def admins():
    return UserController.create_user_admin()


# endpoint view all dosen dan endpoint Insert Data Dosen
@app.route('/dosen', methods=['GET','POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()


# endpoint view dosen mahasiswa, ubah data dosen dan hapus data dosen
@app.route('/dosen/<id>', methods=['GET','PUT', 'DELETE'])
def dosensDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    elif request.method == 'PUT':
        return DosenController.ubah(id)
    elif request.method == 'DELETE':
        return DosenController.hapus(id)