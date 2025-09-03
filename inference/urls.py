# baepo_project/inference/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 기본 주소('')로 접속하면 views.py의 analyze_sentiment 함수를 실행해 줘! (HTML 뷰)
    path('', views.analyze_sentiment, name='analyze'),
    # API 엔드포인트 (프론트엔드용)
    path('api/analyze/', views.analyze_sentiment_api, name='analyze_api'),
]
