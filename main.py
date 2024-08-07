import os, requests, json, argparse, re
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL to the site in BebraWEB", type=str)

args = parser.parse_args()

domain_url = "https://raw.githubusercontent.com/kararasenok-gd/bbrweb/main/domains.json"
cached_sites = requests.get(domain_url).json()
# cached_sites = json.loads(open("domains.json", "r").read())


def execute_script(code):
    exec(code, globals())

def bbr_parse_line(line):
    # if line.startswith('!>'):
        # script_content = line[2:].strip()
        # return f"<pre><code>{script_content}</code></pre>"  # Для показа скрипта в HTML формате
    if line.startswith('!<'):
        return f"<title>{line[2:].strip()}</title>"
    elif line.startswith('!_'):
        return f"<u>{line[2:].strip()}</u>"
    elif line.startswith('!!'):
        return f"<b>{line[2:].strip()}</b>"
    elif line.startswith('!/'):
        return f"<i>{line[2:].strip()}</i>"
    elif line.startswith('!col>'):
        match = re.match(r'!col>(.*)>>\s*(.*)', line)
        if match:
            color = match.group(1).strip()
            text = match.group(2).strip()
            
            if color == "purple":
                color = "h1"
            elif color == "blue":
                color = "h2"
            elif color == "cyan":
                color = "h3"
            elif color == "green":
                color = "h4"
            elif color == "orange":
                color = "h5"
            elif color == "red":
                color = "h6"
            elif color == "gray":
                color = "p"
            elif color == "white":
                color = "a"
            else:
                color = "footer"
            
            return f'<{color}>{text}</{color}>'
    elif line.startswith('!'):
        return f"<footer>{line[1:].strip()}</footer>"
    else:
        return line

def bbr_parse_text(text):
    lines = text.split('\n')
    parsed_lines = []

    for line in lines:
        if not line.startswith('!'):
            continue
        parsed_lines.append(bbr_parse_line(line))

    parslines = '\n'.join(parsed_lines)
    htmltemplete = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
[[CONTENT]]
</body>
</html>
    """
    
    # print(htmltemplete.replace("[[CONTENT]]", parslines))
    return htmltemplete.replace("[[CONTENT]]", parslines)
    
domain_url = "https://raw.githubusercontent.com/kararasenok-gd/bbrweb/main/domains.json"
cached_sites = requests.get(domain_url).json()
# cached_sites = json.loads(open("domains.json", "r").read())

class TextColor:
    H1 = '\u001b[95m'
    H2 = '\u001b[94m'
    H3 = '\u001b[96m'
    H4 = '\u001b[92m'
    H5 = '\u001b[93m'
    H6 = '\u001b[91m'
    P = '\u001b[90m'
    A = '\u001b[97m'
    SPAN = '\u001b[94m'
    STRONG = '\u001b[91m'
    EM = '\u001b[96m'
    B = '\u001b[92m'
    I = '\u001b[93m'
    U = '\u001b[95m'
    SMALL = '\u001b[90m'
    BLOCKQUOTE = '\u001b[96m'
    PRE = '\u001b[97m'
    CODE = '\u001b[92m'
    ENDC = '\u001b[0m'

for i in cached_sites.get("domains"):
    name = i["name"]
    tld = i["tld"]

    full_url = name + "." + tld

if args.url:
    x = args.url
else:
    x = input("URL: ")

print(f"Opening '{x}'...")
x_old = x
x = x.replace("bbr://", "")
if x.endswith("/"):
    x = list(x)[:-1]
    x = "".join(x)
    
if x_old == "bbr:///" or x_old == "bbr://" or x_old == "":
    x = ".home"

found = False

for i in cached_sites.get("domains"):
    if i["name"] + "." + i["tld"] == x:
        found = True
        x_url = i["ip"]
        x_content = requests.get(x_url).text
        break

if not found:
    print("Domain not found")
    quit()
    
if x_url.endswith(".bbr"):
    x_content = bbr_parse_text(x_content)
    
# print(x_content)

soup = BeautifulSoup(x_content, 'html.parser')
body = soup.find('body')
head = soup.find('head')

body_title = soup.body.find('title')
if body_title:
    if not soup.head:
        soup.head = soup.new_tag('head')
    soup.head.append(body_title.extract())
    
# Теперь ищем тег <title> в <head>
title_tag = soup.head.find('title') if soup.head else None

# os.system("cls" if os.name == "nt" else "clear")

if title_tag:
    print(f"{TextColor.CODE}{title_tag.text}{TextColor.ENDC} - BebraWEB")
else:
    print(f"{TextColor.STRONG}ERR: No Title Tag Found{TextColor.ENDC} - BebraWEB\n")

print(f"{TextColor.H5}{x_old}{TextColor.ENDC}\n\n")

color_mapping = {
    'h1': TextColor.H1,
    'h2': TextColor.H2,
    'h3': TextColor.H3,
    'h4': TextColor.H4,
    'h5': TextColor.H5,
    'h6': TextColor.H6,
    'p': TextColor.P,
    'a': TextColor.A,
    'span': TextColor.SPAN,
    'strong': TextColor.STRONG,
    'em': TextColor.EM,
    'b': TextColor.B,
    'i': TextColor.I,
    'u': TextColor.U,
    'small': TextColor.SMALL,
    'blockquote': TextColor.BLOCKQUOTE,
    'pre': TextColor.PRE,
    'code': TextColor.CODE,
}


for tag in body.find_all():
    tag_name = tag.name
    color = color_mapping.get(tag_name, TextColor.ENDC)

    if tag_name == 'a':
        print(color, tag.text, " - ", tag.get('href'), TextColor.ENDC)
    else:
        print(color, tag.text, TextColor.ENDC)
    
input("Press Enter to exit...")