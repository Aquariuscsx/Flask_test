from flask import Flask, Blueprint

admin = Blueprint("admin", __name__)

import app.admin.views