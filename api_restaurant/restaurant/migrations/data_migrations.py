from django.db import migrations


def create_initial_datas(apps, schema_editor):
    Restaurant = apps.get_model('restaurant', 'Restaurant')
    Restaurant.objects.create(name='Green Goose', city='Paris')
    Restaurant.objects.create(name='Le Savoyard', city='Chambery')
    Restaurant.objects.create(name='Excellent!', city='Lyon')


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_datas),
    ]
