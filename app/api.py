from typing import cast
from flask import Blueprint, request
from flask.helpers import flash, url_for
from flask_login.utils import login_required, current_user
import cloudpickle
import pandas as pd
import numpy as np
from datetime import date, datetime
from werkzeug.utils import redirect
from .models.history import History
from . import db

api = Blueprint('api', __name__)


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
    pred = get_prediction(floor_area=floor_area, bedrooms=bedrooms,
                          approval_date=approval_date, lease_commencement_year=lease_commencement_year)
    store_prediction(userid=user.id, floor_area=floor_area, bedrooms=bedrooms,  # type: ignore
                     approval_date=approval_date, lease_commencement_year=lease_commencement_year, resale_pred=pred)
    flash(str(pred), category='prediction')
    return redirect(url_for('routes.home'))


def store_prediction(userid, floor_area, bedrooms, approval_date, lease_commencement_year, resale_pred):
    try:
        db.session.add(History(userid=userid, floor_area=floor_area, bedrooms=bedrooms, approval_date=approval_date,
                       lease_commencement_year=lease_commencement_year, resale_prediction=resale_pred))
        db.session.commit()
    except Exception as e:
        flash(str(e), category='prediction')


def get_prediction(floor_area, bedrooms, approval_date, lease_commencement_year):
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
    return model.predict(X=X)[0]
