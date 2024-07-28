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
    if line.startswith('!>'):
        script_content = line[2:].strip()
        return f"<pre><code>{script_content}</code></pre>"  # Для показа скрипта в HTML формате
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
        return line[1:].strip()
    else:
        return line

def bbr_parse_text(text):
    lines = text.split('\n')
    parsed_lines = []

    for line in lines:
        if not line.startswith('!'):
            continue  # Игнорирование комментариев
        if line.startswith('!>'):
            script_content = line[2:].strip()
            execute_script(script_content)  # Выполнение скрипта
        else:
            parsed_lines.append(bbr_parse_line(line))

    return '\n'.join(parsed_lines)


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
x = list(x)[:-1]
x = "".join(x)

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


title_tag = head.find('title')
if title_tag:
    print(f"{TextColor.CODE}{title_tag.text}{TextColor.ENDC} - BebraWEB")
else:
    print(f"{TextColor.CODE}Untitled{TextColor.ENDC} - BebraWEB\n")

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

    print(color, tag.text, TextColor.ENDC)
    
input("Press Enter to exit...")