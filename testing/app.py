from flask import Flask, request, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({'success': 'File uploaded successfully', 'filename': file.filename})

@app.route('/data/<filename>', methods=['GET'])
def get_data(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    data = pd.read_csv(file_path)
    data_html = data.to_html(classes='table table-striped', index=False)
    return data_html

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/calculate-pricing/<filename>', methods=['GET'])
def calculate_pricing(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    data = pd.read_csv(file_path)

    base_price = 10
    price_per_credit_line = 2
    price_per_credit_score_point = 0.01

    data['SubscriptionPrice'] = base_price + \
        (price_per_credit_line * data['CreditLines']) + \
        (price_per_credit_score_point * data['CreditScore'])

    data_html = data.to_html(classes='table table-striped', index=False)
    return data_html
