from flask import Flask, request, render_template_string
from bs4 import BeautifulSoup

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

    # Check for incorrect or insecure parameters (basic example)
    for tag in soup.find_all(['a', 'form']):
        href = tag.get('href')
        action = tag.get('action')
        if href and "?" in href:
            vulnerabilities.append(f"Check parameters in URL: {href}")
        if action and "?" in action:
            vulnerabilities.append(f"Check parameters in form action: {action}")

    # Add more checks as needed...

    if not vulnerabilities:
        return "No vulnerabilities found"
    else:
        return "<br>".join(vulnerabilities)

if __name__ == '__main__':
    app.run(debug=False)
