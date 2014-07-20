from flask import Flask

app = Flask(__name__)

import blog.db
import blog.views