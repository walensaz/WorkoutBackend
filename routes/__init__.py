from flask import Blueprint, Flask, jsonify, request, Request
from models.database import connect
routes = Blueprint('routes', __name__)

def extract_get(request: Request):
    args = request.args
    return tuple(args.values())

from .index import *
from .workout import *
