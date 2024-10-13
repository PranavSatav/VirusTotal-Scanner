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
<hr>

Javascript version - Just download index.html and run in browser haha, so easy no need to do all sorcery in python...and this is how it looks..<hr>
![image](https://github.com/user-attachments/assets/1aecac92-e83b-4740-95df-62177e7c1801)
<hr>
## 🚀 Features of this javascript version, because its cool..

- **File Upload** 📂:  
  Custom-styled button for uploading Excel or text files containing domains.

- **Domain Processing** 🔍:  
  Extracts domains from uploaded files and displays them in a list.

- **VirusTotal API Integration** ⚡:  
  Checks each domain against the VirusTotal API for malicious content.  
  Displays results indicating whether the domain is "Clean" or "Malicious," along with detection scores.

- **Countdown Timer** ⏳:  
  Displays a countdown before checking the next domain, only if there are more domains left to check.

- **Scan Results History** 📜:  
  Saves scan results to local storage with a timestamp for each scan session.  
  Each history entry can be expanded to view detailed scan results.

- **Download Results** 💾:  
  Provides a button to download the scan results in JSON format after all domains have been checked.

- **Clear History** ❌:  
  Allows users to clear the stored scan history from local storage.

- **Responsive Design** 📱:  
  Utilizes Tailwind CSS for a modern, responsive UI that is visually appealing.

