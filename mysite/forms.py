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
    captcha = CaptchaField() #機器人驗證所需要導入的
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

#把第二層資JJ001透過FORM去做修改利潤的表單
class CategoryLevelTwoForm(forms.ModelForm):
    class Meta:
        model = models.CategoryLevelTwo
        fields = ['name', 'title', 'category', 'image', 'description']
    def __init__(self, *args, **kwargs):
        super(CategoryLevelTwoForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '分類'
        self.fields['title'].label = '中文名稱'
        self.fields['category'].label = '父類別'
        self.fields['image'].label = '商品圖片'
        self.fields['description'].label = '商品描述'
        
class ProfitForm(forms.ModelForm):
    class Meta:
        model = models.Profit
        fields = ['container', 'key', 'value']
    def __init__(self, *args, **kwargs):
        super(ProfitForm, self).__init__(*args, **kwargs)
        self.fields['container'].label = '商品分類'
        self.fields['key'].label = '請輸入數量'
        self.fields['value'].label = '請輸入利潤'