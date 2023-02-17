import os
from html.parser import HTMLParser

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

def transform_txt_to_html(txt_file, html_file):
    with open(txt_file, 'r') as f:
        lines = f.readlines()

    with open(html_file, 'w') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<title>Image Scan Vulnerability</title>\n')
        f.write('<style>\n')
        f.write('table {\n')
        f.write('    border-collapse: collapse;\n')
        f.write('    width: 100%;\n')
        f.write('}\n')
        f.write('th, td {\n')
        f.write('    text-align: left;\n')
        f.write('    padding: 8px;\n')
        f.write('}\n')
        f.write('th {\n')
        f.write('    background-color: #ccc;\n')
        f.write('    border: 1px solid #000;\n')
        f.write('}\n')
        f.write('td {\n')
        f.write('    border: 1px solid #000;\n')
        f.write('}\n')
        f.write('.Low {\n')
        f.write('    background-color: #B7F6B7;\n')
        f.write('}\n')
        f.write('.Medium {\n')
        f.write('    background-color: #FBF6B7;\n')
        f.write('}\n')
        f.write('.High {\n')
        f.write('    background-color: #F6D6B7;\n')
        f.write('}\n')
        f.write('.Critical {\n')
        f.write('    background-color: #F6B7B7;\n')
        f.write('}\n')
        f.write('.Unknown {\n')
        f.write('    background-color: #E0E0E0;\n')
        f.write('}\n')
        f.write('</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<table>\n')
        f.write('<thead><tr><th>Scan results</th><th>Severity</th></tr></thead>\n')
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
        f.write('</body>\n')
        f.write('</html>\n')

    print(f"HTML file written to {os.path.abspath(html_file)}")

transform_txt_to_html('./scan-result.txt', 'output.html')