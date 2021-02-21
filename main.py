from flask import Flask, url_for, request, render_template, redirect, flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        return 'Post'
    else:
        flash('You were successfully logged in', 'error')
        return render_template('index.html')

#url_for('function')
#request.form['username']
#redirect(url_for('login'))
