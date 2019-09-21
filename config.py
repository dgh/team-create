import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	# for heroku
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
	
	POSTS_PER_PAGE = 8
	
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-silly-secret-key'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False