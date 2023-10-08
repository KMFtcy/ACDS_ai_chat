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
        product lists:```goods_name	price	link
Vic Firth DB22 Isolation Headphones for Hearing Protection	33	http://106.52.209.141:18081/goodsDetail?goodsId=B0002F513E&defaultSkuId=1440957997408449281
beyerdynamic DT 770 PRO 250 Ohm Studio Headphone	169	http://106.52.209.141:18081/goodsDetail?goodsId=B0006NL5SM&defaultSkuId=1440957997408449290
Sentry Micro Noise Reduction In-Ear Headphones Color Varies - Sentry HO229	25	http://106.52.209.141:18081/goodsDetail?goodsId=B000IWAP4G&defaultSkuId=1440957997408449325
Bose TriPort In-Ear Headphones - Headphones ( ear-bud ) - black	169	http://106.52.209.141:18081/goodsDetail?goodsId=B000KLZ7VG&defaultSkuId=1440957997408449326
beyerdynamic DT 990 PRO Over-Ear Studio Headphones in black. Open construction, wired	169	http://106.52.209.141:18081/goodsDetail?goodsId=B0011UB9CQ&defaultSkuId=1440957997408449364
Jabra GN9125 Mono Flex-Boom Wireless Headset for Deskphone	150	http://106.52.209.141:18081/goodsDetail?goodsId=B001G66TAM&defaultSkuId=1440957997408449405
Klipsch Image S4i In-Ear Headset with Mic and 3-Button Remote Headphones - White	79	http://106.52.209.141:18081/goodsDetail?goodsId=B00365EB3I&defaultSkuId=1440957997408449466
Diddybeats by Dr. Dre Pink In-Ear Headphone from Monster (Discontinued by Manufacturer)	72	http://106.52.209.141:18081/goodsDetail?goodsId=B003OGQ92K&defaultSkuId=1440957997408449487
Etymotic Research MC5 Noise-Isolating In-Ear Earphones	67	http://106.52.209.141:18081/goodsDetail?goodsId=B003S3RFIQ&defaultSkuId=1440957997408449489
Sennheiser HDR 170 Headphone Receiver	134	http://106.52.209.141:18081/goodsDetail?goodsId=B003ZL916U&defaultSkuId=1440957997408449501
AIAIAI TMA-1 DJ Headphones without Mic, Black	200	http://106.52.209.141:18081/goodsDetail?goodsId=B00404H6DQ&defaultSkuId=1440957997408449507
iFrogz 7067-ERMN EarPollution Ronin Headphones, Midnight (Discontinued by Manufacturer)	40	http://106.52.209.141:18081/goodsDetail?goodsId=B0041E1QLI&defaultSkuId=1440957997408449511
Beyerdynamic T5p Tesla Audiophile Portable and Home Audio Stereo Headphone	749	http://106.52.209.141:18081/goodsDetail?goodsId=B004C04P46&defaultSkuId=1440957997408449525
Rocketfish RF-RBWHP01 Rocketboost Wireless Stereo Headphones	90	http://106.52.209.141:18081/goodsDetail?goodsId=B004H1W1MS&defaultSkuId=1440957997408449544
Monster NTUNE On-Ear Headphones, Red	119	http://106.52.209.141:18081/goodsDetail?goodsId=B004SU1B2Y&defaultSkuId=1440957997408449576
Philips O'Neill SHO9560BK/28 Over-Ear Headphones - Black (Discontinued by Manufacturer)	50	http://106.52.209.141:18081/goodsDetail?goodsId=B005626CMM&defaultSkuId=1440957997408449611
Yurbuds Personalized Series Earphone / Earbuds Combo.	80	http://106.52.209.141:18081/goodsDetail?goodsId=B005F65D24&defaultSkuId=1440957997408449642
Scosche RH1056M Over-The-Ear Headphones (White)	51	http://106.52.209.141:18081/goodsDetail?goodsId=B005HIS6JC&defaultSkuId=1440957997408449656
Blue Tiger Pro Wireless Bluetooth Headphones &ndash; Includes Mic &ndash; Black	160	http://106.52.209.141:18081/goodsDetail?goodsId=B005RZUH9W&defaultSkuId=1440957997408449683
Sony XBA-1IP - 1 Driver Balanced Armature Headset for Apple	80	http://106.52.209.141:18081/goodsDetail?goodsId=B006K556QM&defaultSkuId=1440957997408449730
PlayStation Vita In-ear Headset	45	http://106.52.209.141:18081/goodsDetail?goodsId=B006PP3ZK6&defaultSkuId=1440957997408449733
Sennheiser HD 700 Headphone (Jack plug 1/4" (6.3 mm) stereo)	455	http://106.52.209.141:18081/goodsDetail?goodsId=B0070U8KSM&defaultSkuId=1440957997408449759
Skullcandy Hesh (Discontinued by Manufacturer)	70	http://106.52.209.141:18081/goodsDetail?goodsId=B0071369KE&defaultSkuId=1440957997408449772
Nokia Purity Stereo In-Ear Headphones -Magenta (Discontinued by Manufacturer)	40	http://106.52.209.141:18081/goodsDetail?goodsId=B0074F5DKG&defaultSkuId=1440957997408449783
Yurbuds Ironman Inspire PRO 3 Button Control and Mic Sport Earbuds, White	60	http://106.52.209.141:18081/goodsDetail?goodsId=B007BOIC62&defaultSkuId=1440957997408449802
Yurbuds Ironman Inspire Talk Earbuds with 1-Button Microphone (Black)	30	http://106.52.209.141:18081/goodsDetail?goodsId=B007EQI9X8&defaultSkuId=1440957997408449817
Velodyne vFree Bluetooth Wireless Stereo Headphone with Built-in Mic for Apple iPhone iPad and Android Devices (Gloss Black)	75	http://106.52.209.141:18081/goodsDetail?goodsId=B00A6YPCK8&defaultSkuId=1440957997408450008
iFrogz IF-COD-NBLU Coda Headphones with Mic, Neon Blue	25	http://106.52.209.141:18081/goodsDetail?goodsId=B00ABANLR8&defaultSkuId=1440957997408450038
RoadKing RK100 Wired Hands Free Noise Cancelling Headset	29	http://106.52.209.141:18081/goodsDetail?goodsId=B00AC7E2GO&defaultSkuId=1440957997408450039
ASA HS-1A Headset	144	http://106.52.209.141:18081/goodsDetail?goodsId=B00AKI9LJ8&defaultSkuId=1440957997408450054
Jabra REVO Corded Stereo Headphones - Retail Packaging - White (Discontinued by Manufacturer)	65	http://106.52.209.141:18081/goodsDetail?goodsId=B00BFO3YVW&defaultSkuId=1440957997408450103
Bravo View IH-09AB - KID FRIENDLY Automotive IR Wireless Headphones (Dual Source)	30	http://106.52.209.141:18081/goodsDetail?goodsId=B00BH36PRG&defaultSkuId=1440957997408450107
Eskuche 101512C2BLU Control v2 On-Ear Headphones, Blue	28	http://106.52.209.141:18081/goodsDetail?goodsId=B00BL2M92I&defaultSkuId=1440957997408450115
B&O PLAY by Bang & Olufsen Beoplay H6 (Black)	200	http://106.52.209.141:18081/goodsDetail?goodsId=B00C4VFYFY&defaultSkuId=1440957997408450196
Bang & Olufsen Beoplay H3 In-Ear Headphones - Natural	330	http://106.52.209.141:18081/goodsDetail?goodsId=B00C4VG1XS&defaultSkuId=1440957997408450197
Motorola S11 HD Wireless Stereo Headphones - Retail Packaging - Black	40	http://106.52.209.141:18081/goodsDetail?goodsId=B00CA7FR90&defaultSkuId=1440957997408450200
JVC Kenwood HA-SZ1000-E Victer Stereo Headphones	248	http://106.52.209.141:18081/goodsDetail?goodsId=B00CIQ88UI&defaultSkuId=1440957997408450219
Frends Ella B Earbuds Headphones in Gold and White (Non-retail Packaging)	190	http://106.52.209.141:18081/goodsDetail?goodsId=B00CSQP5MW&defaultSkuId=1440957997408450245
Yurbuds Inspire Talk (Aqua)	34	http://106.52.209.141:18081/goodsDetail?goodsId=B00D31JEYQ&defaultSkuId=1440957997408450268
Yurbuds Inspire Talk Purple	30	http://106.52.209.141:18081/goodsDetail?goodsId=B00D31OE0U&defaultSkuId=1440957997408450269
Shure SE846-CL Sound Isolating Earphones with Quad High Definition MicroDrivers and True Subwoofer	531	http://106.52.209.141:18081/goodsDetail?goodsId=B00DIUGW6A&defaultSkuId=1440957997408450291
Monster DNA On-Ear Headphones (Black Carbon Fiber)	100	http://106.52.209.141:18081/goodsDetail?goodsId=B00E7L2LQE&defaultSkuId=1440957997408450344
Shure SE535LTD Limited Edition Red Sound Isolating Earphones with Remote (Old Model) + Microphone	99	http://106.52.209.141:18081/goodsDetail?goodsId=B00EANUQ4S&defaultSkuId=1440957997408450349
Arm Pocket Yurbuds Signature Series Pete Jacobs Plus Reflective Cloth Cords Sport Earbuds	49	http://106.52.209.141:18081/goodsDetail?goodsId=B00EV14X4I&defaultSkuId=1440957997408450376
Plantronics Backbeat Go 2/R Headset, Black (88600-01)	45	http://106.52.209.141:18081/goodsDetail?goodsId=B00EVNVR2W&defaultSkuId=1440957997408450377
Gioteck Ex-05S Universal Wired Stereo Headset	86	http://106.52.209.141:18081/goodsDetail?goodsId=B00F32V9DM&defaultSkuId=1440957997408450408
Yurbuds Focus LE Limited Edition Wireless Behind The Ear BT Headphones, Black	58	http://106.52.209.141:18081/goodsDetail?goodsId=B00FAYFDYE&defaultSkuId=1440957997408450414
Adventure Time Ear buds Beemo	30	http://106.52.209.141:18081/goodsDetail?goodsId=B00FS1PST4&defaultSkuId=1440957997408450435
Nakamichi Over the Ear Headphone - Retail Packaging - Gray with Blue Thread	30	http://106.52.209.141:18081/goodsDetail?goodsId=B00FYKMNN8&defaultSkuId=1440957997408450448
GOgroove Wireless Over-the-Ear Bluetooth Headphones with Mic & 14-Hour Battery Life - Works With Apple iPhone 6 Plus, Samsung Galaxy S6 Edge, LG G4 and Many Other Bluetooth-Enabled Smartphones	60	http://106.52.209.141:18081/goodsDetail?goodsId=B00G6RIF2Q&defaultSkuId=1440957997408450453
Fhgkjy Headphone Jack Adapter Headset Audio Adaptor Connector Earphone Jack AUX Audio Adapter Splitter Dongle Audio Accessorie	40	http://106.52.209.141:18081/goodsDetail?goodsId=B00GMKKEKI&defaultSkuId=1440957997408450474
Yurbuds Explore Talk Gray/Orange Running Headphones	30	http://106.52.209.141:18081/goodsDetail?goodsId=B00GNKU4SY&defaultSkuId=1440957997408450484
Arm Pocket Yurbuds Adventure Line Venture Duro Sport Earbuds	40	http://106.52.209.141:18081/goodsDetail?goodsId=B00GXDG9G2&defaultSkuId=1440957997408450507
Sony MDR10RNC Premium Noise Canceling Headphone	270	http://106.52.209.141:18081/goodsDetail?goodsId=B00H0PWF06&defaultSkuId=1440957997408450513
Sena 3S Bluetooth Headset and Intercom Wired Boom Microphone Kit (3S-WB)	100	http://106.52.209.141:18081/goodsDetail?goodsId=B00H3847N8&defaultSkuId=1440957997408450524
Beyerdynamic DX160IE Premium In-Ear Headphones (Black)	78	http://106.52.209.141:18081/goodsDetail?goodsId=B00I02300C&defaultSkuId=1440957997408450580
B&O PLAY by Bang & Olufsen 1641325 Beoplay Form 2i On-Ear Headphone (White)	66	http://106.52.209.141:18081/goodsDetail?goodsId=B00IEEZATK&defaultSkuId=1440957997408450616
Jabra ROX Wireless Bluetooth Stereo Earbuds (Black)	26	http://106.52.209.141:18081/goodsDetail?goodsId=B00IL7B2YM&defaultSkuId=1440957997408450629
SMS Audio STREET by 50 First Edition Star Wars On Ear Headphones Stormtrooper	200	http://106.52.209.141:18081/goodsDetail?goodsId=B00IORDBRA&defaultSkuId=1440957997408450632
Skdy Inkd Mic Greeney/Lime	25	http://106.52.209.141:18081/goodsDetail?goodsId=B00J2TGYZU&defaultSkuId=1440957997408450671
Heavy-Duty Kids' Headphone w/Tangle-Free Fabric Cord (Pack of 10)	108	http://106.52.209.141:18081/goodsDetail?goodsId=B00J8QZLDS&defaultSkuId=1440957997408450696
Skullcandy Unisex Uprock Mic'd Gray/Cyan/Black	30	http://106.52.209.141:18081/goodsDetail?goodsId=B00JFGMNR8&defaultSkuId=1440957997408450732
Sony MDRZX750BN Bluetooth and Noise Cancelling Headset	90	http://106.52.209.141:18081/goodsDetail?goodsId=B00JFLAEO2&defaultSkuId=1440957997408450733
Sennheiser HD 280 Pro headband pad Genuine HD280 headphones cushion replacement padding	28	http://106.52.209.141:18081/goodsDetail?goodsId=B00JMZILU0&defaultSkuId=1440957997408450745
Samsung Level In-Ear Headphone - Retail Packaging - White	50	http://106.52.209.141:18081/goodsDetail?goodsId=B00KGGK6XE&defaultSkuId=1440957997408450816
Grado Reference Series RS2e	495	http://106.52.209.141:18081/goodsDetail?goodsId=B00L1O64X6&defaultSkuId=1440957997408450886
Harman International In Ear Sport Headphone Grn JBLREFLECTIGRN	26	http://106.52.209.141:18081/goodsDetail?goodsId=B00LV518MC&defaultSkuId=1440957997408450929
Bose SoundSport In-Ear Headphones for iOS Models, Orange	160	http://106.52.209.141:18081/goodsDetail?goodsId=B00M7Y0KJS&defaultSkuId=1440957997408450951
Plantronics BackBeat PRO Wireless Noise Canceling Hi-Fi Headphones with Mic - Compatible with iPhone, iPad, Android, and Other Smart Devices	40	http://106.52.209.141:18081/goodsDetail?goodsId=B00MBWIL0G&defaultSkuId=1440957997408450956
Insignia Wireless Over-the-Ear Headphone	181	http://106.52.209.141:18081/goodsDetail?goodsId=B00N3B2F3I&defaultSkuId=1440957997408451034
Sharper Image SBT517BKBK Bluetooth Earbuds with Microphone, Tangle Free Flat Cable, Noise Isolating, Black	25	http://106.52.209.141:18081/goodsDetail?goodsId=B00NA49K2W&defaultSkuId=1440957997408451057
Sony MDRXB450AP Extra Bass Smartphone Headset (Black)	60	http://106.52.209.141:18081/goodsDetail?goodsId=B00NBMHT6C&defaultSkuId=1440957997408451064
Sony MDRZ7 Hi-Res Stereo Headphones	1224	http://106.52.209.141:18081/goodsDetail?goodsId=B00NBMHT7Q&defaultSkuId=1440957997408451065
Skullcandy Hesh 2 Bluetooth Wireless Over-Ear Headphones with Microphone, Supreme Sound and Powerful Bass, 15-Hour Rechargeable Battery, Soft Synthetic Leather Ear Cushions, Black	46	http://106.52.209.141:18081/goodsDetail?goodsId=B00NCSIN4W&defaultSkuId=1440957997408451074
Denon AH-MM400 Music Maniac Over-Ear Headphones	209	http://106.52.209.141:18081/goodsDetail?goodsId=B00NWROP5Y&defaultSkuId=1440957997408451123
Modal Over-The-Ear Bluetooth Headphones With Built-In Mic HPBT101-BL	48	http://106.52.209.141:18081/goodsDetail?goodsId=B00NWXLD8K&defaultSkuId=1440957997408451126
B&O PLAY by Bang & Olufsen Beoplay H2 On-Ear Headphone with Microphone (Carbon Blue)	184	http://106.52.209.141:18081/goodsDetail?goodsId=B00OW2PJP8&defaultSkuId=1440957997408451175
Plantronics BackBeat FIT Wireless Bluetooth Headphones - Waterproof Earbuds for Running and Workout, Green, Frustration Free Packaging	70	http://106.52.209.141:18081/goodsDetail?goodsId=B00P89AVRU&defaultSkuId=1440957997408451192
B&O PLAY by Bang & Olufsen Beoplay H8 Wireless On-Ear Headphone with Active Noise Cancelling, Bluetooth 4.2 (Argilla Bright)	395	http://106.52.209.141:18081/goodsDetail?goodsId=B00R45Z2IE&defaultSkuId=1440957997408451251
Sena (SMH5-UNIV) Bluetooth Headset and Intercom for Scooters/Motorcycles with Universal Microphone Kit	93	http://106.52.209.141:18081/goodsDetail?goodsId=B00RB6UM0Y&defaultSkuId=1440957997408451257
Sony MDRAS600BT Active Sports Bluetooth Headset (Orange)	70	http://106.52.209.141:18081/goodsDetail?goodsId=B00TA4HV5Y&defaultSkuId=1440957997408451327
SkullCandy Uproar Onear Wireless Headphones One Size Black/Gray/Black	35	http://106.52.209.141:18081/goodsDetail?goodsId=B00WGMRD2S&defaultSkuId=1440957997408451503
Philips SHB6250/27 Wireless Bluetooth Headphones, Black	26	http://106.52.209.141:18081/goodsDetail?goodsId=B00Y54GYC0&defaultSkuId=1440957997408451590
Bose QuietComfort 15 Acoustic Noise Cancelling Headphones	105	http://106.52.209.141:18081/goodsDetail?goodsId=B00YSQBRZE&defaultSkuId=1440957997408451609
Skullcandy XTFree Bluetooth Wireless Sweat-Resistant Earbud with Microphone, Lightweight and Secure Fit, 6-Hour Rechargeable Battery, Pureclean Tech to Keep Earbuds Fresh, Black/Swirl	52	http://106.52.209.141:18081/goodsDetail?goodsId=B00YZSXGQS&defaultSkuId=1440957997408451618
Jaybird X2 Wireless Sweat-Proof Micro-Sized Bluetooth Sport Headphones &ndash; Charge	70	http://106.52.209.141:18081/goodsDetail?goodsId=B013HSW4N2&defaultSkuId=1440957997408451725
Jabra Eclipse Bluetooth Headset (U.S. Retail Packaging)	48	http://106.52.209.141:18081/goodsDetail?goodsId=B014EUQ492&defaultSkuId=1440957997408451774
Sentry Industries BT300 Bluetooth Stereo Headphones with Mic, Black	25	http://106.52.209.141:18081/goodsDetail?goodsId=B01533PXEG&defaultSkuId=1440957997408451794
Plantronics BackBeat PRO+ Wireless Noise Canceling Hi-Fi Headphones	40	http://106.52.209.141:18081/goodsDetail?goodsId=B015ST2Q18&defaultSkuId=1440957997408451835
JBL Reflect Mini Bluetooth in-Ear Sport Headphones	80	http://106.52.209.141:18081/goodsDetail?goodsId=B015WXF3MO&defaultSkuId=1440957997408451837
Jabra Sport Pace Wireless Bluetooth Earbuds - U.S. Retail Packaging	80	http://106.52.209.141:18081/goodsDetail?goodsId=B0161D1DVY&defaultSkuId=1440957997408451850
Parrot Zik 3 Wireless Bluetooth Headphones - Adaptive Noise Control, Proximity Sensor, Wireless Charging - Black Leather Grain	225	http://106.52.209.141:18081/goodsDetail?goodsId=B016Y37M4I&defaultSkuId=1440957997408451902
Samsung Level U Pro Bluetooth Wireless In-ear Headphones with Microphone and UHQ Audio, Bronze	49	http://106.52.209.141:18081/goodsDetail?goodsId=B017KE9JRS&defaultSkuId=1440957997408451942
Wireless Earbuds Upgraded Graphene 3D Stereo Sound Bluetooth 5.0 with 28Hr Play Time Noise Cancelling HonShoop Lightweight Bluetooth Headphones Built-in Mic	40	http://106.52.209.141:18081/goodsDetail?goodsId=B017T5NLYU&defaultSkuId=1440957997408451959
MEE audio EP-X7Plus-BK-MEE Stereo Bluetooth Wireless Sports in-Ear HD Headphones	60	http://106.52.209.141:18081/goodsDetail?goodsId=B018RP7X0O&defaultSkuId=1440957997408452050
Sport Headphones , AKEDRE&reg; Wireless Sports Bluetooth V4.1 Headphones Sweatproof Running Exercise Stereo with Mic Earbuds Earphones for Iphone 6/6s Plus Galaxy S6 and Android Phones (Gold)	35	http://106.52.209.141:18081/goodsDetail?goodsId=B019OIKKRQ&defaultSkuId=1440957997408452086
Master & Dynamic MW60S2 Wireless Bluetooth 4.1, Over-Ear, Closed Back Headphones with Superior Sound Quality and Highest Level of Design 45mm Neodymium Driver. Premium Brown Leather	405	http://106.52.209.141:18081/goodsDetail?goodsId=B01ASAIF8U&defaultSkuId=1440957997408452118
MOXYO - Mission Earbuds, Clean Inline Mic and a Tangle-Free Flat Cable (Black)	30	http://106.52.209.141:18081/goodsDetail?goodsId=B01B26OM8G&defaultSkuId=1440957997408452133
beyerdynamic T5p Second Generation Audiophile Headphone	900	http://106.52.209.141:18081/goodsDetail?goodsId=B01BCD3DRA&defaultSkuId=1440957997408452139
JBL Reflect Response in-Ear Bluetooth Sport Headphones	90	http://106.52.209.141:18081/goodsDetail?goodsId=B01BX3ZSXQ&defaultSkuId=1440957997408452178
Egghead EGG-IAG-1004-SO 10-Position Stereo Jack Box	95	http://106.52.209.141:18081/goodsDetail?goodsId=B01C35JK5K&defaultSkuId=1440957997408452189
Stereo School Headphone W/Leatherette Ear Cushion (Pack of 20)	217	http://106.52.209.141:18081/goodsDetail?goodsId=B01C35JM08&defaultSkuId=1440957997408452193
Optoma NuForce HEM6 Reference Class Hi-Res in-Ear Headphones with Triple Balanced Armature Drivers	407	http://106.52.209.141:18081/goodsDetail?goodsId=B01C741IVQ&defaultSkuId=1440957997408452199
DRUnKQUEEn Bluetooth Headphones, Bluetooth Headset, V4.1+EDR Noise Cancelling Hi-Fi Foldable Built in Microphone Super Extra Bass Stereo Wireless Over Ear Earphone, Support SD Card FM Radio	40	http://106.52.209.141:18081/goodsDetail?goodsId=B01D86Q858&defaultSkuId=1440957997408452258
Audio Technica ATH-M50X Professional Studio Headphones (Black) with FiiO A3 Portable Headphone Amplifier (Black)	149	http://106.52.209.141:18081/goodsDetail?goodsId=B01DBUHLAC&defaultSkuId=1440957997408452262
Wireless Headphones, Megadream Wireless Stereo Sport BT Headset Neckband Retractable Earbuds w/Mic for Running Gym Yoga Exercise iPhone Samsung (Gold)	21	http://106.52.209.141:18081/goodsDetail?goodsId=B01DK1TDH6&defaultSkuId=1440957997408452268
House of Marley EM-JE041-SB Smile Jamaica In-Ear Headphones, Signature Black OPEN BOX	25	http://106.52.209.141:18081/goodsDetail?goodsId=B01DKGP5U0&defaultSkuId=1440957997408452270
```
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
