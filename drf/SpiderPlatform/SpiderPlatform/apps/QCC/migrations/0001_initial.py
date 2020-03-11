# Generated by Django 3.0.2 on 2020-03-11 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Jbxx',
            fields=[
                ('companyname', models.CharField(db_column='companyName', max_length=255, primary_key=True, serialize=False)),
                ('creditcode', models.CharField(blank=True, db_column='creditCode', max_length=255, null=True)),
                ('organizationcode', models.CharField(blank=True, db_column='organizationCode', max_length=255, null=True)),
                ('registernum', models.CharField(blank=True, db_column='registerNum', max_length=255, null=True)),
                ('businessstate', models.CharField(blank=True, db_column='businessState', max_length=255, null=True)),
                ('industry', models.CharField(blank=True, max_length=255, null=True)),
                ('legalman', models.CharField(blank=True, db_column='legalMan', max_length=255, null=True)),
                ('registermoney', models.CharField(blank=True, db_column='registerMoney', max_length=255, null=True)),
                ('registertime', models.CharField(blank=True, db_column='registerTime', max_length=255, null=True)),
                ('registorgan', models.CharField(blank=True, db_column='registOrgan', max_length=255, null=True)),
                ('confirmtime', models.CharField(blank=True, db_column='confirmTime', max_length=255, null=True)),
                ('businesstimeout', models.CharField(blank=True, db_column='businessTimeout', max_length=255, null=True)),
                ('companytype', models.CharField(blank=True, db_column='companyType', max_length=255, null=True)),
                ('registeraddress', models.CharField(blank=True, db_column='registerAddress', max_length=255, null=True)),
                ('businessscope', models.TextField(blank=True, db_column='businessScope', null=True)),
                ('personnelscale', models.CharField(blank=True, db_column='personnelScale', max_length=255, null=True)),
                ('insuredpersons', models.CharField(blank=True, db_column='insuredPersons', max_length=255, null=True)),
                ('usedname', models.CharField(blank=True, db_column='usedName', max_length=255, null=True)),
                ('operation', models.CharField(blank=True, max_length=255, null=True)),
                ('websource', models.CharField(blank=True, db_column='webSource', max_length=255, null=True)),
                ('storagetime', models.DateTimeField(blank=True, db_column='storageTime', null=True)),
            ],
            options={
                'db_table': 'jbxx',
                'managed': True,
            },
        ),
    ]
