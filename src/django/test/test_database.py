import datetime
from django.test import TestCase
from VLE.models import *


class DataBaseTests(TestCase):
    def test_foreignkeys(self):
        """
        Testing the foreignkeys.
        """
        check = True
        user_test = User(group='SD', email='lers@uva.nl', username='lers',
                         passhash='lers123', education='uva', lti_id='1')
        course_test = Course(name='tname', abbreviation='XXXX',
                             startdate=datetime.date.today())
        user_test.save()
        course_test.save()
        course_test.author.add(user_test)
        ass_test = Assignment(name='tcolloq', description='description')
        ass_test.save()
        ass_test.course.add(course_test)
        journ_test = Journal(user=user_test, assignment=ass_test)
        journ_test.save()
        entr_test = Entry(journal=journ_test,
                          datetime=datetime.datetime.today(), late=True)
        entr_test.save()
        check &= entr_test.journal.pk == journ_test.pk
        check &= journ_test.user.pk == user_test.pk
        check &= journ_test.assignment.pk == ass_test.pk
        check &= course_test.author.all()[0].pk == user_test.pk
        self.assertIs(check, True)
