import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")

database_url = os.environ.get("DATABASE_URL")
if database_url:
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///neon_space.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    category = db.Column(db.String(80), nullable=False, default="General")
    created_at = db.Column(db.DateTime, server_default=db.func.now())


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para acceder al panel.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
def index():
    services = Service.query.order_by(Service.id.desc()).limit(6).all()
    return render_template("index.html", services=services)


@app.route("/servicios")
def servicios():
    services = Service.query.order_by(Service.id.desc()).all()
    return render_template("servicios.html", services=services)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if len(password) < 6:
            flash("La contraseña debe tener mínimo 6 caracteres.", "danger")
            return redirect(url_for("registro"))

        if User.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado.", "danger")
            return redirect(url_for("registro"))

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Cuenta creada correctamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash(f"Bienvenido, {user.name}.", "success")
            return redirect(url_for("panel"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("index"))


@app.route("/panel")
@login_required
def panel():
    services = Service.query.order_by(Service.id.desc()).all()
    users_count = User.query.count()
    return render_template("panel.html", services=services, users_count=users_count)


@app.route("/servicios/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_servicio():
    if request.method == "POST":
        service = Service(
            name=request.form["name"].strip(),
            description=request.form["description"].strip(),
            price=request.form["price"],
            category=request.form["category"].strip()
        )
        db.session.add(service)
        db.session.commit()
        flash("Servicio creado correctamente.", "success")
        return redirect(url_for("panel"))
    return render_template("servicio_form.html", service=None, title="Nuevo servicio")


@app.route("/servicios/editar/<int:service_id>", methods=["GET", "POST"])
@login_required
def editar_servicio(service_id):
    service = Service.query.get_or_404(service_id)

    if request.method == "POST":
        service.name = request.form["name"].strip()
        service.description = request.form["description"].strip()
        service.price = request.form["price"]
        service.category = request.form["category"].strip()
        db.session.commit()
        flash("Servicio actualizado.", "success")
        return redirect(url_for("panel"))

    return render_template("servicio_form.html", service=service, title="Editar servicio")


@app.post("/servicios/eliminar/<int:service_id>")
@login_required
def eliminar_servicio(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash("Servicio eliminado.", "success")
    return redirect(url_for("panel"))


@app.get("/health")
def health():
    return {"status": "ok", "service": "Neon Space"}


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
