# Problem: In Django REST Framework, why does raising serializers.ValidationError return errors in different format in validate() and create() methods?

**Date:** 2026-11-20

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

I am working on a DRF project and have a serializer like: class SomeSerializer(serializers.Serializer): number_field = serializers.IntegerField(required=False, min_value=25, max_value=100) In my settings.py, I have REST_FRAMEWORK = { other settings.... 'EXCEPTION_HANDLER': 'apps.utils.exceptions.custom_exception_handler', } In the custom exception handler, I handle ValidationError as follows: def custom_exception_handler(exc, context): # Call REST framework's default exception handler first resp

## Original URL

https://stackoverflow.com/questions/79271787/in-django-rest-framework-why-does-raising-serializers-validationerror-return-er
