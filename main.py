from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key("1wYKfXFreMqSbRri0w275rLTvntKoXjWbDBmvyFbXEDk")
sheet = spreadsheet.sheet1


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
