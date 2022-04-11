ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','pdf'])

def allowed_file(filename):
    extention = '.' in filename and filename.rsplit('.',1)[1].lower()
    print(f"format gambar => {extention}")
    return extention in ALLOWED_EXTENSIONS