import http.client, urllib.parse, json, csv

subscriptionKey = "224bb0ef6cd348fe9a5e68be95525d22"

host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"

def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."

    addquery = '&count=10&offset=0&mkt=en-US'

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query + addquery, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

init = ['"District"', '"School"', '"Charter"']
intitle = ['Contact','Staff','Faculty']
searchterm = ['"ESL"', '"ELL"', '"Adult"', '"Special Ed"', '"remediation" read','"ESOL"', '"Literacy"', '"GED"']
domain = ['.us','.ca','.edu','.org','.net']


with open('combined.csv', 'a', newline = '') as l:

    fieldnames = ['NAME', 'URL', 'TERM']

    writer = csv.DictWriter(l, fieldnames=fieldnames)
    writer.writeheader()

    for ini in init:

        for intit in intitle:

            for term in searchterm:

                for dom in domain:

                    searchphrase = ini+' intitle:'+ intit + ' ' + term + ' site:' + dom

                    #savefile = term.strip('""') + ini.strip('""') +intit + dom[1:].upper()
                        #writer.writeheader()

                    if len(subscriptionKey) == 32:

                        try:

                            print('Searching the Web for: ', searchphrase)

                            headers, result = BingWebSearch(searchphrase)

                            jsonResponse = json.loads(json.dumps(json.loads(result), indent=4))

                            #print (type(jsonResponse["webPages"]['value']))


                            for item in jsonResponse['webPages']['value']:

                                if jsonResponse['webPages']['value'].index(item) < 10:

                                    writer.writerow({'NAME':item['name'], 'URL':item['url'], 'TERM':searchphrase})




                            #print (jsonResponse['webPages'])
                        except:

                            pass


                    else:

                        print("Invalid Bing Search API subscription key!")
                        print("Please paste yours into the source code.")
