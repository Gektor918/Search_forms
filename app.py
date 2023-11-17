from flask import Flask, request

from service import *

app = Flask(__name__)


@app.route('/create_form', methods=['POST'])
def create_new_form():
    """
    Create a new form.
    """
    data = request.form.to_dict()
    result_validate = validate_data(data)

    if isinstance(result_validate, dict):
        result_insert = insert_in_db(data)
        return {'result_validate':result_validate, 'result_insert':result_insert}, 200
    else:
        result_validate = result_validate.json()
        return {'result_validate':result_validate}, 400


@app.route('/get_form', methods=['POST'])
def get_form():
    """
    Get form data.
    """
    data = request.form.to_dict()
    result_filter = filtering_incoming_data(data)
    result_validate = validate_data(result_filter)

    if isinstance(result_validate, dict):
        search_form_result = search_form(result_filter)
        if search_form_result:
            return {'search_form_result':search_form_result[0]['form_name']}, 200
        else:
            search_form_result = str((FormData.__annotations__))
            return {'search_form_result':search_form_result}, 400
    else:
        search_form_result = need_views(result_validate)
        return {'search_form_result':search_form_result}, 400


if __name__ == '__main__':
    app.run(debug=True)