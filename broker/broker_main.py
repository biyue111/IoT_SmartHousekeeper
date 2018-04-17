from web_requests import web_request
import config_noIoT as config_noIoT

request = web_request()
data = config_noIoT.data_format % (10, 50)
request.send_request(data, config_noIoT.web_url, config_noIoT.api_key)
