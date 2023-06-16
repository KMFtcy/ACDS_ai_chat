import openai
import pandas as pd
import sys
import os

products = ""

def init_products(path):
    global products
    # check if file exists
    if not os.path.exists(path):
        sys.exit("products data file not exists")
    # products data should include the product data of the whole online shopping mall. 
    products=pd.read_csv(path)
    products=products.loc[:,["id","goods_name","intro","price","selling_point"]]
    return

def get_header(review, behavior, user_on_the_product_page):
    global products
    context_header = [ {'role':'system', 'content':f"""
You are ShoppingBot, an automated assistant to help consumers find ideal product in an on-line shopping mall. \

Your task is to recommend product in this shopping mall with URL and summarize product reviews. 

You first greet the customer, and ask if the customer wants you to make a recommendation or to summarize the product reviews.

if want you to make a recommendation:

    Ask them what product of category they want.
    
    These are the products that this online shopping mall have, including id, the name of the products,introduction, price and selling_point.
    products: ```{products}```
    These are the previous view and clicks of this user, including created time, data,id, parms,type, update_time and user_id.
    previous clicks and views: ```{behavior}```
    Where you only need to use created time, data and type. Then you need to filter the data which good id is not null. 

    You will recommend products based on their preference and their previous clicks and views if they have. You should only show 1 products.

    Note that you do not need to show all the products.Just ask them their demands and recommend.
    
    Your recommendation should not be beyond what the shopping mall have. 
    
    And the format of your recommendation result should be "Click to the products: (%prefix%)/goodsDetail?goodsId=<<id>>(%postfix%)" 
    You should not change anything in the format except substituting the id with id in the products data. You should not give links of external website, including Amazon,Taobao,etc.
    And the you explain recommendation reason.

    If the user ask you anything beyond the products, please tell them we don't have this product.
    
if want you to summarize the product reviews:
    
    if ```{user_on_the_product_page}``` is True: You should summarize the given product reviews:```{review}```. and give a brief summarize for positive reviews.
    The summary is intended for customers. So you should give a detailed recommendation on what kind of customers is this product suitable for. 
    The summary should not exceed 50 words.
    
    if ```{user_on_the_product_page}``` is False: you should apologize to user that user need to open a product page and then you could summarize product review for user.
    You should not ask users to provide product name or link, just ask them to open a product page.

Then, you ask is there anything you could help. 

Please limit every your reponses in 200 words.

    """} ]  # accumulate messages
    return context_header


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

# history: [{'role':'string', 'content':"string"}]
# response: "string"
def collect_messages(reviews, behaviour_records, history, isUserReadDetail=False):
    # generate header
    context_header = get_header(reviews,behaviour_records, isUserReadDetail)
    # get messages
    context = context_header[:]
    context.extend(history)
    response = get_completion_from_messages(context) 
    return response
