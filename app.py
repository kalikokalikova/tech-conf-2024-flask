from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Thingy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    is_foo = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return '<Thingyyy %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        thingy_name = request.form['name']
        new_thingy = Thingy(name=thingy_name)

        try:
            db.session.add(new_thingy)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem adding this Thingy to the database'
    else:
        thingys = Thingy.query.all()
        return render_template('index.html', thingys=thingys)

@app.route('/delete/<int:id>')
def delete(id):
    thingy_to_delete = Thingy.query.get_or_404(id)

    try:
        db.session.delete(thingy_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting this thingy"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    thingy = Thingy.query.get_or_404(id)

    if request.method == 'POST':
        thingy.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "whoops"
    else:
        return render_template('update.html', thingy=thingy)

if __name__ == "__main__":
    app.run(debug=True)