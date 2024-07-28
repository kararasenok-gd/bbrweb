import os, requests, json

domain_url = "https://raw.githubusercontent.com/kararasenok-gd/bbrweb/main/domains.json"
cached_sites = requests.get(domain_url).json()

for i in cached_sites.get("domains"):
    name = i["name"]
    tld = i["tld"]

    full_url = name + "." + tld
    print(full_url)

x = input("url: ")

