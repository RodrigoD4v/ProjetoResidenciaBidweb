from django.contrib import admin
from .models import TestConfig, TestResult, Vulnerability

admin.site.register(TestConfig)
admin.site.register(TestResult)
admin.site.register(Vulnerability)
