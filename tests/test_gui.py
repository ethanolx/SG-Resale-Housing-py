import re
import pytest
from datetime import datetime


# Form Input Consistency
@pytest.mark.parametrize('endpoint_list', [
    '/login',
    '/sign-up'
])
def test_form_input(client, endpoint_list, capsys):
    with capsys.disabled():
        response = client.get(endpoint_list)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

        html_content = response.get_data(as_text=True)
        html_content = re.sub('[\\s]+', ' ', html_content)
        form_content = re.findall('<form.*/form>', html_content)[0]
        for form_group in re.findall('<p>(?:(?!</p>).)+</p>', form_content):
            input_type = re.findall('type\\="([^"]*)"', form_group)[0]
            if input_type not in {'submit', 'reset'}:
                assert form_group.find('label') < form_group.find(
                    'input'), 'Label must precede input box'


# Date Format Consistency
@pytest.mark.parametrize('endpoint_list', [
    '/about'
])
def test_date_format(client, endpoint_list, capsys):
    with capsys.disabled():
        response = client.get(endpoint_list)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

        html_content = response.get_data(as_text=True)
        html_content = re.sub('[\\s]+', ' ', html_content)
        table_rows = re.findall('<tr>(?:(?!<tr>).)+</tr>', html_content)
        for row in table_rows:
            if re.match('.*date.*', row, re.IGNORECASE):
                format = re.findall('\\((.*)\\)', row)[0]
                format = format.replace('DD', '%d').replace(
                    'MM', '%m').replace('YYYY', '%Y')
                for date_cell in re.findall('<td>((?:(?!<td>).)+)</td>', row):
                    assert datetime.strptime(
                        date_cell, format), 'Date must match specified format'


# Navbar Consistency
@pytest.mark.parametrize('endpoint_list', [
    '/login',
    '/sign-up',
    '/about'
])
def test_navbar(client, endpoint_list, capsys):
    with capsys.disabled():
        response = client.get(endpoint_list)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

        html_content = response.get_data(as_text=True)
        html_content = re.sub('[\\s]+', ' ', html_content)

        with open('./app/templates/includes/nav.html', 'r') as f:
            navbar_content = f.read().strip()

        navbar_template = re.findall(
            '<nav.*</button>', re.sub('[\\s]+', ' ', navbar_content))[0]
        navbar_template = navbar_template.replace('{{title}}', 'RHAI')

        assert re.findall('<nav(?:(?!</button>).)+</button>',
                          html_content)[0] == navbar_template, 'Rendered navbar must match template'


# Footer Consistency
@pytest.mark.parametrize('endpoint_list', [
    '/login',
    '/sign-up',
    '/about'
])
def test_footer(client, endpoint_list, capsys):
    with capsys.disabled():
        response = client.get(endpoint_list)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

        html_content = response.get_data(as_text=True)
        html_content = re.sub('[\\s]+', ' ', html_content)

        with open('./app/templates/includes/footer.html', 'r') as f:
            footer_content = f.read().strip()

        footer_template = re.sub('[\\s]+', ' ', footer_content)

        assert re.findall('<footer.*</footer>',
                          html_content)[0] == footer_template, 'Rendered footer must match template'


# Unexpected Failure
@pytest.mark.parametrize('endpoint_list', [
    '/home',
    '/history'
])
def test_login(client, endpoint_list, capsys):
    with capsys.disabled():
        response = client.get(endpoint_list)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
