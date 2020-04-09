import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timezone

sns.set(style="darkgrid")

corona_data = pd.read_csv(
    "data/CoronaAC.csv",
    sep=";",
    header="infer",
    comment="#",
    #encoding="windows-1252",
    parse_dates=["Date"],
    dayfirst=True,
    decimal=",",
)
corona_data["New Cases (Region)"] = corona_data["Cases (Region)"].diff()
corona_data["New Cases (Region) Percent"] = corona_data["New Cases (Region)"] / corona_data["Cases (Region)"]

corona_data["New Cases (City)"] = corona_data["Cases (City)"].diff()
corona_data["New Cases (City) Percent"] = corona_data["New Cases (City)"] / corona_data["Cases (City)"]

corona_data["New Cases (City) [Rolling]"] = corona_data["New Cases (City)"].rolling(2).mean()

corona_data.to_html("Corona_AC.html")
fig, axs = plt.subplots(1, 1, figsize=(15, 5), sharex=False)
plt.grid(True, which="both", ls="-")
corona_data.plot(
    x="Date",
    y=["Cases (Region)", "Cases (City)", "Recovered", "Deaths"],
    #data=corona_data,
    ax=axs,
    marker="x",
    legend="brief"
)
fig.autofmt_xdate()
plt.tight_layout()
axs.label_outer()
#plt.yscale("log")
fig.text(0, 0, f"Data as of {datetime.now(tz=timezone.utc).isoformat()}")
fig.savefig("Corona_AC_Cases.png")

corona_data_daily = corona_data.resample(
    "D",
    on="Date"
).max()

fig, axs = plt.subplots(1, 1, figsize=(15, 5), sharex=False)
plt.grid(True, which="both", ls="-")
corona_data_daily.plot.scatter(
    x="Cases (Region)",
    y="New Cases (Region)",
    ax=axs,
    marker="x",
    legend="brief",
    logy=True, logx=True,
    c="blue"
)
corona_data_daily.plot.scatter(
    x="Cases (City)",
    y="New Cases (City)",
    ax=axs,
    marker="x",
    legend="brief",
    logy=True, logx=True,
    c="yellow"
)
plt.tight_layout()
axs.label_outer()
fig.text(0, 0, f"Data as of {datetime.now(tz=timezone.utc).isoformat()}")
fig.savefig("Corona_AC_NewCasesPerCases.png")

fig, axs = plt.subplots(1, 1, figsize=(15, 5), sharex=False)
plt.grid(True, which="both", ls="-")
sns.lineplot(
    data=corona_data_daily,
    x="Date",
    y="New Cases (Region) Percent",
    ax=axs,
    marker="x",
    legend="brief",
    #logy=True, logx=True,
    #c="blue"
)
sns.lineplot(
    data=corona_data_daily,
    x="Date",
    y="New Cases (City) Percent",
    ax=axs,
    marker="x",
    legend="brief",
    #logy=True, logx=True,
    #c="yellow"
)
plt.tight_layout()
axs.label_outer()
fig.autofmt_xdate()
fig.text(0, 0, f"Data as of {datetime.now(tz=timezone.utc).isoformat()}")

fig.savefig("Corona_AC_NewCasesPerCasesPercent.png")