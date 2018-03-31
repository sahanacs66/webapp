from flask import render_template
from app import app
from app.forms import RegisterForm,LoginForm,SearchForm
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user, login_user
from app.models import User
from flask import request , redirect , url_for, flash
from app import db
from app import client
from app import es
from app import login
from flask import session
import requests, json


@app.route('/index',methods=['GET','POST'])
def index():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,FirstName=form.firstName.data,LastName=form.lastName.data,email=form.email.data,password=form.password.data)
        result = User.query.filter_by(username=form.username.data).first()
        if(result):
            flash('username already exists')
            return redirect('/index')
        else:
            session['username'] = result
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect('/search')

    return render_template('index.html' , title='Register In', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/loggedin')
    form = LoginForm()
    if form.validate_on_submit():
        print("hi")
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        else:
            login_user(user)
            return redirect('/loggedin')
    return render_template('login.html', title ='login', form=form)

@login_required
@app.route('/loggedin',methods=['GET','POST'])
def loggedin():
    form = SearchForm()
    return render_template("search.html", title='Home Page',form=form)

@login_required
@app.route('/search',methods=['GET','POST'])
def search():
    form = SearchForm()
    if not form.validate_on_submit():
        return redirect('/loggedin')
    return redirect(url_for('search_results',query=form.search.data))

@login_required
@app.route('/search_results/<query>')
def search_results(query):
    print(query)
    _index = 0
    if request.args.get('start'):
        if request.args.get('start') != None or request.args.get('start') != '':
            _index = request.args.get('start')
    data = {}
    result = performQuery(query,_index)
    last_index = 0
    count = 0

    for d in result['hits']['hits']:
        re = d['_source']
        _id = re['id']
        data[_id] = re
        last_index = _id
        count += 1

    print(data)
    return render_template("results.html",title="results",result=data,q=query,last_index=last_index,count=count)


def performQuery(term,_index):
    # Fetch from ES. Return id and Station Name and check for city and station name
    result = es.search(index="stn",doc_type="station",body={"from" : _index, "size" : 10,"query":{"multi_match":{"query":term,"type":"cross_fields","fields":["city","stationName","status","location"],"operator":"or"}}})
    return result

@login_required
@app.route('/search_detail/<int:id>')
def search_detail(id):
    print(id)
    result = filterResult(id)
    data = {}
    for k,v in result.items():
        if(k!='_id'):
            data[k] = v
    print(result)

    return render_template("detail.html",title="detail",result=data)


def filterResult(term):
    if term:
       database = client['sample']
       coll_stations = database['stations']
       result = coll_stations.find_one({"id":term})
    return result


@app.route('/logout')
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('index'))
