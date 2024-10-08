import time
import openpyxl
import requests
import os
from flask import Flask, request, render_template, jsonify, stream_with_context, Response

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
    for row in range(2, sheet.max_row + 1):  # Assuming first row is headers
        domain = sheet.cell(row=row, column=1).value
        if domain:
            # Clean the domain by removing http/https and any trailing slashes
            domain = domain.replace("https://", "").replace("http://", "").rstrip("/").strip()
            domains.append(domain)
    return domains

@app.route('/upload_and_scan', methods=['POST'])
def upload_and_scan():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = "uploaded.xlsx"
            file.save(file_path)

            domains = fetch_domains(file_path)

            def generate():
                """Generator that yields scan progress for each domain."""
                for index, domain in enumerate(domains):
                    yield f"data: Checking {index + 1} of {len(domains)}: {domain}\n\n"
                    result = get_virus_total_data_v3(domain)
                    if result:
                        malicious = result['data']['attributes']['last_analysis_stats']['malicious']
                        total_scans = sum(result['data']['attributes']['last_analysis_stats'].values())
                        score = f"{malicious}/{total_scans}"
                        status = "malicious" if malicious > 0 else "not malicious"
                    else:
                        score = "Error"
                        status = "Error"
                    
                    yield f"data: Domain: {domain}, Score: {score}, Status: {status}\n\n"
                    
                    # Timer before the next domain
                    time.sleep(20)

            return Response(stream_with_context(generate()), content_type='text/event-stream')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
