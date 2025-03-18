from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from .forms import RegisterForm, LoginForm
from .models import User
from .extensions import db, bcrypt

auth_bp = Blueprint('auth', __name__)




@auth_bp.route('/')
def index():
    return render_template('base.html')






@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Gerar hash da senha 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Criar novo usuário com a senha hasheada
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        # Adicionar ao banco de dados
        db.session.add(new_user)
        db.session.commit()

        flash('Conta criada com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Procurar usuário no banco de dados
        user = User.query.filter_by(email=form.email.data).first()

        # Validar usuário e senha
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.dashboard'))

        # Exibir mensagem de erro em caso de falha
        flash('Login ou senha incorretos.', 'danger')
    return render_template('login.html', form=form)



@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))
