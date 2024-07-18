from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os


app = Flask(__name__)
#base de datos 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/ElYosnelCP/Desktop/Cinncinatus/Flask-Blog/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#ruta especifica de la carpeta donde se subiran las imagenes
app.config['UPLOAD_FOLDER'] = r'C:\Users\ElYosnelCP\Desktop\Cinncinatus\Flask-Blog\static\uploads'

#Permitir pgn, jpg ... 
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
db = SQLAlchemy(app)

#crear columnas de base de datos SQALCHEMY
class Post(db.Model):
	__tablename__ = "posts"
	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String, nullable=False)
	fecha = db.Column(db.DateTime, default=datetime.now)
	texto = db.Column(db.String, nullable=False)
	filename = db.Column(db.String, nullable=True)

#PAGINA DE INICIO
@app.route("/")
def inicio():
	posts = Post.query.order_by(Post.fecha.desc()).all() 
	return render_template("inicio.html", posts=posts)

# redireccionar agregar
@app.route("/agregar")
def agregar():
	return render_template("agregar.html")

# agregar le redirreccione a el panel de login(login.html)
@app.route("/login")
def login():
	return render_template("login.html")

           
#agregar titulo, descrippcion, y un archivo..
@app.route("/crear", methods=["POST"])
def crear_post():
	titulo = request.form.get("titulo")
	texto = request.form.get("texto")
	file = request.files.get('imageInput')
	print(file, file.filename)
	filename = secure_filename(file.filename)
	print(filename)
 #si la extencion del archivo esta permitida, sube la imagen a la carpeta Uploads
	if file and allowed_file(filename):
		print("Permitido")
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
#agrega el post con los datos corespodientes 
	post = Post(titulo=titulo, texto=texto, filename=filename)
#agregar post
	db.session.add(post)
 #realiza el commit en la base de datos 
	db.session.commit()
	return redirect("/")

#Verifica si la extencion del archivo esta permitido dentro de permitida según una lista predefinida (ALLOWED_EXTENSIONS)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Visualiza la imagen subida en el post
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

#borar post, y realiza el commit en la base de datos
@app.route("/borrar", methods=["POST"])
def borrar():
	post_id = request.form.get("post_id")
	post = db.session.query(Post).filter(Post.id==post_id).first()
	db.session.delete(post)
	db.session.commit()
	return redirect("/")



#activar debug
with app.app_context():
    db.create_all()
    
#sqlite:///C:/Users/ElYosnelCP/Desktop/Cinncinatus/Flask-Blog/blog.db
