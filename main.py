import os, requests, json, argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL to the site in BebraWEB", type=str)

args = parser.parse_args()


domain_url = "https://raw.githubusercontent.com/kararasenok-gd/bbrweb/main/domains.json"
cached_sites = requests.get(domain_url).json()

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
    # print(full_url)

if args.url:
    x = args.url
else:
    x = input("URL: ")

print(f"Opening '{x}'...")
x = x.replace("bbr://", "").replace("/", "")

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
    
# print(x_content)

soup = BeautifulSoup(x_content, 'html.parser')
body = soup.find('body')

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