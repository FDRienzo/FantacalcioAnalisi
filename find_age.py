import pandas as pd
import numpy as np
import wikipedia as wiki
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

players = pd.read_csv("data/final_19.csv", sep=";")["Nome"].unique()


def main():
    age = []
    i = 0
    for player in IncrementalBar("Drafting").iter(players):
        try:
            html = wiki.page(player).html()
            soup = BeautifulSoup(html, "html5lib")
        except:
            try:
                html = wiki.page(player + " (football)").html()
                soup = BeautifulSoup(html, "html.parser")
            except:
                age.append(np.nan)
                continue
        try:
            age_info = (
                soup.find("span", attrs={"class": "ForceAgeToShow"})
                .text.replace(" (age\xa0", "")
                .replace(")", "")
            )
        except:
            age_info = np.nan
        age.append(age_info)
    df = pd.DataFrame()
    df.loc[:, "Player"] = players
    df.loc[:, "age"] = age
    df.to_csv("age_wiki.csv", sep=",", index=False)
    print(df)


main()
