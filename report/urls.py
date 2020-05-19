from django.urls import path
from . import views

app_name = 'report'
urlpatterns = [
    # path('', views.my_cases, name='all-cases'),
    path('', views.MyCases.as_view(), name='all-cases'),
    path('<slug:slug>/update/', views.CaseUpdate.as_view(), name='case-update'),
    path('<slug:slug>/delete/', views.CaseDelete.as_view(), name='case-delete'),
    path('email/', views.sent_email, name='sent-report'),
    path('search_results/', views.SearchResultsView.as_view(), name='search-results'),
    path('case_filter/', views.FilterCasesView.as_view(), name='case-filter')
]