from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html',
                           version=os.getenv('APP_VERSION', '1.0.0'))

@app.route('/health')
def health():
    return {'status': 'healthy', 'version': os.getenv('APP_VERSION', '1.0.0')}

@app.route('/about')
def about():
    return {'info': 'Esta es una app de ejemplo para practicar Docker y CI/CD'}

if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
