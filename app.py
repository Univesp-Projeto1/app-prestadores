import os
import sqlite3
from functools import wraps
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "banco.db")
UPLOAD_FOLDER = os.path.join(APP_DIR, "uploads")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app = Flask(__name__)
app.secret_key = "troque-essa-chave-em-producao"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------- DB helpers ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      role TEXT NOT NULL CHECK (role IN ('cliente','prestador')),
      cep TEXT,
      cidade TEXT,
      bairro TEXT,
      telefone TEXT,
      whatsapp TEXT,
      descricao TEXT,
      especialidade TEXT,
      foto TEXT,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS portfolio (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      prestador_id INTEGER NOT NULL,
      imagem TEXT NOT NULL,
      legenda TEXT,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(prestador_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS agendamentos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cliente_id INTEGER NOT NULL,
      prestador_id INTEGER NOT NULL,
      data_hora TEXT NOT NULL,
      descricao_servico TEXT,
      valor REAL,
      status TEXT DEFAULT 'reservado',
      pago INTEGER DEFAULT 0,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(cliente_id) REFERENCES users(id),
      FOREIGN KEY(prestador_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS contatos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cliente_id INTEGER NOT NULL,
      prestador_id INTEGER NOT NULL,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(cliente_id, prestador_id),
      FOREIGN KEY(cliente_id) REFERENCES users(id),
      FOREIGN KEY(prestador_id) REFERENCES users(id)
    );
    """)

    conn.commit()
    conn.close()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------- Auth helpers ----------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

def current_user():
    if "user_id" not in session:
        return None
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()
    return user


# ---------- Tela 1: Login / Cadastro ----------
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if not user or not check_password_hash(user["password_hash"], senha):
            flash("E-mail ou senha inválidos.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["role"] = user["role"]
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        role = request.form.get("role")  # cliente/prestador

        cep = request.form.get("cep")
        cidade = request.form.get("cidade")
        bairro = request.form.get("bairro")

        telefone = request.form.get("telefone")
        whatsapp = request.form.get("whatsapp")
        especialidade = request.form.get("especialidade")
        descricao = request.form.get("descricao")

        if not nome or not email or not senha or role not in ("cliente", "prestador"):
            flash("Preencha nome, e-mail, senha e tipo (Cliente/Prestador).", "error")
            return render_template("cadastro.html")

        password_hash = generate_password_hash(senha)

        conn = get_db()
        try:
            conn.execute("""
                INSERT INTO users (nome, email, password_hash, role, cep, cidade, bairro, telefone, whatsapp, especialidade, descricao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome, email, password_hash, role, cep, cidade, bairro, telefone, whatsapp, especialidade, descricao))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Este e-mail já está cadastrado.", "error")
            return render_template("cadastro.html")
        finally:
            conn.close()

        flash("Cadastro realizado com sucesso. Faça login!", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- Tela 2: Home ----------
@app.route("/home")
@login_required
def home():
    user = current_user()
    return render_template("home.html", user=user)


# ---------- Tela 3: Feed (Pesquisar Prestador) ----------
@app.route("/feed")
@login_required
def feed():
    q = request.args.get("q", "").strip().lower()

    conn = get_db()
    if q:
        prestadores = conn.execute("""
            SELECT id, nome, especialidade, descricao, foto, cidade, bairro, whatsapp, email
            FROM users
            WHERE role = 'prestador' AND lower(nome) LIKE ?
            ORDER BY created_at DESC
        """, (f"%{q}%",)).fetchall()
    else:
        prestadores = conn.execute("""
            SELECT id, nome, especialidade, descricao, foto, cidade, bairro, whatsapp, email
            FROM users
            WHERE role = 'prestador'
            ORDER BY created_at DESC
        """).fetchall()
    conn.close()

    return render_template("feed.html", prestadores=prestadores, q=q)

# Detalhes do prestador (para modal via JS)
@app.route("/prestador/<int:prestador_id>")
@login_required
def prestador_detalhe(prestador_id):
    conn = get_db()
    prestador = conn.execute("""
        SELECT id, nome, especialidade, descricao, foto, cidade, bairro, whatsapp, email
        FROM users WHERE id = ? AND role = 'prestador'
    """, (prestador_id,)).fetchone()

    fotos = conn.execute("""
        SELECT imagem, legenda FROM portfolio
        WHERE prestador_id = ?
        ORDER BY created_at DESC
        LIMIT 10
    """, (prestador_id,)).fetchall()

    qtd_servicos = conn.execute("""
        SELECT COUNT(*) as total FROM agendamentos
        WHERE prestador_id = ?
    """, (prestador_id,)).fetchone()["total"]

    conn.close()

    if not prestador:
        return jsonify({"error": "Prestador não encontrado"}), 404

    return jsonify({
        "prestador": dict(prestador),
        "portfolio": [dict(f) for f in fotos],
        "qtd_servicos": qtd_servicos,
        "avaliacao": 4.7  # MVP (fixo)
    })


# Agendamento (cria agendamento + adiciona contato)
@app.route("/agendar", methods=["POST"])
@login_required
def agendar():
    user = current_user()
    if user["role"] != "cliente":
        flash("Apenas cliente pode agendar.", "error")
        return redirect(url_for("home"))

    prestador_id = int(request.form.get("prestador_id"))
    data_hora = request.form.get("data_hora")  # yyyy-mm-dd hh:mm
    descricao_servico = request.form.get("descricao_servico")
    valor = request.form.get("valor") or None
    pago = 1 if request.form.get("pago") == "1" else 0

    conn = get_db()
    conn.execute("""
        INSERT INTO agendamentos (cliente_id, prestador_id, data_hora, descricao_servico, valor, pago)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user["id"], prestador_id, data_hora, descricao_servico, valor, pago))
    conn.commit()

    conn.execute("""
        INSERT OR IGNORE INTO contatos (cliente_id, prestador_id)
        VALUES (?, ?)
    """, (user["id"], prestador_id))
    conn.commit()
    conn.close()

    flash("Agendamento realizado!", "success")
    return redirect(url_for("agendamentos"))


# ---------- Tela 4: Localização ----------
@app.route("/localizacao")
@login_required
def localizacao():
    cidade = request.args.get("cidade", "").strip()
    bairro = request.args.get("bairro", "").strip()

    conn = get_db()
    query = """
        SELECT id, nome, especialidade, descricao, foto, cidade, bairro, whatsapp, email
        FROM users
        WHERE role = 'prestador'
    """
    params = []

    if cidade:
        query += " AND cidade LIKE ?"
        params.append(f"%{cidade}%")
    if bairro:
        query += " AND bairro LIKE ?"
        params.append(f"%{bairro}%")

    query += " ORDER BY created_at DESC"
    prestadores = conn.execute(query, params).fetchall()
    conn.close()

    return render_template("prestadores.html", prestadores=prestadores, cidade=cidade, bairro=bairro)


# ---------- Tela 5: Contatos ----------
@app.route("/contatos")
@login_required
def contatos():
    user = current_user()
    if user["role"] != "cliente":
        return render_template("contatos.html", contatos=[], user=user)

    conn = get_db()
    lista = conn.execute("""
        SELECT u.id, u.nome, u.especialidade, u.foto, u.whatsapp, u.email
        FROM contatos c
        JOIN users u ON u.id = c.prestador_id
        WHERE c.cliente_id = ?
        ORDER BY c.created_at DESC
    """, (user["id"],)).fetchall()
    conn.close()

    return render_template("contatos.html", contatos=lista, user=user)


# ---------- Tela 6: Agendamentos ----------
@app.route("/agendamentos")
@login_required
def agendamentos():
    user = current_user()
    conn = get_db()

    if user["role"] == "cliente":
        ags = conn.execute("""
            SELECT a.*, u.nome as prestador_nome, u.whatsapp as prestador_whatsapp, u.email as prestador_email
            FROM agendamentos a
            JOIN users u ON u.id = a.prestador_id
            WHERE a.cliente_id = ?
            ORDER BY a.data_hora DESC
        """, (user["id"],)).fetchall()
    else:
        ags = conn.execute("""
            SELECT a.*, u.nome as cliente_nome, u.whatsapp as cliente_whatsapp, u.email as cliente_email
            FROM agendamentos a
            JOIN users u ON u.id = a.cliente_id
            WHERE a.prestador_id = ?
            ORDER BY a.data_hora DESC
        """, (user["id"],)).fetchall()

    conn.close()
    return render_template("agendamentos.html", agendamentos=ags, user=user)


# ---------- Tela 7: Perfil ----------
@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    user = current_user()

    if request.method == "POST":
        nome = request.form.get("nome")
        cep = request.form.get("cep")
        cidade = request.form.get("cidade")
        bairro = request.form.get("bairro")
        telefone = request.form.get("telefone")
        whatsapp = request.form.get("whatsapp")
        especialidade = request.form.get("especialidade")
        descricao = request.form.get("descricao")

        foto_path = user["foto"]

        file = request.files.get("foto")
        if file and file.filename and allowed_file(file.filename):
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            filename = secure_filename(file.filename)
            unique = f"{user['id']}_{int(datetime.now().timestamp())}_{filename}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique))
            foto_path = unique

        conn = get_db()
        conn.execute("""
            UPDATE users
            SET nome=?, cep=?, cidade=?, bairro=?, telefone=?, whatsapp=?, especialidade=?, descricao=?, foto=?
            WHERE id=?
        """, (nome, cep, cidade, bairro, telefone, whatsapp, especialidade, descricao, foto_path, user["id"]))
        conn.commit()
        conn.close()

        flash("Perfil atualizado!", "success")
        return redirect(url_for("perfil"))

    return render_template("perfil.html", user=user)


# Servir uploads (dev)
@app.route("/uploads/<path:filename>")
def uploads(filename):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)