# Generated by Django 3.0.8 on 2020-07-27 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoiceitem',
            old_name='amount_paid',
            new_name='discount_value',
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_discount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_value',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='quote_price',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('discount_value', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('closed_date', models.DateTimeField(auto_now=True)),
                ('is_closed', models.BooleanField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cart_customers', to='api.Customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cart_products', to='api.Product')),
            ],
        ),
    ]
