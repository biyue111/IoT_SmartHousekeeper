from web_requests import web_request
import config_noIoT as config_noIoT

web_request.send_request(config_noIoT.data, config_noIoT.web_url, config_noIoT.api_key)
