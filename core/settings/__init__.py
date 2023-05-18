import os
from dotenv import load_dotenv
load_dotenv()
from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
# Now you can access the MYPROJECT_ENV variable using the os module:
MYPROJECT_ENV = os.getenv("MYPROJECT_ENV")
# if os.environ.get('MYPROJECT_ENV') == 'dev':
if os.getenv("MYPROJECT_ENV"):
   from .dev import *
else:
   from .prod import *