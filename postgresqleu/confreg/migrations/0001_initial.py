# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import postgresqleu.confreg.models
import postgresqleu.util.validators
import postgresqleu.confreg.dbimage
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendeeMail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentat', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=8000)),
            ],
            options={
                'ordering': ('-sentat',),
            },
        ),
        migrations.CreateModel(
            name='BulkPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numregs', models.IntegerField()),
                ('createdat', models.DateField(auto_now_add=True)),
                ('paidat', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('urlname', models.CharField(unique=True, max_length=32, validators=[postgresqleu.util.validators.validate_lowercase])),
                ('conferencename', models.CharField(max_length=64)),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('location', models.CharField(max_length=128)),
                ('contactaddr', models.EmailField(max_length=254)),
                ('sponsoraddr', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=True, verbose_name=b'Registration open')),
                ('callforpapersopen', models.BooleanField(default=False)),
                ('callforsponsorsopen', models.BooleanField(default=False)),
                ('feedbackopen', models.BooleanField(default=True)),
                ('conferencefeedbackopen', models.BooleanField(default=False)),
                ('scheduleactive', models.BooleanField(default=False, verbose_name=b'Schedule publishing active')),
                ('sessionsactive', models.BooleanField(default=False, verbose_name=b'Session list publishing active')),
                ('schedulewidth', models.IntegerField(default=600, verbose_name=b'Width of HTML schedule')),
                ('pixelsperminute', models.FloatField(default=1.5, verbose_name=b'Vertical pixels per minute')),
                ('confurl', models.CharField(max_length=128, validators=[postgresqleu.util.validators.validate_lowercase])),
                ('listadminurl', models.CharField(max_length=128, blank=True)),
                ('listadminpwd', models.CharField(max_length=128, blank=True)),
                ('speakerlistadminurl', models.CharField(max_length=128, blank=True)),
                ('speakerlistadminpwd', models.CharField(max_length=128, blank=True)),
                ('twittersync_active', models.BooleanField(default=False)),
                ('twitter_user', models.CharField(max_length=32, blank=True)),
                ('twitter_attendeelist', models.CharField(max_length=32, blank=True)),
                ('twitter_speakerlist', models.CharField(max_length=32, blank=True)),
                ('twitter_sponsorlist', models.CharField(max_length=32, blank=True)),
                ('twitter_token', models.CharField(max_length=128, blank=True)),
                ('twitter_secret', models.CharField(max_length=128, blank=True)),
                ('asktshirt', models.BooleanField(default=True)),
                ('askfood', models.BooleanField(default=True)),
                ('askshareemail', models.BooleanField(default=False)),
                ('skill_levels', models.BooleanField(default=True)),
                ('additionalintro', models.TextField(help_text=b'Additional text shown just before the list of available additional options', blank=True)),
                ('basetemplate', models.CharField(default=None, max_length=128, null=True, help_text=b'Relative name to template used as base to extend any default templates from', blank=True)),
                ('templatemodule', models.CharField(default=None, max_length=128, null=True, help_text=b"Full path to python module containing a 'templateextra.py' submodule", blank=True)),
                ('templateoverridedir', models.CharField(default=None, max_length=128, null=True, help_text=b'Full path to a directory with override templates in', blank=True)),
                ('badgemodule', models.CharField(default=None, max_length=128, null=True, help_text=b'Full path to python module *and class* used to render badges', blank=True)),
                ('templatemediabase', models.CharField(default=None, max_length=128, null=True, help_text=b'Relative location to template media (must be local to avoid https/http errors)', blank=True)),
                ('callforpapersintro', models.TextField(blank=True)),
                ('sendwelcomemail', models.BooleanField(default=False)),
                ('welcomemail', models.TextField(blank=True)),
                ('lastmodified', models.DateTimeField(auto_now=True)),
                ('newsjson', models.CharField(default=None, max_length=128, null=True, blank=True)),
                ('accounting_object', models.CharField(max_length=30, null=True, verbose_name=b'Accounting object name', blank=True)),
                ('invoice_autocancel_hours', models.IntegerField(blank=True, help_text=b'Automatically cancel invoices after this many hours', null=True, verbose_name=b'Autocancel invoices', validators=[django.core.validators.MinValueValidator(1)])),
                ('attendees_before_waitlist', models.IntegerField(default=0, help_text=b'Maximum number of attendees before enabling waitlist management. 0 for no waitlist management', verbose_name=b'Attendees before waitlist', validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'ordering': ['-startdate'],
            },
        ),
        migrations.CreateModel(
            name='ConferenceAdditionalOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('cost', models.IntegerField()),
                ('maxcount', models.IntegerField()),
                ('public', models.BooleanField(default=True, help_text=b'Visible on public forms (opposite of admin only)')),
                ('upsellable', models.BooleanField(default=True, help_text=b'Can this option be purchased after the registration is completed')),
                ('invoice_autocancel_hours', models.IntegerField(blank=True, help_text=b'Automatically cancel invoices after this many hours', null=True, verbose_name=b'Autocancel invoices', validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ConferenceFeedbackAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rateanswer', models.IntegerField(null=True)),
                ('textanswer', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['conference', 'attendee', 'question'],
            },
        ),
        migrations.CreateModel(
            name='ConferenceFeedbackQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=100)),
                ('isfreetext', models.BooleanField(default=False)),
                ('textchoices', models.CharField(max_length=500, blank=True)),
                ('sortkey', models.IntegerField(default=100)),
                ('newfieldset', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'ordering': ['conference', 'sortkey'],
            },
        ),
        migrations.CreateModel(
            name='ConferenceRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=100, verbose_name=b'First name')),
                ('lastname', models.CharField(max_length=100, verbose_name=b'Last name')),
                ('email', models.EmailField(max_length=254, verbose_name=b'E-mail address')),
                ('company', models.CharField(max_length=100, verbose_name=b'Company', blank=True)),
                ('address', models.TextField(max_length=200, verbose_name=b'Address', blank=True)),
                ('phone', models.CharField(max_length=100, verbose_name=b'Phone number', blank=True)),
                ('dietary', models.CharField(max_length=100, verbose_name=b'Special dietary needs', blank=True)),
                ('twittername', models.CharField(max_length=100, verbose_name=b'Twitter account', blank=True)),
                ('nick', models.CharField(max_length=100, verbose_name=b'Nickname', blank=True)),
                ('shareemail', models.BooleanField(default=False, verbose_name=b'Share e-mail address with sponsors')),
                ('payconfirmedat', models.DateField(null=True, verbose_name=b'Payment confirmed', blank=True)),
                ('payconfirmedby', models.CharField(max_length=16, null=True, verbose_name=b'Payment confirmed by', blank=True)),
                ('created', models.DateTimeField(verbose_name=b'Registration created')),
                ('lastmodified', models.DateTimeField(auto_now=True)),
                ('vouchercode', models.CharField(max_length=100, verbose_name=b'Voucher code', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('starttime', models.DateTimeField(null=True, blank=True)),
                ('endtime', models.DateTimeField(null=True, blank=True)),
                ('cross_schedule', models.BooleanField(default=False)),
                ('can_feedback', models.BooleanField(default=True)),
                ('abstract', models.TextField(blank=True)),
                ('skill_level', models.IntegerField(default=1, choices=[(0, b'Beginner'), (1, b'Intermediate'), (2, b'Advanced')])),
                ('status', models.IntegerField(default=0, choices=[(0, b'Submitted'), (1, b'Approved'), (2, b'Rejected'), (3, b'Pending'), (4, b'Reserve')])),
                ('lastnotifiedstatus', models.IntegerField(default=0, choices=[(0, b'Submitted'), (1, b'Approved'), (2, b'Rejected'), (3, b'Pending'), (4, b'Reserve')])),
                ('lastnotifiedtime', models.DateTimeField(null=True, verbose_name=b'Notification last sent', blank=True)),
                ('submissionnote', models.TextField(verbose_name=b'Submission notes', blank=True)),
                ('initialsubmit', models.DateTimeField(null=True, verbose_name=b'Submitted', blank=True)),
                ('lastmodified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['starttime'],
            },
        ),
        migrations.CreateModel(
            name='ConferenceSessionFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_importance', models.IntegerField()),
                ('content_quality', models.IntegerField()),
                ('speaker_knowledge', models.IntegerField()),
                ('speaker_quality', models.IntegerField()),
                ('speaker_feedback', models.TextField(verbose_name=b'Comments to the speaker', blank=True)),
                ('conference_feedback', models.TextField(verbose_name=b'Comments to the conference organizers', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceSessionScheduleSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceSessionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.IntegerField(null=True)),
                ('comment', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemid', models.IntegerField()),
                ('type', models.CharField(max_length=16)),
                ('deltime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100)),
                ('discountamount', models.IntegerField(default=0)),
                ('discountpercentage', models.IntegerField(default=0)),
                ('regonly', models.BooleanField(default=False, help_text=b"Apply percentage discount only to the registration cost, not additional options. By default, it's applied to both.")),
                ('validuntil', models.DateField(null=True, blank=True)),
                ('maxuses', models.IntegerField(default=0)),
                ('is_invoiced', models.BooleanField(default=False, verbose_name=b'Has an invoice been sent for this discount code.')),
            ],
            options={
                'ordering': ('conference', 'code'),
            },
        ),
        migrations.CreateModel(
            name='PendingAdditionalOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createtime', models.DateTimeField()),
                ('payconfirmedat', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrepaidBatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buyername', models.CharField(max_length=100, null=True, blank=True)),
                ('buyer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('conference', models.ForeignKey(to='confreg.Conference')),
            ],
            options={
                'ordering': ['conference', 'id'],
                'verbose_name_plural': 'Prepaid batches',
            },
        ),
        migrations.CreateModel(
            name='PrepaidVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vouchervalue', models.CharField(unique=True, max_length=100)),
                ('usedate', models.DateTimeField(null=True, blank=True)),
                ('batch', models.ForeignKey(to='confreg.PrepaidBatch')),
                ('conference', models.ForeignKey(to='confreg.Conference')),
            ],
            options={
                'ordering': ['batch', 'vouchervalue'],
            },
        ),
        migrations.CreateModel(
            name='RegistrationClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('regclass', models.CharField(max_length=64)),
                ('badgecolor', models.CharField(blank=True, help_text=b'Badge background color in hex format', max_length=20, validators=[postgresqleu.confreg.models.color_validator])),
                ('badgeforegroundcolor', models.CharField(blank=True, help_text=b'Badge foreground color in hex format', max_length=20, validators=[postgresqleu.confreg.models.color_validator])),
                ('conference', models.ForeignKey(to='confreg.Conference')),
            ],
            options={
                'verbose_name_plural': 'Registration classes',
            },
        ),
        migrations.CreateModel(
            name='RegistrationDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField()),
                ('conference', models.ForeignKey(to='confreg.Conference')),
            ],
            options={
                'ordering': ('day',),
            },
        ),
        migrations.CreateModel(
            name='RegistrationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('regtype', models.CharField(max_length=64)),
                ('cost', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('activeuntil', models.DateField(null=True, blank=True)),
                ('inlist', models.BooleanField(default=True)),
                ('sortkey', models.IntegerField(default=10)),
                ('specialtype', models.CharField(blank=True, max_length=5, null=True, choices=[(b'spk', b'Confirmed speaker'), (b'man', b'Manually confirmed'), (b'staff', b'Confirmed staff')])),
                ('alertmessage', models.TextField(blank=True)),
                ('upsell_target', models.BooleanField(default=False, help_text=b'Is target registration type for upselling in order to add additional options')),
                ('invoice_autocancel_hours', models.IntegerField(blank=True, help_text=b'Automatically cancel invoices after this many hours', null=True, verbose_name=b'Autocancel invoices', validators=[django.core.validators.MinValueValidator(1)])),
                ('conference', models.ForeignKey(to='confreg.Conference')),
                ('days', models.ManyToManyField(to='confreg.RegistrationDay', blank=True)),
                ('regclass', models.ForeignKey(blank=True, to='confreg.RegistrationClass', null=True)),
                ('requires_option', models.ManyToManyField(help_text=b'Requires at least one of the selected additional options to be picked', to='confreg.ConferenceAdditionalOption', blank=True)),
            ],
            options={
                'ordering': ['conference', 'sortkey'],
            },
        ),
        migrations.CreateModel(
            name='RegistrationWaitlistHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('-time',),
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roomname', models.CharField(max_length=20)),
                ('sortkey', models.IntegerField(default=100)),
                ('conference', models.ForeignKey(to='confreg.Conference')),
            ],
            options={
                'ordering': ['sortkey', 'roomname'],
            },
        ),
        migrations.CreateModel(
            name='ShirtSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shirtsize', models.CharField(max_length=32)),
                ('sortkey', models.IntegerField(default=100)),
            ],
            options={
                'ordering': ('sortkey', 'shirtsize'),
            },
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullname', models.CharField(max_length=100)),
                ('twittername', models.CharField(max_length=32, blank=True)),
                ('company', models.CharField(max_length=100, blank=True)),
                ('abstract', models.TextField(blank=True)),
                ('photofile', models.ImageField(storage=postgresqleu.confreg.dbimage.SpeakerImageStorage(), upload_to=postgresqleu.confreg.models._get_upload_path, null=True, verbose_name=b'Photo', blank=True)),
                ('lastmodified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['fullname'],
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trackname', models.CharField(max_length=100)),
                ('color', models.CharField(blank=True, max_length=20, validators=[postgresqleu.confreg.models.color_validator])),
                ('sortkey', models.IntegerField(default=100)),
                ('incfp', models.BooleanField(default=False)),
                ('conference', models.ForeignKey(to='confreg.Conference')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationWaitlistEntry',
            fields=[
                ('registration', models.OneToOneField(primary_key=True, serialize=False, to='confreg.ConferenceRegistration')),
                ('enteredon', models.DateTimeField(auto_now_add=True)),
                ('offeredon', models.DateTimeField(null=True, blank=True)),
                ('offerexpires', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Speaker_Photo',
            fields=[
                ('speaker', models.OneToOneField(primary_key=True, db_column=b'id', serialize=False, to='confreg.Speaker')),
                ('photo', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='speaker',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prepaidvoucher',
            name='user',
            field=models.ForeignKey(blank=True, to='confreg.ConferenceRegistration', null=True),
        ),
        migrations.AddField(
            model_name='prepaidbatch',
            name='regtype',
            field=models.ForeignKey(to='confreg.RegistrationType'),
        ),
    ]
