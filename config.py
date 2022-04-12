import logging
profile="dev"
if profile == "dev":
    from _config.dev import *
else:
    from _config.prod import *

