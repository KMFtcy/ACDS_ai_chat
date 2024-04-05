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
        First, determine whether the user query belongs to either (1) product recommendation/filtering or (2) product evaluation/inspection, as illustrated below. Then follow the guideline below to reply to the query:
1.	Product recommendation or filtering. If users ask you to recommend a product or help them find a product with certain attributes, you should base on the following product lists that our shopping mall has: 
        product lists:```good	price	rating
Vic Firth DB22 Isolation Headphones for Hearing Protection	32.95	4.27
beyerdynamic DT 990 PRO Over-Ear Studio Headphones in black. Open construction, wired	169	4.48
House of Marley EM-JE041-SB Smile Jamaica In-Ear Headphones, Signature Black OPEN BOX	24.99	4.72
beyerdynamic DT 770 PRO 250 Ohm Studio Headphone	169	4.45
Bose TriPort In-Ear Headphones - Headphones ( ear-bud ) - black	169	3.36
Jabra GN9125 Mono Flex-Boom Wireless Headset for Deskphone	149.95	3.87
Klipsch Image S4i In-Ear Headset with Mic and 3-Button Remote Headphones - White	78.87	3.93
Diddybeats by Dr. Dre Pink In-Ear Headphone from Monster (Discontinued by Manufacturer)	72.49	3.53
Etymotic Research MC5 Noise-Isolating In-Ear Earphones	67.49	3.6
Sennheiser HDR 170 Headphone Receiver	134	4.15
Wireless Earbuds Upgraded Graphene 3D Stereo Sound Bluetooth 5.0 with 28Hr Play Time Noise Cancelling HonShoop Lightweight Bluetooth Headphones Built-in Mic	39.99	4.93
Sony MDRZX750BN Bluetooth and Noise Cancelling Headset	89.99	3.83
Monster NTUNE On-Ear Headphones, Red	119	4.65
Philips O'Neill SHO9560BK/28 Over-Ear Headphones - Black (Discontinued by Manufacturer)	49.99	3.86
Yurbuds Personalized Series Earphone / Earbuds Combo.	79.99	4.11
Scosche RH1056M Over-The-Ear Headphones (White)	50.98	3.62
Blue Tiger Pro Wireless Bluetooth Headphones &ndash; Includes Mic &ndash; Black	159.99	3.74
Sony XBA-1IP - 1 Driver Balanced Armature Headset for Apple	79.56	3.47
PlayStation Vita In-ear Headset	44.98	4.33
Skullcandy Hesh (Discontinued by Manufacturer)	69.99	4.48
Fhgkjy Headphone Jack Adapter Headset Audio Adaptor Connector Earphone Jack AUX Audio Adapter Splitter Dongle Audio Accessorie	39.99	4.87
Sony MDRXB450AP Extra Bass Smartphone Headset (Black)	59.95	4.25
Adventure Time Ear buds Beemo	29.99	4.07
Velodyne vFree Bluetooth Wireless Stereo Headphone with Built-in Mic for Apple iPhone iPad and Android Devices (Gloss Black)	74.99	3.7
Skdy Inkd Mic Greeney/Lime	24.99	4.01
RoadKing RK100 Wired Hands Free Noise Cancelling Headset	29.16	3.19
ASA HS-1A Headset	144	4.03
Jabra REVO Corded Stereo Headphones - Retail Packaging - White (Discontinued by Manufacturer)	64.98	4.44
Bravo View IH-09AB - KID FRIENDLY Automotive IR Wireless Headphones (Dual Source)	29.99	4.03
Eskuche 101512C2BLU Control v2 On-Ear Headphones, Blue	28.43	4.06
Nokia Purity Stereo In-Ear Headphones -Magenta (Discontinued by Manufacturer)	39.99	3.95
Frends Ella B Earbuds Headphones in Gold and White (Non-retail Packaging)	189.99	3.4
Yurbuds Inspire Talk (Aqua)	33.99	4.26
MOXYO - Mission Earbuds, Clean Inline Mic and a Tangle-Free Flat Cable (Black)	29.99	4
Sena 3S Bluetooth Headset and Intercom Wired Boom Microphone Kit (3S-WB)	99.99	4.5
Shure SE535LTD Limited Edition Red Sound Isolating Earphones with Remote (Old Model) + Microphone	99	4.32
Arm Pocket Yurbuds Signature Series Pete Jacobs Plus Reflective Cloth Cords Sport Earbuds	49	3.19
Plantronics Backbeat Go 2/R Headset, Black (88600-01)	44.86	3.43
Gioteck Ex-05S Universal Wired Stereo Headset	85.7	3.42
Yurbuds Focus LE Limited Edition Wireless Behind The Ear BT Headphones, Black	57.99	3.24
Yurbuds Inspire Talk Purple	29.99	3.82
Nakamichi Over the Ear Headphone - Retail Packaging - Gray with Blue Thread	30	3.75
GOgroove Wireless Over-the-Ear Bluetooth Headphones with Mic &amp; 14-Hour Battery Life - Works With Apple iPhone 6 Plus, Samsung Galaxy S6 Edge, LG G4 and Many Other Bluetooth-Enabled Smartphones	59.99	4.31
Motorola S11 HD Wireless Stereo Headphones - Retail Packaging - Black	39.99	3.75
Skullcandy Unisex Uprock Mic'd Gray/Cyan/Black	29.99	3.76
Arm Pocket Yurbuds Adventure Line Venture Duro Sport Earbuds	39.95	2.94
Monster DNA On-Ear Headphones (Black Carbon Fiber)	99.99	4.38
Beyerdynamic DX160IE Premium In-Ear Headphones (Black)	78	3.31
B&amp;O PLAY by Bang &amp; Olufsen 1641325 Beoplay Form 2i On-Ear Headphone (White)	66.01	3.86
Jabra ROX Wireless Bluetooth Stereo Earbuds (Black)	25.99	2.97
SMS Audio STREET by 50 First Edition Star Wars On Ear Headphones Stormtrooper	199.5	4.41
Sentry Micro Noise Reduction In-Ear Headphones Color Varies - Sentry HO229	24.99	3.38
Heavy-Duty Kids' Headphone w/Tangle-Free Fabric Cord (Pack of 10)	108.49	3.89
Yurbuds Ironman Inspire Talk Earbuds with 1-Button Microphone (Black)	29.99	3.76
Rocketfish RF-RBWHP01 Rocketboost Wireless Stereo Headphones	89.99	3.59
Samsung Level In-Ear Headphone - Retail Packaging - White	49.99	3.27
Harman International In Ear Sport Headphone Grn JBLREFLECTIGRN	25.99	2.58
Bose SoundSport In-Ear Headphones for iOS Models, Orange	160	4.04
Plantronics BackBeat PRO Wireless Noise Canceling Hi-Fi Headphones with Mic - Compatible with iPhone, iPad, Android, and Other Smart Devices	39.94	4.14
Insignia Wireless Over-the-Ear Headphone	181.33	3.83
Sharper Image SBT517BKBK Bluetooth Earbuds with Microphone, Tangle Free Flat Cable, Noise Isolating, Black	24.97	2.95
Yurbuds Ironman Inspire PRO 3 Button Control and Mic Sport Earbuds, White	59.95	3.45
Skullcandy Hesh 2 Bluetooth Wireless Over-Ear Headphones with Microphone, Supreme Sound and Powerful Bass, 15-Hour Rechargeable Battery, Soft Synthetic Leather Ear Cushions, Black	45.99	4.16
Modal Over-The-Ear Bluetooth Headphones With Built-In Mic HPBT101-BL	47.99	2.65
B&amp;O PLAY by Bang &amp; Olufsen Beoplay H2 On-Ear Headphone with Microphone (Carbon Blue)	184	3.81
Plantronics BackBeat FIT Wireless Bluetooth Headphones - Waterproof Earbuds for Running and Workout, Green, Frustration Free Packaging	69.99	3.65
Sena (SMH5-UNIV) Bluetooth Headset and Intercom for Scooters/Motorcycles with Universal Microphone Kit	92.92	4.26
Sony MDRAS600BT Active Sports Bluetooth Headset (Orange)	69.95	3.5
SkullCandy Uproar Onear Wireless Headphones One Size Black/Gray/Black	34.99	4.21
Philips SHB6250/27 Wireless Bluetooth Headphones, Black	25.95	3.54
Bose QuietComfort 15 Acoustic Noise Cancelling Headphones	105	4.15
Skullcandy XTFree Bluetooth Wireless Sweat-Resistant Earbud with Microphone, Lightweight and Secure Fit, 6-Hour Rechargeable Battery, Pureclean Tech to Keep Earbuds Fresh, Black/Swirl	51.97	3.31
Jaybird X2 Wireless Sweat-Proof Micro-Sized Bluetooth Sport Headphones &ndash; Charge	69.99	3.21
Jabra Eclipse Bluetooth Headset (U.S. Retail Packaging)	47.62	2.97
Sentry Industries BT300 Bluetooth Stereo Headphones with Mic, Black	25.26	3.53
Plantronics BackBeat PRO+ Wireless Noise Canceling Hi-Fi Headphones	39.94	3.93
JBL Reflect Mini Bluetooth in-Ear Sport Headphones	79.99	3.26
Jabra Sport Pace Wireless Bluetooth Earbuds - U.S. Retail Packaging	79.99	2.76
Samsung Level U Pro Bluetooth Wireless In-ear Headphones with Microphone and UHQ Audio, Bronze	48.79	3.83
DRUnKQUEEn Bluetooth Headphones, Bluetooth Headset, V4.1+EDR Noise Cancelling Hi-Fi Foldable Built in Microphone Super Extra Bass Stereo Wireless Over Ear Earphone, Support SD Card FM Radio	39.99	3.69
MEE audio EP-X7Plus-BK-MEE Stereo Bluetooth Wireless Sports in-Ear HD Headphones	59.83	3.37
Sport Headphones, AKEDRE&reg; Wireless Sports Bluetooth V4.1 Headphones Sweatproof Running Exercise Stereo with Mic Earbuds Earphones for Iphone 6/6s Plus Galaxy S6 and Android Phones (Gold)	35.09	2.86
Yurbuds Explore Talk Gray/Orange Running Headphones	29.99	1.8
JBL Reflect Response in-Ear Bluetooth Sport Headphones	89.99	1.83
iFrogz 7067-ERMN EarPollution Ronin Headphones, Midnight (Discontinued by Manufacturer)	39.99	3.5
Audio Technica ATH-M50X Professional Studio Headphones (Black) with FiiO A3 Portable Headphone Amplifier (Black)	149	4.66
Wireless Headphones, Megadream Wireless Stereo Sport BT Headset Neckband Retractable Earbuds w/Mic for Running Gym Yoga Exercise iPhone Samsung (Gold)	20.99	3.4
iFrogz IF-COD-NBLU Coda Headphones with Mic, Neon Blue	24.99	3
```
         If there are multiple products that meet the requirements, then recommend the one with the highest rating. 
   For example:" Yes, our shopping mall has the products you want. One option could be Vic Firth DB22 Isolation Headphones for Hearing Protection. Of course, there are other good products that may fit your preference. “ 
   If the products we have do not satisfy the users’ requirements, or they ask for a product that the mall does not have, then tell them we do not have the product and encourage them to check other products in the mall.
   For example:" Sorry, our shopping mall does not have the product you want now. But you could check other products we have."
   You should not give any links or information from external sources that our shopping mall does not have.
2.	Product evaluation or inspection. If users ask you questions about the product or want you to summarize the product reviews, you should do so based on the following information:
        product description: ```{description}```
        product reviews: ```{reviews}```
       If users need you to summarize reviews or want to know what other customers think about the product, then give a summary based on the reviews. You should include the average rating of the comments at the beginning of your summary. 
   For example: "Based on the reviews, the Sennheiser HD 700 headphones have an average rating of 4.55 out of 5. Users praise the exceptional sound quality, comfort, and wide soundstage. Some mention that they are a worthwhile upgrade from previous models. However, a few users have experienced issues with durability and find the treble to be too sharp."
   The summary should be organic and honestly reflect what consumers think about it. 
   Your summary should be consistent with the content and overall sentiment of the reviews. Do not fabricate. If you cannot answer or do not have enough information, simply reply that our website or the assistant does not have that information.
   Your answer should not exceed 50 words. Avoid using the language of "As an AI-based assistant/language model, I can’t do/ I don’t have the capacity to do", "I don't have real-time reviews".
        """}
        context.insert(-1,review_chat)
    response = get_completion_from_messages(context) 
    return response
