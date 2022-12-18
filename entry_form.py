from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class AddEntry(FlaskForm):
    full_name = StringField('Please insert name or surname:', [InputRequired()], id='kb_autocomplete',
                            render_kw={'placeholder': 'Put the name here'})

    submit = SubmitField('Add entry to knowledge base')
