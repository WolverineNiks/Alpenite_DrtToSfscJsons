import json
_ResultFilePath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\GIT_2021.10.13 OTB_PrivacyJsonsConverter\\DrtJsonToSfscJson\\RESULT.json'
_outputFilePath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\GIT_2021.10.13 OTB_PrivacyJsonsConverter\\DrtJsonToSfscJson\\OUTPUT.json'

fRead = open(_ResultFilePath, encoding="utf-8")
data = json.load(fRead)
fRead.close()
sfscJsonObject = data

outputObj = {}
for country in sfscJsonObject['5_80'].keys():
    outputObj[country] = {}
    for lang in sfscJsonObject['5_80'][country].keys():
        basicObj = {
            'TEXT_Newsletter_Unsubscribe__c':sfscJsonObject['5_80'][country][lang]['TEXT_Newsletter_Unsubscribe__c'],
            'TEXT_Unsubscribe__c':sfscJsonObject['5_80'][country][lang]['TEXT_Unsubscribe__c']
        }
        outputObj[country][lang] = basicObj

with open(_outputFilePath, 'w', encoding='utf-8') as f:
    json.dump(outputObj, f, ensure_ascii=False, indent=4)