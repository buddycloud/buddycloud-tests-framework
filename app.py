import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/<domain_url>')
def inspect(domain_url=None):
	
	#perform tests!
	#first one will be to check if I can find the API server through SRV

	return render_template("index.html", domain_url=domain_url)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
