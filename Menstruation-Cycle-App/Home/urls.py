from django.urls import path
from Home import views
app_name='Home'

urlpatterns = [
  
  path('', views.index, name='home'),
  path('contact', views.contact, name ="contact"),
  path('faq', views.faq, name ="faq"),
  path('pcod', views.pcod, name ="pcod"),
  path('selfcare', views.selfcare, name ="selfcare"),
  path('periodtracker', views.periodtracker, name ="periodtracker"),
  path('pcodpredict', views.pcodpredict, name ="pcodpredict"), 
  path('generate_completion', views.generate_completion, name='generate_completion'),
  path('calendar', views.CalendarView.as_view(), name='calendar'),
  path('^event/new/$', views.event, name='event_new'),
  path('^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]

 