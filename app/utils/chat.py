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
    products=pd.read_csv(path,sep = ',', encoding='utf-8')
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
        1. if users want you to recommend a product, you should base on the following product lists that our shopping mall has: 
        product lists:```goods_name	rating	price
Wireless Earbuds Upgraded Graphene 3D Stereo Sound Bluetooth 5.0 with 28Hr Play Time Noise Cancelling HonShoop Lightweight Bluetooth Headphones Built-in Mic	4.93 	39.99
Fhgkjy Headphone Jack Adapter Headset Audio Adaptor Connector Earphone Jack AUX Audio Adapter Splitter Dongle Audio Accessorie	4.87 	39.99
House of Marley EM-JE041-SB Smile Jamaica In-Ear Headphones, Signature Black OPEN BOX	4.72 	24.99
Audio Technica ATH-M50X Professional Studio Headphones (Black) with FiiO A3 Portable Headphone Amplifier (Black)	4.66 	149
Monster NTUNE On-Ear Headphones, Red	4.65 	119
Sena 3S Bluetooth Headset and Intercom Wired Boom Microphone Kit (3S-WB)	4.50 	99.99
beyerdynamic DT 990 PRO Over-Ear Studio Headphones in black. Open construction, wired	4.48 	169
Skullcandy Hesh (Discontinued by Manufacturer)	4.48 	69.99
beyerdynamic DT 770 PRO 250 Ohm Studio Headphone	4.45 	169
Jabra REVO Corded Stereo Headphones - Retail Packaging - White (Discontinued by Manufacturer)	4.44 	64.98
SMS Audio STREET by 50 First Edition Star Wars On Ear Headphones Stormtrooper	4.41 	199.5
Monster DNA On-Ear Headphones (Black Carbon Fiber)	4.38 	99.99
PlayStation Vita In-ear Headset	4.33 	44.98
Shure SE535LTD Limited Edition Red Sound Isolating Earphones with Remote (Old Model) + Microphone	4.32 	99
GOgroove Wireless Over-the-Ear Bluetooth Headphones with Mic &amp; 14-Hour Battery Life - Works With Apple iPhone 6 Plus, Samsung Galaxy S6 Edge, LG G4 and Many Other Bluetooth-Enabled Smartphones	4.31 	59.99
Vic Firth DB22 Isolation Headphones for Hearing Protection	4.27 	32.95
Sena (SMH5-UNIV) Bluetooth Headset and Intercom for Scooters/Motorcycles with Universal Microphone Kit	4.26 	92.92
Yurbuds Inspire Talk (Aqua)	4.26 	33.99
Sony MDRXB450AP Extra Bass Smartphone Headset (Black)	4.25 	59.95
SkullCandy Uproar Onear Wireless Headphones One Size Black/Gray/Black	4.21 	34.99
Skullcandy Hesh 2 Bluetooth Wireless Over-Ear Headphones with Microphone, Supreme Sound and Powerful Bass, 15-Hour Rechargeable Battery, Soft Synthetic Leather Ear Cushions, Black	4.16 	45.99
Bose QuietComfort 15 Acoustic Noise Cancelling Headphones	4.15 	105
Sennheiser HDR 170 Headphone Receiver	4.15 	134
Plantronics BackBeat PRO Wireless Noise Canceling Hi-Fi Headphones with Mic - Compatible with iPhone, iPad, Android, and Other Smart Devices	4.14 	39.94
Yurbuds Personalized Series Earphone / Earbuds Combo.	4.11 	79.99
Adventure Time Ear buds Beemo	4.07 	29.99
Eskuche 101512C2BLU Control v2 On-Ear Headphones, Blue	4.06 	28.43
Bose SoundSport In-Ear Headphones for iOS Models, Orange	4.04 	160
ASA HS-1A Headset	4.03 	144
Bravo View IH-09AB - KID FRIENDLY Automotive IR Wireless Headphones (Dual Source)	4.03 	29.99
Skdy Inkd Mic Greeney/Lime	4.01 	24.99
MOXYO - Mission Earbuds, Clean Inline Mic and a Tangle-Free Flat Cable (Black)	4.00 	29.99
Nokia Purity Stereo In-Ear Headphones -Magenta (Discontinued by Manufacturer)	3.95 	39.99
Plantronics BackBeat PRO+ Wireless Noise Canceling Hi-Fi Headphones	3.93 	39.94
Klipsch Image S4i In-Ear Headset with Mic and 3-Button Remote Headphones - White	3.93 	78.87
Heavy-Duty Kids' Headphone w/Tangle-Free Fabric Cord (Pack of 10)	3.89 	108.49
Jabra GN9125 Mono Flex-Boom Wireless Headset for Deskphone	3.87 	149.95
B&amp;O PLAY by Bang &amp; Olufsen 1641325 Beoplay Form 2i On-Ear Headphone (White)	3.86 	66.01
Philips O'Neill SHO9560BK/28 Over-Ear Headphones - Black (Discontinued by Manufacturer)	3.86 	49.99
Sony MDRZX750BN Bluetooth and Noise Cancelling Headset	3.83 	89.99
Samsung Level U Pro Bluetooth Wireless In-ear Headphones with Microphone and UHQ Audio, Bronze	3.83 	48.79
Insignia Wireless Over-the-Ear Headphone	3.83 	181.33
Yurbuds Inspire Talk Purple	3.82 	29.99
B&amp;O PLAY by Bang &amp; Olufsen Beoplay H2 On-Ear Headphone with Microphone (Carbon Blue)	3.81 	184
Skullcandy Unisex Uprock Mic'd Gray/Cyan/Black	3.76 	29.99
Yurbuds Ironman Inspire Talk Earbuds with 1-Button Microphone (Black)	3.76 	29.99
Motorola S11 HD Wireless Stereo Headphones - Retail Packaging - Black	3.75 	39.99
Nakamichi Over the Ear Headphone - Retail Packaging - Gray with Blue Thread	3.75 	30
Blue Tiger Pro Wireless Bluetooth Headphones &ndash; Includes Mic &ndash; Black	3.74 	159.99
Velodyne vFree Bluetooth Wireless Stereo Headphone with Built-in Mic for Apple iPhone iPad and Android Devices (Gloss Black)	3.70 	74.99
DRUnKQUEEn Bluetooth Headphones, Bluetooth Headset, V4.1+EDR Noise Cancelling Hi-Fi Foldable Built in Microphone Super Extra Bass Stereo Wireless Over Ear Earphone, Support SD Card FM Radio	3.69 	39.99
Plantronics BackBeat FIT Wireless Bluetooth Headphones - Waterproof Earbuds for Running and Workout, Green, Frustration Free Packaging	3.65 	69.99
Scosche RH1056M Over-The-Ear Headphones (White)	3.62 	50.98
Etymotic Research MC5 Noise-Isolating In-Ear Earphones	3.60 	67.49
Rocketfish RF-RBWHP01 Rocketboost Wireless Stereo Headphones	3.59 	89.99
Philips SHB6250/27 Wireless Bluetooth Headphones, Black	3.54 	25.95
Diddybeats by Dr. Dre Pink In-Ear Headphone from Monster (Discontinued by Manufacturer)	3.53 	72.49
Sentry Industries BT300 Bluetooth Stereo Headphones with Mic, Black	3.53 	25.26
Sony MDRAS600BT Active Sports Bluetooth Headset (Orange)	3.50 	69.95
iFrogz 7067-ERMN EarPollution Ronin Headphones, Midnight (Discontinued by Manufacturer)	3.50 	39.99
Sony XBA-1IP - 1 Driver Balanced Armature Headset for Apple	3.47 	79.56
Yurbuds Ironman Inspire PRO 3 Button Control and Mic Sport Earbuds, White	3.45 	59.95
Plantronics Backbeat Go 2/R Headset, Black (88600-01)	3.43 	44.86
Gioteck Ex-05S Universal Wired Stereo Headset	3.42 	85.7
Frends Ella B Earbuds Headphones in Gold and White (Non-retail Packaging)	3.40 	189.99
Wireless Headphones, Megadream Wireless Stereo Sport BT Headset Neckband Retractable Earbuds w/Mic for Running Gym Yoga Exercise iPhone Samsung (Gold)	3.40 	20.99
Sentry Micro Noise Reduction In-Ear Headphones Color Varies - Sentry HO229	3.38 	24.99
MEE audio EP-X7Plus-BK-MEE Stereo Bluetooth Wireless Sports in-Ear HD Headphones	3.37 	59.83
Bose TriPort In-Ear Headphones - Headphones ( ear-bud ) - black	3.36 	169
Skullcandy XTFree Bluetooth Wireless Sweat-Resistant Earbud with Microphone, Lightweight and Secure Fit, 6-Hour Rechargeable Battery, Pureclean Tech to Keep Earbuds Fresh, Black/Swirl	3.31 	51.97
Beyerdynamic DX160IE Premium In-Ear Headphones (Black)	3.31 	78
Samsung Level In-Ear Headphone - Retail Packaging - White	3.27 	49.99
JBL Reflect Mini Bluetooth in-Ear Sport Headphones	3.26 	79.99
Yurbuds Focus LE Limited Edition Wireless Behind The Ear BT Headphones, Black	3.24 	57.99
Jaybird X2 Wireless Sweat-Proof Micro-Sized Bluetooth Sport Headphones &ndash; Charge	3.21 	69.99
Arm Pocket Yurbuds Signature Series Pete Jacobs Plus Reflective Cloth Cords Sport Earbuds	3.19 	49
RoadKing RK100 Wired Hands Free Noise Cancelling Headset	3.19 	29.16
iFrogz IF-COD-NBLU Coda Headphones with Mic, Neon Blue	3.00 	24.99
Jabra Eclipse Bluetooth Headset (U.S. Retail Packaging)	2.97 	47.62
Jabra ROX Wireless Bluetooth Stereo Earbuds (Black)	2.97 	25.99
Sharper Image SBT517BKBK Bluetooth Earbuds with Microphone, Tangle Free Flat Cable, Noise Isolating, Black	2.95 	24.97
Arm Pocket Yurbuds Adventure Line Venture Duro Sport Earbuds	2.94 	39.95
Sport Headphones , AKEDRE&reg; Wireless Sports Bluetooth V4.1 Headphones Sweatproof Running Exercise Stereo with Mic Earbuds Earphones for Iphone 6/6s Plus Galaxy S6 and Android Phones (Gold)	2.86 	35.09
Jabra Sport Pace Wireless Bluetooth Earbuds - U.S. Retail Packaging	2.76 	79.99
Modal Over-The-Ear Bluetooth Headphones With Built-In Mic HPBT101-BL	2.65 	47.99
Harman International In Ear Sport Headphone Grn JBLREFLECTIGRN	2.58 	25.99
JBL Reflect Response in-Ear Bluetooth Sport Headphones	1.83 	89.99
Yurbuds Explore Talk Gray/Orange Running Headphones	1.80 	29.99
```
        If users want you to help them find a product, give them one product. If there are many products that meet their requirements, please give the one with the highest rating. 
        For example:" Yes, our shopping mall has the products you want. One option could be Vic Firth DB22 Isolation Headphones for Hearing Protection. Besides, there are also other good products to look for. " 
        If the products we have don't satisfy consumers' requirements, or users ask for products we don't have, tell them we only have the products now.
        For example:" Sorry, our shopping mall does not have the product you want now. But you could view for other products."
        You should not give any links or information from external information.
        2. if users want you to summarize the product reviews or ask you questions about reviews, you should do so based on the following information:
        product information: ```{description}```
        product reviews: ```{reviews}```
        if you need to summarize reviews, you should give a brief summary based on the reviews. You should include the average rating of the comments at the beginning of your summary. 
        For example: "Based on the reviews, the Sennheiser HD 700 headphones have an average rating of 4.55 out of 5. Users praise the exceptional sound quality, comfort, and wide soundstage. Some mention that they are a worthwhile upgrade from previous models. However, a few users have experienced issues with durability and find the treble to be too sharp."/
        The summary should be organic and honestly reflect what consumers think about it. 
        Your summary should be consistent with the content and emotional directions of the reviews. Don't make things up. If you cannot answer or do not have enough information, simply reply that our website or the assistant does not have that information.
        Your summary and answer should not exceed 50 words. Avoid repetition of "As an AI-based assistant/language model","I don't have real-time reviews".
        """}
        context.insert(-1,review_chat)
    response = get_completion_from_messages(context) 
    return response
