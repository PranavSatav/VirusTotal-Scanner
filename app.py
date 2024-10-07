import time
import openpyxl
import requests
import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Replace with your actual VirusTotal API key
API_KEY = 'a5e4da964d2817a50f41832426cf2f7bc9f21725b890362430364768798f8c9c'
url = 'https://www.virustotal.com/api/v3/domains/'
headers = {'x-apikey': API_KEY}

def get_virus_total_data_v3(domain):
    """Fetch scan data for a domain from VirusTotal API v3."""
    response = requests.get(f"{url}{domain}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # Log error if there's a problem with the request
        print(f"Error fetching data for {domain}: {response.status_code}, {response.text}")
        return None

def process_domains(file_path):
    """Process each domain and return a list of results."""
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    results = []
    for row in range(2, sheet.max_row + 1):  # Assuming first row is headers
        domain = sheet.cell(row=row, column=1).value
        if domain:
            # Clean the domain to ensure it's in the correct format (without http:// or https://)
            domain = domain.replace("https://", "").replace("http://", "").strip()

            result = get_virus_total_data_v3(domain)
            if result:
                malicious = result['data']['attributes']['last_analysis_stats']['malicious']
                total_scans = sum(result['data']['attributes']['last_analysis_stats'].values())
                score = f"{malicious}/{total_scans}"
                status = "malicious" if malicious > 0 else "not malicious"
                results.append({'domain': domain, 'score': score, 'status': status})
            else:
                results.append({'domain': domain, 'score': "Error", 'status': "Error"})

            # Ensure we don't exceed the 4 requests per minute limit
            if len(results) % 4 == 0:
                time.sleep(60)  # Wait for 1 minute after every 4 requests
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = "uploaded.xlsx"
            file.save(file_path)

            # Process the uploaded Excel file
            results = process_domains(file_path)

            # Return the results to the frontend for display
            return jsonify(results=results)

if __name__ == "__main__":
    # Use Render's dynamic PORT and bind to 0.0.0.0 for public access
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
