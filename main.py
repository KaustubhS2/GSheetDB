from flask import Flask, request, render_template, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configure Google Sheets API credentials
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

# Open your Google Sheets spreadsheet by its URL
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/17emdwuOGKTvCHooRE-R3bWb83DT0AmfAvIp-AEskDK4/edit#gid=0'
spreadsheet = client.open_by_url(spreadsheet_url)
worksheet = spreadsheet.get_worksheet(0)  # Adjust the index or title as needed


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        data = [name, mobile]

        # Append the data to the Google Sheets
        worksheet.append_row(data)

        # Redirect to the success page after submission
        return redirect(url_for('success'))


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
