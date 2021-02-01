from smtplib import SMTP
import pandas as pd
import sqlite3 as sql
import smtplib, ssl
import json


def read_csv(): # function to read csv file
    f_csv = pd.read_csv('Csv_example.csv') # use pandas for read csv
    f_csv = pd.DataFrame(f_csv) # use pandas to convert csv in dataframe
    #print(f_csv)
    return f_csv

def read_json(): # function to read json file
    with open('testjson.json', 'r') as f: # read json file
        f_json = json.load(f) # data in variable f
        f_json = pd.DataFrame.from_dict(f_json, orient="index") # use pandas to convert f in dataframe
        f_json = f_json.T # transpose dataframe
        #print(f_json)
    return f_json

def database_construction(df_csv,df_json):

    df_conct = pd.concat([df_csv,df_json], axis=1) # concatenate dataframes from csv and json
    df_conct=df_conct.drop(["row_id","user_state","userid"], axis=1) # eliminate not necessary columns
    conn = sql.connect("test_database.db") # create and connect with database using sql from sqlite3
    df_conct.to_sql("user", conn, if_exists="replace") # create a new table (using as name "user") if exist replace
    conn = sql.connect("test_database.db") # connect with database
    df_database = pd.read_sql("SELECT * FROM user", conn) # read database from sql using pandas
    #print(df_database) # print database
    return df_database


def class_val(database):
    email_array=[]
    database_name=[]
    index = database.index
    condition = database["classification"] == "high"
    class_val_indices=index[condition]
    class_val = class_val_indices.tolist()
    classification="high"
    for i in class_val:
        email_manager = database.iloc[i]["user_manager"]
        email_array +=[email_manager]
        basename = database.iloc[i]["database_name"]
        database_name += [basename]
        print(database_name)
    return (email_array,classification,database_name)

def email_data(owner_email):
    sender_email = input("Type your email and press enter: ")
    password = input("Type your password and press enter: ")
    receiver_email = owner_email
    return sender_email, password, receiver_email

def secure_connection(sender_email, password, receiver_email,database_name):

    for i in receiver_email and database_name:
        receiver_email=i
        print(receiver_email)
        print(database_name)
        message = "your database is high"
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        # Create a secure SSL context
        context = ssl.create_default_context()
        # Try to log in to server and send email

        try:
            server: SMTP = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            print(e)

        finally:
            server.quit()

df_json = read_json()
df_csv = read_csv()
database=database_construction(df_csv,df_json)
owner_email, classification, database_name = class_val(database)
if classification == "high":
    print("Some databases has high classification send email to owner")
    se, ps, re = email_data(owner_email)
    secure_connection(se, ps, re, database_name)
