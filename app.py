


from flask import Flask, request,render_template
import pickle
from datetime import datetime



app=Flask(__name__)

#loading the model
model=pickle.load(open('model_pickle','rb'))




@app.route('/')
def home():
    return render_template('home.html')



@app.route('/',methods=['POST'])
def predict():
    try:
        '''
        Required input for machine learning model
        1.open
        2.high
        3.low
        4.close
        5.volume
        6.cont_len
        7.cont_pol
        8.date_year
        9.date_month
        10.date_day
        11.sent_negative
        12.sent_neutral
        13.sent_positive
        '''
        # syntax-->     var_name=request.form['<name which in present in html form(index.html)>']
        query_open=request.form['open']
        query_high=request.form['high']
        query_low=request.form['low']
        query_close=request.form['close']
        query_volume=request.form['vol']
        query_date= request.form['date']
        query_cont_len=request.form['comment_length']
        query_cont_pol=request.form['polarity_score']
        query_cont_sent=request.form['tag']


        query_date=datetime.strptime(query_date, "%d-%m-%Y").date()
        date_year=query_date.strftime("%Y")
        date_month=query_date.strftime("%m")
        date_day=query_date.strftime("%d")

        #For neutral
        if query_cont_sent=="neutral":
            sent_neutral=1
            sent_positive=0
            sent_negative=0
        # For positive
        elif query_cont_sent=="positive":
            sent_neutral=0
            sent_positive=1
            sent_negative=0
        else:
        # For negative
            sent_neutral=0
            sent_positive=0
            sent_negative=1



        model_data=[[query_open,
                        query_high,
                        query_low,
                        query_close,
                        query_volume,
                        query_cont_len,
                        query_cont_pol,
                        date_year,
                        date_month,
                        date_day,
                        sent_negative,
                        sent_neutral,
                        sent_positive
                        ]]

        result=model.predict(model_data)

        if result==1:
            val1="Stock price is High"
        elif result == 0:
            val1="Stock Price is Low"
        else:
            val1="Insert Data"


        return render_template('home.html',comment=val1)
    except ValueError:
        return render_template('home.html')


if __name__=="__main__":
    app.run(debug=True)


