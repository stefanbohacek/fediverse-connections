import requests
import csv
import json
import pandas as pd

filename = "connections.csv"
platforms = {}

datareader = csv.reader(open(filename))
domains_count= len(list(datareader))
print(f"found {domains_count} domains, processing...")
step = 0

with open(filename, "r") as csvfile:
    datareader = csv.reader(csvfile)
    next(datareader) # skip the header

    for row in datareader:
        step += 1
        domain = row[0]
        url = f"https://{domain}/.well-known/nodeinfo"

        try:
            response = requests.get(url)
            response_json = response.json()
            nodeinfo_url = response_json["links"][0]["href"]

            response = requests.get(nodeinfo_url)
            response_json = response.json()
            software_name = response_json["software"]["name"]

            print(f"{step}/{domains_count}: {domain} uses {software_name}")

            if software_name in platforms:
                platforms[software_name] += 1
            else:
                platforms[software_name] = 1
        except requests.exceptions.RequestException as e:
            print(f"error accessing {domain}")

platforms_formatted = json.dumps(platforms, indent=2)
print(platforms_formatted)

df = pd.DataFrame(platforms.items(), columns=['platform', 'servers'])
df.to_csv('platforms.csv', encoding='utf-8', index=False)
