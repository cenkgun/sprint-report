from flask import Flask, request, jsonify
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    creds_base64 = os.getenv('GOOGLE_CREDENTIALS')
    if creds_base64:
        creds_json = base64.b64decode(creds_base64).decode('utf-8')
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key("1wYKfXFreMqSbRri0w275rLTvntKoXjWbDBmvyFbXEDk")
        sheet = spreadsheet.sheet1
except Exception as e:
    print(f"Error loading credentials: {str(e)}")


@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        data = request.get_json()
        row = [
            data.get('sprintName', ''),
            data.get('taskLink', ''),
            data.get('taskId', ''),
            data.get('title', ''),
            data.get('status', ''),
            data.get('component', ''),
            data.get('assignee', ''),
            data.get('storyPoints', ''),
            data.get('issueType', ''),
            data.get('pml', '')
        ]
        sheet.append_row(row)
        return jsonify({"message": "Successfully completed!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
