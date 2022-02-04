from flask import *
app = Flask(__name__)

@app.route('/')
def home():
	print("launched")
	return render_template("index.html")

@app.route('/Forum')
def forum():
	return render_template("forum.html")
	
if __name__ == "__main__":
	app.run()
