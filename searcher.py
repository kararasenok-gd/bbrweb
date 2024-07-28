import requests, json, argparse
parser = argparse.ArgumentParser()
# parser.add_argument("search")

tag = input("Search: ") or "findex"

url_domains = "https://raw.githubusercontent.com/kararasenok-gd/bbrweb/main/domains.json"

domains = json.loads(requests.get(url_domains).text)

for domain in domains.get("domains", []):
    # Find tag in domain
    if tag in domain.get("tags", []):
        print(str(domain.get("name")) + "." +  str(domain.get("tld")))
        

