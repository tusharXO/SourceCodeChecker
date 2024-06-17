from flask import Flask, request, render_template_string
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# HTML template for the upload form
upload_form = '''
<!doctype html>
<title>Upload HTML File</title>
<h1>Upload HTML File</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.html'):
            content = file.read().decode('utf-8')
            return check_vulnerabilities(content)
        else:
            return "Please upload a valid HTML file"
    return render_template_string(upload_form)

def check_vulnerabilities(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    vulnerabilities = []

    # Check for SQL injection vulnerabilities (basic example)
    sql_patterns = ["SELECT * FROM", "UNION SELECT", "INSERT INTO", "UPDATE SET", "DELETE FROM"]
    for pattern in sql_patterns:
        if pattern in html_content.upper():
            vulnerabilities.append(f"Potential SQL Injection vulnerability found: {pattern}")

    # Check for XSS vulnerabilities
    script_tags = soup.find_all('script')
    for script in script_tags:
        vulnerabilities.append("Potential XSS vulnerability found in script tag")

    # Check for CSRF vulnerabilities
    form_tags = soup.find_all('form')
    for form in form_tags:
        csrf_token = form.find('input', attrs={'name': 'csrf_token'})
        if not csrf_token:
            vulnerabilities.append("CSRF token missing in form")

    # Check for insecure file upload
    file_inputs = soup.find_all('input', attrs={'type': 'file'})
    for file_input in file_inputs:
        if not file_input.get('accept'):
            vulnerabilities.append("Insecure file upload: 'accept' attribute missing")

    # Check for sensitive data exposure
    sensitive_fields = re.findall(r'(password|secret)', html_content, re.IGNORECASE)
    if sensitive_fields:
        vulnerabilities.append("Sensitive data exposure: Possible sensitive fields found")

    # Check for direct object references
    direct_object_refs = re.findall(r'href=["\'](?!https?://)(.*?)["\']', html_content)
    if direct_object_refs:
        vulnerabilities.append("Direct object reference: Found non-HTTP(S) URLs")

    if not vulnerabilities:
        return "No vulnerabilities found"
    else:
        return "<br>".join(vulnerabilities)

if __name__ == '__main__':
    app.run(debug=False)
