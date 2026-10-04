import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 Teri API Key (jo user use karega)
VALID_KEY = "@Brijesh_21"

# Original API details
ORIGINAL_API_URL = "https://num-to-info-reseller.asurpapa.workers.dev/api"
ORIGINAL_KEY = "SHURUU"  # <-- Original key (jo valid hai)

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "High-Tech Number Info API is working!",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER",
        "endpoints": {
            "info": "/api?key=YOUR_KEY&number=PHONE_NUMBER"
        },
        "example": "/api?key=@Brijesh_21&number=9876543210"
    })

@app.route('/api')
def num_to_info():
    # Get parameters
    key = request.args.get('key')
    number = request.args.get('number')
    
    # 🔐 Key verify
    if not key:
        return jsonify({
            "status": False,
            "error": "Missing API Key!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
        
    if key != VALID_KEY:
        return jsonify({
            "status": False,
            "error": "Invalid API Key!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 401
    
    if not number:
        return jsonify({
            "status": False,
            "error": "Missing 'number' parameter!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
    
    # Clean number
    number = number.strip().replace(" ", "").replace("+", "")
    if number.startswith("91") and len(number) == 12:
        number = number[2:]
    
    if not number.isdigit() or len(number) != 10:
        return jsonify({
            "status": False,
            "error": "Invalid phone number! Must be 10 digits.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
    
    # Forward to original API with ORIGINAL_KEY
    params = {
        'key': ORIGINAL_KEY,  # <-- Original key send kar rahe hain
        'number': number
    }
    
    try:
        response = requests.get(ORIGINAL_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # 🔥 Clean response
        if isinstance(data, dict):
            # Remove key_info completely
            data.pop('key_info', None)
            
            # Remove credit section
            data.pop('credit', None)
            
            # Check if data is not found
            if 'data' in data and isinstance(data['data'], dict):
                if data['data'].get('status') == 'not_found':
                    return jsonify({
                        "status": False,
                        "message": "Phone number not found",
                        "developer": "@x_TRACEOWNER",
                        "credit": "@x_TRACEOWNER"
                    }), 404
            
            # Add our branding
            data['developer'] = '@x_TRACEOWNER'
            data['credit'] = '@x_TRACEOWNER'
            
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        return jsonify({
            "status": False,
            "error": "Server is busy! Please try again after some time.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": False,
            "error": "Network issue! Please check your connection.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 503
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": False,
            "error": "Service temporarily unavailable. Please try again later.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 500
        
    except Exception as e:
        return jsonify({
            "status": False,
            "error": "Something went wrong. Please try again later.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 500

@app.route('/api/<path:path>')
def catch_all(path):
    return jsonify({
        "status": False,
        "error": "Invalid endpoint. Use /api?key=YOUR_KEY&number=PHONE_NUMBER",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": False,
        "message": "Phone number not found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": False,
        "message": "Phone number not found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))