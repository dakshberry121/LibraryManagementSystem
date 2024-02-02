from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('books/', views.bookList.as_view()),
    path('authors/', views.authorList.as_view()),
    path('members/', views.memberList.as_view()),
    path('bookreserve/<int:pk>', views.bookreservation.as_view()),
    path('overduebooks/', views.overduebooks.as_view()),
    path('finecalcMember/', views.finecalcMember.as_view()),
    path('popbooks/', views.popularbooks.as_view()),
    path('activemember/', views.mostactivemember.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)