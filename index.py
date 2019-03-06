from flask import Flask
# import parser
from pars import main

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/avito")
def parser_Main():
    # try:
    #     main()
    # except BaseException as err:
    #     print('ошибка\n {}'.format(err))
    main()

    return '''
    <html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + main() + '''!</h1>
    </body>
</html>'''

if __name__ == "__main__":
    app.run()