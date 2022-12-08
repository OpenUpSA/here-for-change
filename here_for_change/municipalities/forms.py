from django.forms import ModelForm
from .models import FindMyWardCouncillorFeedback

class FindMyWardCouncillorFeedbackForm(ModelForm):
    class Meta:
        model=FindMyWardCouncillorFeedback
        fields=["feedback","email","ward"]
