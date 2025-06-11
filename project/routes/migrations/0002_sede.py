from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=255)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('actualizada_en', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(
            lambda apps, schema_editor: apps.get_model('routes', 'Sede').objects.create(
                direccion='Calle Falsa 123, Santiago',
                latitud=-33.4569,
                longitud=-70.6483
            ),
            migrations.RunPython.noop,
        ),
    ]
