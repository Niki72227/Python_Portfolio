import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from app.models import History

def calc_average_and_plot(symbol, start, end, db):
    history = db.query(History).filter(
        History.symbol == symbol,
        History.date >= start,
        History.date <= end
    ).all()
    if not history:
        return {"average": None, "plot": None}
    df = pd.DataFrame([{"date": h.date, "price": h.price} for h in history])
    avg = df["price"].mean()
    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["price"], marker="o")
    plt.title(f"Price of {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return {"average": avg, "plot": img_base64}