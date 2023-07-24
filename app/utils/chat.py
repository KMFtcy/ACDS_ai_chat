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
def collect_messages(reviews, behaviour_records, history, isUserReadDetail=False):
    # generate header
    context_header = get_header(behaviour_records)
    # get messages
    context = context_header[:]
    context.extend(history)
    # if user is locate in product detail page, add reviews to chat
    if isUserReadDetail:
        review_chat = {'role':'system', 'content':f"""
        if users want you to summarize the product reviews:
        product reviews: ```{reviews}```
        You should give a brief summary based on the reviews. The summary should be organic and honestly reflect what consumers think about it.
        The summary is intended for customers. So you should give a short recommendation on what kind of customers this product is suitable for. 
        The summary should not exceed 50 words.
        """}
        context.insert(-1,review_chat)
    response = get_completion_from_messages(context) 
    return response
