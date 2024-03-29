from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa

from app import response, app, db
from flask import request, jsonify,abort

import math

def index():
    try:
        dosen = Dosen.query.all()
        data = formatarray(dosen)
        return response.success(data, "success")
    except Exception as e:
        print(e)

def formatarray(datas):
    array = []
    
    for i in datas:
        array.append(singleObject(i))
        
    return array
        

def singleObject(data):
    data = {
        'id':data.id,
        'nidn':data.nidn,
        'nama':data.nama,
        'phone':data.phone,
        'alamat':data.alamat
    }
    
    return data

# menampilkan mahasiswa dengan dosen yang sama
def detail(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        mahasiswa = Mahasiswa.query.filter((Mahasiswa.dosen_satu == id) | (Mahasiswa.dosen_dua == id))
        
        if not dosen:
            return response.badRequest([], 'Tidak ada data dosen')
        
        data_mahasiswa = formatMahasiswa(mahasiswa)
        
        data = singleDetailMahasiswa(dosen, data_mahasiswa)
        
        return response.success(data, "success")
    
    except Exception as e:
        print(e)
    

def singleDetailMahasiswa(dosen, mahasiswa):
    data = {
        'id':dosen.id,
        'nidn':dosen.nidn,
        'nama':dosen.nama,
        'phone':dosen.phone,
        'mahasiswa':mahasiswa
    }
    
    return data
     
     
def singleMahasiswa(mahasiswa):
    data = {
        'id': mahasiswa.id,
        'nim': mahasiswa.nim,
        'nama':mahasiswa.nama,
        'phone':mahasiswa.phone
    }
    
    return data
        

def formatMahasiswa(data):
    array = []
    for i in data:
        array.append(singleMahasiswa(i))
        
    return array


# insert data dosen
def save():
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')
        
        input = [
            {
                'nidn'  : nidn,
                'nama'  : nama,
                'phone' : phone,
                'alamat': alamat
            }
        ]
        
        # cek validasi apakah data nomor nidn sudah ada di database
        nidn_dosen_exist = Dosen.query.filter_by(nidn=nidn).first()
        if nidn_dosen_exist :
            return response.badRequest(input, "Nomor NIDN sudah ada")
        
        
        data_dosen = Dosen(nidn=nidn, nama=nama, phone=phone, alamat=alamat)
        db.session.add(data_dosen)
        db.session.commit()
        
        return response.success(input,"Data Dosen Berhasil di tambahkan")
    except Exception as e:
        print(e)
        

# update data dosen berdasarkan id
def ubah(id):
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')
        
        input = [
            {
                'nidn':nidn,
                'nama':nama,
                'phone':phone,
                'alamat':alamat
            }
        ]
        
        dosen = Dosen.query.filter_by(id=id).first()
        
        dosen.nidn = nidn
        dosen.nama = nama
        dosen.phone = phone
        dosen.alamat = alamat
        
        db.session.commit()
        
        return response.success(input, 'Sukses update data dosen!')
    except Exception as e:
        print(e)


# hapus data dosen berdasarkan id
def hapus(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.badRequest([], "Data Dosen Kosong")
        
        
        data = [
            {
                'nidn' : dosen.nidn,
                'nama' : dosen.nama,
                'phone' : dosen.phone,
                'alamat' : dosen.alamat
            }
        ]
        
        db.session.delete(dosen)
        db.session.commit()
        
        return response.success(data, "Data Dosen Berhasil Di Hapus")
    except Exception as e:
        print(e)
        

# page pagination
def get_pagination(cls, url, start, limit):
    # ambil data select query
    results = cls.query.all()
    # ubah format data
    data = formatarray(results)
    # hitung jumlah data
    count = len(data)
    
    obj = {}
    
    if count < start:
        obj['success'] = False
        obj['message'] = "Page yang dipilih melewati batas total data!"
        return obj
    else:
        obj['success'] = True
        obj['start_page'] = start
        obj['per_page'] = limit
        obj['total_data'] = count
        obj['total_page'] = math.ceil(count/limit)
        
        # previous link
        if start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, start-limit)
            limit_copy = start - 1
            obj['previous'] = url + f'?start={start_copy}&limit={limit_copy}'
            
        # next link
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + f'?start={start_copy}&limit={limit}'
            
        obj['result'] = data[(start - 1): (start - 1 + limit)]
        return obj
    
# function paging
def paginate():
    # ambil parameter get
    # sample http://127.0.0.1:5000/dosen?page=1
    
    start = request.args.get('start')
    limit = request.args.get('limit')
    
    try:
        if start == None or limit == None:
            return jsonify(get_pagination(
                Dosen, 
                'http://127.0.0.1:5000/api/dosens/page',
                start=request.args.get('start', 1),
                limit=request.args.get('limit', 3)
            ))
        else:
            return jsonify(get_pagination(
                Dosen,
                'http://127.0.0.1:5000/api/dosens/page',
                start=int(start),
                limit=int(limit)
            ))
    except Exception as e:
        print(e)