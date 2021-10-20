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

_DRTJsonsDirectoryPath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\GIT_2021.10.13 OTB_PrivacyJsonsConverter\\DrtJsonToSfscJson\\testResultJsons'
_SFSCJsonsFilePath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\GIT_2021.10.13 OTB_PrivacyJsonsConverter\\DrtJsonToSfscJson\\privacyTranslations.json'
_ResultFilePath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\GIT_2021.10.13 OTB_PrivacyJsonsConverter\\DrtJsonToSfscJson\\RESULT.json'
_brandsList = {
    '1_130': {
        "LINK_Privacy_marketing__c": "/justcavallipreferences/JustCavalli_MarketingPrivacy",
        "LINK_Privacy_policy": "/justcavallipreferences/JustCavalli_PrivacyPolicy",
        "LINK_Privacy_profiling__c": "/justcavallipreferences/JustCavalli_ProfilingPrivacy"
    }, 
    '1_60': {
        "LINK_Privacy_marketing__c": "/dsquaredpreferences/DSQUARED_MarketingPrivacy",
        "LINK_Privacy_policy": "/dsquaredpreferences/DSQUARED_PrivacyPolicy",
        "LINK_Privacy_profiling__c": "/dsquaredpreferences/DSQUARED_ProfilingPrivacy"
    }, 
    '2_20': {
        "LINK_Privacy_marketing__c": "/dieselpreferences/Diesel_MarketingPrivacy",
        "LINK_Privacy_policy": "/dieselpreferences/Diesel_PrivacyPolicy",
        "LINK_Privacy_profiling__c": "/dieselpreferences/Diesel_ProfilingPrivacy"
    }, 
    '4_40': {
        "LINK_Privacy_marketing__c": "/marnipreferences/Marni_MarketingPrivacy",
        "LINK_Privacy_policy": "/marnipreferences/Marni_PrivacyPolicy",
        "LINK_Privacy_profiling__c": "/marnipreferences/Marni_ProfilingPrivacy"
    }, 
    '5_80': {
        "LINK_Privacy_marketing__c": "/maisonmargielapreferences/MaisonMargiela_MarketingPrivacy",
        "LINK_Privacy_policy": "/maisonmargielapreferences/MaisonMargiela_PrivacyPolicy",
        "LINK_Privacy_profiling__c": "/maisonmargielapreferences/MaisonMargiela_ProfilingPrivacy"
    }
}

_languageIsoToDescMap = {
    "ca":"Catalan",
    "da":"Dansk",
    "de":"Deutsch",
    "el":"ελληνικά",
    "en":"English",
    "en_GB":"English",
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


def fillNewSfscJsonObj(drtBasicObj, newSfscJsonObject, lang, country, brand):
    print(brand + '>' + country + '>' + lang)
    percorso = brand + '>' + country + '>' + lang
    sfscBasicObj = {
        "LABEL": _languageIsoToDescMap[lang] if lang in _languageIsoToDescMap else lang,
        "LINK_Privacy_marketing__c": _brandsList[brand]['LINK_Privacy_marketing__c'],
        "LINK_Privacy_policy": _brandsList[brand]['LINK_Privacy_policy'],
        "LINK_Privacy_profiling__c": _brandsList[brand]['LINK_Privacy_profiling__c'],
        "SUB_TITLE_1": drtBasicObj['HEADER_SUB_1'] if 'HEADER_SUB_1' in drtBasicObj else "",
        "SUB_TITLE_2": drtBasicObj['FOOTER_SUB_1'] if 'FOOTER_SUB_1' in drtBasicObj else "",
        "TEXT_Communication_Data__c": drtBasicObj['COMMUNICATION_DATA'] if 'COMMUNICATION_DATA' in drtBasicObj else "",
        "TEXT_Privacy_general_consent_NAM__c": drtBasicObj['GENERAL_CONSENT_NAM'],
        "TEXT_Privacy_HK__c": "",
        "TEXT_Privacy_marketing__c": drtBasicObj['FLAG_MARKETING_OPTIN_TEXT'],
        "TEXT_Privacy_marketing_online__c": "",
        "TEXT_Privacy_profiling__c": drtBasicObj['FLAG_PROFILING_OPTIN_TEXT'],
        "TEXT_Privacy_text_message__c": drtBasicObj['FLAG_TEXT_MESSAGE'],
        "TEXT_Newsletter_Unsubscribe__c": "",#NOT PRESENT IN DRT
        "TEXT_Unsubscribe__c": "Unsubscribe TEXT",  #NOT PRESENT IN DRT
        "TITLE": "AUTHORIZATION FOR DATA PROCESSING"
    }
    if brand in newSfscJsonObject:
        if country in newSfscJsonObject[brand]:
            if lang in newSfscJsonObject[brand][country]:
                newSfscJsonObject[brand][country][lang] = sfscBasicObj
            else:
                newSfscJsonObject[brand][country][lang] = {}
                newSfscJsonObject[brand][country][lang] = sfscBasicObj
        else:
            newSfscJsonObject[brand][country] = {}
            newSfscJsonObject[brand][country][lang] = {}
            newSfscJsonObject[brand][country][lang] = sfscBasicObj
    else:
        newSfscJsonObject[brand] = {}
        newSfscJsonObject[brand][country] = {}
        newSfscJsonObject[brand][country][lang] = {}
        newSfscJsonObject[brand][country][lang] = sfscBasicObj

#Create DRT FILES JSON OBJECT (n files)
drtJsonObject = {}
print('Reading files...')
for fileEntry in os.scandir(_DRTJsonsDirectoryPath):
    if (fileEntry.path.endswith(".json")) and fileEntry.is_file():
        print(fileEntry.path) 
        fRead = open(fileEntry.path, encoding="utf-8")
        drtData = json.load(fRead)
        drtJsonObject[os.path.basename(fileEntry.path)[:-5]] = drtData
        fRead.close()

#CREATE SFSC FILE JSON OBJECT (1 file)
fRead = open(_SFSCJsonsFilePath, encoding="utf-8")
data = json.load(fRead)
fRead.close()
sfscJsonObject = data


print('Creating new JSON file...')
newSfscJsonObject = {}
for lang in drtJsonObject:
    for brand in drtJsonObject[lang]:
        for country in drtJsonObject[lang][brand]:
            drtBasicObj = drtJsonObject[lang][brand][country]['PRIVACY']
            if(lang == 'en_GB' and country == 'DEFAULT'):
                fillNewSfscJsonObj(drtBasicObj, newSfscJsonObject, 'en', 'INTERNATIONAL', brand)
            elif(lang == 'en_GB'):
                fillNewSfscJsonObj(drtBasicObj, newSfscJsonObject, 'en', country, brand)
            elif(country == 'DEFAULT'):
                fillNewSfscJsonObj(drtBasicObj, newSfscJsonObject, lang, 'INTERNATIONAL', brand)
            else:
                fillNewSfscJsonObj(drtBasicObj, newSfscJsonObject, lang, country, brand)
                
            

with open(_ResultFilePath, 'w', encoding='utf-8') as f:
    json.dump(newSfscJsonObject, f, ensure_ascii=False, indent=4)
    