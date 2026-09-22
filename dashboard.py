from flask import Flask, request, redirect
import json, os
from datetime import datetime

app = Flask(__name__)

def load_data():
    try:
        with open("memory.json","r") as f:
            name = json.load(f)["name"]
    except:
        name = "Tarcisious"
    if os.path.exists("sales.json"):
        with open("sales.json","r") as f:
            history = json.load(f)
    else:
        history = []
    return name, history

def save_data(history):
    with open("sales.json","w") as f:
        json.dump(history, f, indent=2)

@app.route("/")
def home():
    name, history = load_data()
    total_sales = sum(x["sales"] for x in history)
    total_cost = sum(x["cost"] for x in history)
    total_profit = sum(x["profit"] for x in history)
    
    # MPESA CALCULATION
    mpesa_fees = total_sales * 0.005
    net_after_mpesa = total_profit - mpesa_fees
    
    rows = ""
    chart_dates = []
    chart_profits = []
    for h in reversed(history[-10:]):
        rows += f"<tr><td>{h['date']}</td><td>KSH {h['sales']}</td><td>KSH {h['cost']}</td><td style='color:green; font-weight:bold'>KSH {h['profit']}</td></tr>"
        chart_dates.append(f"'{h['date'][5:]}'")
        chart_profits.append(str(h['profit']))
    
    if not rows:
        rows = "<tr><td colspan='4'>No sales yet - Add below!</td></tr>"

    html = f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{{font-family:Arial; background:#f0f2f5; margin:0; padding:15px}}
.card{{background:white; padding:20px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.1); flex:1; text-align:center}}
.header{{background:linear-gradient(90deg, #00c853, #009624); color:white; padding:20px; border-radius:15px; margin-bottom:20px}}
.btn{{background:#00c853; color:white; padding:12px 20px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%}}
input{{padding:12px; border-radius:8px; border:1px solid #ccc; width:100%; margin:5px 0}}
table{{width:100%; background:white; border-collapse:collapse; border-radius:10px; overflow:hidden}}
th{{background:#333; color:white; padding:10px}} td{{padding:8px; border-bottom:1px solid #eee}}
</style></head><body>

<div class="header">
<h1 style="margin:0">PLUTONET AI V5</h1>
<p>Welcome {name} | HQ Ruiru | {datetime.now().strftime('%d %b %Y')}</p>
</div>

<div style="display:flex; gap:15px; flex-wrap:wrap; margin-bottom:20px">
<div class="card"><h4>Total Sales</h4><h1>KSH {total_sales}</h1></div>
<div class="card"><h4>Total Profit</h4><h1 style="color:#00c853">KSH {total_profit}</h1></div>
<div class="card"><h4>After MPESA Fees</h4><h1 style="color:orange">KSH {net_after_mpesa:.1f}</h1><small>Fees: KSH {mpesa_fees:.1f} (0.5%)</small></div>
<div class="card"><h4>Transactions</h4><h1>{len(history)}</h1></div>
</div>

<div style="display:flex; gap:15px; flex-wrap:wrap">
<div class="card" style="flex:2">
<h3>Profit Graph</h3>
<canvas id="profitChart"></canvas>
</div>

<div class="card" style="flex:1">
<h3>Add New Sale</h3>
<form action="/add" method="post">
<input type="number" name="sales" placeholder="Sales Amount (e.g. 5000)" required>
<input type="number" name="cost" placeholder="Cost Amount (e.g. 2000)" required>
<button class="btn" type="submit">Add Sale + MPESA Calc</button>
</form>
<p style="font-size:12px; margin-top:10px">Enter sales & cost, we auto-calc profit + MPESA fees</p>
</div>
</div>

<h3 style="margin-top:20px">History - Built by {name} in Ruiru</h3>
<table><tr><th>Date</th><th>Sales</th><th>Cost</th><th>Profit</th></tr>{rows}</table>

<script>
const ctx = document.getElementById('profitChart').getContext('2d');
new Chart(ctx, {{
  type: 'bar',
  data: {{
    labels: [{','.join(chart_dates) if chart_dates else "'No Data'"}],
    datasets: [{{ label: 'Profit KSH', data: [{','.join(chart_profits) if chart_profits else '0'}], backgroundColor: '#00c853' }}]
  }}
}});
</script>
</body></html>
"""
    return html

@app.route("/add", methods=["POST"])
def add_sale():
    name, history = load_data()
    sales = float(request.form["sales"])
    cost = float(request.form["cost"])
    profit = sales - cost
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sales": sales,
        "cost": cost,
        "profit": profit
    })
    save_data(history)
    return redirect("/")

if __name__ == "__main__":
    print("PLUTONET V5 STARTING... Open http://127.0.0.1:5000")
    app.run(debug=True)