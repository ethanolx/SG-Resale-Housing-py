import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib

matplotlib.use('Agg')


def get_regression_plot(pipeline, input_bounds, bedrooms, floor_area_sqm, approval_date, lease_commencement_year, resale_price):
    def create_stencil(variable: str, **kwargs):
        length = len(kwargs[variable])
        for i in kwargs:
            if i != variable:
                kwargs[i] = np.resize(np.array([kwargs[i]]), (length,))
        return pd.DataFrame(kwargs)[['floor_area_sqm', 'approval_date', 'lease_commencement_year', 'bedrooms']]

    def get_regression_plot(variable, mark, ax, pipeline, input_bounds, resale_price, **kwargs):
        x_var = input_bounds[variable]

        x = (x_var['min'], x_var['max'])
        del kwargs[variable]
        y = pipeline.predict(create_stencil(
            variable, **{variable: x}, **kwargs))
        sns.lineplot(x=x, y=y, ax=ax)
        sns.scatterplot(x=[mark], y=resale_price, facecolor='red', ax=ax)
        ax.set_title(variable)
        ax.set_ylabel('Predicted Resale Price')
        ax.set_xticks(x)
        ax.set_yticklabels([f'{i / 1000:.0f}k' for i in ax.get_yticks()])

    def get_regression_plots(input_bounds, pipeline, bedrooms, floor_area_sqm, approval_date, lease_commencement_year, resale_price):
        fig, ax = plt.subplots(2, 2, figsize=(8, 5))
        get_regression_plot(input_bounds=input_bounds, variable='bedrooms', mark=bedrooms, bedrooms=bedrooms, floor_area_sqm=floor_area_sqm,
                            approval_date=approval_date, lease_commencement_year=lease_commencement_year, ax=ax[0, 0], pipeline=pipeline, resale_price=resale_price)
        get_regression_plot(input_bounds=input_bounds, variable='floor_area_sqm', mark=floor_area_sqm, bedrooms=bedrooms, floor_area_sqm=floor_area_sqm,
                            approval_date=approval_date, lease_commencement_year=lease_commencement_year, ax=ax[0, 1], pipeline=pipeline, resale_price=resale_price)
        get_regression_plot(input_bounds=input_bounds, variable='approval_date', mark=approval_date, bedrooms=bedrooms, floor_area_sqm=floor_area_sqm,
                            approval_date=approval_date, lease_commencement_year=lease_commencement_year, ax=ax[1, 0], pipeline=pipeline, resale_price=resale_price)
        get_regression_plot(input_bounds=input_bounds, variable='lease_commencement_year', mark=lease_commencement_year, bedrooms=bedrooms, floor_area_sqm=floor_area_sqm,
                            approval_date=approval_date, lease_commencement_year=lease_commencement_year, ax=ax[1, 1], pipeline=pipeline, resale_price=resale_price)
        plt.tight_layout()
        return fig

    return get_regression_plots(input_bounds=input_bounds, pipeline=pipeline, bedrooms=bedrooms, floor_area_sqm=floor_area_sqm, approval_date=approval_date, lease_commencement_year=lease_commencement_year, resale_price=resale_price)
