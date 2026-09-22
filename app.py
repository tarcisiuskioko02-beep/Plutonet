import json, os
from datetime import datetime

print("PLUTONET AI - V3 BUSINESS BANK - HQ RUIRU")

# 1. Memory - Unbreakable
if os.path.exists("memory.json"):
	try:
		with open("memory.json", "r") as f:
			json.load(f)
	except Exception:
		os.remove("memory.json")

try:
	with open("memory.json", "r") as f:
		name = json.load(f)["name"]
	print(f"Welcome BACK {name}!")
except Exception:
	name = input("Founder name? ").strip() or "Tarcisious"
	with open("memory.json", "w") as f:
		json.dump({"name": name}, f)
	print(f"Welcome {name}!")

# 2. Load old sales
if os.path.exists("sales.json"):
	with open("sales.json", "r") as f:
		history = json.load(f)
else:
	history = []

# 3. New sale
sales = float(input("Sales KSH? "))
cost = float(input("Cost KSH? "))
profit = sales - cost

# 4. Save to bank
history.append({
	"date": datetime.now().strftime("%Y-%m-%d %H:%M"),
	"sales": sales,
	"cost": cost,
	"profit": profit,
})

with open("sales.json", "w") as f:
	json.dump(history, f, indent=2)

# 5. Report
total_profit = sum(x["profit"] for x in history)
total_sales = sum(x["sales"] for x in history)

print("\n--- REPORT ---")
print(f"Today Profit: KSH {profit}")
print(f"Total Sales Ever: KSH {total_sales}")
print(f"Total Profit Ever: KSH {total_profit}")
print(f"Transactions: {len(history)}")

if profit > 20000:
	print(f"WOW {name}! Big profit! Keep pushing!")
else:
	print(f"Good job {name}! Keep growing!")
