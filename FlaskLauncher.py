from flask import *
app = Flask(__name__)

@app.route('/')
def home():
	return render_template("indexhome.html")
	print("launched")

if __name__ == "__main__":
	app.run()