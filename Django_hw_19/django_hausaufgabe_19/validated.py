from rest_framework import serializers
from .models import Category
from django.utils import timezone

def validated_name(value, instance=None):
    if instance and instance.name == value:
        return value
    if Category.objects.filter(name=value).exists():
        raise serializers.ValidationError('Category is exists')
    return value


def validate_deadline(data):
    if data > timezone.now():
        return data
    else:
        raise serializers.ValidationError('the deadline date cannot be in the past')
