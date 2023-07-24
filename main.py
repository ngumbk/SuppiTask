import pandas as pd
import json

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)
    orders = pd.json_normalize(data,
                               record_path=['products'],
                               meta=['order_id', 'warehouse_name',
                                     'highway_cost'])
    orders = orders.reindex(columns=['order_id', 'warehouse_name',
                                     'highway_cost', 'product','price',
                                     'quantity'])
    