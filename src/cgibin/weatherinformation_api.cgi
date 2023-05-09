#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from routes import app

CGIHandler().run(app)