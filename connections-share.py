import requests
import csv
import json
import pandas as pd

filename = "connections-sample.csv"
platforms = {}

datareader = csv.reader(open(filename))
domains_count= len(list(datareader))

domains_accessed_count = 0
single_user_instance_count = 0
multi_user_instance_count = 0
data = []

print(f"found {domains_count} domains, processing...")
step = 0

with open(filename, "r") as csvfile:
    datareader = csv.reader(csvfile)
    next(datareader) # skip the header

    for row in datareader:
        step += 1
        domain = row[0]
        connections = int(row[1])
        url = f"https://{domain}/.well-known/nodeinfo"

        try:
            response = requests.get(url, timeout=360)
            response_json = response.json()
            nodeinfo_url = response_json["links"][0]["href"]

            response = requests.get(nodeinfo_url, timeout=360)
            response_json = response.json()
            total_users = int(response_json["usage"]["users"]["total"])
            print(f"{step:,}/{domains_count:,}: {domain} has {total_users:,} total users")

            domains_accessed_count += 1

            if (total_users == 1):
                single_user_instance_count += 1
            else:
                multi_user_instance_count += 1

            data.append({
                'domain': domain,
                'connections': connections,
                'total_users': total_users,
                'connections_share_percent': (connections/total_users) * 100,
            })

        except requests.exceptions.RequestException as e:
            print(f"error accessing {domain}")

data_formatted = json.dumps(data, indent=2)
print(data_formatted)

single_user_instance_percent = (single_user_instance_count/domains_accessed_count) * 100
multi_user_instance_percent = (multi_user_instance_count/domains_accessed_count) * 100

print(f"Processed {domains_accessed_count:,}/{domains_count:,} domain(s)")
print("You are connected to:")
print(f"- {single_user_instance_count:,} single-user instance(s) ({single_user_instance_percent}%)")
print(f"- {multi_user_instance_count:,} multi-user instance(s) ({multi_user_instance_percent}%)")

df = pd.DataFrame(data, columns=['domain', 'total_users', 'connections', 'connections_share_percent'])
df.sort_values(by=['connections_share_percent'], ascending=False).to_csv('connections_share.csv', encoding='utf-8', index=False)

df = pd.DataFrame({
    'instances_total' : domains_accessed_count,
    'instances_single_user' : single_user_instance_count,
    'instances_multi_user' : multi_user_instance_count,
}, index=[0])

df.to_csv('connections_share_results.csv', encoding='utf-8', index=False)
