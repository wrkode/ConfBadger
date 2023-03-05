# ConfBadger

This simple program, creates conference badges given a CSV file with the appropriate column headers (please see example).
In the badge, details of the attendee such as first name, last name, job title and company will be printed, along with a QRCode containing a VCARD. 
A flag with the attendee country will be added as well. To remove this, simpy assign ```false``` to the ```addFlag``` variable.
The Flags of the attendee are retrieved from https://countryflagsapi.com/. I have noticed that with a poor connection, the whole script might fail.

## Install Required Modules

while in the directory of the project. run the following to install all required modules:
```pip3 install -r requirements.txt```

## Update your variables

* ```dataFile``` - CSV file containing your attendees.
* ```template``` - Your base image file for the badge. Use ```KCDAMS2023_Badge_Template.png``` for sizing reference.

## Fonts

To change the TrueType font used, update ```font```, ```font2``` and ```font``` varible to point to your font path.

* ```font``` - used for First Name
* ```font2``` - used for Last Name and Job Title
* ```font3``` - Used for Company Name

## Attendees Types

The Colour and Text at the bottom of the badge, is updated according to the attendee ```discount```. Update the follwoing varialble values to your needs:

* ```speaker```
* ```organizer```
* ```vip```
* ```student```
* ```sponsor```

## Flags

* ```addFlag``` - Used to enable/disable flage retrieval and addition.

## Badge Format

The badge will be created as PDF. You can swtch the format to png by updating the extension in this function:
```img_base.save(f"badges/{lastname}_{firstname}_{order}.pdf")```

## Run ConfBadger

you can run confBadger by:

```python3 confbadger.py```
