import pyqrcode
import pandas as pd
import numpy as np
import png
import urllib.request
import unicodedata
import argparse
import logging
import sys
import yaml
from PIL import Image, ImageFile, ImageFont, ImageDraw

font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 140)
font2 = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 70)
font3 = ImageFont.truetype("fonts/OpenSans-Semibold.ttf", 80)

def main():

    logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description='Generating conference badges.')

    parser.add_argument('--data', default="data.csv",
                            help='List of attendees in the CSV format as exported from Bevy. Default is data.csv')
    parser.add_argument('--save-path', default="./codes",
                            help='Path to save the generated badges. Default is ./codes')
    parser.add_argument('--template', default="KCDAMS2023_Badge_Template.png",
                            help='Template for the badges. Default is the example KCDAMS2023_Badge_Template.png file')
    parser.add_argument('--config', default="config.yaml",
                            help='Config file. Default is config.yaml.')
    parser.add_argument('--debug', action="store_true",
                            help='Print debug logs.')
    args = parser.parse_args()
    # print(args)
    if args.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug logging is ON")

    data_file   = args.data
    save_path  = args.save_path
    template   = args.template
    config_file = args.config

    logger.debug(f"Data file is {data_file}")
    logger.debug(f"Save path file is {save_path}")
    logger.debug(f"Template is {template}")
    logger.debug(f"Config file is {config_file}")

    createBadge(template, save_path, data_file, config_file)

def createBadge(template = "KCDAMS2023_Badge_Template.png",
                save_path = "badges",
                data_file = "data.csv",
                config_file = "config.yaml" ):
    
    logger = logging.getLogger(__name__)
    logger.debug(f"teplate: {template}, save_path: {save_path}, data_file: {data_file}, config_file: {config_file}")

    with open(config_file, 'r') as f:
        config_data = yaml.load(f, Loader=yaml.SafeLoader)

    df = read_data_file(data_file)
    
    for index, values in df.iterrows():
        order_number            = values["Order number"]        
        ticket_number           = values["Ticket number"]
        firstname               = values["First Name"]
        lastname                = values["Last Name"]
        email                   = values["Email"]
        twitter                 = values["Twitter"]
        company                 = values["Company"]
        title                   = values["Title"]
        featured                = values["Featured"]
        ticket_title            = values["Ticket title"]
        ticket_venue            = values["Ticket venue"]
        access_code             = values["Access code"]
        price                   = values["Price"]
        currency                = values["Currency"]
        number_of_tickets       = values["Number of tickets"]
        paid_by_name            = values["Paid by (name)"]
        paid_by_email           = values["Paid by (email)"]
        paid_date               = values["Paid date (UTC)"]
        checkin_date            = values["Checkin Date (UTC)"]
        ticket_price_paid       = values["Ticket Price Paid"]

        data = f'''BEGIN:VCARD
N:{lastname};{firstname};
FN:{lastname}+{firstname}
TITLE:{title}
EMAIL;WORK;INTERNET:{email}
ORG:{company}
VERSION:3.0
END:VCARD'''

        qrcode = pyqrcode.create(unicodedata.normalize('NFKD', data).encode('ascii','ignore').decode('ascii'))
        qrcode.png(f"{save_path}/{lastname}_{firstname}_{order_number}.png", scale="4")

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img_base = Image.open(template).convert("RGB")
          
        # Opening the secondary image (overlay image)
        img_qcode = Image.open(f"{save_path}/{lastname}_{firstname}_{order_number}.png").convert("RGB")
          
        # Pasting qrcode image on top of teamplate image 
        # starting at coordinates (70, 1300)
        img_base.paste(img_qcode, (70, 1300))
        
        upperName = firstname.upper()

        draw = ImageDraw.Draw(img_base)
        draw.text((100,400), f"{upperName}",(207,19,19),font=font)
        draw.text((100,600), f"{lastname}",(0,0,0),font=font2)
        draw.text((50,1050), f"{title}",(207,19,19),font=font2)
        draw.text((50,1150), f"{company}", (20,206,219),font=font3)

        attendee_type = "ATTENDEE"
        for attendee in config_data["attendee-types"]:
                if ticket_title in attendee["ticket-titles"]:
                        logger.debug(f"name: {firstname} {lastname}, ticket type: {attendee['name']}")
                        attendee_type = attendee["name"].capitalize()
        draw.line((0,1750, 1230,1750), (247,106,5), width=220)
        draw.text((270,1610), attendee_type, (255,255,255), font=font)

        img_base.save(f"badges/{lastname}_{firstname}_{order_number}.pdf")

def read_data_file(csv_file):
        df = pd.read_csv(csv_file)
        # Filling empty places with proper things
        df.iloc[:, 0:11] = df.iloc[:, 0:11].fillna('')
        df.iloc[:, 12] = df.iloc[:, 12].fillna(0)
        df.iloc[:, 13] = df.iloc[:, 13].fillna('')
        df.iloc[:, 14] = df.iloc[:, 14].fillna(0)
        df.iloc[:, 15:18] = df.iloc[:, 15:18].fillna('')
        df.iloc[:, 19] = df.iloc[:, 19].fillna(0)
        return df

if __name__ == "__main__":
    main()
