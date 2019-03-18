from django.contrib.sites.models import Site
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mysite import models, forms
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def index(request, pid=None, del_pass=None):
    products = models.Product.objects.all()
    if products:
        print(products[0])
    years = range(1960, 2021)
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    moods = models.Mood.objects.all()
    #p = models.CategoryLevelThree.objects.filter(name='JJ001-0001')
    #print(p[0].profit['50'])
    
    #是否有支援cookieS
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        message_cookie = "cookie support!"
    else:
        message_cookie = 'cookie not supported'
    request.session.set_test_cookie()
    
    #檢查使用者是否Login (使用session)
    #if 'username' in request.session:
    #    username = request.session['username']
    #    password = request.session['password']
    
    #使用auth
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
        password = request.user.password
    try:
        messages.get_message(request)
    except:
        pass
    
    
    #ch008www心情留言的程式段落
    try:
        
        ch08user_id = request.GET['ch08user_id']
        ch08user_pass = request.GET['ch08user_pass']
        ch08user_mood = request.GET['mood']
        ch08user_post = request.GET['ch08user_post']
    
    except:
        ch08user_id = None
        message = '如果要張貼資訊，每一個欄位都需要填寫'

    if del_pass and pid:
        try:
            post = models.Post.objects.get(id=pid)
        except:
            post = None
        if post:
            if post.del_pass == del_pass:
                post.delete()
                message = "資料刪除成功"
            else:
                message = "密碼錯誤"
    
    elif ch08user_id != None:
        mood = models.Mood.objects.get(status=ch08user_mood)
        post = models.Post.objects.create(mood=mood, nickname=ch08user_id, del_pass=ch08user_pass, message=ch08user_post)
        post.save()
        message = '成功儲存！請記得您的編輯密碼[{}]！訊息需經過審查才會顯示。'.format(ch08user_pass)
    
    
    try:
        urid = request.GET['user_id']
        urpass = request.GET['user_pass']
    except:
        urid = None
        
    if urid != None and urpass == '12345':
        verified = True
    else:
        verified = False
    
    try:
        uryear = request.GET['byear'] 
    except:
        uryear = None
    
    try:
        urfcolor = request.GET.getlist('fcolor')
    except:
        urfcolor = None
    

    return render(request, 'index.html', locals())
    
def leveltwoinfo(request, del_key=None, del_product=None):
    products = models.CategoryLevelTwo.objects.all()
    profit_form = forms.ProfitForm()
    
    if del_key and del_product:
        #依據商品的型號跟數量找到該筆資料後刪除
        del_profit = models.Profit.objects.filter(container__name=del_product, key=del_key)#.values('key', 'value')
        #刪除該筆數據，要注意queryset是無法被print出來的，要看就要後面加上.values('','')       ↑
        del_profit.delete()
        return HttpResponseRedirect("/leveltwoinfo/")

    if request.method == 'POST':
        profit_form = forms.ProfitForm(request.POST)
        if profit_form.is_valid():
            try:
                profit_form.save()
                print('正確地把資料存檔了')
                print(profit_form)
            except:
                print('數量重複')
        else:
            print('表單沒有傳回數量與毛利率')
        try:
            list = request.POST.getlist('dropleveltwo') #select name = 'dropleveltwo'
            #option name="{{org.id}} 這樣才會從select抓出JJ002的名字
            get_products = models.CategoryLevelTwo.objects.get(name=list[0])
            print(get_products.title)
            profit = models.Profit.objects.filter(container__name=list[0]).values('key', 'value').order_by('key')
            #print(profit)
        except:
            message = '資料出現異常'
            print('找不到資料')
    return render(request, 'leveltwoinfo.html', locals())

    
def detail(request, id):
    try:
        product = models.Product.objects.get(id=id)
        images = models.PPhoto.objects.filter(product=product)
    except:
        pass
    return render(request, 'detail.html', locals())
    
def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())
    
@csrf_exempt
def posting(request):
    moods = models.Mood.objects.all()
    try:
        user_id = request.POST['user_id']
        user_pass = request.POST['user_pass']
        user_post = request.POST['user_post']
        user_mood = request.POST['mood']
    except:
        user_id = None
        message = '如果要張貼訊息，每個欄位都要填版資料'
    if user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message='成功儲存！請記得您的編輯密碼[{}]！，訊息需要經過審查才會顯示。'.format(user_pass)
    return render(request, 'posting.html', locals())

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感謝您的來信"
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
        
            mail_body = u'''
網友姓名:{}
網友信箱:{}
居住城市:{}
是否在學:{}
反映意見:如下
{}'''.format(user_name, user_email, user_city, user_school, user_message)
            email = EmailMessage(   '來自【不吐不快】網站的網友意見',
                                    mail_body,
                                    user_email,
                                    ['waha1206@gmail.com'])
            email.send()
        else:
            message = "請檢查您輸入的資料是否正確!"
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())
    
#8.3模型表單類別ModelForm的應用
def post2db(request):
    # 使用session的方式
    #if 'username' in request.session:
    #    username = request.session['username']
    if request.user.is_authenticated:
        username = request.user.username
    
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            message_post = "目前的訊息改成不需要管理員審核。"
            post_form.save()
            return HttpResponseRedirect('/list/')
        else:
            message_post = "每個欄位都要填寫喔"
    else:
        post_form = forms.PostForm()
        message_post = '如果要張貼訊息，每個欄位都要填滿資料'
        
    return render(request, 'post2db.html', locals())

#9.1 使用cookie登入    
def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip() #strip 移除字首與字尾的空白或換行符號
            login_password = request.POST['password']
            message_cookie = "登入成功"
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, '成功登入了')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '帳號尚未啟用')
            else:
                messages.add_message(request, messages.WARNING, '登入失敗')
        else:
            messages.add_message(request, messages.INFO, '請檢查輸入欄位的內容')
    else:
        login_form = forms.LoginForm()

    return render(request, 'login.html', locals())
    
def logout(request):
    # 使用session的方式
    #if 'username' in request.session:
    #    Session.objects.all().delete()
    #    return redirect('/login/')
    #return redirect('/')
    
    # 使用auth的方式
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功登出了")
    return redirect('/')
    
@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username
        try:
            user = User.objects.get(username=username)
            userinfo = models.Profile.objects.get(user=user)
            print("---使用者與使用者資訊---")
            print(user.password)
            print(userinfo.website)
        except:
            pass
    return render(request, 'userinfo.html', locals())
    print("return之後有執行到這一行")
    
@login_required(login_url='/login/')
def diarypost(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)
    print(messages)
    
    if request.method == 'POST':
        user = User.objects.get(username=username) #先去auth那邊找出使用者資訊放到user裡面
        diary = models.Diary(user=user) #再去建立一個該使用者的diary
        post_form = forms.DiaryForm(request.POST, instance=diary) 
        #↑ 把表單裡面的DiaryForm帶入使用者與web傳回來的diary資訊
        if post_form.is_valid(): #isvlid() 檢查表單有無資料與正確性
            messages.add_message(request, messages.INFO, "日記已儲存")
            post_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, "每個欄位都要填寫")
    else:
        post_form = forms.DiaryForm()
        messages.add_message(request, messages.INFO, '每個欄位都要填寫喔')
    return render(request, 'diarypost.html', locals())
        
        