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
        1. if users want you to recommend a product,you should base on the following product lists that our shopping mall have: 
        product lists:```goods_name	price
Vic Firth DB22 Isolation Headphones for Hearing Protection	33
beyerdynamic DT 770 PRO 250 Ohm Studio Headphone	169
Sentry Micro Noise Reduction In-Ear Headphones Color Varies - Sentry HO229	25
Bose TriPort In-Ear Headphones - Headphones ( ear-bud ) – black	169
beyerdynamic DT 990 PRO Over-Ear Studio Headphones in black. Open construction, wired	169
Jabra GN9125 Mono Flex-Boom Wireless Headset for Deskphone	150
Klipsch Image S4i In-Ear Headset with Mic and 3-Button Remote Headphones – White	79
Diddybeats by Dr. Dre Pink In-Ear Headphone from Monster (Discontinued by Manufacturer)	72
Etymotic Research MC5 Noise-Isolating In-Ear Earphones	67
Sennheiser HDR 170 Headphone Receiver	134
iFrogz 7067-ERMN EarPollution Ronin Headphones, Midnight (Discontinued by Manufacturer)	40
Rocketfish RF-RBWHP01 Rocketboost Wireless Stereo Headphones	90
Monster NTUNE On-Ear Headphones, Red	119
Philips O'Neill SHO9560BK/28 Over-Ear Headphones - Black (Discontinued by Manufacturer)	50
Yurbuds Personalized Series Earphone / Earbuds Combo	80
Scosche RH1056M Over-The-Ear Headphones (White)	51
Blue Tiger Pro Wireless Bluetooth Headphones &ndash; Includes Mic &ndash; Black	160
Sony XBA-1IP - 1 Driver Balanced Armature Headset for Apple	80
PlayStation Vita In-ear Headset	45
Skullcandy Hesh (Discontinued by Manufacturer)	70
Nokia Purity Stereo In-Ear Headphones -Magenta (Discontinued by Manufacturer)	40
Yurbuds Ironman Inspire PRO 3 Button Control and Mic Sport Earbuds, White	60
Yurbuds Ironman Inspire Talk Earbuds with 1-Button Microphone (Black)	30
Velodyne vFree Bluetooth Wireless Stereo Headphone with Built-in Mic for Apple iPhone iPad and Android Devices (Gloss Black)	75
iFrogz IF-COD-NBLU Coda Headphones with Mic, Neon Blue	25
RoadKing RK100 Wired Hands Free Noise Cancelling Headset	29
ASA HS-1A Headset	144
Jabra REVO Corded Stereo Headphones - Retail Packaging - White (Discontinued by Manufacturer)	65
Bravo View IH-09AB - KID FRIENDLY Automotive IR Wireless Headphones (Dual Source)	30
Eskuche 101512C2BLU Control v2 On-Ear Headphones, Blue	28
Motorola S11 HD Wireless Stereo Headphones - Retail Packaging – Black	40
Frends Ella B Earbuds Headphones in Gold and White (Non-retail Packaging)	190
Yurbuds Inspire Talk (Aqua)	34
Yurbuds Inspire Talk Purple	30
Monster DNA On-Ear Headphones (Black Carbon Fiber)	100
Shure SE535LTD Limited Edition Red Sound Isolating Earphones with Remote (Old Model) + Microphone	99
Arm Pocket Yurbuds Signature Series Pete Jacobs Plus Reflective Cloth Cords Sport Earbuds	49
Plantronics Backbeat Go 2/R Headset, Black (88600-01)	45
Gioteck Ex-05S Universal Wired Stereo Headset	86
Yurbuds Focus LE Limited Edition Wireless Behind The Ear BT Headphones, Black	58
Adventure Time Ear buds Beemo	30
Nakamichi Over the Ear Headphone - Retail Packaging - Gray with Blue Thread	30
GOgroove Wireless Over-the-Ear Bluetooth Headphones with Mic & 14-Hour Battery Life - Works With Apple iPhone 6 Plus, Samsung Galaxy S6 Edge, LG G4 and Many Other Bluetooth-Enabled Smartphones	60
Fhgkjy Headphone Jack Adapter Headset Audio Adaptor Connector Earphone Jack AUX Audio Adapter Splitter Dongle Audio Accessorie	40
Yurbuds Explore Talk Gray/Orange Running Headphones	30
Arm Pocket Yurbuds Adventure Line Venture Duro Sport Earbuds	40
Sena 3S Bluetooth Headset and Intercom Wired Boom Microphone Kit (3S-WB)	100
Beyerdynamic DX160IE Premium In-Ear Headphones (Black)	78
B&O PLAY by Bang & Olufsen 1641325 Beoplay Form 2i On-Ear Headphone (White)	66
Jabra ROX Wireless Bluetooth Stereo Earbuds (Black)	26
SMS Audio STREET by 50 First Edition Star Wars On Ear Headphones Stormtrooper	200
Skdy Inkd Mic Greeney/Lime	25
Heavy-Duty Kids' Headphone w/Tangle-Free Fabric Cord (Pack of 10)	108
Skullcandy Unisex Uprock Mic'd Gray/Cyan/Black	30
Sony MDRZX750BN Bluetooth and Noise Cancelling Headset	90
Sennheiser HD 280 Pro headband pad Genuine HD280 headphones cushion replacement padding	28
Samsung Level In-Ear Headphone - Retail Packaging – White	50
Harman International In Ear Sport Headphone Grn JBLREFLECTIGRN	26
Bose SoundSport In-Ear Headphones for iOS Models, Orange	160
Plantronics BackBeat PRO Wireless Noise Canceling Hi-Fi Headphones with Mic - Compatible with iPhone, iPad, Android, and Other Smart Devices	40
Insignia Wireless Over-the-Ear Headphone	181
Sharper Image SBT517BKBK Bluetooth Earbuds with Microphone, Tangle Free Flat Cable, Noise Isolating, Black	25
Sony MDRXB450AP Extra Bass Smartphone Headset (Black)	60
Skullcandy Hesh 2 Bluetooth Wireless Over-Ear Headphones with Microphone, Supreme Sound and Powerful Bass, 15-Hour Rechargeable Battery, Soft Synthetic Leather Ear Cushions, Black	46
Modal Over-The-Ear Bluetooth Headphones With Built-In Mic HPBT101-BL	48
B&O PLAY by Bang & Olufsen Beoplay H2 On-Ear Headphone with Microphone (Carbon Blue)	184
Plantronics BackBeat FIT Wireless Bluetooth Headphones - Waterproof Earbuds for Running and Workout, Green, Frustration Free Packaging	70
Sena (SMH5-UNIV) Bluetooth Headset and Intercom for Scooters/Motorcycles with Universal Microphone Kit	93
Sony MDRAS600BT Active Sports Bluetooth Headset (Orange)	70
SkullCandy Uproar Onear Wireless Headphones One Size Black/Gray/Black	35
Philips SHB6250/27 Wireless Bluetooth Headphones, Black	26
Bose QuietComfort 15 Acoustic Noise Cancelling Headphones	105
Skullcandy XTFree Bluetooth Wireless Sweat-Resistant Earbud with Microphone, Lightweight and Secure Fit, 6-Hour Rechargeable Battery, Pureclean Tech to Keep Earbuds Fresh, Black/Swirl	52
Jaybird X2 Wireless Sweat-Proof Micro-Sized Bluetooth Sport Headphones &ndash; Charge	70
Jabra Eclipse Bluetooth Headset (U.S. Retail Packaging)	48
Sentry Industries BT300 Bluetooth Stereo Headphones with Mic, Black	25
Plantronics BackBeat PRO+ Wireless Noise Canceling Hi-Fi Headphones	40
JBL Reflect Mini Bluetooth in-Ear Sport Headphones	80
Jabra Sport Pace Wireless Bluetooth Earbuds - U.S. Retail Packaging	80
Samsung Level U Pro Bluetooth Wireless In-ear Headphones with Microphone and UHQ Audio, Bronze	49
Wireless Earbuds Upgraded Graphene 3D Stereo Sound Bluetooth 5.0 with 28Hr Play Time Noise Cancelling HonShoop Lightweight Bluetooth Headphones Built-in Mic	40
MEE audio EP-X7Plus-BK-MEE Stereo Bluetooth Wireless Sports in-Ear HD Headphones	60
Sport Headphones , AKEDRE&reg; Wireless Sports Bluetooth V4.1 Headphones Sweatproof Running Exercise Stereo with Mic Earbuds Earphones for Iphone 6/6s Plus Galaxy S6 and Android Phones (Gold)	35
MOXYO - Mission Earbuds, Clean Inline Mic and a Tangle-Free Flat Cable (Black)	30
JBL Reflect Response in-Ear Bluetooth Sport Headphones	90
Egghead EGG-IAG-1004-SO 10-Position Stereo Jack Box	95
DRUnKQUEEn Bluetooth Headphones, Bluetooth Headset, V4.1+EDR Noise Cancelling Hi-Fi Foldable Built in Microphone Super Extra Bass Stereo Wireless Over Ear Earphone, Support SD Card FM Radio	40
Audio Technica ATH-M50X Professional Studio Headphones (Black) with FiiO A3 Portable Headphone Amplifier (Black)	149
Wireless Headphones, Megadream Wireless Stereo Sport BT Headset Neckband Retractable Earbuds w/Mic for Running Gym Yoga Exercise iPhone Samsung (Gold)	21
House of Marley EM-JE041-SB Smile Jamaica In-Ear Headphones, Signature Black OPEN BOX	25
```
        If users want you to help them find a product, give users one product. 
        For example:" Yes, our shopping mall has the products you want. One option could be Vic Firth DB22 Isolation Headphones for Hearing Protection." 
        If the products we have don't satisfy consumers' requirements, or users ask for products we don't have, tell them we only have the products now.
        For example:" Sorry, our shopping mall does not have the product you want now. But you could view for other products."
        You should not give any links or information from external information.
        2. if users want you to summarize the product reviews or ask you questions about reviews, you should do so based on the following information:
        product information: ```{description}```
        product reviews: ```{reviews}```
        if you need to summarize reviews, you should give a brief summary based on the reviews. You should include the average rating of the comments at the beginning of your summary. 
        For example: "Based on the reviews, the Sennheiser HD 700 headphones have an average rating of 4.55 out of 5. Users praise the exceptional sound quality, comfort, and wide soundstage. Some mention that they are a worthwhile upgrade from previous models. However, a few users have experienced issues with durability and find the treble to be too sharp."/
        The summary should be organic and honestly reflect what consumers think about it. 
        Your summary should be consistent with the content and emotional directions of the reviews. Don't make things up.
        Your summary and answer should not exceed 50 words. Avoid repetition of "As an AI-based assistant/language model","I don't have real-time reviews".
        """}
        context.insert(-1,review_chat)
    response = get_completion_from_messages(context) 
    return response
