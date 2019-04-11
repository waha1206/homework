import django_tables2 as tables

from .models import Profit

        
class ProfitTable(tables.Table):
    delete = tables.TemplateColumn(
        '<form action="/del_profit/{{record.id}}/" method="post">{% csrf_token %}<input type="hidden" name="_method" value="delete"><button data-toggle="tooltip" title="Please note that deletion cannot be undone" type="submit" class="btn btn-danger btn-xs">delete</button></form>',
        orderable=False,
        verbose_name='刪除'
    )

    class Meta:
        model = Profit
        fields = ['id', 'container', 'key', 'value', 'delete']
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        