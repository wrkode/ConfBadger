import pyqrcode
import pandas as pd
import numpy as np
import png
import unicodedata
from PIL import Image, ImageFile, ImageFont, ImageDraw



dataFile = "data.csv"
save_path  = './codes'


font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 140)
font2 = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 70)
font3 = ImageFont.truetype("fonts/OpenSans-Semibold.ttf", 80)


speaker   = "100.00% - KCDNL2023SPKR"
organizer = "100.00% - KCDAMS23_ORGANIZERS_42"
vip       = ["100.00% - KCDAMS23-WILLIAMFRIENDS",
              "100.00% - KCDAMS_LOVES_DODAMS",
              "100.00% - KCDAMS23-ANDYFRIENDS"
              ]
student   =   ["75.00% - STUDENTKCD75",
              "100.00% - KCDAMS23_CODAMFRIENDS"]
sponsor   = ["100.00% - KCDAMS23_MULTILAYER_FREE_RRTFS",
              "100.00% - KCDAMS23_AVISI_FREE_YUHTG",
              "100.00% - KCDAMS23_CIRCLECI_FREE_UIGHT",
              "100.00% - KCDAMS23_BUOYANT_FREE_AAXDC",
              "100.00% - KCDAMS23_ELASTIC_FREE_IJUHY",
              "100.00% - KCDAMS23_ATCOMP_FREE_RRTFS",
              "100.00% - KCDAMS23_FULLSTAQ_FREE_ASDCX",
              "100.00% - KCDAMS23_AKNOSTIC_FREE_UHYGJ",
              "100.00% - KCDAMS23_FIKAWORKS_FREE_YGVHS",
              "100.00% - KCDAMS23_ING_FREE_ASDCX",
              "100.00% - KCDAMS23_REDKUBES_FREE_VGBSD",
              "100.00% - KCDAMS23_FERMYON_FREE_GYHUT"
              "100.00% - KCDAMS23_DOIT_FREE_TYGGHF",
              "100.00% - KCDAMS23_RABO_FREE_BHNJK",
              "100.00% - KCDAMS23_A1_FREE_ASDCX",
              "100.00% - KCDAMS23_SPECTROCLOUD_FREE_GTCFS"
              "100.00% - KCDAMS23_SUSE_FREE_JJHGT",
              "100.00% - KCDAMS23_MIA_FREE_GYHUT",
              "100.00% - KCDAMS23_HCS_FREE_RRTFS",
              "100.00% - KCDAMS23_SOLO.IO_FREE_ASDCX",
              "100.00% - KCDAMS23_APPVIA_FREE_TYYGH"
              "100.00% - KCDAMS23_EDB_FREE_JAESR",
              "100.00% - KCDAMS23_EDGELESS_FREE_HUGYF",
              ]

def createBadge():
    df = pd.read_csv(dataFile)
    df.fillna('', inplace=True)
    

    for index, values in df.iterrows():
        order     = values["Order #"]
        firstname = values["First Name"]
        lastname  = values["Last Name"]
        email     = values["Email"]
        phone     = values["Phone Number"]
        country   = values["Country"]
        landcode  = values["Country Code"]
        title     = values["Job Title"]
        org       = values["Company"]
        promo     = values["Discount"]

        data = f'''BEGIN:VCARD
N:{lastname};{firstname};
FN:{lastname}+{firstname}
TITLE:{title}
TEL;TYPE=work,VOICE:{phone}
EMAIL;WORK;INTERNET:{email}
ORG:{org}
GEO:{country}
VERSION:3.0
END:VCARD'''

        flag = "https://countryflagsapi.com/png/"+landcode

        qrcode = pyqrcode.create(unicodedata.normalize('NFKD', data).encode('ascii','ignore').decode('ascii'))
        qrcode.png(f"{save_path}/{lastname}_{firstname}_{order}.png", scale="4")

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img1 = Image.open("KCDAMS2023_Badge_Template.png").convert("RGB")
          
        # Opening the secondary image (overlay image)
        img2 = Image.open(f"{save_path}/{lastname}_{firstname}_{order}.png").convert("RGB")
          
        # Pasting img2 image on top of img1 
        # starting at coordinates (70, 1300)
        img1.paste(img2, (70, 1300))
        #flag = urllib.request.urlretrieve(flag, f"flags/{landcode}.png")
        img3 = Image.open(f"flags/{landcode}.png").convert("RGB")
        img1.paste(img3, (850, 1100))  
        
        upperName = firstname.upper()

        draw = ImageDraw.Draw(img1)
        draw.text((100,400), f"{upperName}",(207,19,19),font=font)
        draw.text((100,600), f"{lastname}",(0,0,0),font=font2)
        draw.text((50,1050), f"{title}",(207,19,19),font=font2)
        draw.text((50,1150), f"{org}", (20,206,219),font=font3)
        
        if promo == speaker:
                draw.line((0,1750, 1230,1750), fill="red", width=220)
                draw.text((280,1610), "SPEAKER", (255,255,255), font=font)
        elif promo == organizer:
                draw.line((0,1750, 1230,1750), fill="green", width=220)
                draw.text((210,1610), "ORGANIZER", (255,255,255), font=font)
        elif promo in vip:
                draw.line((0,1750, 1230,1750), (219,20,173), width=220)
                draw.text((490,1610), "VIP", (255,255,255), font=font)
        elif promo in student:
                draw.line((0,1750, 1230,1750), (17,205,247), width=220)
                draw.text((280,1610), "STUDENT", (255,255,255), font=font)
        elif promo in sponsor:
                draw.line((0,1750, 1230,1750), (16,37,224), width=220)
                draw.text((280,1610), "SPONSOR", (255,255,255), font=font)
        else:
                draw.line((0,1750, 1230,1750), (247,106,5), width=220)
                draw.text((270,1610), "ATTENDEE", (255,255,255), font=font)

        img1.save(f"badges/{lastname}_{firstname}_{order}.png")
createBadge()