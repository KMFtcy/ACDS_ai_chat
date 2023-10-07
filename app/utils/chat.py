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
        product lists:```{id	goods_name	price	sku_id
B0002F513E	Vic Firth DB22 Isolation Headphones for Hearing Protection	32.95	1440957997408440000 
B0006NL5SM	beyerdynamic DT 770 PRO 250 Ohm Studio Headphone	169	1440957997408440000 
B000IWAP4G	Sentry Micro Noise Reduction In-Ear Headphones Color Varies - Sentry HO229	24.99	1440957997408440000 
B000KLZ7VG	Bose TriPort In-Ear Headphones - Headphones ( ear-bud ) - black	169	1440957997408440000 
B0011UB9CQ	beyerdynamic DT 990 PRO Over-Ear Studio Headphones in black. Open construction, wired	169	1440957997408440000 
B001G66TAM	Jabra GN9125 Mono Flex-Boom Wireless Headset for Deskphone	149.95	1440957997408440000 
B00365EB3I	Klipsch Image S4i In-Ear Headset with Mic and 3-Button Remote Headphones - White	78.87	1440957997408440000 
B003OGQ92K	Diddybeats by Dr. Dre Pink In-Ear Headphone from Monster (Discontinued by Manufacturer)	72.49	1440957997408440000 
B003S3RFIQ	Etymotic Research MC5 Noise-Isolating In-Ear Earphones	67.49	1440957997408440000 
B003ZL916U	Sennheiser HDR 170 Headphone Receiver	134	1440957997408440000 
B00404H6DQ	AIAIAI TMA-1 DJ Headphones without Mic, Black	200	1440957997408440000 
B0041E1QLI	iFrogz 7067-ERMN EarPollution Ronin Headphones, Midnight (Discontinued by Manufacturer)	39.99	1440957997408440000 
B004C04P46	Beyerdynamic T5p Tesla Audiophile Portable and Home Audio Stereo Headphone	749	1440957997408440000 
B004H1W1MS	Rocketfish RF-RBWHP01 Rocketboost Wireless Stereo Headphones	89.99	1440957997408440000 
B004SU1B2Y	Monster NTUNE On-Ear Headphones, Red	119	1440957997408440000 
B005626CMM	Philips O'Neill SHO9560BK/28 Over-Ear Headphones - Black (Discontinued by Manufacturer)	49.99	1440957997408440000 
B005F65D24	Yurbuds Personalized Series Earphone / Earbuds Combo.	79.99	1440957997408440000 
B005HIS6JC	Scosche RH1056M Over-The-Ear Headphones (White)	50.98	1440957997408440000 
B005RZUH9W	Blue Tiger Pro Wireless Bluetooth Headphones &ndash; Includes Mic &ndash; Black	159.99	1440957997408440000 
B006K556QM	Sony XBA-1IP - 1 Driver Balanced Armature Headset for Apple	79.56	1440957997408440000 
B006PP3ZK6	PlayStation Vita In-ear Headset	44.98	1440957997408440000 
B0070U8KSM	Sennheiser HD 700 Headphone (Jack plug 1/4 (6.3 mm) stereo)	455.02	1440957997408440000 
B0071369KE	Skullcandy Hesh (Discontinued by Manufacturer)	69.99	1440957997408440000 
B0074F5DKG	Nokia Purity Stereo In-Ear Headphones -Magenta (Discontinued by Manufacturer)	39.99	1440957997408440000 
B007BOIC62	Yurbuds Ironman Inspire PRO 3 Button Control and Mic Sport Earbuds, White	59.95	1440957997408440000 
B007EQI9X8	Yurbuds Ironman Inspire Talk Earbuds with 1-Button Microphone (Black)	29.99	1440957997408440000 
B00A6YPCK8	Velodyne vFree Bluetooth Wireless Stereo Headphone with Built-in Mic for Apple iPhone iPad and Android Devices (Gloss Black)	74.99	1440957997408450000 
B00ABANLR8	iFrogz IF-COD-NBLU Coda Headphones with Mic, Neon Blue	24.99	1440957997408450000 
B00AC7E2GO	RoadKing RK100 Wired Hands Free Noise Cancelling Headset	29.16	1440957997408450000 
B00AKI9LJ8	ASA HS-1A Headset	144	1440957997408450000 
B00BFO3YVW	Jabra REVO Corded Stereo Headphones - Retail Packaging - White (Discontinued by Manufacturer)	64.98	1440957997408450000 
B00BH36PRG	Bravo View IH-09AB - KID FRIENDLY Automotive IR Wireless Headphones (Dual Source)	29.99	1440957997408450000 
B00BL2M92I	Eskuche 101512C2BLU Control v2 On-Ear Headphones, Blue	28.43	1440957997408450000 
B00C4VFYFY	B&O PLAY by Bang & Olufsen Beoplay H6 (Black)	200	1440957997408450000 
B00C4VG1XS	Bang & Olufsen Beoplay H3 In-Ear Headphones - Natural	330	1440957997408450000 
B00CA7FR90	Motorola S11 HD Wireless Stereo Headphones - Retail Packaging - Black	39.99	1440957997408450000 
B00CIQ88UI	JVC Kenwood HA-SZ1000-E Victer Stereo Headphones	248	1440957997408450000 
B00CSQP5MW	Frends Ella B Earbuds Headphones in Gold and White (Non-retail Packaging)	189.99	1440957997408450000 
B00D31JEYQ	Yurbuds Inspire Talk (Aqua)	33.99	1440957997408450000 
B00D31OE0U	Yurbuds Inspire Talk Purple	29.99	1440957997408450000 
B00DIUGW6A	Shure SE846-CL Sound Isolating Earphones with Quad High Definition MicroDrivers and True Subwoofer	531	1440957997408450000 
B00E7L2LQE	Monster DNA On-Ear Headphones (Black Carbon Fiber)	99.99	1440957997408450000 
B00EANUQ4S	Shure SE535LTD Limited Edition Red Sound Isolating Earphones with Remote (Old Model) + Microphone	99	1440957997408450000 
B00EV14X4I	Arm Pocket Yurbuds Signature Series Pete Jacobs Plus Reflective Cloth Cords Sport Earbuds	49	1440957997408450000 
B00EVNVR2W	Plantronics Backbeat Go 2/R Headset, Black (88600-01)	44.86	1440957997408450000 
B00F32V9DM	Gioteck Ex-05S Universal Wired Stereo Headset	85.7	1440957997408450000 
B00FAYFDYE	Yurbuds Focus LE Limited Edition Wireless Behind The Ear BT Headphones, Black	57.99	1440957997408450000 
B00FS1PST4	Adventure Time Ear buds Beemo	29.99	1440957997408450000 
B00FYKMNN8	Nakamichi Over the Ear Headphone - Retail Packaging - Gray with Blue Thread	30	1440957997408450000 
B00G6RIF2Q	GOgroove Wireless Over-the-Ear Bluetooth Headphones with Mic & 14-Hour Battery Life - Works With Apple iPhone 6 Plus, Samsung Galaxy S6 Edge, LG G4 and Many Other Bluetooth-Enabled Smartphones	59.99	1440957997408450000 
B00GMKKEKI	Fhgkjy Headphone Jack Adapter Headset Audio Adaptor Connector Earphone Jack AUX Audio Adapter Splitter Dongle Audio Accessorie	39.99	1440957997408450000 
B00GNKU4SY	Yurbuds Explore Talk Gray/Orange Running Headphones	29.99	1440957997408450000 
B00GXDG9G2	Arm Pocket Yurbuds Adventure Line Venture Duro Sport Earbuds	39.95	1440957997408450000 
B00H0PWF06	Sony MDR10RNC Premium Noise Canceling Headphone	269.99	1440957997408450000 
B00H3847N8	Sena 3S Bluetooth Headset and Intercom Wired Boom Microphone Kit (3S-WB)	99.99	1440957997408450000 
B00I02300C	Beyerdynamic DX160IE Premium In-Ear Headphones (Black)	78	1440957997408450000 
B00IEEZATK	B&O PLAY by Bang & Olufsen 1641325 Beoplay Form 2i On-Ear Headphone (White)	66.01	1440957997408450000 
B00IL7B2YM	Jabra ROX Wireless Bluetooth Stereo Earbuds (Black)	25.99	1440957997408450000 
B00IORDBRA	SMS Audio STREET by 50 First Edition Star Wars On Ear Headphones Stormtrooper	199.5	1440957997408450000 
B00J2TGYZU	Skdy Inkd Mic Greeney/Lime	24.99	1440957997408450000 
B00J8QZLDS	Heavy-Duty Kids' Headphone w/Tangle-Free Fabric Cord (Pack of 10)	108.49	1440957997408450000 
B00JFGMNR8	Skullcandy Unisex Uprock Mic'd Gray/Cyan/Black	29.99	1440957997408450000 
B00JFLAEO2	Sony MDRZX750BN Bluetooth and Noise Cancelling Headset	89.99	1440957997408450000 
B00JMZILU0	Sennheiser HD 280 Pro headband pad Genuine HD280 headphones cushion replacement padding	28.49	1440957997408450000 
B00KGGK6XE	Samsung Level In-Ear Headphone - Retail Packaging - White	49.99	1440957997408450000 
B00L1O64X6	Grado Reference Series RS2e	495	1440957997408450000 
B00LV518MC	Harman International In Ear Sport Headphone Grn JBLREFLECTIGRN	25.99	1440957997408450000 
B00M7Y0KJS	Bose SoundSport In-Ear Headphones for iOS Models, Orange	160	1440957997408450000 
B00MBWIL0G	Plantronics BackBeat PRO Wireless Noise Canceling Hi-Fi Headphones with Mic - Compatible with iPhone, iPad, Android, and Other Smart Devices	39.94	1440957997408450000 
B00N3B2F3I	Insignia Wireless Over-the-Ear Headphone	181.33	1440957997408450000 
B00NA49K2W	Sharper Image SBT517BKBK Bluetooth Earbuds with Microphone, Tangle Free Flat Cable, Noise Isolating, Black	24.97	1440957997408450000 
B00NBMHT6C	Sony MDRXB450AP Extra Bass Smartphone Headset (Black)	59.95	1440957997408450000 
B00NBMHT7Q	Sony MDRZ7 Hi-Res Stereo Headphones	1224	1440957997408450000 
B00NCSIN4W	Skullcandy Hesh 2 Bluetooth Wireless Over-Ear Headphones with Microphone, Supreme Sound and Powerful Bass, 15-Hour Rechargeable Battery, Soft Synthetic Leather Ear Cushions, Black	45.99	1440957997408450000 
B00NWROP5Y	Denon AH-MM400 Music Maniac Over-Ear Headphones	209	1440957997408450000 
B00NWXLD8K	Modal Over-The-Ear Bluetooth Headphones With Built-In Mic HPBT101-BL	47.99	1440957997408450000 
B00OW2PJP8	B&O PLAY by Bang & Olufsen Beoplay H2 On-Ear Headphone with Microphone (Carbon Blue)	184	1440957997408450000 
B00P89AVRU	Plantronics BackBeat FIT Wireless Bluetooth Headphones - Waterproof Earbuds for Running and Workout, Green, Frustration Free Packaging	69.99	1440957997408450000 
B00R45Z2IE	B&O PLAY by Bang & Olufsen Beoplay H8 Wireless On-Ear Headphone with Active Noise Cancelling, Bluetooth 4.2 (Argilla Bright)	395	1440957997408450000 
B00RB6UM0Y	Sena (SMH5-UNIV) Bluetooth Headset and Intercom for Scooters/Motorcycles with Universal Microphone Kit	92.92	1440957997408450000 
B00TA4HV5Y	Sony MDRAS600BT Active Sports Bluetooth Headset (Orange)	69.95	1440957997408450000 
B00WGMRD2S	SkullCandy Uproar Onear Wireless Headphones One Size Black/Gray/Black	34.99	1440957997408450000 
B00Y54GYC0	Philips SHB6250/27 Wireless Bluetooth Headphones, Black	25.95	1440957997408450000 
B00YSQBRZE	Bose QuietComfort 15 Acoustic Noise Cancelling Headphones	105	1440957997408450000 
B00YZSXGQS	Skullcandy XTFree Bluetooth Wireless Sweat-Resistant Earbud with Microphone, Lightweight and Secure Fit, 6-Hour Rechargeable Battery, Pureclean Tech to Keep Earbuds Fresh, Black/Swirl	51.97	1440957997408450000 
B013HSW4N2	Jaybird X2 Wireless Sweat-Proof Micro-Sized Bluetooth Sport Headphones &ndash; Charge	69.99	1440957997408450000 
B014EUQ492	Jabra Eclipse Bluetooth Headset (U.S. Retail Packaging)	47.62	1440957997408450000 
B01533PXEG	Sentry Industries BT300 Bluetooth Stereo Headphones with Mic, Black	25.26	1440957997408450000 
B015ST2Q18	Plantronics BackBeat PRO+ Wireless Noise Canceling Hi-Fi Headphones	39.94	1440957997408450000 
B015WXF3MO	JBL Reflect Mini Bluetooth in-Ear Sport Headphones	79.99	1440957997408450000 
B0161D1DVY	Jabra Sport Pace Wireless Bluetooth Earbuds - U.S. Retail Packaging	79.99	1440957997408450000 
B016Y37M4I	Parrot Zik 3 Wireless Bluetooth Headphones - Adaptive Noise Control, Proximity Sensor, Wireless Charging - Black Leather Grain	225	1440957997408450000 
B017KE9JRS	Samsung Level U Pro Bluetooth Wireless In-ear Headphones with Microphone and UHQ Audio, Bronze	48.79	1440957997408450000 
B017T5NLYU	Wireless Earbuds Upgraded Graphene 3D Stereo Sound Bluetooth 5.0 with 28Hr Play Time Noise Cancelling HonShoop Lightweight Bluetooth Headphones Built-in Mic	39.99	1440957997408450000 
B018RP7X0O	MEE audio EP-X7Plus-BK-MEE Stereo Bluetooth Wireless Sports in-Ear HD Headphones	59.83	1440957997408450000 
B019OIKKRQ	Sport Headphones , AKEDRE&reg; Wireless Sports Bluetooth V4.1 Headphones Sweatproof Running Exercise Stereo with Mic Earbuds Earphones for Iphone 6/6s Plus Galaxy S6 and Android Phones (Gold)	35.09	1440957997408450000 
B01ASAIF8U	Master & Dynamic MW60S2 Wireless Bluetooth 4.1, Over-Ear, Closed Back Headphones with Superior Sound Quality and Highest Level of Design 45mm Neodymium Driver. Premium Brown Leather	404.87	1440957997408450000 
B01B26OM8G	MOXYO - Mission Earbuds, Clean Inline Mic and a Tangle-Free Flat Cable (Black)	29.99	1440957997408450000 
B01BCD3DRA	beyerdynamic T5p Second Generation Audiophile Headphone	899.97	1440957997408450000 
B01BX3ZSXQ	JBL Reflect Response in-Ear Bluetooth Sport Headphones	89.99	1440957997408450000 
B01C35JK5K	Egghead EGG-IAG-1004-SO 10-Position Stereo Jack Box	94.56	1440957997408450000 
B01C35JM08	Stereo School Headphone W/Leatherette Ear Cushion (Pack of 20)	216.84	1440957997408450000 
B01C741IVQ	Optoma NuForce HEM6 Reference Class Hi-Res in-Ear Headphones with Triple Balanced Armature Drivers	407.36	1440957997408450000 
B01D86Q858	DRUnKQUEEn Bluetooth Headphones, Bluetooth Headset, V4.1+EDR Noise Cancelling Hi-Fi Foldable Built in Microphone Super Extra Bass Stereo Wireless Over Ear Earphone, Support SD Card FM Radio	39.99	1440957997408450000 
B01DBUHLAC	Audio Technica ATH-M50X Professional Studio Headphones (Black) with FiiO A3 Portable Headphone Amplifier (Black)	149	1440957997408450000 
B01DK1TDH6	Wireless Headphones, Megadream Wireless Stereo Sport BT Headset Neckband Retractable Earbuds w/Mic for Running Gym Yoga Exercise iPhone Samsung (Gold)	20.99	1440957997408450000 
B01DKGP5U0	House of Marley EM-JE041-SB Smile Jamaica In-Ear Headphones, Signature Black OPEN BOX	24.99	1440957997408450000 
}```
        Give users one product and the hyperlink to the product. You can find the links in the product list data. NOTE THAT YOU ALREADY HAVE THE LINK. Don't say you could not access the links.
        If the products we have don't satisfy consumers' requirements, or users ask for products we don't have, tell them we only have the products now.
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
