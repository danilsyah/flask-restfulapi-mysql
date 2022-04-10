from app.model.user import User

from app import response, app, db
from flask import request

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