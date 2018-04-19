import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json 

class web_requests:
        
        def __init__(self):
                pass
        
        def send_request(self, data, url, api_key):

                body = str.encode(json.dumps(data))

                headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

                req = urllib2.Request(url, body, headers) 

                try:
                    response = urllib2.urlopen(req)

                    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
                    # req = urllib.request.Request(url, body, headers) 
                    # response = urllib.request.urlopen(req)

                    result = response.read()
                    #print(result)
                    return result
                except urllib2.HTTPError, error:
                    print("The request failed with status code: " + str(error.code))

                    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
                    print(error.info())

                    print(json.loads(error.read()))        
