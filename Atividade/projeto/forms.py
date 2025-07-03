from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from projeto.models import Usuario


def validate_email(self,email):
    usuario = Usuario.query.filter_by(email=email.data).first()
    if usuario:
        raise ValidationError("Email já cadastrado. Faça Login para continuar")

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators = [DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators = [DataRequired(), Email()])
    username = StringField("Nome de usuário", validators = [DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField("Confirme a senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar conta")

class FormTarefa(FlaskForm):
    tarefas = StringField("Descrição da tarefa", validators=[DataRequired()])
    categoria_id = SelectField("Categoria", coerce=int, validators=[DataRequired()])
    botao_confirmacao = SubmitField("Criar tarefa")

class FormCategoria(FlaskForm):
    nome = StringField("Nome da categoria", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Criar categoria")


