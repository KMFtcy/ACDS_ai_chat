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
    products=pd.read_csv(path,sep = '\t')
    products=products.loc[:,["id","goods_name","intro","price","selling_point", "sku_id"]]
    # add recommend link
    products["recommend_link"] = ""
    for index, row in products.iterrows():
        products.at[index, 'recommend_link'] = "http://106.52.209.141:18081/goodsDetail?goodsId="+ row ["id"]+"&defaultSkuId=" + str(row["sku_id"])
    return

def get_header(behavior):
    global products
    context_header = [ {'role':'system', 'content':f"""
You are ShoppingBot, an automated assistant to help consumers read reviews in the shopping process. 
You should first greet the consumers and ask them whether they want you to summarize reviews or want to ask you some questions about the reviews.
    """} ]  # accumulate messages
    return context_header

def get_completion_from_messages(messages, model="gpt-3.5-turbo-16k", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

# history: [{'role':'string', 'content':"string"}]
# response: "string"
def collect_messages( description, reviews, behaviour_records, history, isUserReadDetail=False):
    # generate header
    context_header = get_header(behaviour_records)
    # get messages
    context = context_header[:]
    context.extend(history)
    # if user is locate in product detail page, add reviews to chat
    if isUserReadDetail:
        review_chat = {'role':'system', 'content':f"""
        First, determine whether the question of users belongs to the recommendation category or reviews-related category:
        1. if users want you to recommend a product,you should base on the following product lists that our shopping mall have: 
        product lists:```{products}```
        Give users three products and the links of the products. You can find the links in the product list data. 
        If the products we have don't satisfy consumers' requirements, or users ask for products we don't have, tell them we don't have the products until now.
        You should not give any links or information from external information.
        2. if users want you to summarize the product reviews or ask you questions about reviews, you should do so based on the following information:
        product information: ```{description}```
        product reviews: ```{reviews}```
        if you need to summarize reviews, you should give a brief summary based on the reviews. You first tell them the average rating in product information data, and then summarize the reviews. The summary should be organic and honestly reflect what consumers think about it. 
        Your summary should be consistent with the content and emotional directions of the reviews. Don't make things up.
        Your summary and answer should not exceed 50 words. Avoid repetition of "As an AI-based assistant/language model","I don't have real-time reviews".
        """}
        context.insert(-1,review_chat)
    response = get_completion_from_messages(context) 
    return response
