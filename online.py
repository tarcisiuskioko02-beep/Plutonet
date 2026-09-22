from pyngrok import ngrok
from dashboard import app

# Create public link
public_url = ngrok.connect(5000, domain="yogurt-unadvised-juicy.ngrok-free.dev")
print("\n" + "="*60)
print(f" PLUTONET AI IS ONLINE WORLDWIDE!")
print(f" LINK: {public_url}")
print(f" Share this link to anyone!")
print("="*60 + "\n")

# Start your website
app.run(port=5000)