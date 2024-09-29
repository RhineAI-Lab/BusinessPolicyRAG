from flask import Flask, send_file

app = Flask(__name__)

@app.route('/business.pdf')
def serve_pdf():
    return send_file('../../data/rag/business.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7880)
