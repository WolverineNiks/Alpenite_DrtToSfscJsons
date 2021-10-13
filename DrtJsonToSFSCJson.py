"""
    2021.10.13 
    This script converts Privacy Jsons used in DRT into Jsons used in Salesforce Privacy Sites. 
    DRT Json structure:
        - one file per language
        - each file has:
            - BRAND => COUNTRY => "PRIVACY" => key:value
            ex. en.JSON
            {
                "2_20": {
                    "GB": {
                        "PRIVACY": {
                            "FLAG_MARKETING_OPTIN_TEXT": "PRIVACY TEXT",
                            ...
                        }
                    }...
                },
                "1_30": {
                    ...
                }...
            }
    SFSC Json structure:
        - one file for whole data
        - BRAND => COUNTRY => LANGUAGE => key:value
        ex. 
        {
            "2_20": {
                "GB": {
                    "en": {
                        "LABEL": "labelText",
                        ...
                    },
                    "it": {
                        ...
                    }
                },...
            },...
        }
"""
import json
import copy
import os

_DRTJsonsDirectoryPath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\2021.10.13 LatestPrivacyJsons from DRT\\testData'
_SFSCJsonsFilePath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\2021.10.13 LatestPrivacyJsons from DRT\\privacyTranslations.json'
_brandsList = ['1_130', '1_60', '2_20', '4_40', '5_80']
_languageIsoToDescMap = {
    "ca":"Catalan",
    "da":"Dansk",
    "de":"Deutsch",
    "el":"ελληνικά",
    "en":"English",
    "es":"Español",
    "fi":"Suomi",
    "fr":"Français",
    "it":"Italiano",
    "ja":"日本語 ",
    "ko":"한국어",
    "nl":"Nederlands",
    "no":"Norsk",
    "pt":"Português",
    "sv":"Svenska",
    "zh_HK":"Cantonese",
    "zh":"Chinese"
}
_diesel = 'diesel'


def createSfscObject(newSfscJsonObject, drtJsonObject, sfscBasicObj, drtBasicObj, brand, lang, country):
    newSfscJsonObject = 'ee'
    sfscBasicObject = {
        "LABEL": _languageIsoToDescMap[lang] if lang in _languageIsoToDescMap else lang,
        "LINK_Privacy_marketing__c": "/justcavallipreferences/JustCavalli_MarketingPrivacy",
        "LINK_Privacy_policy": "/justcavallipreferences/JustCavalli_PrivacyPolicy",
        "LINK_Privacy_profiling__c": "/justcavallipreferences/JustCavalli_ProfilingPrivacy",
        "SUB_TITLE_1": "I confirm I’m over 16 years old and I have read the Privacy Policy provided by the Data Controllers in accordance with local applicable laws, and I",
        "SUB_TITLE_2": "",
        "TEXT_Communication_Data__c": "",
        "TEXT_Privacy_general_consent_NAM__c": "",
        "TEXT_Privacy_HK__c": "",
        "TEXT_Privacy_marketing__c": "I agree to the use of the Personal Data for marketing purposes (newsletters, news and promotions), in accordance to letter b. paragraph 2 of the information notice",
        "TEXT_Privacy_marketing_online__c": "",
        "TEXT_Privacy_profiling__c": "I agree to the use of the Personal Data for profiling purposes of my consumer behaviour, in accordance to letter c. paragraph 2 of the information notice",
        "TEXT_Privacy_text_message__c": "",
        "TEXT_Unsubscribe__c": "",
        "TITLE": "AUTHORIZATION FOR DATA PROCESSING"
    }

#Create DRT FILES JSON OBJECT (n files)
drtJsonObject = {}
data = '{\n'
print('Reading files...')
for fileEntry in os.scandir(_DRTJsonsDirectoryPath):
    if (fileEntry.path.endswith(".json")) and fileEntry.is_file():
        print(fileEntry.path)
        data = data + '\t\"' + os.path.basename(fileEntry.path)[:-5]  + '\":\n\t\t' 
        fRead = open(fileEntry.path, encoding="utf-8")
        data = data + fRead.read()
        data = data + ','
        #drtJsonObject[os.path.basename(fileEntry.path)[:-5]] = data
        fRead.close()
data = data[:-1]
data = data + '\n}'
drtJsonObject = json.loads(data)

#CREATE SFSC FILE JSON OBJECT (1 file)
fRead = open(_SFSCJsonsFilePath, encoding="utf-8")
data = json.load(fRead)
fRead.close()
sfscJsonObject = data


newSfscJsonObject = {}
for brand in _brandsList:
    sfscBasicObj = sfscJsonObject[brand]["INTERNATIONAL"]["en"]
    newSfscJsonObject[brand] = {}
    for lang in drtJsonObject.keys():
        langObj = drtJsonObject[lang]
        for country in drtJsonObject[lang][brand].keys():
            newSfscJsonObject[brand][country] = {}
            newSfscJsonObject[brand][country][lang] = {}
            for drtObject in drtJsonObject[lang][brand][country]["PRIVACY"]:
                drtBasicObj = drtJsonObject[lang][brand][country]["PRIVACY"][drtObject]
                print(newSfscJsonObject)
                #createSfscObject(newSfscJsonObject, drtJsonObject, sfscBasicObj, drtBasicObj, brand, lang, country)