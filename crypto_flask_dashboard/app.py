from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "http://localhost:8000"

@app.route("/", methods=["GET", "POST"])
def index():
    symbol = request.form.get("symbol", "BTC")
    start = request.form.get("start", "2025-09-01T00:00:00")
    end = request.form.get("end", "2025-09-05T23:59:59")

    analytics = requests.get(f"{API_URL}/analytics/{symbol}", params={"start": start, "end": end}).json()
    history = requests.get(f"{API_URL}/history/{symbol}", params={"start": start, "end": end}).json()

    plot_img = None
    if analytics.get("plot"):
        plot_img = f"data:image/png;base64,{analytics['plot']}"

    return render_template(
        "index.html",
        symbol=symbol,
        start=start,
        end=end,
        average=analytics.get("average"),
        history=history,
        plot_img=plot_img
    )

if __name__ == "__main__":
    app.run(debug=True)