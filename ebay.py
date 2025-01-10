import requests
import pandas as pd
import xml.etree.ElementTree as ET
import re
import time
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os
dir = os.path.dirname(os.path.abspath(__file__))


def request(page):
    data = ""
    url = "https://svcs.ebay.com/services/search/FindingService/v1"
    head = {
        "X-EBAY-SOA-SECURITY-APPNAME": "NoahEise-MyKeySet-PRD-3fa6592a8-f4dd5c0b",
        "X-EBAY-SOA-OPERATION-NAME": "findItemsByKeywords", 
        "X-EBAY-SOA-REQUEST-DATA-FORMAT": "XML",
        "Content-Type": "text/xml"
    }
    
    xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
    <findItemsByKeywordsRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
      <keywords>Michael Jordan Fleer 1986</keywords>
      <paginationInput>
        <entriesPerPage>100</entriesPerPage>
        <pageNumber>{page}</pageNumber>
      </paginationInput>
    </findItemsByKeywordsRequest>"""
    
    
    response = requests.post(url, headers=head, data = xml_data)
    
    if response.status_code == 200:
        data = response.text
        return data
    else:
        print(f"Error: {response.status_code}")
        print(f"Error: {response.text}")

def parse(data): 
    root = ET.fromstring(data)
    ns = {'': 'http://www.ebay.com/marketplace/search/v1/services'}
    items = []
    for item in root.findall(".//searchResult/item", ns):
        item_d = {
            "title": item.find('title', ns).text if item.find('title', ns) is not None else None,
            "price": item.find('.//currentPrice', ns).text if item.find('.//currentPrice', ns) is not None else None,
            "url": item.find('viewItemURL', ns).text if item.find('viewItemURL', ns) is not None else None,
            "item_id": item.find('itemId', ns).text if item.find('itemId', ns) is not None else None,
            "bid_count": item.find('bidCount', ns).text if item.find('bidCount', ns) is not None else None,
            "location": item.find('location', ns).text if item.find('location', ns) is not None else None,
            "condition": item.find('condition/conditionDisplayName', ns).text if item.find('condition/conditionDisplayName', ns) is not None else None,
            "start_time": item.find('.//startTime', ns).text[0:10] if item.find('.//startTime', ns) is not None else None,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "sold_amount": item.find('.//sellingStatus/currentPrice', ns).text if item.find('.//sellingStatus/currentPrice', ns) is not None else None,
            "date_sold": item.find('.//sellingStatus/sellingState', ns).text if item.find('.//sellingStatus/sellingState', ns) is not None else None
        }
        items.append(item_d)
    return(items)

def wrangle(items):
    df = pd.DataFrame(items)
    def psa(title):
        return re.findall(r"(BGS|PSA)\s?(\d+)", title)
    df["rating"] = df["title"].apply(psa)
    df = df[df["condition"] == "Graded"]
    df = df[df["rating"].apply(len)>0]
    df["rating"] = df["rating"].apply(lambda x: x[0][1])
    return(df)
df = None

def get_cards():
    df = None
    for page in range(1, 11):
        data = request(page)
        items = parse(data)
        if df is None:
            df = wrangle(items)
        else:
            df = pd.concat([df, wrangle(items)], ignore_index=True)
    date = datetime.now().strftime('%Y-%m-%d')
    df.to_csv(f"{dir}/cards/mj-{date}.csv")
    
def run():
    get_cards()
    date = datetime.now().strftime('%Y-%m-%d')
    old = pd.read_csv(f"{dir}/mj.csv")
    new = pd.read_csv(f"{dir}/cards/mj-{date}.csv")
    old_m = old[["item_id", "date", "rating", "start_time", "price"]]
    new_m = new[["item_id", "date", "price"]]
    full = old_m.merge(new_m, on="item_id", how="inner", suffixes=('_old', '_new'))
    changes = full[full["price_old"] != full["price_new"]]
    price_melt = pd.melt(
        changes,
        id_vars=['item_id', 'rating', 'start_time'], 
        value_vars=['price_old', 'price_new'],         
        var_name='price_type',                        
        value_name='price')
    
    date_melt = pd.melt(
        changes,
        id_vars=['item_id', 'rating', 'start_time'], 
        value_vars=['date_old', 'date_new'],            
        var_name='date_type',                        
        value_name='date')
    
    changes = pd.concat([price_melt.drop(columns='price_type'), date_melt['date']], axis=1)
    changes = changes.drop_duplicates()
    changes_2 = changes.groupby(["item_id", "date"]).sum()
    conc = pd.concat([old, new])
    no_change = conc[~conc["item_id"].isin(changes_2.index.get_level_values(0))]
    change = conc[conc["item_id"].isin(changes_2.index.get_level_values(0))]
    no_change = no_change[no_change["date"] == date]
    mj = pd.concat([change, no_change]).drop("Unnamed: 0", axis=1)
    mj = mj.drop_duplicates()
    mj.to_csv(f"{dir}/mj.csv")
    changes.to_csv(f"{dir}/changes.csv")
    changes_2.to_csv(f"{dir}/changes2.csv")
    print(f"Done: {date}")

run()



