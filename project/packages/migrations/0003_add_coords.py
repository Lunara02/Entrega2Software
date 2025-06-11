from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_paquete_conductor'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='latitud',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paquete',
            name='longitud',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]

