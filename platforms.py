import pandas as pd
import matplotlib.pyplot as plt

filename = "platforms.csv"
data = pd.read_csv(filename)
df = pd.DataFrame(data)

df_sorted = df.sort_values(by=["servers"], ascending=False)
chart = df_sorted.plot.bar(x="platform", y="servers", rot=45)

chart.bar_label(chart.containers[0])

plt.title("Popularity of fediverse platforms")
plt.xlabel("Platform")
plt.ylabel("Number of servers")

plt.savefig("platforms.png", bbox_inches='tight', dpi=100)
