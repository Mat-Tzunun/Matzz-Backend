import os

db_host = os.environ.get('MYSQL_HOST', 'localhost')
db_user = os.environ.get('MYSQL_USER', 'root')
db_password = os.environ.get('MYSQL_PASSWORD', '54628')
db_name = os.environ.get('MYSQL_DB', 'matzz')
db_port = os.environ.get('MYSQL_PORT', '3306')

env = os.environ.get('ENV', 'development')
debug_mode = True if env == 'development' else False
openai_api_key = os.environ.get(
    'OPENAI_API_KEY', 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
