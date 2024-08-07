import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    file = 'bakerysales.csv'
    df = pd.read_csv(file)
    # copy the rename step from the note book here
    df.rename(columns={'Unnamed: 0': 'id', 
           'article': 'product', 
           'Quantity': 'quantity'},
           inplace=True)
    # copy the cleaning steps from the note book here
    df.unit_price = df.unit_price.str.replace(',', '.').str.replace('€', '').str.strip()
    # copy the conversion step from the note book here
    df.unit_price = df.unit_price.astype('float')
    # calculate sales. (This create a new sales column)
    df['sales'] = df.quantity * df.unit_price
    # drop columns with zero(0) sales
    df.drop(df[df.sales == 0].index, inplace=True)
    # convert date column to date format
    df['date'] = pd.to_datetime(df.date)
    return df

# load the data
df = load_data()

# app title
st.title('Bakery Sales App')
# display the table
st.dataframe(df.head(50))

# select and display specific products
# add filters
products = df['product'].unique()
selected_product = st.sidebar.multiselect(
                    'Choose Product',
                    products,
                    [products[0],
                    products[2]
                    ])
filtered_table = df[df['product'].isin(selected_product)]

# display some metrics
# total_sales = 0
if len(filtered_table) > 0:
    total_sales = filtered_table['sales'].sum()
else:
    total_sales = df.sales.sum()

if len(filtered_table) > 0:
    total_qty = filtered_table['quantity'].sum()
else:
    total_qty = df.quantity.sum()

if len(filtered_table) > 0:
    total_no_transactions = filtered_table['id'].count()
else:
    total_no_transactions = df.id.count()


corr = df['unit_price'].corr(df['sales']) # New Additions
top_tickets = df['ticket_number'].value_counts()
top_tickets2 = top_tickets.head(1)
avg_price_per_prdt = df.groupby('product')['unit_price'].mean()
avg_price_per_prdt2 = avg_price_per_prdt.sort_values(ascending=False).head(1)

st.divider()
st.subheader('Calculations') # This gives a subheading
col1, col2, col3 = st.columns(3) # display each metrics in a column format

col1.metric('No of Transactions',total_no_transactions)
col2.metric('Total Quantity',total_qty)
col3.metric('Total Sales',total_sales)
# end of metrics 1

st.divider()

# start of metrics 2
colA, colB, colC = st.columns(3)

colA.metric('Unit Price & Sales Correlation',corr)
colB.metric('Top Value',avg_price_per_prdt2)
colC.metric('Top Ticket',top_tickets2)

st.divider()
# end of metrics 2

# display the filtered table
st.dataframe(filtered_table[['date','product',
                             'quantity','unit_price',
                             'sales']])

# bar chat

try:
    st.write('## Total sales of selected products')
    bar1 = filtered_table.groupby(['product'])['sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1)
except ValueError as e:
    st.error(
        """Error""" % e.reason
    )

# Sales Analysis
try:
    st.write('Total Daily Sales') # gives the graph a title
    if len(filtered_table) > 0:
        daily_sales = filtered_table.groupby('date')['sales'].sum()
    else:
        daily_sales = df.groupby('date')['sales'].sum()

    daily_sales_df = daily_sales.reset_index().rename(columns={'sales': 'total sales'})
   #ax = daily_sales_df.plot.area(x = 'date',
   #                             y = 'total sales')
    st.area_chart(daily_sales_df,
                  x = 'date',
                  y = 'total sales')
except ValueError as e:
    st.error(
        """Error""" % e.reason
    )

# Quantity Analysis
try:
    st.write('Total Daily Quantity') # gives the graph a title
    if len(filtered_table) > 0:
        daily_qty_sold = filtered_table.groupby('date')['quantity'].sum() # calculate total daily quantity sold
    else:
        daily_qty_sold = df.groupby('date')['quantity'].sum() # calculate total daily quantity sold
    daily_qty_sold_df = daily_qty_sold.reset_index().rename(columns={'quantity':'total qty'}) # Create a table
    my_plot2 = st.line_chart(daily_qty_sold_df,
                     x = 'date',
                    y = 'total qty') # plots a line chart
except ValueError as e:
    st.error(
        """Error""" % e.reason
        )



