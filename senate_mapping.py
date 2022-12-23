import pandas as pd
import requests
from bs4 import BeautifulSoup as Soup
import seaborn as sns
import matplotlib.pyplot as plt


def parse_row(row):
    ret_row = [str(x.string) for x in row.find_all(["td", "span"])][0:5]
    ret_row.remove("None")
    return ret_row


response = requests.get("https://www.senate.gov/senators/")
soup = Soup(response.text, "lxml")

table = soup.find_all("table")[0]
rows = table.find_all("tr")

list_of_parsed_rows = [parse_row(row) for row in rows[1:]]

df = pd.DataFrame(list_of_parsed_rows)
df.columns = ["Name", "State", "Party", "Class"]


new = df["Name"].str.split(", ", expand = True)
df["First_Name"] = new[1]
df["Last_Name"] = new[0]
df = df[["First_Name", "Last_Name", "State", "Party", "Class"]]

sns.countplot(x="Party", hue = "Class", data = df)
plt.show()
