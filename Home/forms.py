from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.CharField(max_length=150)
    message = forms.CharField(widget= forms.Textarea, max_length=2000)

class PeriodTracker(forms.Form):
    lastperiod = forms.DateField(label=" Your last period date ")
    duration = forms.IntegerField(label=" Duration of your last period ")

class PCODForm(forms.Form):
    follicle_R = forms.FloatField(label=" Follicle No.(R) ")
    follicle_L = forms.FloatField(label=" Follicle No.(L) ")
    skindarkening = forms.FloatField(label=" Skin Darkening(1/0) ")
    hair = forms.FloatField(label=" Hair growth(1/0) ")
    weight = forms.FloatField(label=" Weight gain(1/0) ")
    cycle = forms.FloatField(label=" Cycle(Regular-1/Irregular-0) ")