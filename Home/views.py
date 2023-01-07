from django.shortcuts import render,redirect
from django.views.generic import ListView
from .forms import ContactForm, PeriodTracker, PCODForm
from .models import UserPeriod
from django.core.mail import message, send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression  
from sklearn.datasets import load_iris  
from sklearn.model_selection import train_test_split
import pickle
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
import openai

def timeline(request):
    return render(request, 'Home/timeline.html')

def generate_completion(request):
    test = "Hi"
    openai.api_key = "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"

    prompt = request.POST.get("user_input")
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
    print(response)
    return render(request, 'Home/chatbot.html', {'test':test,'res':response})

Pkl_Filename = "Home/Pickle_RL_Model.pkl" 
with open(Pkl_Filename, 'rb') as file:  
    Pickled_LR_Model = pickle.load(file)


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
        print(period_start_dates)
        print(type(period_start_dates))

        for i in range(0,len(period_start_dates)):
          period_start_dates[i]=period_start_dates[i].replace('-','')
          period_start_dates[i]=period_start_dates[i][:4]+period_start_dates[i][:2]+period_start_dates[i][2:4]
          if i!=0:
            d=abs(int(period_start_dates[i][6:8])-int(period_start_dates[i-1][6:8]))
            if (int(period_start_dates[i][4:6])!=1):
                  m=abs(int(period_start_dates[i][4:6])-int(period_start_dates[i-1][4:6]))
                  y=int(period_start_dates[i][:4])-int(period_start_dates[i-1][:4])
            else:
                 m=abs(13-int(period_start_dates[i-1][4:6]))
                 y=int(period_start_dates[i][:4])-int(period_start_dates[i-1][:4])-1
            period_gaps.append(int(((30*m)-d)))
        last_start_date = period_start_dates[-1]
        period_model.fit(np.array(period_start_dates).reshape(-1, 1), period_gaps)
        prediction = period_model.predict(np.array([last_start_date]).reshape(-1, 1))
        print("prediction ",prediction)
        date=float(last_start_date) + prediction[0]
        date= str(date)[:4]+str(date)[4:6]+str(date)[6:8]
        mth=['01','02','03','04','05','06','07','08','09','10','11','12']
        d=date[6:8]
        m=date[4:6]
        y=date[:4]
        print(d)
        print(m)
        print(y)
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
        date=d+'-'+m+'-'+y   
        print(date)
    return render(request, 'Home/periodtracker.html', context={'form':form,'user':current_user})

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
