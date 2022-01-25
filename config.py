import logging
profile="dev"
if profile == "dev":
    from config.dev import *
else:
    from config.prod import *

logging.basicConfig(filename='easy_rights.log', encoding='utf-8', level=logging.DEBUG)