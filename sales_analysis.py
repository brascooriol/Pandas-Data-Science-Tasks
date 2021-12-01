import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]

path = r'SalesAnalysis/Output/output_data.csv' # use your path

all_data_frame=pd.read_csv(path,index_col=None,header=0)

#Clean the data
all_data_frame=all_data_frame.dropna(how='all')
all_data_frame=all_data_frame[all_data_frame['Order Date'].str[0:2] != 'Or']
all_data_frame['Quantity Ordered']=all_data_frame['Quantity Ordered'].astype('int32')
all_data_frame['Price Each']=all_data_frame['Price Each'].astype('float')




#Get the month
all_data_frame['month']=all_data_frame['Order Date'].str[0:2]
all_data_frame['month']=all_data_frame['month'].astype('int32')

#Get city colum
all_data_frame['City']=all_data_frame['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

#Get the sales value
all_data_frame['Sales']=all_data_frame['Quantity Ordered']*all_data_frame['Price Each']
month_sum=all_data_frame.groupby('month').sum()

#Get sales volume by city
sales_city=all_data_frame.groupby('City').sum()

#Convert datetime
all_data_frame['Order Date']=pd.to_datetime(all_data_frame['Order Date'],format='%m/%d/%y %H:%M')

#Sum the sales by hour of the day
def get_sales_by_hour():
    df = all_data_frame.groupby([all_data_frame['Order Date'].dt.hour,'City'])['Quantity Ordered'].sum().unstack().plot()
    hours=[hour for hour, df in all_data_frame.groupby(all_data_frame['Order Date'].dt.hour)]
    plt.xticks(hours)
    plt.grid()
    plt.show()

#Get products sold together
def get_products_sold_together():
    df=all_data_frame[all_data_frame['Order ID'].duplicated(keep=False)]

    df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
    df.drop_duplicates(subset=['Order ID'],inplace=True)

    df['Grouped']=df['Grouped'].apply(lambda x: x.split(','))
    product_lists=df['Grouped'].to_list()

    count=Counter()
    for sublist in product_lists:
        count.update(Counter(combinations(sublist,3)))


#Get the products sold the most
def get_products_sold():
    df = all_data_frame.groupby('Product')['Quantity Ordered'].sum()
    products=[product for product, df in all_data_frame.groupby('Product')]

    prices=all_data_frame.groupby('Product').mean()['Price Each']


    fig,ax1=plt.subplots()

    ax1.set_xlabel('Product')
    ax1.set_ylabel('Quantity')
    ax1.bar(products,df.values)
    ax1.set_xticklabels(products,rotation='vertical')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


    ax2.set_ylabel('Price')  # we already handled the x-label with ax1
    ax2.plot(products,prices,color='red')
    # ax2.tick_params(products,rotation='vertical')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.show()


# get_sales_by_hour()
get_products_sold()
print(all_data_frame.head())