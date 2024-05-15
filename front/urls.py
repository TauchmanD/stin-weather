from django.urls import path, register_converter

from . import views, converters

register_converter(converters.FloatUrlParameterConverter, 'float')

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("payment/", views.payment, name="payment"),
    path('<float:lat>/<float:lon>/', views.index, name='index_with_coordinates'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/', views.remove_favorite, name='remove_favorite'),
]
