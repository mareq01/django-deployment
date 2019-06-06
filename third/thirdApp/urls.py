from thirdApp import views
from django.urls import path

app_name = 'thirdApp'

urlpatterns = [
    path('other/',views.page_1,name="page_1"),
    path('relative_url_template/',views.page_2,name="page_2"),
    path('registrate/',views.form_page,name="form_page"),
    path('login/',views.user_login,name="user_login"),
]
