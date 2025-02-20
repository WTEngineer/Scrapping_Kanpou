from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = None
    start_date = None
    end_date = None
    
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
    return render_template('index.html', search_query=search_query, start_date=start_date, end_date=end_date)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False, threaded=False, port=3012)  # Set debug=False