from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import jwt
import hashlib
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
Migrate(app, db)
CORS(app)

def generate_password_hash(password):
    password_hashed = hashlib.md5(password.encode()).hexdigest()
    return password_hashed

# модель для хранения задачи
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.Strring, nullable=False)

# презентер для задачи
def present_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "is_done": task.is_done
    }

# получаем все задачи
@app.route('/api/sign_up', methods=['GET'])
def sign_up():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    
    if not name or not password : 
        return jsonify({"status": "error", "message": "Имя и пароль - обязательные поля"}), 400
    
    special_symbols = '\"()*/+-,.:;>=<[\\]^_`{|}!?&$#%@"'
    if len(password) < 8 : 
        return jsonify({"status": "error", "message": "Пароль слишком короткий."}), 400
    elif (not any(bukva.isdigit() for bukva in password)):
        return jsonify({"status": "error", "message": "Пароль не содержит цифр"}), 400
    
    contains_ss = False
    for i in special_symbols : 
        if password.find(i) != -1 : 
            contains_ss = True
    if not contains_ss : 
        return jsonify({"status": "error", "message": "Пароль не содержит спец символы"}), 400

    existing_name = User.query.filter_by(name=data.get("name")).first()

    if existing_name : 
        return jsonify({"status": "error", "message": "Такое имя уже занято"}), 409
    
    hashed_password = generate_password_hash(data["password"])
    new_user_id = str(uuid.uuid4())
    token = jwt.encode({"user_uuid": new_user_id}, RANDOM_SECRET, algorithm="HS256")
    new_user = User( 
        uuid = new_user_id,
        name = data.get("name"),
        password = hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"token": token, "user_id": new_user_id}), 200


@app.route("/api/sign-in", methods=["POST"])
def sign_in():
    data = request.json
    if not data:
        return jsonify({"msg": "Missing Json"}), 400
    
    password = data.get("password")
    name = data.get("name")
    if not password or not name : 
        return jsonify({"status": "error", "message": "Имя и пароль - обязательные поля"}), 400
    user_info = User.query.filter_by(name=name).first()
    if not business_info or not business_info.password or not (business_info.password == generate_password_hash(password)) : 
        return jsonify({"status": "error", "message": "Неверный email или пароль"}), 401
    
    token = jwt.encode({"bis_uuid": business_info.uuid}, RANDOM_SECRET, algorithm="HS256")
    return jsonify({"token": token}), 200

# при запросе главной страницы возвращаем html файл с фронтендом как файл (без шаблонизатора)
@app.route('/')
def index():
    return send_file('static/index.html')

# при запросе главной страницы возвращаем html файл с фронтендом как файл (без шаблонизатора)
@app.route("/favicon.ico")
def ico():
    return send_file('static/favicon.ico')

# при запросе главной страницы возвращаем html файл с фронтендом как файл (без шаблонизатора)
@app.route("/assets/<filename>")
def assets(filename):
    return send_file('static/assets/' + filename)

# # при запросе главной страницы возвращаем html файл с фронтендом как файл (без шаблонизатора)
# @app.route("/assets/index-DnVUw_vK.css")
# def css():
#     return send_file('static/assets/index-DnVUw_vK.css')

if __name__ == '__main__':
    app.run(debug=True, port=5174, host="0.0.0.0")