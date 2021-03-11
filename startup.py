from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')

@app.route('/contact', methods=["GET"])
def contact():
    return  render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)