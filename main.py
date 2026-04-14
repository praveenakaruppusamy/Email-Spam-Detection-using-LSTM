from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
from datetime import date
import time
import mysql.connector
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
import datetime

x = datetime.datetime.now()

#print(x.year)
date=x.strftime("%d-%m-%Y")
time1=x.strftime("%X")
@app.route("/")
def homepage():
    return render_template('index1.html')
@app.route("/inbox")
def inbox():
    smailid = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where rmailid='" + smailid + "' and status='Normal' and mstatus='0'")
    data = cursor.fetchall()
    return render_template('inbox.html',data=data)
@app.route("/compose")
def compose():
    return render_template('compose.html')
@app.route("/send")
def send():
    smailid = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where smailid='" + smailid + "' and mstatus='0'")
    data = cursor.fetchall()
    return render_template('send.html',data=data)
@app.route("/spam")
def spam():
    smailid = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where rmailid='" + smailid + "' and status='Fraudulent' and mstatus='0'")
    data = cursor.fetchall()
    return render_template('spam.html',data=data)
@app.route("/Theft")
def Theft1():
    smailid = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where rmailid='" + smailid + "' and status='Suspicious' and mstatus='0'")
    data = cursor.fetchall()

    return render_template('theft.html',data=data)
@app.route("/Social")
def social():
    smailid = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where rmailid='" + smailid + "'and status='Harrasment' and mstatus='0'")
    data = cursor.fetchall()
    return render_template('social.html',data=data)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      uname = request.form['uname']
      password = request.form['password']
      username = request.form['uname']
      password = request.form['password']
      session['uname'] = request.form['uname']
      conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
      cursor = conn.cursor()
      cursor.execute("SELECT * from register where email='" + username + "' and password='" + password + "'")
      data = cursor.fetchone()

      if data is None:
          return 'Username or Password is wrong'
      else:
          return render_template('inbox.html')

      return render_template('index.html')
@app.route("/newregister", methods=['GET', 'POST'])
def newregister():
    if request.method == 'POST':
        n = request.form['name']
        dob = request.form['dob']
        address = request.form['address']
        pnumber = request.form['pnumber']
        email = request.form['email']
        password = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO register VALUES ('','" + n + "','" + dob + "','" + address + "','" + pnumber + "','" + email + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'
        return render_template('index1.html')

@app.route("/mail", methods=['GET', 'POST'])
def mail():

    if request.method == 'POST':
        rmailid = request.form['mailto']
        msubject = request.form['msubject']
        message = request.form['message']
        data = [message]
        from tensorflow.keras.models import load_model
        from tensorflow.keras.preprocessing.text import Tokenizer
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        import numpy as np
        # Step 1: Load the pre-trained model
        model = load_model('spam_analysis_lstm.h5')  # Use your model's path
        # Step 2: Prepare the tokenizer (use the same tokenizer used during training)
        tokenizer = Tokenizer(num_words=10000)  # Same parameters used during training
        # Example data
        texts = data
        # Step 3: Preprocess the text data
        tokenizer.fit_on_texts(texts)  # Fit the tokenizer (if not saved)
        sequences = tokenizer.texts_to_sequences(texts)
        max_sequence_length = 100  # Same length used during training
        padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)
        # Step 4: Predict sentiment using the model
        predictions = model.predict(padded_sequences)
        print(predictions)
        rounded_numbers = [round(num) for num in predictions[0]]
        print(rounded_numbers)
        labels = ["Normal", "Fraudulent", "Harrasment", "Suspicious"]
        predicted_labels = [labels[np.argmax(pred)] for pred in predictions]
        print(predicted_labels[0])
        status=predicted_labels[0]
        #sname=session['uname']
        smailid=session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
        cursor = conn.cursor()
        cursor.execute("SELECT * from register where email='" + smailid + "'")
        data = cursor.fetchone()
        print(data)
        sname=data[1]
        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
        cursor1 = conn1.cursor()
        cursor1.execute("SELECT * from register where email='" + rmailid + "'")
        data1 = cursor1.fetchone()
        print(data1)
        rname = data1[1]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mail VALUES ('','" + str(sname) + "','" + smailid + "','" + str(rname) + "','" + rmailid + "','" + msubject + "','" + message + "','"+status+"','0','"+date+"','"+time1+"')")
        conn.commit()
        conn.close()
        return render_template('inbox.html')
@app.route("/register")
def register():
    return render_template('register.html')
@app.route("/view")
def view():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where id='" + id + "'")
    data = cursor.fetchone()
    return render_template('view.html',data=data)
@app.route("/view1")
def view1():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where id='" + id + "'")
    data = cursor.fetchone()
    return render_template('view1.html',data=data)
@app.route("/view2")
def view2():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where id='" + id + "'")
    data = cursor.fetchone()
    return render_template('view2.html',data=data)
@app.route("/view3")
def view3():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where id='" + id + "'")
    data = cursor.fetchone()
    return render_template('view3.html',data=data)
@app.route("/view4")
def view4():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='spammail')
    cursor = conn.cursor()
    cursor.execute("SELECT * from mail where id='" + id + "'")
    data = cursor.fetchone()
    return render_template('view4.html',data=data)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)