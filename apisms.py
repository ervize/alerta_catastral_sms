from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sms 

app = Flask(__name__)
# CORS(app)
cors = CORS(app, resources={"/api/*": {"origins": "http://localhost:3001"}})

@app.route('/api/v1/enviarsms', methods=['POST'])
def enviarsms():
    json = request.get_json(force=True)
    if json.get('numcel') is None:
        return jsonify({'message': 'Ingrese numero de celular'}), 400
    if json.get('message') is None:
        return jsonify({'message': 'Ingrese mensaje'}), 400

    try:

        msg={'Ok': True,
                    'Mensaje': 'Mensaje enviado correctamente'}

        lsms = sms.TextMessage(json.get('numcel') , json.get('message'))
        lsms.connectPhone()
        lsms.sendMessage()
        lsms.disconnectPhone()
        print(msg)
       
    except:
        msg={'Ok': False,
                    'Mensaje': 'Error enviando mensaje'}
        print('error')

    finally:
        return jsonify(msg)
    
if __name__ ==  '__main__':
    app.run(debug=True,port=5000)