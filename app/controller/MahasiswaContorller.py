from app.model.mahasiswa import Mahasiswa
from app.model.dosen import Dosen

from app import response, db
from flask import request, jsonify

def index():
    try:
        mahasiswa = Mahasiswa.query.all()
        data = formatArray(mahasiswa)
        return response.success(data, 'success')
    except Exception as e:
        print(e)
        
        

def formatArray(datas):
    array = []
    for i in datas:
        dosen_satu= Dosen.query.filter_by(id = i.dosen_satu).first()
        dosen_dua = Dosen.query.filter_by(id = i.dosen_dua).first()

        dosen_satu = singleDosen(dosen_satu)
        dosen_dua = singleDosen(dosen_dua)
        array.append(singleObject(i, dosen_satu, dosen_dua))
        
    return array
        
        

def singleObject(data, dosen_satu, dosen_dua):
    data = {
        'id' : data.id,
        'nim': data.nim,
        'nama':data.nama,
        'phone':data.phone,
        'alamat':data.alamat,
        'dosen_satu' : dosen_satu,
        'dosen_dua' : dosen_dua,
    }
    
    return data

def singleDosen(dosen):
    data = {
        'id':dosen.id,
        'nidn':dosen.nidn,
        'nama':dosen.nama,
        'phone':dosen.phone,
        'alamat':dosen.alamat
    }
    
    return data


# ========= CREATE DATA MAHASISWA

def save():
    try:
        nim = request.form.get('nim')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')
        dosen_satu = request.form.get('dosen_satu')
        dosen_dua = request.form.get('dosen_dua')
        
        input = [
            {
                'nim' : nim,
                'nama' : nama,
                'phone' : phone,
                'alamat' : alamat,
                'dosen_satu' : dosen_satu,
                'dosen_dua' : dosen_dua
            }
        ]
        
        # cek duplikasi nomor nim
        nim_mhs = Mahasiswa.query.filter_by(nim = nim).first()
        if nim_mhs :
            return response.badRequest(input, "Nomor NIM sudah ada")
        
        data_mhs = Mahasiswa(nim=nim, nama=nama, phone=phone, alamat=alamat, dosen_satu=dosen_satu, dosen_dua=dosen_dua)
        db.session.add(data_mhs)
        db.session.commit()
        
        return response.success(input, "Data Mahasiswa Berhasil di tambahkan!!!")
    except Exception as e:
        print(e)
        
        
# ============== UPDATE MAHASISWA BY ID
def ubah(id):
    try:
        nim = request.form.get('nim')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')
        dosen_satu = request.form.get('dosen_satu')
        dosen_dua = request.form.get('dosen_dua')
        
        input = [
            {
                'nim' : nim,
                'nama' : nama,
                'phone' : phone,
                'alamat' : alamat,
                'dosen_satu' : dosen_satu,
                'dosen_dua' : dosen_dua
            }
        ]
        
        mhs = Mahasiswa.query.filter_by(id=id).first()
        
        mhs.nim = nim
        mhs.nama = nama
        mhs.phone = phone
        mhs.alamat = alamat
        mhs.dosen_satu = dosen_satu
        mhs.dosen_dua = dosen_dua
        
        db.session.commit()
        
        return response.success(input, 'Sukses Update data mahasiswa')
    except Exception as e:
        print(e)
        
        
# =========== HAPUS DATA MAHASISWA BY ID
def hapus(id):
    try:
        mhs = Mahasiswa.query.filter_by(id=id).first()
        if not mhs:
            return response.badRequest([],"Data Mahasiswa Tidak ada")
        
        data = [
            {
                'nim' : mhs.nim,
                'nama' : mhs.nama,
                'phone' : mhs.phone,
                'alamat' : mhs.alamat,
                'dosen_satu' : mhs.dosen_satu,
                'dosen_dua' : mhs.dosen_dua
            }
        ]
        
        db.session.delete(mhs)
        db.session.commit()
        
        return response.success(data, "Data Mahasiswa Dihapus")
    except Exception as e:
        print(e)