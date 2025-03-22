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

font_first_name = None
font_last_name = None
font_title = None
font_company = None
font_attendee_type = None

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
    parser.add_argument('--pre-order-data',
                            help='Optional data file of the Pre order form from Bevy. To utilize information form here add a pre-order-data section to config.yaml')
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
    pre_order_data = None
    if args.pre_order_data:
        pre_order_data = args.pre_order_data

    logger.debug(f"Data file is {data_file}")
    logger.debug(f"Save path file is {save_path}")
    logger.debug(f"Template is {template}")
    logger.debug(f"Config file is {config_file}")

    createBadge(template,
                save_path,
                data_file,
                config_file,
                pre_order_data)

def createBadge(template = "KCDAMS2023_Badge_Template.png",
                save_path = "badges",
                data_file = "data.csv",
                config_file = "config.yaml", 
                pre_order_data = None):
    
    logger = logging.getLogger(__name__)
    logger.debug(f"teplate: {template}, save_path: {save_path}, data_file: {data_file}, config_file: {config_file}")

    with open(config_file, 'r') as f:
        config_data = yaml.load(f, Loader=yaml.SafeLoader)

    df = read_data_file(data_file)
    #logger.debug(f"Df pre merge: {df.columns}")
    if pre_order_data and ("pre-order-data" in config_data):
        df_pre_order = read_data_file(pre_order_data)
        #logger.debug(f"Df pre pre merge: {df_pre_order.columns}")
        df = df.merge(df_pre_order, left_on='Order number', right_on='Order Number', suffixes=('', '_pre_order'))

        fields_with_extends = [(item['field'], item['extends']) for item in config_data['pre-order-data-extend']]
        for field in fields_with_extends:
                logger.debug(f"Extending {field[1]} with {field[0]}")
                df.loc[df[field[1]] == '', field[1]] = df[field[0]]

    #logger.debug(f"Df post merge: {df.columns}")
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

        #logger.debug(data)

        qrcode = pyqrcode.create(unicodedata.normalize('NFKD', data).encode('ascii','ignore').decode('ascii'))
        qrcode.png(f"{save_path}/{lastname}_{firstname}_{order_number}.png", scale="4")

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img_base = Image.open(template).convert("RGB")
          
        # Opening the secondary image (overlay image)
        img_qcode = Image.open(f"{save_path}/{lastname}_{firstname}_{order_number}.png").convert("RGB")
          
        # Pasting qrcode image on top of teamplate image 
        # starting at coordinates (70, 1300)
        img_base.paste(img_qcode, (70, 1300))

        draw = ImageDraw.Draw(img_base)
        for item in config_data.get("data", []):
               #logger.debug(f'Adding item {item.get("field")}, {item.get("position")}, {item.get("color")}, {item.get("font")}')
               text = f'{values[item.get("field")]}'
               draw_text(draw, text, item)
        if pre_order_data:
                for item in config_data.get("pre-order-data", []):
                        #logger.debug(f'Adding extra item {item.get("field")}, {item.get("position")}, {item.get("color")}, {item.get("font")}')
                        text = f'{values[item.get("field")]}'
                        draw_text(draw, text, item)

        attendee_type = "attendee"
        for attendee in config_data["attendee-types"]:
                if ticket_title in attendee["ticket-titles"]:
                        logger.debug(f"name: {firstname} {lastname}, ticket type: {attendee['name']}")
                        attendee_type = attendee["name"]
        draw.line((0,1750, 1230,1750), (247,106,5), width=220)
        
        item = next((item for item in config_data["fonts"] if item.get("field") == "attendee-type"), None)
        draw_text(draw, attendee_type, item)
#        draw.text((270,1610), attendee_type, (255,255,255), font=font)

        img_base.save(f"badges/{lastname}_{firstname}_{order_number}.pdf")

def read_data_file(csv_file):
        logger = logging.getLogger(__name__)
        df = pd.read_csv(csv_file)

        # Filling empty places with proper things
        if "Twitter" in df.columns:
                df['Twitter'] = df['Twitter'].astype('object')
        if "Title" in df.columns:
                df['Title'] = df['Title'].astype('object')
        if "Featured" in df.columns:
                df['Featured'] = df['Featured'].astype('object')
        if 'Checkin Date (UTC)' in df.columns:
                df['Checkin Date (UTC)'] = df['Checkin Date (UTC)'].astype('object')
        
        for column in df.columns:
                if df[column].dtype == 'object':  # String columns (object type)
                        df[column] = df[column].fillna('')
                else:  # Numeric columns (int, float)
                        df[column] = df[column].fillna(0)
        return df

def get_font(font_file, size):
        logger = logging.getLogger(__name__)
        font = None
        try:
                font = ImageFont.truetype(font_file, size)
        except OSError:
                logger.debug(f"Font file ({font_file}) not found, using defaults.")
                font = ImageFont.load_default()
        return font
       
def draw_text(draw, text, item, position=None, color=None):
        if not position:
                position = str_to_tuple(item.get("position"))
        if not color:
                color = str_to_tuple(item.get("color"))
        if "capitals" == item.get("style"):
                text = text.upper()
        draw.text(position, text, color, font=get_font(item.get("font"), item.get("size")))

def build_text(text, font_type, config_data):
        conf = next((item for item in config_data["fonts"] if font_type in item), {})
        if conf.get("style", "default") == "capitals":
              return text.upper()
        else:
              return text

def str_to_tuple(position):
       return tuple(map(int, position.split(",")))

if __name__ == "__main__":
    main()
