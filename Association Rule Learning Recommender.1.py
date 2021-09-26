

#SEPET AŞAMASINDA KULLANICILARA ÜRÜN ÖNERİSİNDE BULUNMAK(Association Rule Learning Recommender)



import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.width',500)
from mlxtend.frequent_patterns import apriori,association_rules




def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


def retail_data_prep(dataframe):
    dataframe.drop(dataframe[dataframe["StockCode"]=="POST"].index, inplace=True)
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe

#VERİ ÖN İŞLEME

df_=pd.read_excel("/Users/dilanicer/Desktop/DSMLBC-çalışmalar/datasets/online_retail_II.xlsx",sheet_name="Year 2010-2011")
df = df_.copy()
df = retail_data_prep(df)

#GERMANY MÜŞTERİLERİ ÜZERİNDEN BİRLİKTELİK KURALLARI
#Alman müşterilerin seçilmesi:

df=df[df['Country']=="Germany"]
df.head(30)




df.groupby(['Invoice', 'Description']).agg({"Quantity":"sum"}).head(10)
df.groupby(['Invoice', 'Description']).agg({"Quantity": "sum"}).unstack()
df.groupby(['Invoice', 'Description']).agg({"Quantity": "sum"}).unstack().fillna(0)
invoice_product_df = df.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0).applymap(lambda x: 1 if x > 0 else 0)

def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)


Invoice_product_df = create_invoice_product_df(df)

Invoice_product_df.head()
Invoice_product_df.head(30)

frequent_itemsets = apriori(invoice_product_df, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)

def create_rules(dataframe, id=True, country="Germany"):
    dataframe = dataframe[dataframe['Country'] == country]
    dataframe = create_invoice_product_df(dataframe, id)
    frequent_itemsets = apriori(dataframe, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
    return rules

rules_grm = create_rules(df, country="Germany")

#ID'LERİ VERİLEN ÜRÜNLERİN İSİLERİNİ BULALIM

def check_id(dataframe,stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

    check_id(df,21987)
    #['PACK OF 6 SKULL PAPER CUPS']

    check_id(df, 23235)
    #['STORAGE TIN VINTAGE LEAF']

    check_id(df, 22747)
    #["POPPY'S PLAYHOUSE BATHROOM"]

#SEPETTEKİ KULLANICILAR İÇİN ÜRÜN ÖNERİSİ YAPALIM

def arl_recommender(rules_df,product_id,rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in sorted_rules["antecedents"].items():
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"]))
    recommendation_list = list({item for item_list in recommendation_list for item in item_list})
    return recommendation_list[:rec_count]

arl_recommender(rules_grm, 21987, 1)
arl_recommender(rules_grm, 23235, 1)
arl_recommender(rules_grm, 22747, 1)

#ÖNERİLEN ÜRÜNLERİN İSMLERİNİ BULALIM
check_id(df, arl_recommender(rules_grm, 21987, 1)[0])
#['JUMBO BAG RED RETROSPOT']

check_id(df, arl_recommender(rules_grm, 23235, 1)[0])
#['JUMBO BAG RED RETROSPOT']

check_id(df, arl_recommender(rules_grm, 22747, 1)[0])
#['CHARLOTTE BAG APPLES DESIGN']
