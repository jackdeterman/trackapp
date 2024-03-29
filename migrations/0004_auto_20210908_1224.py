# Generated by Django 3.2.6 on 2021-09-08 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trackapp', '0003_alter_result_milestones'),
    ]

    operations = [
        migrations.CreateModel(
            name='QualifyingLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=255)),
                ('value', models.FloatField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifying_levels', to='trackapp.event')),
                ('season', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualifying_levels', to='trackapp.season')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='qualifications',
            field=models.ManyToManyField(related_name='qualifying_results', to='trackapp.QualifyingLevel'),
        ),
    ]
