from flask_login import current_user

def get_dato():
    if current_user.is_authenticated:
        variable = 'hola' + current_user.get_id()
    else:
        variable = 'no se'

    return variable
