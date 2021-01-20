import pandas as pd
import numpy as np
import sqlite3 as sql
import smtplib, ssl

def read_csv():
    df = pd.read_csv ('Csv_example.csv')
    print(df)
    return(df)

def secure_connection():
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "chingatemonica@gmail.com"
    password = input("Type your password and press enter: ")

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)

    finally:
        server.quit()



secure_connection()


