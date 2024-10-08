# VirusTotal Domain Scanner
https://virustotal-scanner.onrender.com/

This project is a VirusTotal Domain Scanner that allows you to upload an Excel file containing a list of domains. It scans each domain against the VirusTotal API, provides the result for each domain, and allows you to download the results in an Excel file. Additionally, it stores the scan history locally in the browser, and users can view previous scan histories with the option to clear them.

## Features:
- Upload an Excel file containing domains
- Fetches scan results for each domain from VirusTotal API
- Stores scan history in browser's localStorage
- Download scan results in Excel format
- History feature with expandable sections for previous scans

---

## Steps to Deploy the Project on Render
NOTE- make an acocunt on virus total and get your api key, replace that in app.py, you can use github editor to do the same and click commit.

Now,
1. Make an account on render.com
2. Make a new webservice, link your github account, make sure you have cloned this repo onto your github.
3. after cloning, select the repo, in build commands paste this- 
pip install -r requirements.txt

4. In start command paste this -
python app.py

5. Select the free tier CPU and hit start/deploy.

![image](https://github.com/user-attachments/assets/3bcedfa1-3b55-44bd-9801-fc697e281278)

