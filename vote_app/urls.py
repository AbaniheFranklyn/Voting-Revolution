from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render
from . import views, views2, views3
from django.contrib.auth.views import LoginView
app_name = 'vote_app'
urlpatterns = [
    path('', views.base, name='base'),
    path('/vote', views.vote, name='vote'),
    path('/login', LoginView.as_view(template_name='vote_app/login.html'),  name='login'),
    path('/signup', views.signup, name='signup'),
    path('/logout', views.logout_now, name= 'logout'),
    path('/result', views.results, name='result'),
    path('setvote',views.setvote, name='setvote'),
    path('setcsv',views.upload_csv, name='setcsv'),
    path('/GOVERNOR',views.gov, name='gov'),
    path('/PRESIDENT',views.pres, name='pres'),
    path('/SENATOR',views.senate, name='senate'),
    path('/LOCAL GOV. CHAIRMAN',views.chm, name='lgc'),
    path('/HOUSE OF REP',views.hor, name='hor'),
    path('/HOUSE OF ASSEMBLY',views.hoa, name='hoa'),
    path('/GOVERNOR token verification',views2.gov_tvn, name='gov_tvn'),
    path('/PRESIDENT token verification',views2.pres_tvn, name='pres_tvn'),
    path('/SENATOR token verification',views2.senate_tvn, name='senate_tvn'),
    path('/LOCAL GOV. CHAIRMAN token verification',views2.chm_tvn, name='chm_tvn'),
    path('/HOUSE OF REPRESENTATIVE token verification',views2.hor_tvn, name='hor_tvn'),
    path('/HOUSE OF ASSEMBLY token verification',views2.hoa_tvn, name='hoa_tvn'),
    path('/Voted No Revoting', views.voted, name='voted'),
    path('/President Result', views3.result_pres, name='pres_result'),
    path('/Senate Result', views3.result_senate, name='senate_result'),
    path('/House Of Rep Result', views3.result_hor, name='hor_result'),
    path('/House Of Assembly Result', views3.result_hoa, name='hoa_result'),
    path('/Governor Result', views3.result_gov, name='gov_result'),
    path('/Local Government Chairman Result', views3.result_lgc, name='chm_result'),
    path('/Thanks for voting', views.thank, name='thank'),
]
