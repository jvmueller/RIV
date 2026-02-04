from flask import Flask, render_template, request
from demand import main
from demand.rail_line import RailLine
import os


app = Flask(__name__, static_folder = "static")
# Set the database path for your app
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['DATABASE_PATH'] = os.path.join(basedir, 'database.db')

@app.route('/')
def home():
    return render_template('index.html', error_message = "")


@app.route('/results', methods=['POST'])
def results():
    city_names: list[str] = []
    form_data = request.form
    
    i = 1
    while f'input{i}' in form_data:
        city_names.append(form_data[f'input{i}'])
        i += 1
    
    line: RailLine = main.get_line(city_names,160)
    if line:
        mode_str = f"rail mode: {line.mode.value}  average speed (mph): {line.avg_speed}\n"
        line_str = line.to_string()
        city_pair_str = line.get_city_pair_info()
        return render_template('result.html', mode_str = mode_str, line_str = line_str, city_pair_str = city_pair_str)
    else:
        return render_template('index.html', error_message = "error: invalid city names entered.")
        
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/make-a-line')
def mal():
    return render_template('index.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(debug=True)