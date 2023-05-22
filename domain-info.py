import datetime
import pandas as pd
import matplotlib.pyplot as plt

filename = "domain-info.csv"
data = pd.read_csv(filename)
df = pd.DataFrame(data)

# We will need to convert the dates so that matplotlib understands them.

dates = list(map(lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"), df["creation_date"]))

plt.plot_date(dates, df["domain"])
plt.title("Age of fediverse domains")
plt.xlabel("Domain creation date")

# Let's remove the Y axis for a cleaner look.

plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
plt.savefig("domain-info.png", bbox_inches='tight', dpi=100)
