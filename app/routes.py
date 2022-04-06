from flask import request
from app import app
from app.controller import DosenController

@app.route('/')
def index():
    return 'Hello Flask App'

# endpoint view all dosen dan endpoint Insert Data Dosen
@app.route('/dosen', methods=['GET','POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()


# endpoint view mahasiswa dengan dosen yang sama 
@app.route('/dosen/<id>', methods=['GET'])
def dosensDetail(id):
    return DosenController.detail(id)