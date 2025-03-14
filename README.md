# ConfBadger

This simple program creates conference badges given a CSV file with the appropriate column headers (please see example).
In the badge, details of the attendee such as first name, last name, job title and company will be printed, along with a QRCode containing a VCARD.

A flag with the attendee country will be added as well. To remove this, simpy assign ```false``` to the ```addFlag``` variable.
The Flags of the attendee are retrieved from https://countryflagsapi.com/. I have noticed that with a poor connection, the whole script might cascade-fail trying to retrieve the flags. If you encounter this proble, just disable the flag retrieval.

## Install Required Modules

while in the directory of the project. run the following to install all required modules:

```pip3 install -r requirements.txt```

## Usage

```python3 confbadger.py```


## Update your configuration

Configuration is stored in a yaml file, which is config.yaml by default.

### Attendee types

Create one list item in `attendee-types` for each attendee type. Each list item should have a `name` which will be
printed to the badge and a `ticket-titles` which is a list of ticket types from the data file.  

## Customize the code 
### Fonts

To change the TrueType font used you need to update the source code, update ```font```, ```font2``` and ```font3```
varible to point to your font path.

* ```font```  - used for First Name
* ```font2``` - used for Last Name and Job Title
* ```font3``` - Used for Company Name

### Badge Format

The badge will be created as PDF. You can swtch the format to png by updating the extension in this function:
```img_base.save(f"badges/{lastname}_{firstname}_{order}.pdf")```

## Run ConfBadger

you can run confBadger by:

```python3 confbadger.py```

* By default the badges will be created in the ```badges/``` directory.
* By default the QRCodes will be created in the ```codes/``` directory.
* If enabled, the flags will be created in the ```flags/``` directory.

### Command line options

 -h, --help            show this help message and exit
  --data DATA           List of attendees in the CSV formar as exported from Bevy. Default is data.csv
  --save-path SAVE_PATH
                        Path to save the generated badges. Default is ./codes
  --template TEMPLATE   Template for the badges. Default is the example KCDAMS2023_Badge_Template.png file
  --flags               Adds flags to the badges. False by default.
  --config CONFIG       Config file. Default is config.yaml.
  --debug               Print debug logs.


## TODO

* Add Auto adjustment of text size and position
* Add option to remove source images
* Add code for base image drawing