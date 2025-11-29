from flask import (
    render_template, request, redirect, url_for, flash,
    abort, jsonify, session
)
import requests
import hashlib
import re
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

from src.database import engine
from src.Model.models import (
    Usuario, Reserva, Quarto, Hospede, Tipo_de_quarto
)
from src import app
from flask import (
    render_template, request, redirect, url_for, flash, session
)
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash
from datetime import datetime

from src.database import engine
from src.Model.models import (
    Usuario, Reserva, Quarto, Hospede, Tipo_de_quarto, Perfil
)


SessionLocal = scoped_session(sessionmaker(bind=engine))



# -------------------------------------------------------------------------
# Utils
# -------------------------------------------------------------------------

def isEmailValid(email):
    regex = r"^[a-zA-Z0-9._-]+@[a-zA-Z]+\.[a-z]{2,}$"
    return bool(re.fullmatch(regex, email))


def fetchGithubImg(githubProfile):
    try:
        res = requests.get(f"https://api.github.com/users/{githubProfile}")
        data = res.json()
        return data.get("avatar_url")
    except:
        return None


# -------------------------------------------------------------------------
# Database helpers
# -------------------------------------------------------------------------
def login(email):
    """
    Login padrão usando email.
    """
    db = SessionLocal()
    user = db.query(Usuario).filter(Usuario.email == email).first()

    if not user:
        return None

    return user  # retorna None automaticamente se não achar



def findReservaByUserId(id_hospede):
    db = SessionLocal()
    reservas = (
        db.query(Reserva)
        .filter(Reserva.id_hospede_principal == id_hospede)
        .all()
    )
    return reservas


def roomsByNameId(id_hospede):
    """
    Retorna os quartos das reservas do hóspede.
    """
    db = SessionLocal()
    reservas = findReservaByUserId(id_hospede)

    if not reservas:
        return []

    result = []
    for r in reservas:
        quarto = db.query(Quarto).filter(Quarto.numero_quarto == r.numero_quarto).first()
        if quarto:
            result.append(quarto)

    return result


def getHospedeByUsuarioID(id_usuario):
    db = SessionLocal()
    return db.query(Hospede).filter(Hospede.id_usuario_sistema == id_usuario).first()


# -------------------------------------------------------------------------
# Rotas principais
# -------------------------------------------------------------------------



# -------------------------------------------------------------------------
# Middleware de autenticação admin
# -------------------------------------------------------------------------
def admin_required(f):
    """Decorator para proteger rotas admin"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Faça login para acessar esta área.", "error")
            return redirect(url_for("index"))
        
        db = SessionLocal()
        user = db.query(Usuario).filter(Usuario.id == session["user_id"]).first()
        
        if not user or not user.perfil_id:
            flash("Acesso negado. Você não tem permissões de administrador.", "error")
            return redirect(url_for("guest_area"))
        
        perfil = db.query(Perfil).filter(Perfil.id == user.perfil_id).first()
        
        if not perfil or perfil.nome_perfil.lower() not in ["admin", "administrador"]:
            flash("Acesso negado. Apenas administradores podem acessar.", "error")
            return redirect(url_for("guest_area"))
        
        return f(*args, **kwargs)
    
    return decorated_function


# -------------------------------------------------------------------------
# Dashboard Admin
# -------------------------------------------------------------------------
@app.route("/admin")
@admin_required
def admin_dashboard():
    db = SessionLocal()
    
    # Estatísticas gerais
    total_reservas = db.query(Reserva).count()
    total_quartos = db.query(Quarto).count()
    total_hospedes = db.query(Hospede).count()
    reservas_ativas = db.query(Reserva).filter(
        Reserva.status_reserva == "Confirmada"
    ).count()
    
    # Reservas recentes
    reservas_recentes = db.query(Reserva).order_by(
        Reserva.id_reserva.desc()
    ).limit(10).all()
    
    # Quartos disponíveis
    quartos_disponiveis = db.query(Quarto).filter(
        Quarto.status_limpeza == "limpo"
    ).count()
    
    return render_template("admin/dashboard.html",
                         total_reservas=total_reservas,
                         total_quartos=total_quartos,
                         total_hospedes=total_hospedes,
                         reservas_ativas=reservas_ativas,
                         reservas_recentes=reservas_recentes,
                         quartos_disponiveis=quartos_disponiveis)


# -------------------------------------------------------------------------
# Gestão de Reservas
# -------------------------------------------------------------------------
@app.route("/admin/reservas")
@admin_required
def admin_reservas():
    db = SessionLocal()
    reservas = db.query(Reserva).order_by(Reserva.data_checkin.desc()).all()
    
    # Pegar informações dos hóspedes e quartos
    reservas_detalhadas = []
    for r in reservas:
        hospede = db.query(Hospede).filter(
            Hospede.id_hospede == r.id_hospede_principal
        ).first()
        quarto = db.query(Quarto).filter(
            Quarto.numero_quarto == r.numero_quarto
        ).first()
        
        reservas_detalhadas.append({
            'reserva': r,
            'hospede': hospede,
            'quarto': quarto
        })
    
    return render_template("admin/reservas.html", 
                         reservas=reservas_detalhadas)


@app.route('/admin/reservas/nova', methods=['GET', 'POST'])
@admin_required
def admin_nova_reserva():
    """Página para cadastrar nova reserva"""
    db = SessionLocal()
    
    if request.method == 'POST':
        try:
            # Capturar dados do formulário
            id_hospede_principal = request.form.get('id_hospede_principal')
            data_checkin = request.form.get('data_checkin')
            data_checkout = request.form.get('data_checkout')
            numero_quarto = request.form.get('numero_quarto')
            valor_total = request.form.get('valor_total')
            status_reserva = request.form.get('status_reserva')
            print("******************************* \n",id_hospede_principal,data_checkin,data_checkout,numero_quarto,valor_total,status_reserva,"\n")

            # Validações básicas
            if not all([id_hospede_principal, data_checkin, data_checkout, numero_quarto, status_reserva, valor_total]):
                flash('Por favor, preencha todos os campos obrigatórios.', 'error')
                return redirect(url_for('admin_nova_reserva'))
            
            # Converter datas
            from datetime import datetime
            checkin = datetime.strptime(data_checkin, '%Y-%m-%d').date()
            checkout = datetime.strptime(data_checkout, '%Y-%m-%d').date()
            
            # Validar datas
            if checkout <= checkin:
                flash('A data de check-out deve ser posterior à data de check-in.', 'error')
                return redirect(url_for('admin_nova_reserva'))
            
            # Criar nova reserva
            nova_reserva = Reserva(
                id_hospede_principal=int(id_hospede_principal),
                numero_quarto=int(numero_quarto),
                data_checkin=checkin,
                data_checkout=checkout,
                status_reserva=status_reserva,
                valor_total=float(valor_total)
            )
            
            db.add(nova_reserva)
            db.commit()
            
            flash(f'Reserva cadastrada com sucesso! ID: {nova_reserva.id_reserva}', 'success')
            return redirect(url_for('admin_reservas'))
            
        except ValueError as e:
            flash(f'Erro nos dados fornecidos: {str(e)}', 'error')
            return redirect(url_for('admin_nova_reserva'))
        except Exception as e:
            flash(f'Erro ao cadastrar reserva: {str(e)}', 'error')
            return redirect(url_for('admin_nova_reserva'))
        finally:
            db.close()
    
    # GET - Buscar dados para preencher os selects
    hospedes = db.query(Hospede).order_by(Hospede.nome_completo).all()
    tipos_quarto = db.query(Tipo_de_quarto).order_by(Tipo_de_quarto.nome_tipo).all()
    quartos = db.query(Quarto).filter(Quarto.status_limpeza == 'limpo').order_by(Quarto.numero_quarto).all()
    
    return render_template(
        'admin/nova_reserva.html',
        hospedes=hospedes,
        tipos_quarto=tipos_quarto,
        quartos=quartos
    )

@app.route("/admin/reservas/editar/<int:id_reserva>", methods=["GET", "POST"])
@admin_required
def admin_editar_reserva(id_reserva):
    db = SessionLocal()
    reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
    
    if not reserva:
        flash("Reserva não encontrada.", "error")
        return redirect(url_for("admin_reservas"))
    
    if request.method == "POST":
        reserva.data_checkin = request.form.get("data_checkin")
        reserva.data_checkout = request.form.get("data_checkout")
        reserva.status_reserva = request.form.get("status_reserva")
        reserva.valor_total = request.form.get("valor_total")
        
        db.commit()
        flash("Reserva atualizada com sucesso!", "success")
        return redirect(url_for("admin_reservas"))
    
    hospedes = db.query(Hospede).all()
    quartos = db.query(Quarto).all()
    
    return render_template("admin/editar_reserva.html",
                         reserva=reserva,
                         hospedes=hospedes,
                         quartos=quartos)


@app.route("/admin/reservas/deletar/<int:id_reserva>")
@admin_required
def admin_deletar_reserva(id_reserva):
    db = SessionLocal()
    reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
    
    if not reserva:
        flash("Reserva não encontrada.", "error")
        return redirect(url_for("admin_reservas"))
    
    db.delete(reserva)
    db.commit()
    
    flash("Reserva deletada com sucesso!", "success")
    return redirect(url_for("admin_reservas"))


# -------------------------------------------------------------------------
# Gestão de Quartos
# -------------------------------------------------------------------------
@app.route("/admin/quartos")
@admin_required
def admin_quartos():
    db = SessionLocal()
    quartos = db.query(Quarto).all()
    
    quartos_detalhados = []
    for q in quartos:
        tipo = db.query(Tipo_de_quarto).filter(
            Tipo_de_quarto.id_tipo == q.id_tipo
        ).first()
        
        quartos_detalhados.append({
            'quarto': q,
            'tipo': tipo
        })
    
    return render_template("admin/quartos.html", quartos=quartos_detalhados)


@app.route("/admin/quartos/novo", methods=["GET", "POST"])
@admin_required
def admin_novo_quarto():
    db = SessionLocal()
    
    if request.method == "POST":
        numero = request.form.get("numero_quarto")
        id_tipo = request.form.get("id_tipo")
        status = request.form.get("status_limpeza", "sujo")
        localizacao = request.form.get("localizacao")
        
        # Verificar se o número já existe
        existe = db.query(Quarto).filter(Quarto.numero_quarto == numero).first()
        if existe:
            flash("Este número de quarto já existe.", "error")
            return redirect(url_for("admin_novo_quarto"))
        
        novo_quarto = Quarto(
            numero_quarto=numero,
            id_tipo=id_tipo,
            status_limpeza=status,
            localizacao=localizacao
        )
        
        db.add(novo_quarto)
        db.commit()
        
        flash("Quarto criado com sucesso!", "success")
        return redirect(url_for("admin_quartos"))
    
    tipos = db.query(Tipo_de_quarto).all()
    return render_template("admin/novo_quarto.html", tipos=tipos)


@app.route("/admin/quartos/editar/<int:numero_quarto>", methods=["GET", "POST"])
@admin_required
def admin_editar_quarto(numero_quarto):
    db = SessionLocal()
    quarto = db.query(Quarto).filter(Quarto.numero_quarto == numero_quarto).first()
    
    if not quarto:
        flash("Quarto não encontrado.", "error")
        return redirect(url_for("admin_quartos"))
    
    if request.method == "POST":
        quarto.id_tipo = request.form.get("id_tipo")
        quarto.status_limpeza = request.form.get("status_limpeza")
        quarto.localizacao = request.form.get("localizacao")
        
        db.commit()
        flash("Quarto atualizado com sucesso!", "success")
        return redirect(url_for("admin_quartos"))
    
    tipos = db.query(Tipo_de_quarto).all()
    return render_template("admin/editar_quarto.html", quarto=quarto, tipos=tipos)


@app.route("/admin/quartos/deletar/<int:numero_quarto>")
@admin_required
def admin_deletar_quarto(numero_quarto):
    db = SessionLocal()
    quarto = db.query(Quarto).filter(Quarto.numero_quarto == numero_quarto).first()
    
    if not quarto:
        flash("Quarto não encontrado.", "error")
        return redirect(url_for("admin_quartos"))
    
    # Verificar se há reservas associadas
    tem_reservas = db.query(Reserva).filter(
        Reserva.numero_quarto == numero_quarto
    ).first()
    
    if tem_reservas:
        flash("Não é possível deletar um quarto com reservas associadas.", "error")
        return redirect(url_for("admin_quartos"))
    
    db.delete(quarto)
    db.commit()
    
    flash("Quarto deletado com sucesso!", "success")
    return redirect(url_for("admin_quartos"))


# -------------------------------------------------------------------------
# Gestão de Hóspedes
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Gestão de Hóspedes (ATUALIZADO)
# -------------------------------------------------------------------------
@app.route("/admin/hospedes")
@admin_required
def admin_hospedes():
    db = SessionLocal()
    hospedes = db.query(Hospede).all()
    
    # Buscar usuários vinculados para exibir na lista
    hospedes_com_usuarios = []
    for h in hospedes:
        usuario_vinculado = None
        if h.id_usuario_sistema:
            usuario_vinculado = db.query(Usuario).filter(
                Usuario.id == h.id_usuario_sistema
            ).first()
        
        hospedes_com_usuarios.append({
            'hospede': h,
            'usuario': usuario_vinculado
        })
    
    return render_template("admin/hospedes.html", 
                         hospedes_data=hospedes_com_usuarios)


@app.route("/admin/hospedes/novo", methods=["GET", "POST"])
@admin_required
def admin_novo_hospede():
    db = SessionLocal()
    
    if request.method == "POST":
        nome = request.form.get("nome_completo")
        documento = request.form.get("documento")
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        id_usuario_sistema = request.form.get("id_usuario_sistema")
        
        # Converter string vazia para None
        if id_usuario_sistema == "":
            id_usuario_sistema = None
        
        # Verificar duplicatas
        existe = db.query(Hospede).filter(
            (Hospede.documento == documento)
        ).first()
        
        if existe:
            flash("Hóspede com este documento já existe.", "error")
            return redirect(url_for("admin_novo_hospede"))
        
        # Verificar se email já está em uso (se fornecido)
        if email:
            email_existe = db.query(Hospede).filter(Hospede.email == email).first()
            if email_existe:
                flash("Este email já está cadastrado para outro hóspede.", "error")
                return redirect(url_for("admin_novo_hospede"))
        
        # Verificar se o usuário já está vinculado a outro hóspede
        if id_usuario_sistema:
            usuario_ja_vinculado = db.query(Hospede).filter(
                Hospede.id_usuario_sistema == id_usuario_sistema
            ).first()
            
            if usuario_ja_vinculado:
                flash("Este usuário já está vinculado a outro hóspede.", "error")
                return redirect(url_for("admin_novo_hospede"))
        
        novo_hospede = Hospede(
            nome_completo=nome,
            documento=documento,
            telefone=telefone,
            email=email,
            id_usuario_sistema=id_usuario_sistema
        )
        
        db.add(novo_hospede)
        db.commit()
        
        if id_usuario_sistema:
            flash("Hóspede criado e vinculado ao usuário com sucesso!", "success")
        else:
            flash("Hóspede criado com sucesso!", "success")
        
        return redirect(url_for("admin_hospedes"))
    
    # Buscar todos os usuários para o select
    usuarios = db.query(Usuario).order_by(Usuario.nome_completo).all()
    
    return render_template("admin/novo_hospede.html", usuarios=usuarios)


@app.route("/admin/hospedes/editar/<int:id_hospede>", methods=["GET", "POST"])
@admin_required
def admin_editar_hospede(id_hospede):
    db = SessionLocal()
    hospede = db.query(Hospede).filter(Hospede.id_hospede == id_hospede).first()
    
    if not hospede:
        flash("Hóspede não encontrado.", "error")
        return redirect(url_for("admin_hospedes"))
    
    if request.method == "POST":
        hospede.nome_completo = request.form.get("nome_completo")
        hospede.telefone = request.form.get("telefone")
        hospede.email = request.form.get("email")
        
        id_usuario_sistema = request.form.get("id_usuario_sistema")
        
        # Converter string vazia para None
        if id_usuario_sistema == "":
            id_usuario_sistema = None
        
        # Verificar se o usuário já está vinculado a outro hóspede
        if id_usuario_sistema:
            usuario_ja_vinculado = db.query(Hospede).filter(
                Hospede.id_usuario_sistema == id_usuario_sistema,
                Hospede.id_hospede != id_hospede  # Excluir o próprio hóspede
            ).first()
            
            if usuario_ja_vinculado:
                flash("Este usuário já está vinculado a outro hóspede.", "error")
                usuarios = db.query(Usuario).order_by(Usuario.nome_completo).all()
                perfis = db.query(Perfil).all()
                return render_template("admin/editar_hospede.html", 
                                     hospede=hospede, 
                                     usuarios=usuarios,
                                     perfis=perfis)
        
        hospede.id_usuario_sistema = id_usuario_sistema
        
        db.commit()
        flash("Hóspede atualizado com sucesso!", "success")
        return redirect(url_for("admin_hospedes"))
    
    # Buscar todos os usuários e perfis para o select
    usuarios = db.query(Usuario).order_by(Usuario.nome_completo).all()
    perfis = db.query(Perfil).all()
    
    return render_template("admin/editar_hospede.html", 
                         hospede=hospede, 
                         usuarios=usuarios,
                         perfis=perfis)

# -------------------------------------------------------------------------
# Gestão de Tipos de Quarto
# -------------------------------------------------------------------------
@app.route("/admin/tipos-quarto")
@admin_required
def admin_tipos_quarto():
    db = SessionLocal()
    tipos = db.query(Tipo_de_quarto).all()
    
    return render_template("admin/tipos_quarto.html", tipos=tipos)


@app.route("/admin/tipos-quarto/novo", methods=["GET", "POST"])
@admin_required
def admin_novo_tipo_quarto():
    db = SessionLocal()
    
    if request.method == "POST":
        nome = request.form.get("nome_tipo")
        capacidade = request.form.get("capacidade_maxima")
        preco = request.form.get("preco_diaria_base")
        descricao = request.form.get("descricao")
        
        novo_tipo = Tipo_de_quarto(
            nome_tipo=nome,
            capacidade_maxima=capacidade,
            preco_diaria_base=preco,
            descricao=descricao
        )
        
        db.add(novo_tipo)
        db.commit()
        
        flash("Tipo de quarto criado com sucesso!", "success")
        return redirect(url_for("admin_tipos_quarto"))
    
    return render_template("admin/novo_tipo_quarto.html")


@app.route("/admin/tipos-quarto/editar/<int:id_tipo>", methods=["GET", "POST"])
@admin_required
def admin_editar_tipo_quarto(id_tipo):
    db = SessionLocal()
    tipo = db.query(Tipo_de_quarto).filter(Tipo_de_quarto.id_tipo == id_tipo).first()
    
    if not tipo:
        flash("Tipo de quarto não encontrado.", "error")
        return redirect(url_for("admin_tipos_quarto"))
    
    if request.method == "POST":
        tipo.nome_tipo = request.form.get("nome_tipo")
        tipo.capacidade_maxima = request.form.get("capacidade_maxima")
        tipo.preco_diaria_base = request.form.get("preco_diaria_base")
        tipo.descricao = request.form.get("descricao")
        
        db.commit()
        flash("Tipo de quarto atualizado com sucesso!", "success")
        return redirect(url_for("admin_tipos_quarto"))
    
    return render_template("admin/editar_tipo_quarto.html", tipo=tipo)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = request.form
        email = form.get("email")
        password = form.get("password")

        user = login(email)

        if not user:
            flash("Usuário não encontrado.", "error")
            return redirect(url_for("index"))

        if not check_password_hash(user.senha_hash, password):
            flash("Senha incorreta.", "error")
            return redirect(url_for("index"))

        # Guardar sessão básica
        session["user_id"] = user.id

        # ========================================
        # VERIFICAR SE É ADMINISTRADOR
        # ========================================
        if user.perfil_id:
            db = SessionLocal()
            perfil = db.query(Perfil).filter(Perfil.id == user.perfil_id).first()
            db.close()
            
            # Se for admin, redirecionar para painel administrativo
            if perfil and perfil.nome_perfil.lower() in ["admin", "administrador"]:
                flash(f"Bem-vindo, {user.nome_completo}!", "success")
                return redirect(url_for("admin_dashboard"))
        
        # ========================================
        # SE NÃO FOR ADMIN, TRATAR COMO HÓSPEDE
        # ========================================
        hospede = getHospedeByUsuarioID(user.id)
        if not hospede:
            flash("Este usuário não está vinculado a um hóspede do sistema.", "warning")
            return redirect(url_for("index"))

        # Guardar sessão de hóspede
        session["hospede_id"] = hospede.id_hospede

        reservas = findReservaByUserId(hospede.id_hospede)
        rooms = roomsByNameId(hospede.id_hospede)

        return render_template("guest.html",
                               user=user,
                               hospede=hospede,
                               reservas=reservas,
                               rooms=rooms,
                               profilePic=None)

    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    db = SessionLocal()

    if request.method == "POST":
        nome = request.form.get("fullname")
        email = request.form.get("email")
        senha = request.form.get("password")

        if not isEmailValid(email):
            flash("Email inválido.", "error")
            return redirect(url_for("register"))

        if db.query(Usuario).filter(Usuario.email == email).first():
            flash("Email já registrado.", "error")
            return redirect(url_for("register"))

        novo_usuario = Usuario(
            nome_completo=nome,
            email=email,
            senha_hash=generate_password_hash(senha)
        )

        db.add(novo_usuario)
        db.commit()

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("register.html")


# -------------------------------------------------------------------------
# Reservas
# -------------------------------------------------------------------------

@app.route("/reservar", methods=["POST"])
def reservar():
    if "hospede_id" not in session:
        flash("Faça login para realizar uma reserva.", "error")
        return redirect(url_for("index"))

    hospede_id = session["hospede_id"]
    db = SessionLocal()

    numero_quarto = request.form.get("numero_quarto")
    data_in = request.form.get("data_checkin")
    data_out = request.form.get("data_checkout")

    if not numero_quarto or not data_in or not data_out:
        flash("Preencha todos os campos.", "warning")
        return redirect(url_for("guest_area"))

    quarto = db.query(Quarto).filter(Quarto.numero_quarto == numero_quarto).first()
    if not quarto:
        flash("Quarto inexistente.", "error")
        return redirect(url_for("guest_area"))

    nova_reserva = Reserva(
        id_hospede_principal=hospede_id,
        numero_quarto=numero_quarto,
        data_checkin=data_in,
        data_checkout=data_out,
        status_reserva="Confirmada",
        valor_total=200.00  # exemplo
    )

    db.add(nova_reserva)
    db.commit()

    flash("Reserva criada com sucesso!", "success")
    return redirect(url_for("guest_area"))


@app.route("/cancelar/<int:id_reserva>")
def cancelar_reserva(id_reserva):
    if "hospede_id" not in session:
        flash("Faça login para continuar.", "error")
        return redirect(url_for("index"))

    db = SessionLocal()
    reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

    if not reserva:
        flash("Reserva não encontrada.", "error")
        return redirect(url_for("guest_area"))

    # verificar se é do dono
    if reserva.id_hospede_principal != session["hospede_id"]:
        flash("Você não pode cancelar reservas de outros usuários.", "error")
        return redirect(url_for("guest_area"))

    db.delete(reserva)
    db.commit()

    flash("Reserva cancelada.", "info")
    return redirect(url_for("guest_area"))


# -------------------------------------------------------------------------
# Guest Page (página de usuário após login)
# -------------------------------------------------------------------------

@app.route("/guest")
def guest_area():
    if "user_id" not in session:
        return redirect(url_for("index"))

    db = SessionLocal()

    user = db.query(Usuario).filter(Usuario.id == session["user_id"]).first()
    hospede = getHospedeByUsuarioID(user.id)

    reservas = findReservaByUserId(hospede.id_hospede)
    rooms = roomsByNameId(hospede.id_hospede)

    return render_template("guest.html",
                           user=user,
                           hospede=hospede,
                           reservas=reservas,
                           rooms=rooms,
                           profilePic=None)
