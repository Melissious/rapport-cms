import os
from app import create_app, db

app = create_app(os.getenv("CMS_CONFIG") or 'default')

if __name__ == '__main__':
    app.run()
