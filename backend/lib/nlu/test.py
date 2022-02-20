import requests
import json
#from sutime import SUTime

#sutime = SUTime(mark_time_ranges=True, include_range=True)

properties = {
    "annotators": "tokenize,ner",
    "outputFormat": "json",
    "ner.docdate.usePresent": "true",
    "sutime.includeRange": "true",
    "sutime.markTimeRanges": "true"
}

print("Reached")
#print(sutime.parse("How many people have been infected with COVID on the 30th of November?"))
res = requests.post(f'http://localhost:9000/?properties={json.dumps(properties)}',
                    data={'data': 'How many people have been infected with COVID on the 30th of November?'}).text

print(res)


