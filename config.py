"""[General Configuration Params]
"""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
publicdir = path.abspath(path.dirname(__file__)) + "/public/"
load_dotenv(path.join(basedir, '.env'))
