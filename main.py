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


# Task 3 function
def make_orders_stat(orders, warehouse_rates):
    orders = orders.copy()
    orders['cost'] = orders.price * orders.quantity
    res_df = orders.groupby('order_id', as_index=False)['cost'].sum()
    df_expenses = orders.groupby('order_id', as_index=False)['highway_cost'].first()
    
    res_df['order_profit'] = res_df.cost + df_expenses.highway_cost
    res_df = res_df.drop(['cost'], axis=1)
    return res_df


# Task 4 function
def find_warehouse_percent(orders, warehouse_rates):
    # Формируем исходный df
    orders = orders.copy()
    res_df = orders.loc[:, ['warehouse_name', 'product', 'quantity']]
    
    # Считаем прибыль для каждого товара
    res_df = res_df.merge(warehouse_rates, on='warehouse_name')
    res_df['profit'] = orders.price * orders.quantity + orders.quantity * res_df.rate
    
    # Считаем процент прибыли товаров от общей прибыли товаров склада
    warehouse_profit_series = res_df.groupby(['warehouse_name'], as_index=False)['profit'].sum()
    res_df = res_df.merge(warehouse_profit_series, on='warehouse_name')
    res_df = res_df.rename(columns={'profit_x': 'profit', 'profit_y': 'warehouse_profit'})
    res_df['percent_profit_product_of_warehouse'] = res_df.profit / res_df.warehouse_profit * 100
    
    # Убираем все дубликаты товаров
    res_df = res_df.drop(['rate', 'warehouse_profit'], axis=1)
    res_df = res_df.groupby(['warehouse_name', 'product'], as_index=False).sum()
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
    
    # Task 3
    orders_stat = make_orders_stat(orders, warehouse_rates)
    print('Table 3:\n', orders_stat, end='\n\n')
    print('Средняя прибыль с заказа:', orders_stat.mean()[1], end='\n\n')

    # Task 4
    wh_percent = find_warehouse_percent(orders, warehouse_rates)
    print('Table 4:\n', wh_percent, end='\n\n')


if __name__ == '__main__':
    main()
