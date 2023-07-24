import numpy as np
import pandas as pd
import json


def find_warehouse_rates(orders):
    warehouse_rates = pd.DataFrame(
        {'warehouse': orders['warehouse_name'].unique(), 'rate': np.nan})
    orders_grouped = orders.groupby(['order_id', 'warehouse_name', 'highway_cost'], as_index=False)['quantity'].sum()
    for wh in warehouse_rates['warehouse']:
        wh_n = orders_grouped[orders_grouped['warehouse_name'] == wh]
        warehouse_rates.loc[warehouse_rates['warehouse'] == wh, 'rate'] = wh_n.highway_cost.iloc[0] / wh_n.quantity.iloc[0]
    return warehouse_rates


def main():
    with open('data.json', encoding='utf-8') as f:
        data = json.load(f)
        orders = pd.json_normalize(data,
                                record_path=['products'],
                                meta=['order_id', 'warehouse_name',
                                        'highway_cost'])
        orders = orders.reindex(columns=['order_id', 'warehouse_name',
                                        'highway_cost', 'product','price',
                                        'quantity'])
    # Task 1
    wh_rates = find_warehouse_rates(orders)
    print(wh_rates)
    

if __name__ == '__main__':
    main()
