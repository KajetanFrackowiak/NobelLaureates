import json

import pandas as pd
import os
import requests
import sys
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    df = pd.read_json('../Data/Nobel_laureates.json')
    df.to_csv('../Data/Nobel_laureateso.csv')

    df.dropna(subset='gender', axis=0, inplace=True)
    df.reset_index(inplace=True, drop=True)
    newbi = df['place_of_birth'].apply(
        lambda x: str.split(x, ",")[-1].strip() if (x is not None and ',' in x) else None)
    df['born_in'].replace(to_replace="", regex=True, value=np.nan, inplace=True)
    df['born_in'].fillna(newbi, inplace=True, axis=0)
    df['born_in'].replace(to_replace=['United States', 'U.S.', 'US'], regex=True, value='USA', inplace=True)
    df['born_in'].replace(to_replace=['USAA'], regex=True, value='USA', inplace=True)
    df['born_in'].replace(to_replace=['United Kingdom'], regex=True, value='UK', inplace=True)
    df.dropna(inplace=True, subset=["born_in"])
    df.reset_index(inplace=True, drop=True)

    # Extract year of birth and calculate age of winning using vectorized operations
    df['year_born'] = df['date_of_birth'].str.extract(r'(\d{4})').astype(float)
    df['age_of_winning'] = df['year'] - df['year_born']

    # Replace countries appearing less than 25 times with 'Other countries'
    # df['ctpie'] = df['born_in'].apply(lambda x: x if df['born_in'].value_counts()[x] >= 25 else 'Other countries')

    # Extract data for the pie chart
    # pdata = df['ctpie'].value_counts().tolist()
    # plabels = df['ctpie'].value_counts().keys().tolist()
    # pcolors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']
    # pexplode = [0, 0, 0, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]

    # Create a pie chart with autopct formatting
    # plt.figure(figsize=(12, 12))
    # plt.pie(pdata,
    #         explode=pexplode,
    #         labels=plabels,
    #         colors=pcolors,
    #         autopct=lambda p: f'{p:.2f}%\n({p * sum(pdata) / 100 :.0f})'
    #         )
    # plt.show()

    # df = df[df['category'] != ""]
    # category_male = df[df['gender'] == 'male'].groupby(['category'])['category'].count()
    # category_female = df[df['gender'] == 'female'].groupby(['category'])['category'].count()
    # category_male_keys = category_male.keys().tolist()
    #
    # x_axis = np.arange(len(category_male_keys))
    #
    # fig, ax = plt.subplots(figsize=(10, 10))
    #
    # ax.bar(x_axis - 0.2, category_male, width=0.4, label='Males', color='blue')
    # ax.bar(x_axis + 0.2, category_female, width=0.4, label="Females", color='crimson')
    #
    # # set tick labels and their location
    # ax.set_xticks(x_axis, category_male_keys)
    # # ax.set_xticklabels(category_male_keys)
    #
    # ax.set_xlabel('Category', fontsize=14)
    # ax.set_ylabel('Nobel Laureates Count', fontsize=14)
    # ax.set_title('The total count of male and female Nobel Prize winners by categories', fontsize=20)
    #
    # ax.legend()
    #
    # plt.show()

    # Ensure consistent category names
    categories = ['Chemistry', 'Economics', 'Literature', 'Peace', 'Physics', 'Physiology or Medicine',
                  'All categories']

    # Handle NaN values if necessary
    data = [df[df['category'] == cat]['age_of_winning'].dropna() for cat in categories]
    all_categories = df['age_of_winning'].dropna()
    data.append(all_categories)

    fig, ax = plt.subplots(figsize=(10, 10))

    # Use consistent category names in labels
    labels = categories + ['All categories']

    # Use ax.boxplot instead of plt.boxplot
    ax.boxplot(data, labels=labels, showmeans=True)

    ax.set_ylabel('Age of Obtaining the Nobel Prize', fontsize=14)
    ax.set_xlabel('Category', fontsize=14)
    ax.set_title('Distribution of Ages by Category', fontsize=20)

    plt.show()
