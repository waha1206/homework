from django import forms
from mysite import models
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    CITY = [
        ['TP', 'Taipei'],
        ['TY', 'Taoyuang'],
        ['TC', 'Taichung'],
        ['TN', 'Tainan'],
        ['KS', 'Kaohsiung'],
        ['NA', 'Others'],
    ]
    user_name = forms.CharField(label='您的姓名', max_length=50, initial='李大仁')
    user_city = forms.ChoiceField(label='居住城市', choices=CITY)
    user_school = forms.BooleanField(label='是否在學', required=False)
    user_email = forms.EmailField(label='電子郵件')
    user_message = forms.CharField(label='您的意見', widget=forms.Textarea)
    
    
#8.3模型表單類別ModelForm的應用
class PostForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:

        model = models.Post
        fields = ['mood', 'nickname', 'message', 'del_pass', 'enabled']
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['mood'].label = '現在心情'
        self.fields['nickname'].label = '你的暱稱'
        self.fields['message'].label = '心情留言'
        self.fields['del_pass'].label = '設定密碼'
        self.fields['captcha'].label = '你確定你不是機器人'
        self.fields['enabled'].label = '審核'

class LoginForm(forms.Form):

    username = forms.CharField(label='姓名', max_length=10)
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())
    
    
#寫日記 直接在GFORM上挖一個欄位讓他的輸入格式為 date
#Built-in widgets 要挖其他欄位可以參考下面
# https://docs.djangoproject.com/en/2.1/ref/forms/widgets/#built-in-widgets
class DateInput(forms.DateInput):
    input_type = 'date'
    
class DiaryForm(forms.ModelForm):
    class Meta:
        model = models.Diary
        fields = ['budget', 'weight', 'note', 'ddate']
        widgets = {
            'ddate': DateInput(),
        }
    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        self.fields['budget'].label = '今日花費 (元)'
        self.fields['weight'].label = '今日體重 (KG)'
        self.fields['note'].label = '心情留言'
        self.fields['ddate'].label = '日期'
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['height', 'male', 'website']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['height'].label = '身高 (cm)'
        self.fields['male'].label = '是男生嗎？'
        self.fields['website'].label = '個人網站'
        