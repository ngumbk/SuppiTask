import numpy as np
import pandas as pd
import json


# Task 1 function
def find_warehouse_rates(orders):
    warehouse_rates = pd.DataFrame(
        {'warehouse_name': orders['warehouse_name'].unique(), 'rate': np.nan})
    orders_grouped = orders.groupby(['order_id', 'warehouse_name', 'highway_cost'], as_index=False)['quantity'].sum()
    for wh in warehouse_rates['warehouse_name']:
        wh_n = orders_grouped[orders_grouped['warehouse_name'] == wh]
        warehouse_rates.loc[warehouse_rates['warehouse_name'] == wh, 'rate'] = wh_n.highway_cost.iloc[0] / wh_n.quantity.iloc[0]
    return warehouse_rates


# Task 2 function
def find_income_expenses_profit(orders, warehouse_rates):
    res_df = orders.groupby(['product', 'price'], as_index=False)['quantity'].sum()
    res_df['income'] = res_df.price * res_df.quantity
    
    orders_grouped = orders.groupby(['warehouse_name', 'product'], as_index=False)['quantity'].sum()
    merged_df = orders_grouped.merge(warehouse_rates, left_on='warehouse_name', right_on='warehouse_name', how='left')
    merged_df['expenses'] = merged_df.quantity * merged_df.rate
    res_df['expenses'] = merged_df.groupby('product', as_index=False)['expenses'].sum().loc[:, 'expenses']
    res_df['profit'] = res_df.income + res_df.expenses
    return res_df


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
    warehouse_rates = find_warehouse_rates(orders)
    print('Table 1:\n', warehouse_rates, end='\n\n')

    # Task 2
    iep = find_income_expenses_profit(orders, warehouse_rates)
    print('Table 2:\n', iep, end='\n\n')
    

if __name__ == '__main__':
    main()
