from typing import cast
from flask import Blueprint, request
from flask.helpers import flash, url_for
from flask_login.utils import login_required, current_user
import cloudpickle
import pandas as pd
import numpy as np
from datetime import datetime
from werkzeug.utils import redirect
from .models.history import History
from . import db

api = Blueprint('api', __name__)


with open('./app/static/input_boundaries.p', 'rb') as output_bounds_file:
    output_boundaries = cloudpickle.load(file=output_bounds_file)


@api.route('/predict', methods=['POST'])
@login_required
def predict():
    user = current_user
    floor_area = float(cast(str, request.form.get('floor_area')))
    bedrooms = int(cast(str, request.form.get('bedrooms')))
    approval_date = pd.to_datetime(
        cast(str, request.form.get('approval_date')), format='%Y-%m-%d')
    lease_commencement_year = int(
        cast(str, request.form.get('lease_commencement_year')))
    pred = new_prediction(floor_area=floor_area, bedrooms=bedrooms,
                          approval_date=approval_date, lease_commencement_year=lease_commencement_year)
    store_prediction(userid=user.id, floor_area=floor_area, bedrooms=bedrooms,  # type: ignore
                     approval_date=approval_date, lease_commencement_year=lease_commencement_year, resale_pred=pred)
    flash(str(pred), category='prediction')
    return redirect(url_for('routes.home'))


def store_prediction(userid, floor_area, bedrooms, approval_date, lease_commencement_year, resale_pred):
    try:
        db.session.add(History(userid=userid, floor_area=floor_area, bedrooms=bedrooms, approval_date=approval_date,
                       lease_commencement_year=lease_commencement_year, resale_prediction=resale_pred, predicted_on=datetime.utcnow()))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(str(e), category='prediction')


def get_latest_prediction(userid):
    try:
        return History.query.filter_by(userid=userid).order_by(History.userid.desc()).first()
    except Exception as e:
        flash(str(e), category='prediction')


def get_all_predictions(userid, limit=5):
    try:
        return History.query.filter_by(userid=userid).order_by(History.userid.desc()).limit(limit)
    except Exception as e:
        flash(str(e), category='prediction')


def new_prediction(floor_area, bedrooms, approval_date, lease_commencement_year):
    with open('./app/static/regressor.p', 'rb') as model_file:
        model = cloudpickle.load(model_file)
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


def remove_prediction(prediction_id):
    try:
        record = History.query.get(prediction_id)
        db.session.delete(record)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(str(error), category="prediction")
