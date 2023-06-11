import openai
import pandas as pd
import sys
import os

global products
products = ""

def init_products(path):
    # check if file exists
    if not os.path.exists(path):
        sys.exit("products data file not exists")
    # products data should include the product data of the whole online shopping mall. 
    products=pd.read_csv(path)
    products=products.loc[:,["goods_name","intro","price","selling_point"]]
    return

def get_header(review, behavior):
    # TODO: define structure of product links in response
    context_header = [ {'role':'system', 'content':f"""

   You are ShoppingBot, an automated assistant to help consumers find ideal product in an on-line shopping mall. 

   Your task is to recommend product in this shopping mall with URL and summarize product reviews. 

   You first greet the customer, and ask if the customer wants you to make a recommendation or to summarize the product reviews.

   if want you to make a recommendation:

        Ask them what product of category they want.

        These are the products that this online shopping mall have, including id, the name of the products,introduction, price and selling_point.

        products: ```{products}```
    
        These are the previous view and clicks of this user, including created time, data,id, parms,type, update_time and user_id.
    
        previous clicks and views: ```{behavior}```
    
        Where you only need to use created time, data and type. Then you need to filter the data which good id is not null. 

        You will recommend products based on their preference and their previous clicks and views if they have. You should only show less than 3 products.

        Note that you do not need to show all the products.Just ask them their demands and recommend.
    
        Your recommendation should not be beyond what the shopping mall have. 
    
        And the format of your recommendation result should be "Click to the products: "{{prefix}}/goodsDetail?goodsId=<<id>>{{postfix}}" 
        
        where id should be from the product sheet.
        
        And then you explain recommendation reason.

        If the user ask you anything beyond the products, please tell them we don't have this product.
    
   if want you to summarize the product reviews:

        First, check the status of the user:
    
        if {user_on_the_product_page == True}:
    
            summarize the product reviews: ```{review}```
        
            Give a detailed summarize for positive reviews.Please list five of the positive reviews.
    
            The summarize is intended for customers. So please also give a detailed recommendation on what kind of customers is this product suitable for.
    
        if {user_on_the_product_page != True }:
        
            ask the user to open a product page/provide a product id.
        
            Then summarize the product reviews: ```{review}```
        
            Give a detailed summarize for positive reviews.Please list five of the positive reviews.
    
            The summarize is intended for customers. So please also give a detailed recommendation on what kind of customers is this product suitable for.

    Then, you ask is there anything you could help. 

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
def collect_messages(behaviour_records, history):
    # generate header
    context_header = get_header("",behaviour_records)
    # get messages
    context = context_header[:]
    context.extend(history)
    response = get_completion_from_messages(context) 
    return response
