def calculate_total_profit_loss(Trade_position):
    rows = Trade_position.query.filter(Trade_position.date_sell != None).order_by(Trade_position.date_sell).all()
    
    total_profit = 0.0
    
    for row in rows:
        profit_or_loss = row.crypto_price_at_sell - row.crypto_price_at_buy
        total_profit += profit_or_loss
    
    return total_profit