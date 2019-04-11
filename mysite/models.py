from django.db import models
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField
from django.db.models import Q
from model_utils import Choices

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'create_time'),
    ('2', 'name'),
    ('3', 'company_tax_id'),
    ('4', 'contact_sales'),
    ('5', 'contact_sales_phone'),
    ('6', 'contact_sales_mob'),
    ('7', 'address'),
)

# Create your models here.
class Maker(models.Model):
    name = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class PModel(models.Model):
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    url = models.URLField(default='https://i.imgur.com/CQtJpDU.png')
    def __str__(self):
        return self.name

class Product(models.Model):
    pmodel = models.ForeignKey(PModel, on_delete=models.CASCADE, verbose_name='型號')
    nickname = models.CharField(max_length=15, default='超值二手機', verbose_name='摘要')
    description = models.TextField(default='暫無說明')
    year = models.PositiveIntegerField(default=2016, verbose_name='出廠年份')
    price = models.PositiveIntegerField(default=0, verbose_name='價格')
    
    def __str__(self):
        return self.nickname
        
class PPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=20, default='產品照片')
    url = models.URLField(default='https://i.imgur.com/CQtJpDU.png')
    
    def __str__(self):
        return self.description
        
class Mood(models.Model):
    status = models.CharField(max_length=10, null=False)
    
    def __str__(self):
        return self.status

class Post(models.Model):
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='不願意透漏身分的人', verbose_name='暱稱')
    message = models.TextField(null=False, verbose_name='訊息')
    del_pass = models.CharField(max_length=10, help_text='要記住密碼')
    pub_time = models.DateTimeField(auto_now=True, verbose_name='發文時間')
    enabled = models.BooleanField(default=False, verbose_name = '審-核')
    
    def __str__(self):
        return self.message
        
#建立一個使用者 session

class User2(models.Model):
    name = models.CharField(max_length=20, null=False)
    email = models.EmailField()
    password = models.CharField(max_length=20, null=False)
    enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveIntegerField(default=160)
    male = models.BooleanField(default=False)
    website = models.URLField(null=True)
    
    def __str__(self):
        return self.user.username
#stmp.gmail.com
#django.core.mail.backends.smtp.EmailBackend
#django_mailgun.MailgunBackend
class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    note = models.TextField()
    ddate = models.DateField()
    
    def __str__(self):
        return "{}({})".format(self.ddate, self.user)
        
#下面為大分類的model
class CategoryLevelOne(models.Model):
    name = models.CharField(max_length=10, verbose_name='分類')
    title = models.CharField(max_length=10, verbose_name='中文名稱')
    description = models.TextField()    
    def __str__(self):
        return self.name
    class Meta:#plural 使用複數名，才不會多一個s在尾巴
        verbose_name_plural = u'建立第一層分類名稱'
        unique_together = ('name',)

class CategoryLevelTwo(models.Model):
    name        = models.CharField(max_length=10, verbose_name='分類')
    title       = models.CharField(max_length=10, verbose_name='中文名稱')
    category    = models.ForeignKey(CategoryLevelOne, on_delete=models.CASCADE)
    image       = FilerImageField(related_name='product_image', on_delete=models.CASCADE, null=True, verbose_name='圖片')
    description = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = u'建立第二層分類名稱'
        unique_together = ('name',)
        
class CategoryLevelThree(models.Model):
    name        = models.CharField(max_length=10, verbose_name='分類')
    title       = models.CharField(max_length=10, verbose_name='中文名稱')
    category    = models.ForeignKey(CategoryLevelTwo, on_delete=models.CASCADE)
    description = models.TextField()
    class Meta:
        verbose_name_plural = u'建立第三層分類名稱'
        unique_together = ('name',)
    
class Profit(models.Model):
    container = models.ForeignKey(CategoryLevelTwo, on_delete=models.CASCADE, db_index=True, verbose_name='商品類別')
    key       = models.IntegerField(db_index=True, verbose_name='數量')
    value     = models.DecimalField(max_digits=3, decimal_places=2, db_index=True, verbose_name='利率')
    class Meta:
        db_table = "profit"
        verbose_name_plural = '利潤分配表'
        unique_together = ('key','container')#聯合約束此為一組的狀態JJ001只會有一個數量20的意思
    def __str__(self):
        return str(self.container)

class Music(models.Model):
    song = models.TextField()
    singer = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "music"

class MyoSupplier(models.Model):
    PAYMENT_CHOICES = (
        ('0', '現金'),
        ('30', '月結30天'),
        ('45', '月結45天'),
    )
    name = models.CharField(max_length=50, unique= True, verbose_name='廠商名稱')
    company_tax_id = models.CharField(max_length=20, blank=True, verbose_name='統一編號')
    tel       = models.CharField(max_length=20, blank=True, verbose_name='公司電話')
    fax       = models.CharField(max_length=20, blank=True, verbose_name='公司傳真')
    postal    = models.CharField(max_length=20, blank=True, verbose_name='3+2郵遞區號')
    address     = models.CharField(max_length=50, blank=True, verbose_name='公司地址')
    tax_address     = models.CharField(max_length=50, blank=True, verbose_name='發票地址')
    #email = models.EmailField(max_length=70,blank=True, null= True, unique= True, verbose_name='EMAIL')
    email = models.EmailField(max_length=70, blank=True, verbose_name='EMAIL')
    website= models.URLField(max_length=250, blank=True, verbose_name='廠商網頁')
    contact_sales  = models.CharField(max_length=20, blank=True, verbose_name='聯絡人')
    contact_sales_phone  = models.CharField(max_length=20, blank=True, verbose_name='聯絡人電話')
    contact_sales_mob  = models.CharField(max_length=20, blank=True, verbose_name='聯絡人手機')
    payment = models.CharField(max_length=2, choices=PAYMENT_CHOICES,default='0', verbose_name='票期')
    bank = models.CharField(max_length=20, blank=True, verbose_name='銀行')
    transit_number = models.CharField(max_length=20, blank=True, verbose_name='銀行代碼')
    branch_name = models.CharField(max_length=20, blank=True, verbose_name='分行名稱')
    branch_id = models.CharField(max_length=20, blank=True, verbose_name='分行代碼')
    bank_account = models.CharField(max_length=20, blank=True, verbose_name='匯款帳號')
    account_name = models.CharField(max_length=20, blank=True, verbose_name='戶名')
    account_contact_name = models.CharField(max_length=20, blank=True, verbose_name='帳戶聯絡人')
    account_contact_tel = models.CharField(max_length=20, blank=True, verbose_name='帳戶聯絡人電話')
    account_contact_email = models.CharField(max_length=20, blank=True, verbose_name='帳戶郵件')
    description = models.TextField(blank=True, verbose_name='備註')
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='建檔日期')
    last_modify_date = models.DateTimeField(auto_now=True, null=True, verbose_name='資料更新日期')
    class Meta:
        verbose_name_plural = '供應商資料'
        unique_together = ('company_tax_id',)#聯合約束此為一組的狀態JJ001只會有一個數量20的意思
    def __str__(self):
        return self.name
        
def query_myosupplier_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]
    
    order_column = ORDER_COLUMN_CHOICES[order_column]
    
    
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column
        
    queryset = MyoSupplier.objects.all()
    total = queryset.count()
    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                        Q(create_time__icontains=search_value) |
                                        Q(name__icontains=search_value) |
                                        Q(company_tax_id__icontains=search_value) |
                                        Q(contact_sales__icontains=search_value) |
                                        Q(contact_sales_phone__icontains=search_value) |
                                        Q(contact_sales_mob__icontains=search_value) |
                                        Q(address__icontains=search_value))
    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

class MaterialLevelOne(models.Model):
    name = models.CharField(max_length=10, verbose_name='分類')
    title = models.CharField(max_length=10, verbose_name='中文名稱')
    image       = FilerImageField(related_name='material_one_image', on_delete=models.CASCADE, null=True, verbose_name='圖片')
    description = models.TextField()    
    def __str__(self):
        return self.name
    class Meta:#plural 使用複數名，才不會多一個s在尾巴
        verbose_name_plural = u'建立原料第一層分類名稱'
        unique_together = ('name',)

class MaterialLevelTwo(models.Model):
    name        = models.CharField(max_length=10, verbose_name='分類')
    title       = models.CharField(max_length=10, verbose_name='中文名稱')
    category    = models.ForeignKey(MaterialLevelOne, on_delete=models.CASCADE)
    image       = FilerImageField(related_name='material_two_image', on_delete=models.CASCADE, null=True, verbose_name='圖片')
    description = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = u'建立原料第二層分類名稱'
        unique_together = ('name',)

class MaterialLevelThree(models.Model):
    myo_supplier = models.ManyToManyField(MyoSupplier, db_index=True, verbose_name='供應商')
    name        = models.CharField(max_length=50, verbose_name='商品名稱')
    title       = models.CharField(max_length=50, blank=True, verbose_name='中文名稱')
    category    = models.ForeignKey(MaterialLevelTwo, on_delete=models.CASCADE)
    image       = FilerImageField(related_name='material_three_image', on_delete=models.CASCADE, null=True, verbose_name='圖片')
    description = models.TextField(blank=True, verbose_name='商品說明')
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='建檔日期')
    last_modify_date = models.DateTimeField(auto_now=True, null=True, verbose_name='資料更新日期')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = u'建立原料第三層分類名稱'
        unique_together = ('name',)
        
