from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from api_utils import get_current_sp500_price

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///trade_sim.db'
db = SQLAlchemy(app)

class Trade_position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(50), nullable=False)
    ammount_bought = db.Column(db.Integer, nullable=False)
    stock_price_at_buy = db.Column(db.Float, nullable=False)
    stock_price_at_sell = db.Column(db.Float, nullable=True)
    date_buy = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_sell = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Bought_stock {self.stock_name}, {self.id}"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_position_price = request.form['price']
        new_position = Trade_position(stock_price_at_buy=new_position_price)

        try:
            db.session.add(new_position)
            db.session.commit()
            return Flask.redirect('/')
        except:
            return 'Opening new position failed'
    else:
        api_data = get_current_sp500_price()
        trade_positions = Trade_position.query.order_by(Trade_position.date_buy).all()
        return render_template('index.html', trade_positions=trade_positions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)