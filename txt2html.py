import os
from html.parser import HTMLParser
import subprocess

# Prompt the user for the name of the image to scan
image_name = input("Please enter the name of the image to scan: ")

# Run the scan using grype and capture the output
scan_output = subprocess.check_output(['grype', image_name])

# Write the output to a text file
with open('scan-result.txt', 'w') as file:
    file.write(scan_output.decode('utf-8'))
    
# Print a confirmation message
print(f"Scan results saved to scan-result.txt for image: {image_name}")

class MyHTMLParser(HTMLParser):
    def __init__(self, outfile):
        super().__init__()
        self.outfile = outfile

    def handle_starttag(self, tag, attrs):
        self.outfile.write(' ' * self.getpos()[1] + f'<{tag}>\n')

    def handle_endtag(self, tag):
        self.outfile.write(' ' * self.getpos()[1] + f'</{tag}>\n')

    def handle_data(self, data):
        self.outfile.write(' ' * self.getpos()[1] + f'{data}\n')

    def handle_comment(self, data):
        self.outfile.write(' ' * self.getpos()[1] + f'<!--{data}-->\n')

    def handle_entityref(self, name):
        self.outfile.write(' ' * self.getpos()[1] + f'&{name};\n')

    def handle_charref(self, name):
        self.outfile.write(' ' * self.getpos()[1] + f'&#{name};\n')

def generate_filter_html():
    return '''
        <label for="severity-filter" style="font-weight: bold;">Filter by severity:</label>
        <select id="severity-filter" style="padding: 5px; border-radius: 5px; margin-left: 10px;">
            <option value="">All</option>
            <option value="Critical" style="background-color: #F56767; color: white;">Critical</option>
            <option value="High" style="background-color: #FC986D; color: white;">High</option>
            <option value="Medium" style="background-color: #FCD56D; color: white;">Medium</option>
            <option value="Low" style="background-color: #AEE56D; color: white;">Low</option>
            <option value="Unknown" style="background-color: #E0ECE0; color: black;">Unknown</option>
        </select>
    '''

def transform_txt_to_html(txt_file, html_file):
    with open(txt_file, 'r') as f:
        lines = f.readlines()

    with open(html_file, 'w') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<title>ImScan</title>\n')
        f.write('<link rel="icon" type="image/png" href="./img/imscan.ico">\n')
        f.write('<style>\n')
        f.write('body {\n')
        f.write('    background-color: #162041;\n')
        f.write('    color: #fff;\n')
        f.write('}\n')
        f.write('table {\n')
        f.write('    border-collapse: collapse;\n')
        f.write('    width: 80%;\n')
        f.write('    margin: auto;\n')
        f.write('}\n')
        f.write('th, td {\n')
        f.write('    text-align: left;\n')
        f.write('    padding: 12px;\n')
        f.write('}\n')
        f.write('th {\n')
        f.write('    background-color: #D6EAF8;\n')
        f.write('    border-bottom: 2px solid #7FB3D5;\n')
        f.write('    color: #34495E;\n')
        f.write('}\n')
        f.write('td {\n')
        f.write('    border-bottom: 1px solid #E0E0E0;\n')
        f.write('}\n')
        f.write('.Low {\n')
        f.write('    background-color: #AEE56D;\n')
        f.write('    color: #1E8449;\n')
        f.write('}\n')
        f.write('.Medium {\n')
        f.write('    background-color: #FCD56D;\n')
        f.write('    color: #B7950B;\n')
        f.write('}\n')
        f.write('.High {\n')
        f.write('    background-color: #FC986D;\n')
        f.write('    color: #922B21;\n')
        f.write('}\n')
        f.write('.Critical {\n')
        f.write('    background-color: #F56767;\n')
        f.write('    color: #641E16;\n')
        f.write('}\n')
        f.write('.Unknown {\n')
        f.write('    background-color: #E0ECE0;\n')
        f.write('    color: #6E6E6E;\n')
        f.write('}\n')
        f.write('tr:hover {\n')
        f.write('    background-color: #7FB3D5;\n')
        f.write('}\n')
        f.write('</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<div style="display:flex;align-items:center;">')
        f.write('<img src="./img/imscan.png" style="width: 200px; height: auto; border-radius: 21px; margin-right: 20px;"></img>')
        f.write('</div>\n')
        f.write('<p>The following vulnerabilities were found in the image:</p>\n')
        f.write(generate_filter_html())
        f.write('<table id="scan-table">\n')
        f.write('<thead style="background: #9EB5DB;"><tr><th style="padding: 10px;">Description</th><th style="padding: 10px;">Severity</th></tr></thead>\n')
        f.write('<tbody>\n')

        severity_order = ['Critical', 'High', 'Medium', 'Low', 'Unknown']

        lines_with_severity = []
        for line in lines:
            severity = ""
            if "Low" in line:
                severity = "Low"
            elif "Medium" in line:
                severity = "Medium"
            elif "High" in line:
                severity = "High"
            elif "Critical" in line:
                severity = "Critical"
            elif "Unknown" in line:
                severity = "Unknown"

            if severity != "":
                lines_with_severity.append((line.strip(), severity))
            else:
                lines_with_severity.append((line.strip(), ""))

        # sort by severity
        lines_with_severity.sort(key=lambda x: severity_order.index(x[1]) if x[1] in severity_order else len(severity_order))

        for line, severity in lines_with_severity:
            if severity != "":
                f.write(f'<tr class="{severity}"><td>{line}</td><td>{severity}</td></tr>\n')
            else:
                f.write(f'<tr><td>{line}</td><td></td></tr>\n')

        f.write('</tbody>\n')
        f.write('</table>\n')
        f.write('<script>\n')
        f.write('document.getElementById("severity-filter").addEventListener("change", function() {\n')
        f.write('    var selected = this.value;\n')
        f.write('    var rows = document.querySelectorAll("#scan-table tbody tr");\n')
        f.write('    for (var i = 0; i < rows.length; i++) {\n')
        f.write('        if (selected === "" || rows[i].classList.contains(selected)) {\n')
        f.write('            rows[i].style.display = "table-row";\n')
        f.write('        } else {\n')
        f.write('            rows[i].style.display = "none";\n')
        f.write('        }\n')
        f.write('    }\n')
        f.write('});\n')
        f.write('</script>\n')
        f.write('</body>\n')
        f.write('</html>\n')

    print(f"HTML file written to {os.path.abspath(html_file)}")

transform_txt_to_html('./scan-result.txt', 'output.html')