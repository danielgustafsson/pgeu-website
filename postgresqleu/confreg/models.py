#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

from postgresqleu.confreg.dbimage import SpeakerImageStorage

import datetime
import pytz

from postgresqleu.countries.models import Country
from postgresqleu.invoices.models import Invoice

SKILL_CHOICES = (
	(0, "Beginner"),
	(1, "Intermediate"),
	(2, "Advanced"),
)

STATUS_CHOICES = (
	(0, "Submitted"),
	(1, "Approved"),
	(2, "Rejected"),
	(3, "Pending"), # Approved, but not confirmed
)
STATUS_CHOICES_LONG = (
	(0, "Submitted, not processed yet"),
	(1, "Fully approved"),
	(2, "Rejected"),
	(3, "Pending speaker confirmation"), # Approved, but not confirmed
)
def get_status_string(val):
	return (t for v,t in STATUS_CHOICES if v==val).next()
def get_status_string_long(val):
	return (t for v,t in STATUS_CHOICES_LONG if v==val).next()

def color_validator(value):
	if not value.startswith('#'):
		raise ValidationError('Color values must start with #')
	if len(value) != 7:
		raise ValidationError('Color values must be # + 7 characters')
	for n in range(0,3):
		try:
			int(value[n*2+1:n*2+2+1], 16)
		except ValueError:
			raise ValidationError('Invalid value in color specification')

class PaymentOption(models.Model):
	name = models.CharField(max_length=64, blank=False, null=False)
	infotext = models.TextField(blank=False, null=False)
	paypalrecip = models.EmailField(max_length=1024, null=True, blank=True)
	sortkey = models.IntegerField(null=False, blank=False)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['sortkey', ]

class Conference(models.Model):
	urlname = models.CharField(max_length=32, blank=False, null=False, unique=True)
	conferencename = models.CharField(max_length=64, blank=False, null=False)
	startdate = models.DateField(blank=False, null=False)
	enddate = models.DateField(blank=False, null=False)
	location = models.CharField(max_length=128, blank=False, null=False)
	contactaddr = models.EmailField(blank=False,null=False)
	paymentoptions = models.ManyToManyField(PaymentOption)
	active = models.BooleanField(blank=False,null=False,default=True, verbose_name="Registration open")
	callforpapersopen = models.BooleanField(blank=False,null=False,default=False)
	feedbackopen = models.BooleanField(blank=False,null=False,default=True)
	conferencefeedbackopen = models.BooleanField(blank=False,null=False,default=False)
	scheduleactive = models.BooleanField(blank=False,null=False,default=False,verbose_name="Schedule publishing active")
	sessionsactive = models.BooleanField(blank=False,null=False,default=False,verbose_name="Session list publishing active")
	schedulewidth = models.IntegerField(blank=False, default=600, null=False, verbose_name="Width of HTML schedule")
	pixelsperminute = models.FloatField(blank=False, default=1.5, null=False, verbose_name="Vertical pixels per minute")
	confurl = models.CharField(max_length=128, blank=False, null=False)
	listadminurl = models.CharField(max_length=128, blank=True, null=False)
	listadminpwd = models.CharField(max_length=128, blank=True, null=False)
	speakerlistadminurl = models.CharField(max_length=128, blank=True, null=False)
	speakerlistadminpwd = models.CharField(max_length=128, blank=True, null=False)
	twitter_user = models.CharField(max_length=32, blank=True, null=False)
	twitter_attendeelist = models.CharField(max_length=32, blank=True, null=False)
	twitter_speakerlist = models.CharField(max_length=32, blank=True, null=False)
	twitter_token = models.CharField(max_length=128, blank=True, null=False)
	twitter_secret = models.CharField(max_length=128, blank=True, null=False)

	administrators = models.ManyToManyField(User, null=False, blank=True)
	testers = models.ManyToManyField(User, null=False, blank=True, related_name="testers_set")
	talkvoters = models.ManyToManyField(User, null=False, blank=True, related_name="talkvoters_set")
	asktshirt = models.BooleanField(blank=False, null=False, default=True)
	askfood = models.BooleanField(blank=False, null=False, default=True)
	askshareemail = models.BooleanField(null=False, blank=False, default=False)
	skill_levels = models.BooleanField(blank=False, null=False, default=True)
	autoapprove = models.BooleanField(blank=False, null=False, default=False)
	additionalintro = models.TextField(blank=True, null=False)
	basetemplate = models.CharField(max_length=128, blank=True, null=True, default=None)
	templatemodule = models.CharField(max_length=128, blank=True, null=True, default=None)
	templatemediabase = models.CharField(max_length=128, blank=True, null=True, default=None)
	callforpapersintro = models.TextField(blank=True, null=False)
	lastmodified = models.DateTimeField(auto_now=True, null=False, blank=False)
	newsjson = models.CharField(max_length=128, blank=True, null=True, default=None)
	accounting_object = models.CharField(max_length=30, blank=True, null=True, verbose_name="Accounting object name")

	def __unicode__(self):
		return self.conferencename

	class Meta:
		ordering = [ '-startdate', ]

	@property
	def conferencedatestr(self):
		if self.enddate and not self.startdate==self.enddate:
			return "%s - %s" % (
				self.startdate.strftime("%Y-%m-%d"),
				self.enddate.strftime("%Y-%m-%d")
			)
		else:
			return self.startdate.strftime("%Y-%m-%d")

	@property
	def template_override(self):
		if self.basetemplate and len(self.basetemplate) > 0:
			return self.basetemplate
		return None

	@property
	def mediabase_override(self):
		if self.templatemediabase and len(self.templatemediabase) > 0:
			return self.templatemediabase
		return None

class RegistrationClass(models.Model):
	conference = models.ForeignKey(Conference, null=False)
	regclass = models.CharField(max_length=64, null=False, blank=False)
	badgecolor = models.CharField(max_length=20, null=False, blank=True, help_text='Badge color in hex format', validators=[color_validator, ])

	def __unicode__(self):
		return self.regclass

	def colortuple(self):
		return tuple([int(self.badgecolor[n*2+1:n*2+2+1], 16) for n in range(0,3)])

	class Meta:
		verbose_name_plural = 'Registration classes'

class RegistrationDay(models.Model):
	conference = models.ForeignKey(Conference, null=False)
	day = models.DateField(null=False, blank=False)

	def __unicode__(self):
		return self.day.strftime('%a, %d %b')

class RegistrationType(models.Model):
	conference = models.ForeignKey(Conference, null=False)
	regtype = models.CharField(max_length=64, null=False, blank=False)
	regclass = models.ForeignKey(RegistrationClass, null=True, blank=True)
	cost = models.IntegerField(null=False)
	active = models.BooleanField(null=False, blank=False, default=True)
	inlist = models.BooleanField(null=False, blank=False, default=True)
	sortkey = models.IntegerField(null=False, blank=False, default=10)
	days = models.ManyToManyField(RegistrationDay, blank=True)

	class Meta:
		ordering = ['conference', 'sortkey', ]

	def __unicode__(self):
		if self.cost == 0:
			return self.regtype
		else:
			return "%s (EUR %s)" % (self.regtype, self.cost)

	def is_registered_type(self):
		# Starts with * means "not attending"
		if self.regtype.startswith('*'): return False
		return True

	@property
	def stringcost(self):
		return str(self.cost)

class ShirtSize(models.Model):
        shirtsize = models.CharField(max_length=32)

        def __unicode__(self):
                return self.shirtsize

class ConferenceAdditionalOption(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	name = models.CharField(max_length=100, null=False, blank=False)
	cost = models.IntegerField(null=False)
	maxcount = models.IntegerField(null=False)

	class Meta:
		ordering = ['name', ]

	def __unicode__(self):
		# This is what renders in the multichoice checkboxes, so make
		# it nice for the end user.
		if self.cost > 0:
			coststr = " (EUR %s)" % self.cost
		else:
			coststr = ""
		if self.maxcount == -1:
			return "%s%s (currently not available)" % (self.name, coststr)
		if self.maxcount > 0:
			usedcount = self.conferenceregistration_set.count()
			return "%s%s (%s of %s available)" % (self.name, coststr,
												  self.maxcount - usedcount,
												  self.maxcount)
		return "%s%s" % (self.name, coststr)

class BulkPayment(models.Model):
	# User that owns this bulk payment
	user = models.ForeignKey(User, null=False, blank=False)

	# We attach it to a specific conference
	conference = models.ForeignKey(Conference, null=False, blank=False)

	# Invoice, once one has been created
	invoice = models.ForeignKey(Invoice, null=True, blank=True)
	numregs = models.IntegerField(null=False, blank=False)

	createdat = models.DateField(null=False, blank=False, auto_now_add=True)
	paidat = models.DateField(null=True, blank=True)

	def ispaid(self):
		return self.paidat and True or False
	ispaid.boolean = True

	def adminstring(self):
		return "%s at %s" % (self.user, self.createdat)

	def __unicode__(self):
		return u"Bulk payment for %s created %s (%s registrations, €%s): %s" % (self.conference, self.createdat, self.numregs, self.invoice.total_amount, self.paidat and 'Paid' or 'Not paid yet')

class ConferenceRegistration(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	regtype = models.ForeignKey(RegistrationType, null=True, blank=True, verbose_name="Registration type")
	attendee = models.ForeignKey(User, null=False, blank=False)
	firstname = models.CharField(max_length=100, null=False, blank=False, verbose_name="First name")
	lastname = models.CharField(max_length=100, null=False, blank=False, verbose_name="Last name")
	email = models.EmailField(null=False, blank=False, verbose_name="E-mail address")
	company = models.CharField(max_length=100, null=False, blank=True, verbose_name="Company")
	address = models.TextField(max_length=200, null=False, blank=True, verbose_name="Address")
	country = models.ForeignKey(Country, null=False, blank=False, verbose_name="Country")
	phone = models.CharField(max_length=100, null=False, blank=True, verbose_name="Phone number")
	shirtsize = models.ForeignKey(ShirtSize, null=True, blank=True, verbose_name="Preferred T-shirt size")
	dietary = models.CharField(max_length=100, null=False, blank=True, verbose_name="Special dietary needs")
	additionaloptions = models.ManyToManyField(ConferenceAdditionalOption, null=False, blank=True, verbose_name="Additional options")
	twittername = models.CharField(max_length=100, null=False, blank=True, verbose_name="Twitter account")
	nick = models.CharField(max_length=100, null=False, blank=True, verbose_name="Nickname")
	shareemail = models.BooleanField(null=False, blank=False, default=False, verbose_name="Share e-mail address with sponsors")

	# Admin fields!
	payconfirmedat = models.DateField(null=True, blank=True, verbose_name="Payment confirmed")
	payconfirmedby = models.CharField(max_length=16, null=True, blank=True, verbose_name="Payment confirmed by")
	created = models.DateTimeField(null=False, blank=False, default=datetime.datetime.now, verbose_name="Registration created")

	# If an invoice is generated, link to it here so we can find our
	# way back easily.
	invoice = models.ForeignKey(Invoice, null=True, blank=True)
	bulkpayment = models.ForeignKey(BulkPayment, null=True, blank=True)

	# Access from templates requires properties
	@property
	def isregistered(self):
		if not self.id: return False
		if not self.regtype: return False
		return self.regtype.is_registered_type()

	@property
	def needspayment(self):
		if not self.regtype: return False
		if self.regtype.cost == 0:
			# If we have additional options that cost, we might still need
			# to check this.
			for ao in self.additionaloptions.all():
				if ao.cost > 0:
					# If any option has a cost, we need to request payment
					return True
			return False
		return True

	@property
	def fullname(self):
		return "%s %s" % (self.firstname, self.lastname)

	@property
	def invoicerows(self):
		# Return the rows that would be used to build an invoice for this
		# registration. Format is tuple of (description, num, cost)
		r = [('%s - %s (%s)' % (self.conference, self.regtype.regtype, self.email), 1, self.regtype.cost)]
		for a in self.additionaloptions.all():
			if a.cost > 0:
				r.append(('   %s' % a.name, 1, a.cost))
		return r

	def has_invoice(self):
		return not self.invoice is None
	has_invoice.boolean = True

	def short_regtype(self):
		return self.regtype.regtype[:30]
	short_regtype.short_description = 'Reg type'

	@property
	def additionaloptionlist(self):
		return ",\n".join([a.name for a in self.additionaloptions.all()])

	# For the admin interface (mainly)
	def __unicode__(self):
		return "%s: %s %s <%s>" % (self.conference, self.firstname, self.lastname, self.email)

class Track(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	trackname = models.CharField(max_length=100, null=False, blank=False)
	color = models.CharField(max_length=20, null=False, blank=True, validators=[color_validator, ])
	sortkey = models.IntegerField(null=False, default=100, blank=False)

	def __unicode__(self):
		return "%s (%s)" % (self.trackname, self.conference)

class Room(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	roomname = models.CharField(max_length=20, null=False, blank=False)

	def __unicode__(self):
		return "%s (%s)" % (self.roomname, self.conference)


class Speaker(models.Model):
	def get_upload_path(instance, filename):
		return "%s" % instance.id

	user = models.ForeignKey(User, null=True, blank=True, unique=True)
	fullname = models.CharField(max_length=100, null=False, blank=False)
	twittername = models.CharField(max_length=32, null=False, blank=True)
	company = models.CharField(max_length=100, null=False, blank=True)
	abstract = models.TextField(null=False, blank=True)
	photofile = models.ImageField(upload_to=get_upload_path, storage=SpeakerImageStorage(), blank=True, null=True, verbose_name="Photo")
	lastmodified = models.DateTimeField(auto_now=True, null=False, blank=False)


	@property
	def name(self):
		return self.fullname

	@property
	def email(self):
		return self.user.email

	def has_abstract(self):
		return len(self.abstract)>0
	has_abstract.boolean = True

	def has_photo(self):
		return (self.photofile != None and self.photofile != "")
	has_photo.boolean= True

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['fullname', ]

class DeletedItems(models.Model):
	itemid = models.IntegerField(null=False, blank=False)
	type = models.CharField(max_length=16, blank=False, null=False)
	deltime = models.DateTimeField(blank=False, null=False)

class Speaker_Photo(models.Model):
	speaker = models.ForeignKey(Speaker, db_column='id', primary_key=True)
	photo = models.TextField(null=False, blank=False)

	def __unicode__(self):
		return self.speaker.name

	def delete(self):
		# Remove reference from speaker, so we don't think the pic is there
		self.speaker.photofile = None
		self.speaker.save()
		super(Speaker_Photo, self).delete()

class ConferenceSessionScheduleSlot(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	starttime = models.DateTimeField(null=False, blank=False)
	endtime = models.DateTimeField(null=False, blank=False)

	def __unicode__(self):
		return "%s - %s" % (self.starttime, self.endtime)

class ConferenceSession(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	speaker = models.ManyToManyField(Speaker, blank=True)
	title = models.CharField(max_length=200, null=False, blank=False)
	starttime = models.DateTimeField(null=True, blank=True)
	endtime = models.DateTimeField(null=True, blank=True)
	track = models.ForeignKey(Track, null=True, blank=True)
	room = models.ForeignKey(Room, null=True, blank=True)
	cross_schedule = models.BooleanField(null=False, default=False)
	can_feedback = models.BooleanField(null=False, default=True)
	abstract = models.TextField(null=False, blank=True)
	skill_level = models.IntegerField(null=False, default=1, choices=SKILL_CHOICES)
	status = models.IntegerField(null=False, default=0, choices=STATUS_CHOICES)
	submissionnote = models.TextField(null=False, blank=True, verbose_name="Submission notes")
	initialsubmit = models.DateTimeField(null=True, blank=True, verbose_name="Submitted")
	tentativescheduleslot = models.ForeignKey(ConferenceSessionScheduleSlot, null=True, blank=True)
	tentativeroom = models.ForeignKey(Room, null=True, blank=True, related_name='tentativeroom')
	lastmodified = models.DateTimeField(auto_now=True, null=False, blank=False)

	# NOTE! Any added fields need to be considered for inclusion in
	# forms.CallForPapersForm!

	# Not a db field, but set from the view to track if the current user
	# has given any feedback on this session.
	has_feedback = False

	@property
	def speaker_list(self):
		return ", ".join([s.name for s in self.speaker.all()])

	@property
	def skill_level_string(self):
		return (t for v,t in SKILL_CHOICES if v==self.skill_level).next()

	@property
	def status_string(self):
		return get_status_string(self.status)

	@property
	def status_string_long(self):
		return get_status_string_long(self.status)

	def __unicode__(self):
		return "%s: %s (%s)" % (
			self.speaker_list,
			self.title,
			self.starttime,
		)

	@property
	def shorttitle(self):
		return "%s (%s)" % (
			self.title,
			self.starttime,
		)

	@property
	def utcstarttime(self):
		return self._utc_time(self.starttime)

	@property
	def utcendtime(self):
		return self._utc_time(self.endtime)

	def _utc_time(self, time):
		if not hasattr(self, '_localtz'):
			self._localtz = pytz.timezone(settings.TIME_ZONE)
		return self._localtz.localize(time).astimezone(pytz.utc)

	class Meta:
		ordering = [ 'starttime', ]

class ConferenceSessionVote(models.Model):
	session = models.ForeignKey(ConferenceSession, null=False, blank=False)
	voter = models.ForeignKey(User, null=False, blank=False)
	vote = models.IntegerField(null=True, blank=False)
	comment = models.CharField(max_length=200, null=True, blank=True)

	class Meta:
		unique_together = ( ('session', 'voter',), )

class ConferenceSessionFeedback(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	session = models.ForeignKey(ConferenceSession, null=False, blank=False)
	attendee = models.ForeignKey(User, null=False, blank=False)
	topic_importance = models.IntegerField(null=False, blank=False)
	content_quality = models.IntegerField(null=False, blank=False)
	speaker_knowledge = models.IntegerField(null=False, blank=False)
	speaker_quality = models.IntegerField(null=False, blank=False)
	speaker_feedback = models.TextField(null=False, blank=True, verbose_name='Comments to the speaker')
	conference_feedback = models.TextField(null=False, blank=True, verbose_name='Comments to the conference organizers')

	def __unicode__(self):
		return unicode("%s - %s (%s)") % (self.conference, self.session, self.attendee)

class ConferenceFeedbackQuestion(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	question = models.CharField(max_length=100, null=False, blank=False)
	isfreetext = models.BooleanField(blank=False, null=False, default=False)
	textchoices = models.CharField(max_length=500, null=False, blank=True)
	sortkey = models.IntegerField(null=False, default=100)
	newfieldset = models.CharField(max_length=100, null=False, blank=True)

	def __unicode__(self):
		return "%s: %s" % (self.conference, self.question)

	class Meta:
		ordering = ['conference', 'sortkey', ]

class ConferenceFeedbackAnswer(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	question = models.ForeignKey(ConferenceFeedbackQuestion, null=False, blank=False)
	attendee = models.ForeignKey(User, null=False, blank=False)
	rateanswer = models.IntegerField(null=True)
	textanswer = models.TextField(null=False, blank=True)

	def __unicode__(self):
		return "%s - %s: %s" % (self.conference, self.attendee, self.question.question)

	class Meta:
		ordering = ['conference', 'attendee', 'question', ]

class PrepaidBatch(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	regtype = models.ForeignKey(RegistrationType, null=False, blank=False)
	buyer = models.ForeignKey(User, null=False, blank=False)

	def __unicode__(self):
		return "%s: %s for %s" % (self.conference, self.regtype, self.buyer)

	class Meta:
		verbose_name_plural = "Prepaid batches"
		ordering = ['conference', 'id', ]

class PrepaidVoucher(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	vouchervalue = models.CharField(max_length=100, null=False, blank=False, unique=True)
	batch = models.ForeignKey(PrepaidBatch, null=False, blank=False)
	user = models.ForeignKey(ConferenceRegistration, null=True, blank=True)
	usedate = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return self.vouchervalue

	class Meta:
		ordering = ['batch', 'vouchervalue', ]
