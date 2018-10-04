"""
This module runs the application, starts flask's builtin
server on port 5000.
"""
from fastfoodfast import app
import os


if __name__ == '__main__':
    os.environ['DATABASE_URL'] = 'postgres://ongebo:nothing@127.0.0.1:5432/fffdb'
    app.run(debug=True)
