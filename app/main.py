from graphene import ObjectType, String, Field, Schema, List, Int
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.graphql import GraphQLApp
import json
import os
import urllib.request
from sqlalchemy import create_engine
from fastapi.encoders import jsonable_encoder
import base64
import requests
import sqlite3

from check_args import check_args


con = sqlite3.connect('example.db')

DBPASSWORD = os.environ.get('DBPASSWORD')
DBUSER = os.environ.get('DBUSER')
DBHOST = '192.168.31.177'
DBNAME = 'forestry_bd'

DATABASE_URL = 'postgresql://' + DBUSER + ':' + DBPASSWORD +  '@192.168.31.177/forest_bd_work'

db = create_engine(DATABASE_URL)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def index():

    return 'd'
