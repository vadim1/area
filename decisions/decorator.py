from django.contrib.auth.decorators import login_required, user_passes_test

# 2019-03-09 Check to see if the user has exceeded the access limit
# ref: "Limiting access to modules discussion notes"
user_login_required = user_passes_test(lambda user: user.is_allowed_access(), login_url='/decisions/limit_reached')

def active_user_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func