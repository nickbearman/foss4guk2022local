#!/usr/bin/env python
# coding: utf-8

# ### Requirements
# pandas              1.4.3  <br>
# requests            2.28.1 <br>
# psycopg2            2.9.3 <br>
#

# # OS Downloads API - Open Data



import os
import pandas as pd
import requests as r
import json
import hashlib
import zipfile
import psycopg2

#Get the result of the OS Downloads API call
open_prod = r.get('https://api.os.uk/downloads/v1/products').json()


#Load view into DataFrame
df = pd.DataFrame(open_prod)
df


#define download location
download_loc = r''


#create download function
def download_file(url,file):
    with r.get(url, stream=True) as d:
        d.raise_for_status()
        with open(download_loc+'/'+file, 'wb') as f:
            for chunk in d.iter_content(chunk_size=8192):
                f.write(chunk)
    return download_loc


# ## What is MD5?
# MD5 (message-digest algorithm) is a cryptographic protocol used for authenticating messages as well as content verification and digital signatures. MD5 is based on a hash function that verifies that a file you sent matches the file received by the person you sent it to.


#create md5 function
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


#define our product of interest
open_product = 'OpenRivers'


df = df.loc[df['id'] == open_product] #locate the correct product
product = r.get(df.iloc[0]['url']).json() #get URL request for product
download = product['downloadsUrl'] #find the download URL
filetypes = r.get(download).json() #get filetypes with download URLs
pd.DataFrame(filetypes)


#define desired filetype
download_filetype = 'GeoPackage'

#find the right filetype
for x in range(len(filetypes)):
    if filetypes[x]['format'] == download_filetype:
        #download the file
        download_file(filetypes[x]['url'],filetypes[x]['fileName'])
        #check the file md5's match
        if md5(download_loc +'/'+ filetypes[x]['fileName']) == filetypes[x]['md5']:
            print('Successfully Downloaded ')
            file_path = download_loc +'\\'+ filetypes[x]['fileName']
        else:
            print('MD5 does not match')


#unzip the file
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall(download_loc+'\\'+open_product)
path = os.listdir(download_loc+'\\'+open_product +'\\' + 'data')
file = download_loc+'\\'+open_product +'\\' + 'data' + '\\' + path[0]


#create schema
#if using Linux use getpass.getuser() as the variable in schema creation

#connection details
dbname = 'foss4g'
host = '18.135.248.161'
port = '5432'
user = 'postgres'
password = 'V2ql011Bw5A6'

conn_local = psycopg2.connect(database="postgres", user=f"postgres", password=f"password",host="localhost")
#conn_cloud = psycopg2.connect(database=dbname, user=user, password=password,host=host)
cursor = conn_local.cursor()
sql = f'''CREATE SCHEMA IF NOT EXISTS {os.getlogin( )}; '''
cursor.execute(sql)
conn_local.commit()
conn_local.close()

#create schema if you have postgresql installed
#if using Linux use getpass.getuser() as the variable in schema creation
pg_connection = '-d postgres -U postgres -p password -h localhost -p 5432'
create_schema = f'''psql {pg_connection} -c "CREATE SCHEMA IF NOT EXISTS {os.getlogin( )}"'''
print(create_schema)
os.system(create_schema)


#load data if you have ogr2ogr
#if using Linux use getpass.getuser() as the variable in active_schema
pg_connection_ogr = f'PG:"dbname=postgres user=postgres password=password active_schema={os.getlogin( )} host=localhost port=5432"'
#pg_connection_ogr = f'PG:"dbname={dbname} user={user} password={password} active_schema={os.getlogin( )} host={host} port={port}"'
command = f'ogr2ogr -f PostgreSQL {pg_connection_ogr} {file}'
print(command)
os.system(command)

