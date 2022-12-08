"""
This script clears all feedbacks in ward details. This is intended for debugs only.
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import WardDetail

if __name__=="__main__":
    for ward_detail in WardDetail.objects.all():
        ward_detail.feedback={"positive":0,"negative":0}
        ward_detail.save()
