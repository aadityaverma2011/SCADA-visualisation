from flask import Flask, request, jsonify

app = Flask(__name__)

# Initial state for the plc1
plc1_data = {
    "temperature": 23,
    "control": "off"
}

# Initial state for the plc2
plc2_data = {
    "window": 0,
    "curtain": 1,
    "control": "off"
}

# Initial state for the plc3
plc3_data = {
    "ac_state": 0,
    "ac_temp": 23,
    "control": "off"
}

# Endpoint to get and post data for plc1
@app.route('/plc1', methods=['GET', 'POST'])
def plc1():
    if request.method == 'GET':
        # Return the current data as JSON
        return jsonify(plc1_data)
    
    elif request.method == 'POST':
        # Only update temperature, not control
        new_data = request.get_json()

        if 'temperature' in new_data:
            plc1_data['temperature'] = new_data['temperature']

        # Return the updated data
        return jsonify(plc1_data), 200

# Server to change both temperature and control for plc1
@app.route('/plc1/update', methods=['POST'])
def update_plc1():
    new_data = request.get_json()
    
    if 'temperature' in new_data:
        plc1_data['temperature'] = new_data['temperature']
    
    if 'control' in new_data:
        plc1_data['control'] = new_data['control']
    
    # Return the updated data
    return jsonify(plc1_data), 200

# Endpoint to get and post data for plc2
@app.route('/plc2', methods=['GET', 'POST'])
def plc2():
    if request.method == 'GET':
        # Return the current data as JSON
        return jsonify(plc2_data)
    
    elif request.method == 'POST':
        # Only update window, curtain, and control
        new_data = request.get_json()

        if 'window' in new_data:
            plc2_data['window'] = new_data['window']

        if 'curtain' in new_data:
            plc2_data['curtain'] = new_data['curtain']

        if 'control' in new_data:
            plc2_data['control'] = new_data['control']

        # Return the updated data
        return jsonify(plc2_data), 200

# Server to change window, curtain, and control for plc2
@app.route('/plc2/update', methods=['POST'])
def update_plc2():
    new_data = request.get_json()
    
    if 'window' in new_data:
        plc2_data['window'] = new_data['window']
    
    if 'curtain' in new_data:
        plc2_data['curtain'] = new_data['curtain']
    
    if 'control' in new_data:
        plc2_data['control'] = new_data['control']
    
    # Return the updated data
    return jsonify(plc2_data), 200

# Endpoint to get and post data for plc3
@app.route('/plc3', methods=['GET', 'POST'])
def plc3():
    if request.method == 'GET':
        # Return the current data as JSON
        return jsonify(plc3_data)
    
    elif request.method == 'POST':
        # Only update ac_state, ac_temp, and control
        new_data = request.get_json()

        if 'ac_state' in new_data:
            plc3_data['ac_state'] = new_data['ac_state']

        if 'ac_temp' in new_data:
            plc3_data['ac_temp'] = new_data['ac_temp']

        if 'control' in new_data:
            plc3_data['control'] = new_data['control']

        # Return the updated data
        return jsonify(plc3_data), 200

# Server to change ac_state, ac_temp, and control for plc3
@app.route('/plc3/update', methods=['POST'])
def update_plc3():
    new_data = request.get_json()
    
    if 'ac_state' in new_data:
        plc3_data['ac_state'] = new_data['ac_state']
    
    if 'ac_temp' in new_data:
        plc3_data['ac_temp'] = new_data['ac_temp']
    
    if 'control' in new_data:
        plc3_data['control'] = new_data['control']
    
    # Return the updated data
    return jsonify(plc3_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
