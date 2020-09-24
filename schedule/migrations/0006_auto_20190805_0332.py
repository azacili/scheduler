from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0005_auto_20190610_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='term',
            field=models.CharField(db_index=True, default='2019-2020-01', max_length=64),
        ),
    ]
