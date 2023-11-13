from flask import Flask
from url_shortener.routes import bp  
from url_shortener.__init__ import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
