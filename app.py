import time
import openpyxl
import requests
import os
from flask import Flask, request, render_template, jsonify, send_file

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

def fetch_domains(file_path):
    """Extract domains from the Excel file."""
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    domains = []
    for row in range(1, sheet.max_row + 1):  # Start from row 1 to include headers
        domain = sheet.cell(row=row, column=1).value
        if domain:
            # Clean the domain by removing http/https and any trailing slashes
            domain = domain.replace("https://", "").replace("http://", "").rstrip("/").strip()
            domains.append(domain)
    return domains

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_excel', methods=['POST'])
def check_excel():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = "uploaded.xlsx"
            file.save(file_path)

            # Fetch domains from the uploaded Excel file
            domains = fetch_domains(file_path)

            # Return the domains to the frontend for display
            return jsonify(domains=domains)

@app.route('/scan_domain', methods=['POST'])
def scan_domain():
    if request.method == 'POST':
        domain = request.form.get('domain')
        if domain:
            result = get_virus_total_data_v3(domain)
            if result:
                malicious = result['data']['attributes']['last_analysis_stats']['malicious']
                total_scans = sum(result['data']['attributes']['last_analysis_stats'].values())
                score = f"{malicious}/{total_scans}"
                status = "malicious" if malicious > 0 else "not malicious"
                return jsonify({'domain': domain, 'score': score, 'status': status})
            else:
                return jsonify({'domain': domain, 'score': "Error", 'status': "Error"})

@app.route('/download_results', methods=['POST'])
def download_results():
    if request.method == 'POST':
        results = request.json.get('results', [])
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['Domain Name', 'Scan Result'])  # Header row

        for result in results:
            ws.append([result['domain'], result['score'] + " (" + result['status'] + ")"])

        output_file = "scan_results.xlsx"
        wb.save(output_file)
        return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    # Use Render's dynamic PORT and bind to 0.0.0.0 for public access
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
