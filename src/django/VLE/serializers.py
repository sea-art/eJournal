from rest_framework import serializers
from VLE.models import *
from random import randint


def user_to_dict(user):
    """Get a object of a single user

    Arguments:
    user -- user to create the object with

    returns dictionary of that user
    """
    return {
        'name': user.username,
        'picture': user.profile_picture,
        'uID': user.id
    } if user else None


def course_to_dict(course):
    return {
        'cID': course.id,
        'name': course.name,
        'auth': user_to_dict(course.author),
        'date': course.startdate,
        'abbr': course.abbreviation
    } if course else None


def student_assignment_to_dict(assignment, user):
    if not assignment:
        return None
    try:
        journal = Journal.objects.get(assignment=assignment, user=user)
    except Journal.DoesNotExist:
        journal = None

    assignment_dict = assignment_to_dict(assignment)
    assignment_dict['journal'] = journal_to_dict(journal) if journal else None

    return assignment_dict


def deadline_to_dict(assignment):
    if not assignment:
        return None

    assignment_dict = assignment_to_dict(assignment)
    assignment_dict['courses'] = [course_to_dict(course) for c in assignment.courses.all()]

    return assignment_dict


def assignment_to_dict(assignment):
    return {
        'aID': assignment.id,
        'name': assignment.name,
        'auth': user_to_dict(assignment.author),
        'description': assignment.description
    } if assignment else None


def journal_to_dict(journal):
    return {
        'jID': journal.id,
        'student': user_to_dict(journal.user),
        'stats': {
            'acquired_points': randint(0, 10),
            'graded': 1,
            'submitted': 1,
            'total_points': 10
        }  # TODO: Change random to real stats
    } if journal else None
