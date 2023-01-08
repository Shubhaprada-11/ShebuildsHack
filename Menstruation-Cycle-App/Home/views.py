from django.shortcuts import render,redirect
from django.views.generic import ListView
from .forms import ContactForm, PeriodTracker, PCODForm, EventForm
from .models import UserPeriod, Event
from django.http import HttpResponse, HttpRequest
from django.core.mail import message, send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import numpy as np
import pandas as pd
import json
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression  
from sklearn.datasets import load_iris  
from sklearn.model_selection import train_test_split
import pickle
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
import openai
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta, date
import calendar
from .utils import Calendar
from django.contrib.auth.mixins import LoginRequiredMixin


Pkl_Filename = "Home/Pickle_RL_Model.pkl" 
with open(Pkl_Filename, 'rb') as file:  
    Pickled_LR_Model = pickle.load(file)
Pkl_Filename1 = "Home/model_MNB_actual.pkl"
Pkl_Filename2 = "Home/model_NB.pkl" 
with open(Pkl_Filename1, 'rb') as file:  
    Pickled_LR_Model1 = pickle.load(file)
with open(Pkl_Filename2, 'rb') as file:  
    Pickled_LR_Model2 = pickle.load(file)

loaded_vectorizer = pickle.load(open('Home/vectorizer.pickle', 'rb'))


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'Home/calendar.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        dategraph=[]
        scoregraph=[]
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, current_user.id)
        html_cal = cal.formatmonth(withyear=True)
        queryset = Event.objects.all()
        queryset = queryset.filter(userid_id=current_user)
        if queryset:
            df = pd.DataFrame(list(queryset.values()))
            df.drop(columns = ['userid_id','id','description','mood'],inplace=True)
            print(df)
            dategraph = df['start_time'].tolist()
            scoregraph = df['moodscore'].tolist()
            for i in range(0,len(dategraph)):
                dategraph[i] = str(dategraph[i].date())
                dategraph[i]=dategraph[i].replace("-","")
            print(dategraph)
            print(scoregraph)
            for i in range(len(scoregraph)):
                scoregraph[i] = scoregraph[i]+5
        context['dategraph'] = json.dumps(dategraph)
        context['scoregraph'] = scoregraph
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    current_user = request.user.pk
    queryset = Event.objects.all()
    queryset = queryset.filter(userid_id=current_user)
    #instance = Event()
    if event_id:
        instance = get_object_or_404(queryset, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
            desc = form.cleaned_data['description']
            st = form.cleaned_data['start_time']
            moodlist = moodtracker(request,desc)
            score = moodlist[0]
            mood = moodlist[1]
            p = Event(userid_id=current_user,description=desc,start_time=st,mood=mood,moodscore=score)
            p.save()
            return HttpResponseRedirect(reverse('Home:calendar'))
    return render(request, 'home/event.html', {'form': form})

@login_required
def moodtracker(request,desc):
    text = [desc]
    d = {"sadness": -2 ,"anger": 0 ,"love": 2,"joy":3 ,"fear": -1,"surprise": 1}
    test_result1 = Pickled_LR_Model1.predict(loaded_vectorizer.transform(text))
    test_result2 = Pickled_LR_Model2.predict(loaded_vectorizer.transform(text))
    score = int((test_result1+test_result2)/2)
    mood = (list(d.keys())[list(d.values()).index(int((test_result1+test_result2)/2))])
    return [score,mood]
    

def generate_completion(request):
    openai.api_key = "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"

    prompt = request.POST.get("user_input")
    print(prompt)
    model ="text-davinci-002"
    response="Oh my god just work!!"

    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completions.choices[0].text
    print("Hello")
    print(response)
    return render(request, 'Home/chatbot.html', {'prompt':prompt,'res':response})

def index(request):
    return render(request,'Home/home.html')
def faq(request):
    return render(request,'Home/faq.html')
def pcod(request):
    return render(request,'Home/pcod.html')
def selfcare(request):
    return render(request,'Home/selfcare.html')

class home(ListView):
    template_name='Home/home.html'

@login_required
def periodtracker(request):
    current_user = request.user.pk
    print(current_user)
    lp = "Hi"
    ped = 2
    print("Hello")
    form = PeriodTracker()
    if request.method == 'POST':
        print("Enter")
        form = PeriodTracker(request.POST)
        print("Hello")
        if form.is_valid():
            print("Enter1")
            lp = form.cleaned_data['lastperiod']
            ped = form.cleaned_data['duration']
            print(lp)
            print(ped)
            print(type(current_user))
            p = UserPeriod(uid_id=current_user,lasperioddate=lp,duration=ped)
            p.save()
    queryset = UserPeriod.objects.all()
    queryset = queryset.filter(uid_id=current_user)
    print(queryset)
    if queryset is not None:
        period_start_dates = []
        period_lengths = []
        df = pd.DataFrame(list(queryset.values()))
        df.drop(columns = ['uid_id','id'],inplace=True)
        print(df)
        period_start_dates = df['lasperioddate'].tolist()
        period_lengths = df['duration'].tolist()
        period_gaps=[28]
        period_model = LinearRegression()
        #print(period_start_dates)
        #print(type(period_start_dates))
        temp = str(period_start_dates[-1])
        for i in range(0,len(period_start_dates)):
          period_start_dates[i] = str(period_start_dates[i])
          #print(period_start_dates[i])
          period_start_dates[i]=period_start_dates[i].replace("-","")
          #print(period_start_dates[i])
          period_start_dates[i]=period_start_dates[i][:4]+period_start_dates[i][6:8]+period_start_dates[i][4:6]
          #print(period_start_dates[i])
          if i!=0:
            d=abs(int(period_start_dates[i][6:8])-int(period_start_dates[i-1][6:8]))
            if (int(period_start_dates[i][4:6])!=1):
                  m=abs(int(period_start_dates[i][4:6])-int(period_start_dates[i-1][4:6]))
                  y=int(period_start_dates[i][:4])-int(period_start_dates[i-1][:4])
            else:
                 m=abs(13-int(period_start_dates[i-1][4:6]))
                 y=int(period_start_dates[i][:4])-int(period_start_dates[i-1][:4])-1
            period_gaps.append(int(((30*m)-d)))
        #print(period_start_dates)
        #print(period_gaps)
       
        period_model.fit(np.array(period_start_dates).reshape(-1, 1), period_gaps)
        last_start_date = period_start_dates[-1]
        prediction = period_model.predict(np.array([last_start_date]).reshape(-1, 1))
        print("prediction ",prediction)
        date=float(last_start_date) + prediction[0]
        date= str(date)[:4]+str(date)[4:6]+str(date)[6:8]
        mth=['01','02','03','04','05','06','07','08','09','10','11','12']
        d=date[6:8]
        m=date[4:6]
        y=date[:4]
        no_of_days={'01':'31','02':'28','03':'31','04':'30','05':'31','06':'30','07':'31','08':'31','09':'30','10':'31','11':'30','12':'31'};
        if int(date[6:8])>int(no_of_days[date[4:6]]):
            d=int(date[6:8])-int(no_of_days[date[4:6]])
            if d<10:
                    d='0'+str(d)
            if(date[4:6]!='12'):
                print(date[4:6])
                m=mth[int(date[4:6])]
            else:
                m='01'
                y=int(date[:4])+1
        date=str(y)+'-'+str(d)+'-'+str(m)
        temp = datetime.strptime(temp,'%Y-%d-%m').date()
        date = datetime.strptime(date,'%Y-%d-%m').date()
        middate = temp + (date-temp)/2
    return render(request, 'Home/periodtracker.html', context={'form':form,'date':date,'prevperiod':temp,'middate':middate})

def pcodpredict(request):
    l = []
    inp = []
    res = "Waiting for result"
    y_pred=-1
    form = PCODForm()
    if request.method =='POST':
        form = PCODForm(request.POST)
        if form.is_valid():
            follicle_r = form.cleaned_data['follicle_R']
            follicle_l = form.cleaned_data['follicle_L']
            startdate = form.cleaned_data['skindarkening']
            hair = form.cleaned_data['hair']
            weight = form.cleaned_data['weight']
            cycle = form.cleaned_data['cycle']
            l.append(follicle_r)
            l.append(follicle_l)
            l.append(startdate)
            l.append(hair)
            l.append(weight)
            l.append(cycle)
    print(l)
    inp.append(l)
    print(inp)
    if len(l)==6:
        y_pred = Pickled_LR_Model.predict(inp)
    print(y_pred)
    if y_pred == 1:
        res="Prone to PCOD"
    elif y_pred==0:
        res="safe" 
    return render(request, 'Home/pcodpredict.html', context={'form':form,'res':res})
            

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body={
                'first_name':form.cleaned_data['first_name'],
                'last_name':form.cleaned_data['last_name'],
                'email':form.cleaned_data['email'],
                'message':form.cleaned_data['message'],


            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message,'admin@example.com',['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("Home:home")
        
    form = ContactForm()
    return render(request, "Home/contact.html", {'form':form})
