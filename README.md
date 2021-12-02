# DOAA CA1 Assignment

|               |                       |
|---------------|-----------------------|
|   Name        |   Ethan Tan           |
|   Admin       |   P2012085            |
|   Class       |   DAAA/2B/03          |
|   Languages   |   SQL, Python, Web    |

## File Structure

```
CA1 ---- app ---- controllers ---- api.py
     |        |                |-- auth.py
     |        |                `-- routes.py
     |        |
     |        |-- forms ---- __init__.py
     |        |          |-- login_form.py
     |        |          |-- prediction_form.py
     |        |          `-- sign_up_form.py
     |        |
     |        |-- models ---- history.py
     |        |           `-- user.py
     |        |
     |        |-- static ---- css ---- base.css
     |        |           |        `-- styles.css
     |        |           |
     |        |           |-- dist ---- input_boundaries.p
     |        |           |         |-- output_boundaries.p
     |        |           |         `-- regressor.p
     |        |           |
     |        |           `-- img ---- favicon.ico
     |        |
     |        |-- templates ---- includes ---- footer.html
     |        |              |             |-- macros.html
     |        |              |             `-- nav.html
     |        |              |
     |        |              |-- about.html
     |        |              |-- home.html
     |        |              |-- layout.html
     |        |              |-- login.html
     |        |              `-- sign-up.html
     |        |
     |        |-- __init__.py
     |        |-- .gitignore
     |        |-- config_dev.cfg
     |        |-- config_test.cfg
     |        |-- database.db
     |        |-- Pipfile
     |        `-- Pipfile.lock
     |
     |-- doc ---- CA1_Brief.docx
     |        |-- slides.pptx
     |        `-- wireframe-for-site.drawio
     |
     |-- ml-model ---- data ---- flat-prices.csv
     |             |
     |             |-- models ---- input_boundaries.p
     |             |           |-- output_boundaries.p
     |             |           `-- regressor.p
     |             |
     |             |-- Pipfile
     |             |-- Pipfile.lock
     |             `-- train-model.ipynb
     |
     |-- tests ---- conftest.py
     |          |-- test_apis.py
     |          |-- test_gui.py
     |          `-- test_models.py
     |
     |-- .gitignore
     |-- app.py
     `-- README.md
```

## GitLab Repository

Repository Link:

## See Also

Assignment Brief: `doc/CA1_Brief.docx`