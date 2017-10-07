import random
from django.core.mail import send_mail
from django.conf import settings


def send_from_default_email(subject, message, recipient_list, **kwargs):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
              recipient_list, **kwargs)


def generate_otp(length=6):
    # allowed_at_zero = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    # allowed = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # not_allowed = ['0']
    # otp = ''.join(random.SystemRandom().choice(allowed) for _ in range(length))
    # if otp[0] in not_allowed:
    #     otp_ = random.SystemRandom().choice(allowed_at_zero)
    #     otp = otp_ + otp[1:]
    # return otp
    min_ = 111111
    max_ = 999999
    return str(random.SystemRandom().randint(min_, max_))


def send_otp(mobile_number, otp, msg=None):
    from django.conf import settings
    import bandwidth
    message = msg
    try:
        client = bandwidth.client('messaging', user_id=settings.BANDWIDTH_USER_ID,
                                  api_token=settings.BANDWIDTH_TOKEN,
                                  api_secret=settings.BANDWIDTH_SECRET_KEY)
        sender_number = settings.SENDER_MOBILE_NUMBER
        if message is None:
            message = "Hello, Use %s OTP to verify your number(identity) at app.areamethod.com" % otp
        client.send_message(sender_number, mobile_number, text=message)
        return True
    except:
        return False
