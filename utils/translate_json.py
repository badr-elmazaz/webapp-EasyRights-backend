import deepl
from googletrans import Translator
translator = Translator()
import traceback
import json


# translation = translator.translate("ciao mondo")
# print(translation)

def trans(a: str):
    # return deepl.translate(source_language="EN", target_language="AR", text=a)
    print(f"trying to translate this sentence: {a}")
    try:
        txt= translator.translate(a, src='en',dest="uk")
        return txt.text
    except:
        return "ERROR TRANSLATING"
        traceback.print_exc()


with open("languages.json") as f:
    json_en=json.load(f)

# translate to Italian
for k in json_en:
    if "label" in k.keys():
        k["label"] = trans(k["label"])
    if "title" in k.keys():
        k["title"] = trans(k["title"])
    if "answers" in k:
        for j in k["answers"]:
            if "label" in j.keys():
                j["label"] = trans(j["label"])
            if "helperText" in j.keys():
                j["helperText"] = trans(j["helperText"])

with open("../ukrainian.json", "w") as f:
    json.dump(json_en, f)