from django.contrib.auth.decorators import user_passes_test


def payment_required(payment_url=None):
    return user_passes_test(lambda u: u.paying, login_url=payment_url)