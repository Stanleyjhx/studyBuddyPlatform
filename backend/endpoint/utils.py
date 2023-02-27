from flask_restful import reqparse


def get_parser(params):
    parser = reqparse.RequestParser()
    for param, param_type in params.items():
        parser.add_argument(param, type=param_type)
    return parser
