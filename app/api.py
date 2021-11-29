import json
from typing import List, cast
from flask import Blueprint, request, jsonify
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login.utils import login_required, current_user
import cloudpickle
import pandas as pd
import numpy as np
from datetime import datetime
import sqlalchemy
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash
from app.forms import PredictionForm
from .utils.regression_plot import get_regression_plot
from .models.history import History
from . import db, model, TITLE, input_boundaries
import requests
from .models.user import User
import re

api = Blueprint('api', __name__)


with open('./app/static/output_boundaries.p', 'rb') as output_bounds_file:
    output_boundaries = cloudpickle.load(file=output_bounds_file)


# Get regression plot API
from flask.wrappers import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from matplotlib import pyplot as plt
import warnings

warnings.filterwarnings('ignore')

@api.route('/api/reg/<userid>', methods=['GET'])
def get_reg_plot(userid):
    latest_prediction = get_latest_prediction(userid=userid)
    if latest_prediction is not None:
        fig = get_regression_plot(pipeline=model, bedrooms=latest_prediction.bedrooms, floor_area_sqm=latest_prediction.floor_area, approval_date=latest_prediction.approval_date, lease_commencement_year=latest_prediction.lease_commencement_year, input_bounds=input_boundaries)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    return Response()

# Get user API
def get_user(user_id):
    try:
        return User.query.filter_by(id=int(user_id)).first()
    except Exception as e:
        flash(str(e))

@api.route('/api/user/get/<userid>', methods=['GET'])
def get_user_api(userid):
    user: User = get_user(user_id=userid)
    data = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'password': user.password
    }
    return jsonify(data)


# Add user API
def add_new_user(email, username, password):
    try:
        new_user = User(email=email, username=username,
                        password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return new_user.id
    except sqlalchemy.exc.IntegrityError as err:
        raise err


@api.route('/api/user/add', methods=['POST'])
def add_new_user_api():
    try:
        data = request.get_json()
        if type(data) is str:
            data = json.loads(data)
        email = data['email']
        username = data['username']
        password = data['password']
        new_user_id = add_new_user(email=email, username=username, password=password)
        return jsonify({'new_user_id': new_user_id})
    except sqlalchemy.exc.IntegrityError as e:
        return jsonify({'error': 'Email or Username has already been taken!'})

# Get one API
def get_latest_prediction(userid):
    try:
        return History.query.filter_by(userid=userid).order_by(History.id.desc()).first()
    except Exception as e:
        flash(str(e), category='prediction')


@api.route("/api/prediction/get/latest/<userid>", methods=['GET'])
def get_latest_prediction_api(userid):
    latest_prediction: History = cast(
        History, get_latest_prediction(userid=int(userid)))
    data = {
        'id': latest_prediction.id,
        'userid': latest_prediction.userid,
        'floor_area': latest_prediction.floor_area,
        'bedrooms': latest_prediction.bedrooms,
        'approval_date': datetime.strftime(latest_prediction.approval_date, '%Y-%m-%d'),
        'lease_commencement_year': latest_prediction.lease_commencement_year,
        'resale_pred': latest_prediction.resale_prediction
    }
    return jsonify(data)


# Get all API
def get_all_predictions(userid, limit=None):
    try:
        if limit is None:
            return History.query.filter_by(userid=userid).order_by(History.id.desc())
        return History.query.filter_by(userid=userid).order_by(History.id.desc()).limit(limit)
    except Exception as e:
        flash(str(e), category='prediction')


@api.route('/api/prediction/get/<userid>', methods=['GET'])
def get_all_predictions_api(userid):
    limit = request.args.get('limit')
    all_predictions: List[History] = cast(
        List[History], get_all_predictions(userid=int(userid), limit=limit))
    data = [{
        'id': prediction.id,
        'userid': prediction.userid,
        'floor_area': prediction.floor_area,
        'bedrooms': prediction.bedrooms,
        'approval_date': datetime.strftime(prediction.approval_date, '%Y-%m-%d'),
        'lease_commencement_year': prediction.lease_commencement_year,
        'resale_pred': prediction.resale_prediction
    } for prediction in all_predictions]
    return jsonify(data)


# Add API
def store_prediction(userid, floor_area, bedrooms, approval_date, lease_commencement_year, resale_pred):
    try:
        new_record = History(
            userid=userid,
            floor_area=floor_area,
            bedrooms=bedrooms,
            approval_date=approval_date,
            lease_commencement_year=lease_commencement_year,
            resale_prediction=resale_pred,
            predicted_on=datetime.utcnow()
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record.id
    except Exception as e:
        db.session.rollback()
        flash(str(e), category='prediction')


@api.route('/api/prediction/add', methods=['POST'])
def store_prediction_api():
    data = request.get_json()
    if type(data) is str:
        data = json.loads(data)
    userid = int(data['userid'])
    floor_area = float(data['floor_area'])
    bedrooms = int(data['bedrooms'])
    approval_date = datetime.strptime(data['approval_date'], '%Y-%m-%d')
    lease_commencement_year = int(data['lease_commencement_year'])
    resale_pred = float(data['resale_pred'])
    new_id = store_prediction(userid=userid, floor_area=floor_area, bedrooms=bedrooms,
                              approval_date=approval_date, lease_commencement_year=lease_commencement_year, resale_pred=resale_pred)
    return jsonify({'new_id': new_id})


# New Prediction API
def new_prediction(floor_area, bedrooms, approval_date, lease_commencement_year):
    X = pd.DataFrame(
        data=np.array([
            [floor_area,
             approval_date,
             lease_commencement_year,
             bedrooms]
        ]),
        columns=['floor_area_sqm', 'approval_date',
                 'lease_commencement_year', 'bedrooms']
    )
    return max(model.predict(X=X)[0], output_boundaries['min'])


@api.route('/api/predict', methods=['POST'])
def new_prediction_api():
    data = request.get_json()
    if type(data) is str:
        data = json.loads(data)

    floor_area = float(data['floor_area'])
    bedrooms = int(data['bedrooms'])
    approval_date = datetime.strptime(data['approval_date'], '%Y-%m-%d')
    lease_commencement_year = int(data['lease_commencement_year'])

    resale_pred = new_prediction(floor_area=floor_area, bedrooms=bedrooms,
                                 approval_date=approval_date, lease_commencement_year=lease_commencement_year)

    return jsonify({'resale_pred': resale_pred})


# Predict API
@api.route('/predict', methods=['POST'])
@login_required
def predict():
    form = PredictionForm(request.form)
    if form.validate():
        user = current_user

        result = {k: v for k, v in request.form.items()}
        response = requests.post(
            url=request.host_url[:-1] + url_for('api.new_prediction_api'), json=json.dumps(result))

        resale_pred = response.json()['resale_pred']
        result['resale_pred'] = resale_pred
        result['userid'] = user.id

        response = requests.post(
            url=request.host_url[:-1] + url_for('api.store_prediction_api'), json=json.dumps(result)
        )

        flash(str(resale_pred), category='prediction')
        return redirect(url_for('routes.home'))
    else:
        return render_template('home.html', title=TITLE, target='home', show='new', form=form)



# Delete API
def remove_prediction(prediction_id):
    try:
        record = History.query.get(prediction_id)
        db.session.delete(record)
        db.session.commit()
        return 0
    except Exception as error:
        db.session.rollback()
        flash(str(error), category="prediction")
        return 1


@api.route('/api/delete/<pred_id>', methods=['DELETE'])
def remove_prediction_api(pred_id):
    result = remove_prediction(prediction_id=int(pred_id))
    if result == 0:
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'fail'})


@api.route('/remove', methods=['POST'])
def delete_record():
    pred_id = request.form['id']
    response = requests.delete(url=request.host_url[:-1] + url_for('api.remove_prediction_api', pred_id=pred_id))
    if response.json()['result'] != 'ok':
        flash('Error deleting record', category='error')
        past_predictions = get_all_predictions(userid=current_user.id)
        render_template('home.html', title=TITLE, target='home', show='history', past_predictions=past_predictions)
    return redirect(url_for('routes.history'))