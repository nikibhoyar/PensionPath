from flask import Flask, request, jsonify
from flask_cors import CORS
from investment_calculator import calculate_investment_strategy

app = Flask(__name__)

# Allow only your Netlify domain to access the backend
CORS(app, origins=["https://sensational-tanuki-f5fb90.netlify.app"])

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Validate if the request body is JSON
        if not request.is_json:
            return jsonify({'error': 'Request must be in JSON format'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['retirementAge', 'currentAge', 'desiredFund', 'monthlyInvestment', 'riskCategory']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract and validate data types
        try:
            retirement_age = int(data['retirementAge'])
            current_age = int(data['currentAge'])
            desired_fund = float(data['desiredFund'])
            monthly_investment = float(data['monthlyInvestment'])
            risk_category = int(data['riskCategory'])
        except ValueError:
            return jsonify({'error': 'Invalid data type provided'}), 400

        # Call your investment strategy function
        result = calculate_investment_strategy(
            retirement_age,
            current_age,
            desired_fund,
            monthly_investment,
            risk_category
        )
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Ensure the app uses the correct host and port for deployment
if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible on Render
    app.run(host='0.0.0.0', port=5000, debug=False)
