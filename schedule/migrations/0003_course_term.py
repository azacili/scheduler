from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0002_auto_20180829_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='term',
            field=models.CharField(db_index=True, default='2018-2019-01', max_length=64),
            preserve_default=False,
        ),
    ]
