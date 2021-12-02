# Data Manipulation Dependencies
from datetime import datetime
import numpy as np
import pandas as pd

# Application Dependencies
import requests
import sqlalchemy

from flask import Blueprint, json, jsonify, redirect, request
from flask.wrappers import Response
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login.utils import login_required, current_user

from werkzeug.security import generate_password_hash

# Graphing Dependencies
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Custom Dependencies
from .. import OUTPUT_BOUNDARIES, db, MODEL, TITLE, INPUT_BOUNDARIES
from ..forms.prediction_form import PredictionForm
from ..models.history import History
from ..models.user import User
from ..utils.regression_plot import get_regression_plot

# Miscellaneous Dependencies
from warnings import filterwarnings
from typing import List, cast
import io


# Instantiate Blueprint
api = Blueprint('api', __name__)


# Get regression plot API
@api.route('/api/reg/<userid>', methods=['GET'])
def get_reg_plot(userid):
    filterwarnings('ignore')
    latest_prediction = get_latest_prediction(userid=userid)
    if latest_prediction is not None:
        fig = get_regression_plot(pipeline=MODEL, bedrooms=latest_prediction.bedrooms, floor_area_sqm=latest_prediction.floor_area, approval_date=latest_prediction.approval_date,
                                  lease_commencement_year=latest_prediction.lease_commencement_year, input_bounds=INPUT_BOUNDARIES, resale_price=latest_prediction.resale_prediction)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    return Response()


# Get user API
def get_user(user_id):
    try:
        return User.query.filter_by(id=int(user_id)).first()
    except Exception as e:
        flash(str(e), category='error')


@api.route('/api/user/get/<userid>', methods=['GET'])
def get_user_api(userid):
    user: User = get_user(user_id=userid)  # type: ignore
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
        email = data['email']  # type: ignore
        username = data['username']  # type: ignore
        password = data['password']  # type: ignore
        new_user_id = add_new_user(
            email=email, username=username, password=password)
        return jsonify({'new_user_id': new_user_id})
    except sqlalchemy.exc.IntegrityError:
        return jsonify({'error': 'Email or Username has already been taken!'}), 500


# Get latest prediction API
def get_latest_prediction(userid):
    try:
        return History.query.filter_by(userid=userid).order_by(History.id.desc()).first()
    except Exception as e:
        flash(str(e), category='error')


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


# Get all predictions API
def get_all_predictions(userid, limit=None):
    try:
        if limit is None:
            return History.query.filter_by(userid=userid).order_by(History.id.desc())
        return History.query.filter_by(userid=userid).order_by(History.id.desc()).limit(limit)
    except Exception as e:
        flash(str(e), category='error')


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
        'resale_prediction': prediction.resale_prediction
    } for prediction in all_predictions]
    return jsonify(data)


# Add prediction API
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
        flash(str(e), category='error')


@api.route('/api/prediction/add', methods=['POST'])
def store_prediction_api():
    data = request.get_json()
    if type(data) is str:
        data = json.loads(data)
    userid = int(data['userid'])  # type: ignore
    floor_area = float(data['floor_area'])  # type: ignore
    bedrooms = int(data['bedrooms'])  # type: ignore
    approval_date = datetime.strptime(
        data['approval_date'], '%Y-%m-%d')  # type: ignore
    lease_commencement_year = int(
        data['lease_commencement_year'])  # type: ignore
    resale_pred = float(data['resale_pred'])  # type: ignore
    new_id = store_prediction(userid=userid, floor_area=floor_area, bedrooms=bedrooms,
                              approval_date=approval_date, lease_commencement_year=lease_commencement_year, resale_pred=resale_pred)
    return jsonify({'new_id': new_id})


# New prediction API
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
    return max(MODEL.predict(X=X)[0], OUTPUT_BOUNDARIES['min'])


@api.route('/api/predict', methods=['POST'])
def new_prediction_api():
    data = request.get_json()
    if type(data) is str:
        data = json.loads(data)

    floor_area = float(data['floor_area'])  # type: ignore
    bedrooms = int(data['bedrooms'])  # type: ignore
    approval_date = datetime.strptime(
        data['approval_date'], '%Y-%m-%d')  # type: ignore
    lease_commencement_year = int(
        data['lease_commencement_year'])  # type: ignore

    resale_pred = new_prediction(floor_area=floor_area, bedrooms=bedrooms,
                                 approval_date=approval_date, lease_commencement_year=lease_commencement_year)

    return jsonify({'resale_pred': resale_pred})


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
        result['userid'] = user.id  # type: ignore

        response = requests.post(
            url=request.host_url[:-1] + url_for('api.store_prediction_api'), json=json.dumps(result)
        )

        flash(str(resale_pred), category='prediction')
        return redirect(url_for('routes.home'))
    else:
        return render_template('home.html', title=TITLE, target='home', show='new', form=form)


# Delete prediction API
def remove_prediction(prediction_id):
    try:
        record = History.query.get(prediction_id)
        db.session.delete(record)
        db.session.commit()
        return 0
    except Exception as error:
        db.session.rollback()
        flash(str(error), category="error")
        return 1


@api.route('/api/delete/<pred_id>', methods=['DELETE'])
def remove_prediction_api(pred_id):
    result = remove_prediction(prediction_id=int(pred_id))
    if result == 0:
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'fail'})


@api.route('/remove', methods=['POST'])
@login_required
def delete_record():
    pred_id = request.form['id']
    response = requests.delete(
        url=request.host_url[:-1] + url_for('api.remove_prediction_api', pred_id=pred_id))
    if response.json()['result'] != 'ok':
        flash('Error deleting record', category='error')
        past_predictions = get_all_predictions(
            userid=current_user.id)  # type: ignore
        render_template('home.html', title=TITLE, target='home',
                        show='history', past_predictions=past_predictions)
    return redirect(url_for('routes.history'))
