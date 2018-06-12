from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'group',
                  'email',
                  'username',
                  'education',
                  'lti_id'
                  )


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id',
                  'author',
                  'abbreviation',
                  'startdate',
                  )


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('name',
                  'description',
                  'course',
                  )


class Journal(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('assignment',
                  'user',
                  )


class Entry(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('journal',
                  'datetime',
                  'late',
                  )
