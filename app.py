from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from api_utils import get_current_sp500_price

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///trade_sim.db'
db = SQLAlchemy(app)

class Bought_stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(50), nullable=False)
    stock_price_at_purchace = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Bought_stock {self.stock_name}, {self.id}"

@app.route('/', methods=['POST', 'GET'])
def index():
    api_data = get_current_sp500_price()
    return render_template('index.html', api_data=api_data)

@app.route('/test')
def fucku():
    return 'Hey, testing.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)