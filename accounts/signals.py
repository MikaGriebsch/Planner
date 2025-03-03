from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def store_first_login_status(sender, request, user, **kwargs):
    
    if not request.session.get('first_login_checked', False):
        request.session['first_login'] = True
        request.session['first_login_checked'] = True
    else:
        request.session['first_login'] = False

    request.session.modified = True  