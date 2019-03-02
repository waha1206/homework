# Generated by Django 2.1.7 on 2019-03-02 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20190302_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=10, verbose_name='數量')),
                ('value', models.CharField(db_index=True, max_length=10, verbose_name='利率')),
            ],
            options={
                'verbose_name_plural': '建立第三層分類名稱',
            },
        ),
        migrations.AlterModelOptions(
            name='categorylevelone',
            options={'verbose_name_plural': '建立第一層分類名稱'},
        ),
        migrations.AlterModelOptions(
            name='categoryleveltwo',
            options={'verbose_name_plural': '建立第二層分類名稱'},
        ),
        migrations.AlterUniqueTogether(
            name='categorylevelone',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='categoryleveltwo',
            unique_together={('name',)},
        ),
        migrations.AddField(
            model_name='profit',
            name='container',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mysite.CategoryLevelTwo'),
        ),
    ]
