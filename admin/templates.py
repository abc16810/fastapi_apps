from .constants import BASE_DIR
from starlette.templating import Jinja2Templates
import os


templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))