from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main_view():
    template = "index.html"
    return render_template(template)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
