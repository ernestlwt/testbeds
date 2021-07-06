from flask import Blueprint
from app.task import print_hello

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/')
def index():
    print("1")
    print_hello.delay()
    print("2")
    return "Hello World!", 200