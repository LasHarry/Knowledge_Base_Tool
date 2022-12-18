from flask import Flask, request, render_template, flash, Response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.serving import run_simple

from knowledge_base_db import KBDatabase
from knowledge_base import KnowledgeBase
from db_handler import create_connection

from entry_form import AddEntry

import json
import random

KBDatabase = KBDatabase()
KBDatabase.setup_database()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOPSECRETKEY!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knowledgebase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize SQLAlchemy
db = SQLAlchemy(app)

# initialize bootstrap layout
bootstrap = Bootstrap(app)

conn = create_connection('knowledgebase.db')


@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    # get names from the knowledge base for the autocomplete function
    names = db.session.query(KnowledgeBase.full_name).all()
    results_raw = [list(row) for row in names]
    results = [x for xs in results_raw for x in xs]

    return Response(json.dumps(results), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def add_new_entry():
    # initialize Flask form
    form1 = AddEntry(request.form)
    # make action on submit
    if form1.validate_on_submit():
        # get name from text field
        full_name = request.form['full_name']
        # set a default trust score between 0 and 1
        trust_score = round(random.random(), 2)

        # create SQL insert query
        entry = KnowledgeBase(full_name, trust_score)

        db.session.add(entry)
        db.session.commit()

        # provide message about successful database entry
        message = f'{full_name} has been added to your knowledge base'
        return render_template('data_entry_autocomplete.html', message=message)

    else:
        # handle errors
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Input error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('data_entry_autocomplete.html', form1=form1)


@app.route('/edit', methods=['GET', 'POST'])
def edit_entry():
    # get all entries with the highest trust scores
    names = KnowledgeBase.query.order_by(KnowledgeBase.trust_score.desc()).limit(10)
    print(names)

    return render_template('data_table.html', title='Knowledge base table', names=names)


@app.route('/process_action', methods=['GET', 'POST'])
def process_action():
    pk_new_accept = 0.8
    pk_new_reject = 0.2
    if request.method == 'POST':
        # process trust score calculation for acceptance
        if request.form.get('submit'):
            name_id = request.form.get('submit')
            # get the selected row from the data table
            response = db.session.query(KnowledgeBase.trust_score).filter_by(id=name_id).first()
            # transform to float value
            pk = str(response)
            pk_string = pk[1:-2]
            pk_float = float(pk_string)
            # recalculate trust score
            pk_star = pk_float + (1 - pk_float) * pk_new_accept

            item = KnowledgeBase.query.filter_by(id=name_id).first()
            # update trust score in database
            item.trust_score = pk_star

            db.session.commit()

            message = f'Adapted trust score for {item.full_name} to {item.trust_score}'

        # process trust score calculation for rejection
        elif request.form.get('reject'):
            # recalculate all positions in the database with a lesser trust score
            KnowledgeBase.query.update({KnowledgeBase.trust_score: KnowledgeBase.trust_score * pk_new_reject})
            # delete all untrustworthy names from the database
            invalid_results = KnowledgeBase.query.filter(KnowledgeBase.trust_score < 0.2)
            invalid_results.delete()

            db.session.commit()
            message = f'Adapted all trust scores and deleted invalid ones'
    elif request.method == 'GET':
        db.session.close()

    return render_template('process_action.html', message=message)


if __name__ == '__main__':
    run_simple('127.0.0.1', 8080, app, use_reloader=True, use_debugger=True)
