from flask import render_template, url_for, redirect
from flask_login import login_user, logout_user, current_user, login_required
from projeto import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from projeto.models import Usuario, Foto, Tarefas, Categoria
from projeto.forms import FormLogin, FormCriarConta, FormTarefa, FormCategoria

from werkzeug.utils import secure_filename

#dizemos onde vai ser criado
@app.route('/', methods=[ "GET" , "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=formlogin, usuario=current_user)

@app.route('/perfil/<int:id_usuario>')
@login_required
def perfil(id_usuario):
    if id_usuario == current_user.id:
        usuario = Usuario.query.get(id_usuario)
        tarefas = Tarefas.query.filter_by(usuario_id=id_usuario).all()
        return render_template('perfil_completo.html', usuario=usuario , tarefas=tarefas)
    else:
        return redirect(url_for('homepage'))


@app.route("/criar-conta", methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, email=formcriarconta.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('logout', id_usuario=usuario.id))
    return render_template('criarconta.html', form=formcriarconta)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route("/nova-tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    form = FormTarefa()
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    if form.validate_on_submit():
        nova = Tarefas(tarefas=form.tarefas.data, categoria_id=form.categoria_id.data, usuario_id=current_user.id)
        database.session.add(nova)
        database.session.commit()
        return redirect(url_for('perfil', id_usuario=current_user.id))
    return render_template("nova_tarefa.html", form=form)


@app.route("/nova-categoria", methods=["GET", "POST"])
@login_required
def nova_categoria():
    form = FormCategoria()
    if form.validate_on_submit():
        nova = Categoria(nome=form.nome.data)
        database.session.add(nova)
        database.session.commit()
        return redirect(url_for("perfil"))
    return render_template("nova_categoria.html", form=form)

@app.route("/excluir-tarefa/<int:id>")
@login_required
def excluir_tarefa(id):
    tarefa = Tarefas.query.get(id)
    if tarefa and tarefa.usuario_id == current_user.id:
        database.session.delete(tarefa)
        database.session.commit()
    return redirect(url_for('perfil', id_usuario=current_user.id))




