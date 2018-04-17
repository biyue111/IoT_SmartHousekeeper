from web_requests import web_request
import config_noIoT as config_noIoT

def format_data(data, d, v):
  ind = data["inputs"]["input2"]["ColumnNames"].index(d)
  data["inputs"]["input2"]["Values"][ind] = v
  
  return data


request = web_request()
data = format_data(data, "temperature", 20)
data = format_data(data, "humidity", 20)
request.send_request(data, config_noIoT.web_url, config_noIoT.api_key)
