import logging
profile="dev"
if profile == "dev":
    from _config.dev import *
else:
    from _config.prod import *


logging.basicConfig(filename='easy_rights.log', encoding='utf-8', level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")