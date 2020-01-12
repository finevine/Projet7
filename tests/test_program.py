import program.download_agents as script

import urllib.request

from io import BytesIO
import json

# def hello(name):
#     return 'Hello ' + name

# def test_hello():
#     assert hello('Celine') == 'Hello Celine'

# def test_http_return(monkeypatch):
#     results = [{
#             "age": 84,
#             "agreeableness": 0.74
#           }
#         ]

#     def mockreturn(request):
#         return BytesIO(json.dumps(results).encode())

#     monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)
#     assert script.get_agents(1) == results