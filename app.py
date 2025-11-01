from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/magazine/')
def magazine():
    return render_template('magazine/index.html')
# Add to app.py
@app.route('/achievers/')
def achievers():
    return render_template('achievers.html')
@app.route('/faculty/')
def faculty():
    return render_template('faculty.html')

if __name__ == '__main__':
    app.run(debug=True)