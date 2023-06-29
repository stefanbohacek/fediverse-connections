import pandas as pd
import matplotlib.pyplot as plt
import tldextract
import collections

filename = "connections.csv"
data = pd.read_csv(filename)
df = pd.DataFrame(data)

domain_info = list(map(lambda domain: tldextract.extract(f'https://{domain}/'), df["domain"]))
tlds = [ domain.suffix for domain in domain_info ]

tld_counter = collections.Counter(tlds)
df = pd.DataFrame.from_dict(tld_counter, orient='index').reset_index()
df = df.rename(columns={'index':'TLD', 0:'count'})
df = df.sort_values('count', ascending=False)
top_ten_tlds = df.head(10)
print(top_ten_tlds)

chart = top_ten_tlds.plot.bar(x="TLD", y="count", rot=45)

chart.bar_label(chart.containers[0])
plt.title("Popularity of TLDs in the fediverse")
plt.xlabel("TLD")
plt.ylabel("Number of servers")

plt.savefig("tlds.png", bbox_inches='tight', dpi=100)
