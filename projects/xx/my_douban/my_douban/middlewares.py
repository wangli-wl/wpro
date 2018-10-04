from settings import USER_AGENTS
from settings import PROXIES
import random

class User_agentMiddleware(object):
    def process_request(self,request,spider):
        useragent = random.choice(USER_AGENTS)
        print useragent
        request.headers.setdefault(useragent)
class ProxyMiddleware(object):
    def process_request(self,request,spider):
        proxy = random.choice(PROXIES)
        print proxy
        request.meta['proxy'] = "http://"+proxy['ip_port']

