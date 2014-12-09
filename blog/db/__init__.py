from flask.ext.sqlalchemy import SQLAlchemy
from ..app import app

db = SQLAlchemy(app)

from .users import Users
from .pas_tag import pas_tag
from .tags import Tags
from .passages import Passages
from .comments import Comments
from .talks import Talks
from .votes import Votes
from .details import Details
from .friends import Friends
from .reports import Reports
