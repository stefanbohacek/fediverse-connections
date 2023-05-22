import requests
import csv
import json
import pandas as pd

filename = "connections.csv"
user_counts = {}

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
            try:
                users_total = response_json["usage"]["users"]["total"]
                print(f"{step}/{domains_count}: {domain} has {users_total} total users")
                user_counts[domain] = users_total
            except Exception as e:
                print(f"error accessing {domain} user information")

        except requests.exceptions.RequestException as e:
            print(f"error accessing {domain}")

user_counts_formatted = json.dumps(user_counts, indent=2)
print(user_counts_formatted)

df = pd.DataFrame(user_counts.items(), columns=['platform', 'users_total'])
df.to_csv('user-counts.csv', encoding='utf-8', index=False)
