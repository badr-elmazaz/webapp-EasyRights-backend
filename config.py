profile="dev"
if profile == "dev":
    from config.dev import *
else:
    from config.prod import *