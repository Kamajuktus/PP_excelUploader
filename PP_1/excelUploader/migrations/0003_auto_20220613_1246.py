# Generated by Django 3.2.6 on 2022-06-13 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('excelUploader', '0002_rename_finalreport_tbl_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='ACS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50)),
                ('datetime', models.DateTimeField()),
                ('direction', models.CharField(max_length=5)),
                ('door', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='tbl_Employee',
        ),
        migrations.AddField(
            model_name='acs',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='excelUploader.employee'),
        ),
    ]