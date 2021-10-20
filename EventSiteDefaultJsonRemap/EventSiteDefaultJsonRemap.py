"""
    This scripts takes default.json for Event Sites and remap it including brands.
"""
import json
import os

_defaultJsonFilePath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\GIT_2021.10.13 OTB_PrivacyJsonsConverter\\EventSiteDefaultJsonRemap\\default.json'
_ResultFilePath = 'C:\\Users\\NikhilChander\\Documents\\OTB\\GIT_2021.10.13 OTB_PrivacyJsonsConverter\\EventSiteDefaultJsonRemap\\RESULT.json'
_brandsGeneralMap = {
    '1_130': {
        "genericError": "Ops, something went wrong.",
        "tooLateError": "Sorry, you just missed it! That event is over but don't worry, we have plenty more exciting opportunities coming up.",
        "tooEarlyError": "Wait for us! We're not quite ready to launch yet, but stick around and make sure you're front of the queue when we do.",
        "notActiveError": "This event is not active.",
        "fullEventError": "Sorry, we're already maxed out for this event! Make sure you keep your eyes peeled for the next one.",
        "reCAPTCHAnotDoneError": "Please do the captcha before submit!",
        "error": "Error",
        "success": "Success",
        "successMessage": "Thanks for joining D:CODE! We've got so much to share with you (starting with personalised birthday and anniversary gifts, members-only promotions & collection preview and more…).",
        "opsErrMessage": "Ops, something went wrong.",
        "alreadyRegErrMessage": "It looks like you've already registered for this event. Don't worry, we all have those days.",
        "alreadyRegErrMessageFakeEvent": "You are already registered, please log in.",
        "notAvailErrMessage": "The event is not available"
    }, 
    '1_60': {
        "genericError": "Ops, something went wrong.",
        "tooLateError": "Sorry, you just missed it! That event is over but don't worry, we have plenty more exciting opportunities coming up.",
        "tooEarlyError": "Wait for us! We're not quite ready to launch yet, but stick around and make sure you're front of the queue when we do.",
        "notActiveError": "This event is not active.",
        "fullEventError": "Sorry, we're already maxed out for this event! Make sure you keep your eyes peeled for the next one.",
        "reCAPTCHAnotDoneError": "Please do the captcha before submit!",
        "error": "Error",
        "success": "Success",
        "successMessage": "Thanks for joining D:CODE! We've got so much to share with you (starting with personalised birthday and anniversary gifts, members-only promotions & collection preview and more…).",
        "opsErrMessage": "Ops, something went wrong.",
        "alreadyRegErrMessage": "It looks like you've already registered for this event. Don't worry, we all have those days.",
        "alreadyRegErrMessageFakeEvent": "You are already registered, please log in.",
        "notAvailErrMessage": "The event is not available"
    }, 
    '2_20': {
        "genericError": "Ops, something went wrong.",
        "tooLateError": "Sorry, you just missed it! That event is over but don't worry, we have plenty more exciting opportunities coming up.",
        "tooEarlyError": "Wait for us! We're not quite ready to launch yet, but stick around and make sure you're front of the queue when we do.",
        "notActiveError": "This event is not active.",
        "fullEventError": "Sorry, we're already maxed out for this event! Make sure you keep your eyes peeled for the next one.",
        "reCAPTCHAnotDoneError": "Please do the captcha before submit!",
        "error": "Error",
        "success": "Success",
        "successMessage": "Thank you!",
        "opsErrMessage": "Ops, something went wrong.",
        "alreadyRegErrMessage": "It looks like you've already registered for this event. Don't worry, we all have those days.",
        "alreadyRegErrMessageFakeEvent": "You are already registered, please log in.",
        "notAvailErrMessage": "The event is not available"
    }, 
    '4_40': {
        "iAgree": "Agree",
        "genericError": "Ops, something went wrong.",
        "tooLateError": "Sorry, you just missed it! That event is over but don't worry, we have plenty more exciting opportunities coming up.",
        "tooEarlyError": "Wait for us! We're not quite ready to launch yet, but stick around and make sure you're front of the queue when we do.",
        "notActiveError": "This event is not active.",
        "fullEventError": "Sorry, we're already maxed out for this event! Make sure you keep your eyes peeled for the next one.",
        "error": "Error",
        "success": "Success",
        "successMessage": "Thank you for joining Marni",
        "opsErrMessage": "Ops, something went wrong.",
        "alreadyRegErrMessage": "It looks like you've already registered for this event. Don't worry, we all have those days.",
        "alreadyRegErrMessageFakeEvent": "You are already registered.",
        "notAvailErrMessage": "The event is not available"
    }, 
    '5_80': {
        "iAgree": "Agree",
        "genericError": "Ops, something went wrong.",
        "tooLateError": "Sorry, you just missed it! That event is over but don't worry, we have plenty more exciting opportunities coming up.",
        "tooEarlyError": "Wait for us! We're not quite ready to launch yet, but stick around and make sure you're front of the queue when we do.",
        "notActiveError": "This event is not active.",
        "fullEventError": "Sorry, we're already maxed out for this event! Make sure you keep your eyes peeled for the next one.",
        "reCAPTCHAnotDoneError": "Please do the captcha before submit!",
        "error": "Error",
        "success": "Success",
        "successMessage": "Thank you for joining Maison Margiela",
        "opsErrMessage": "Ops, something went wrong.",
        "alreadyRegErrMessage": "It looks like you've already registered for this event. Don't worry, we all have those days.",
        "alreadyRegErrMessageFakeEvent": "You are already registered.",
        "notAvailErrMessage": "The event is not available"
    }
}

fRead = open(_defaultJsonFilePath, encoding="utf-8")
data = json.load(fRead)
fRead.close()
defaultJsonObj = data
newDefaultJsonObj = {}
for brand in _brandsGeneralMap.keys():
    newDefaultJsonObj[brand] = {}
    for lang in defaultJsonObj.keys():
        newDefaultJsonObj[brand][lang] = {}
        multipleKeysObj = {}
        for brandMapKey in _brandsGeneralMap[brand].keys():
            if brandMapKey not in newDefaultJsonObj[brand][lang]:
                newDefaultJsonObj[brand][lang][brandMapKey] = _brandsGeneralMap[brand][brandMapKey]
            elif newDefaultJsonObj[brand][lang][brandMapKey] == '':
                newDefaultJsonObj[brand][lang][brandMapKey] = _brandsGeneralMap[brand][brandMapKey]
        for defaultMapKey in defaultJsonObj[lang].keys():
            if defaultMapKey not in newDefaultJsonObj[brand][lang]:
                newDefaultJsonObj[brand][lang][defaultMapKey] = defaultJsonObj[lang][defaultMapKey]
            elif newDefaultJsonObj[brand][lang][brandMapKey] == '':
                newDefaultJsonObj[brand][lang][brandMapKey] = defaultJsonObj[lang][defaultMapKey]

with open(_ResultFilePath, 'w', encoding='utf-8') as f:
    json.dump(newDefaultJsonObj, f, ensure_ascii=False, indent=4)