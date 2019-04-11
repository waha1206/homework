from django import forms
from mysite import models
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

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
        
class MyoSupplierForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'EMAIL請注意格式'}))
    account_contact_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'EMAIL請注意格式'}))
    class Meta:
        model = models.MyoSupplier
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(MyoSupplierForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '廠商名稱'
        self.fields['company_tax_id'].label = '統一編號'
        self.fields['tel'].label = '公司電話'
        self.fields['fax'].label = '公司傳真'
        self.fields['postal'].label = '3+2郵遞區號'
        self.fields['address'].label = '公司地址'
        self.fields['tax_address'].label = '發票地址'
        self.fields['email'].label = 'EMAIL'
        self.fields['website'].label = '廠商網頁'
        self.fields['contact_sales'].label = '聯絡人'
        self.fields['contact_sales_phone'].label = '聯絡人電話'
        self.fields['contact_sales_mob'].label = '聯絡人手機'
        self.fields['payment'].label = '票期'
        self.fields['bank'].label = '銀行'
        self.fields['transit_number'].label = '銀行代碼'
        self.fields['branch_name'].label = '分行名稱'
        self.fields['branch_id'].label = '分行代碼'
        self.fields['bank_account'].label = '匯款帳號'
        self.fields['account_name'].label = '戶名'
        self.fields['account_contact_name'].label = '帳戶聯絡人'
        self.fields['account_contact_tel'].label = '帳戶聯絡人電話'
        self.fields['account_contact_email'].label = '聯絡人帳戶郵件'
        self.fields['description'].label = '備註'
        self.fields['company_tax_id'].required = False
        self.fields['tel'].required = False
        self.fields['fax'].required = False
        self.fields['postal'].required = False
        self.fields['address'].required = False
        self.fields['tax_address'].required = False
        self.fields['email'].required = False
        self.fields['website'].required = False
        self.fields['contact_sales'].required = False
        self.fields['contact_sales_phone'].required = False
        self.fields['contact_sales_mob'].required = False
        self.fields['payment'].required = False
        self.fields['bank'].required = False
        self.fields['transit_number'].required = False
        self.fields['branch_name'].required = False
        self.fields['branch_id'].required = False
        self.fields['bank_account'].required = False
        self.fields['account_name'].required = False
        self.fields['account_contact_name'].required = False
        self.fields['account_contact_tel'].required = False
        self.fields['account_contact_email'].required = False
        self.fields['description'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('website', css_class='form-group col-md-3 mb-0'),
                Column('tel', css_class='form-group col-md-3 mb-0'),
                Column('fax', css_class='form-group col-md-3 mb-0'),
                Column('company_tax_id', css_class='form-group col-md-2 mb-0'),
                Column('email', css_class='form-group col-md-3 mb-0'),
                Column('postal', css_class='form-group col-md-2 mb-0'),
                Column('contact_sales', css_class='form-group col-md-2 mb-0'),
                Column('contact_sales_phone', css_class='form-group col-md-3 mb-0'),
                Column('contact_sales_mob', css_class='form-group col-md-3 mb-0'),
                Column('account_contact_email', css_class='form-group col-md-3 mb-0'),
                Column('bank', css_class='form-group col-md-3 mb-0'),
                Column('transit_number', css_class='form-group col-md-2 mb-0'),
                Column('branch_name', css_class='form-group col-md-3 mb-0'),
                Column('branch_id', css_class='form-group col-md-2 mb-0'),
                Column('payment', css_class='form-group col-md-2 mb-0'),
                Column('account_name', css_class='form-group col-md-3 mb-0'),
                Column('bank_account', css_class='form-group col-md-3 mb-0'),
                Column('account_contact_name', css_class='form-group col-md-3 mb-0'),
                Column('account_contact_tel', css_class='form-group col-md-3 mb-0'),
                Column('address', css_class='form-group col-md-6 mb-0'),
                Column('tax_address', css_class='form-group col-md-6 mb-0'),
                
                css_class='form-row'
            ),
            'description',
        )


