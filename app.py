from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from api_utils import get_current_sp500_price

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///trade_sim.db'
db = SQLAlchemy(app)
recreate_db = False

class Trade_position(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_ticker = db.Column(db.String(50), nullable=False)
    ammount_bought = db.Column(db.Integer, nullable=False)
    stock_price_at_buy = db.Column(db.Float, nullable=False)
    stock_price_at_sell = db.Column(db.Float, nullable=True)
    date_buy = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    date_sell = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Bought_stock {self.stock_name}, {self.id}"
    
# RECREATE DB
if recreate_db:
    app.app_context().push()
    db.drop_all()
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    trade_positions_opened = Trade_position.query.where(Trade_position.date_sell==None).order_by(Trade_position.date_buy).all()
    trade_positions_closed = Trade_position.query.where(Trade_position.date_sell!=None).order_by(Trade_position.date_sell).all()
    return render_template('index.html', trade_positions_opened=trade_positions_opened, trade_positions_closed=trade_positions_closed, api_data=True)

@app.route('/buy', methods=['POST'])
def buy():
    new_position = Trade_position(stock_ticker=request.form['stock_ticker'], ammount_bought=1, stock_price_at_buy=request.form['stock_price_current'])
    db.session.add(new_position)
    db.session.commit()
    return redirect('/')

@app.route('/sell', methods=['POST'])
def sell():
    position_to_sell = Trade_position.query.get(request.form['id'])
    position_to_sell.stock_price_at_sell = request.form['stock_price_at_sell']
    position_to_sell.date_sell = datetime.utcnow()
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)