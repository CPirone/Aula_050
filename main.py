from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
  name = StringField('Informe o seu nome', validators=[DataRequired()])
  sobrenome = StringField('Informe o seu sobrenome:',
                          validators=[DataRequired()])
  instituicao = StringField('Informe a sua Instituição de ensino:',
                            validators=[DataRequired()])
  disciplina = SelectField('Informe a sua disciplina:',
                           choices=[('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'),
                                    ('GPSA5', 'Gestão de Projetos')],
                           validators=[DataRequired()])
  submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    old_name = session.get('name')
    session['name'] = form.name.data
    session['sobrenome'] = form.sobrenome.data
    session['instituicao'] = form.instituicao.data
    session['disciplina'] = form.disciplina.data
    if old_name != session['name']:
      flash('Você alterou o seu nome!')
    return redirect(url_for('index'))
  return render_template('index.html',
                         form=form,
                         name=session.get('name'),
                         sobrenome=session.get('sobrenome'),
                         instituicao=session.get('instituicao'),
                         disciplina=session.get('disciplina'))


@app.context_processor
def inject_now():
  return {'now': datetime.now()}


if __name__ == '__main__':
  app.run(debug=True)
