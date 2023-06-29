import os
import csv
import json
import re
import pandas as pd
import matplotlib.pyplot as plt

filename = "domains.csv"

datareader = csv.reader(open(filename))
domains_count= len(list(datareader))
print(f"found {domains_count} domains, processing...")
step = 0

domain_info = {}

with open(filename, "r") as csvfile:
    datareader = csv.reader(csvfile)
    next(datareader) # skip the header

    for rows in datareader:
        step += 1
        domain = rows[0]
        print(f"{step}/{domains_count}: {domain}")

        try:
            stream = os.popen(f"whois {domain}")
            output = stream.read()

            match = re.search(r"Creation Date: (\d{4}-\d{2}-\d{2})", output)
            creation_date = match.group(1)

            domain_info[domain] = creation_date
            print(creation_date)

        except (AttributeError, UnicodeDecodeError) as e:
            print("creation date not available")

        if (step % 5 == 0):
            print('saving data...')
            df = pd.DataFrame(domain_info.items(), columns=["domain", "creation_date"])
            df.to_csv("domain-info.csv", encoding="utf-8", index=False)


print(json.dumps(domain_info, indent=2))

df = pd.DataFrame(domain_info.items(), columns=["domain", "creation_date"])
df.to_csv("domain-info.csv", encoding="utf-8", index=False)


