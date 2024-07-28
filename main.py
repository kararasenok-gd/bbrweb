import os, requests, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL to the site in BebraWEB", type=str)

args = parser.parse_args()


domain_url = "https://raw.githubusercontent.com/kararasenok-gd/bbrweb/main/domains.json"
cached_sites = requests.get(domain_url).json()

for i in cached_sites.get("domains"):
    name = i["name"]
    tld = i["tld"]

    full_url = name + "." + tld
    # print(full_url)

if args.url:
    x = args.url
else:
    x = input("URL: ")

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
    
print(x_content)

# forming html output
