from VLE.models import *
import random
import datetime


def make_user(username, password, email=None, lti_id=None, profile_picture=None):
    user = User(username=username, email=email, lti_id=lti_id)
    user.save()
    user.set_password(password)
    user.profile_picture = profile_picture if profile_picture else '/static/oh_no/{}.png'.format(random.randint(1, 10))
    user.save()
    return user


def make_course(name, abbrev, date=None):
    course = Course(name=name, abbreviation=abbrev, startdate=date)
    course.save()
    return course


def make_assignment(name, description, author=None):
    assign = Assignment(name=name, description=description, author=author)
    assign.save()
    return assign


def make_journal(assignment, user):
    journal = Journal(assignment=assignment, user=user)
    journal.save()
    return journal


def make_entry(journal, template=None, grade=False, late=False):
    entry = Entry(journal=journal, template=template, grade=grade, late=late)
    entry.save()
    return entry


def make_entry_template(name):
    entry_template = EntryTemplate(name=name)
    entry_template.save()
    return entry_template


def make_field(descrip, loc, template, type='t'):
    field = Field(type=type, description=descrip, location=loc, template=template)
    field.save()
    return field


def make_content(entry, data, field=None):
    content = Content(field=field, entry=entry, data=data)
    content.save()
    return content


def make_deadline(format, datetime=datetime.datetime.now()):
    deadline = Deadline(format=format, datetime=datetime)
    deadline.save()
    return deadline


def make_journal_format():
    journal_format = JournalFormat()
    journal_format.save()
    return journal_format
