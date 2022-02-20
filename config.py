import logging
profile="dev"
if profile == "dev":
    from _config.dev import *
else:
    from _config.prod import *


BLOCK_ALL_THEY_DIDNT_PAY_US=False