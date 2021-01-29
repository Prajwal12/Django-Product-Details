from django.db import models


# Create your models here.

class L1(models.Model):
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_heirarchy_data'


class L2(models.Model):
    category = models.ForeignKey(L1,on_delete=models.CASCADE,max_length=255, blank=True, null=True)
    product_line = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'product_heirarchy_data'



class CompetitionData(models.Model):
    dt = models.DateField(blank=True, null=True)
    sku_id = models.IntegerField(blank=True, null=True)
    comp_id = models.CharField(max_length=255, blank=True, null=True)
    comp_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition_data'


class ProductHeirarchyData(models.Model):
    sku_id = models.IntegerField(primary_key=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    product_line_id = models.IntegerField(blank=True, null=True)
    product_line = models.CharField(max_length=255, blank=True, null=True)
    brick_id = models.IntegerField(blank=True, null=True)
    brick = models.CharField(max_length=255, blank=True, null=True)
    brand_id = models.IntegerField(blank=True, null=True)
    brand_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_heirarchy_data'


class SalesData(models.Model):
    sales_date = models.DateField(blank=True, null=True)
    sku = models.ForeignKey(ProductHeirarchyData, models.DO_NOTHING, blank=True, null=True)
    sale_price = models.IntegerField(blank=True, null=True)
    units_sold = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_data'
