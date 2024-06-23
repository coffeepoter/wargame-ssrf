from flask import Flask, request
import urllib.request

app = Flask(__name__)

@app.route('/render', methods=['GET'])
def fetch_url():
    url = request.args.get('url')

    if url:
        try:
            req = urllib.request.urlopen(url)
            data = req.read()
            req.close()
        except:
            return 'Error fetching URL'
        return data
    else:
        return 'URL parameter required'
    
if __name__ == '__main__':
    app.run(port=3000)