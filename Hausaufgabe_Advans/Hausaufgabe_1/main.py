from flask import Flask, request

main = Flask(__name__)

@main.route("/")
def hallo_flask():
    return 'Hallo Flask !'

@main.route("/user/<name>")
def get_user_name(name):
    return f'Hallo {name} !'


if __name__ == '__main__':
    main.run(debug=True)
