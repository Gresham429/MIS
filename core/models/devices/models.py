from django.db import models


class Devices(models.Model):
    category = models.CharField(max_length=100, verbose_name='物资类别')
    fixed_asset_number = models.CharField(max_length=100, verbose_name='固定资产编号')
    name = models.CharField(max_length=100, verbose_name='物资名称')
    model = models.CharField(max_length=100, verbose_name='型号')
    production_date = models.DateField(verbose_name='生产/出厂日期')
    invoice_number = models.CharField(blank=True, null=True, max_length=100, verbose_name='发票号码')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    quantity = models.IntegerField(verbose_name='数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    purchase_date = models.DateField(blank=True, null=True, verbose_name='采购日期')
    purchaser = models.CharField(blank=True, null=True,  max_length=100, verbose_name='采购人')
    purchaser_phone = models.CharField(blank=True, null=True, max_length=100, verbose_name='采购人电话')
    team = models.CharField(max_length=100, verbose_name='领用团队')
    recipient = models.CharField(blank=True, null=True, max_length=100, verbose_name='领用人')
    recipient_phone = models.CharField(blank=True, null=True, max_length=100, verbose_name='领用人电话')
    storage_location = models.CharField(max_length=100, verbose_name='存放地点')
    responsible_person = models.CharField(max_length=100, verbose_name='责任人')
    current_status = models.CharField(max_length=100, verbose_name='当前状态')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'devices'
