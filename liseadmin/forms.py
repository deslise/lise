from django import forms

from managedata.models import RequestCategory, CategoryBusiness


class RefuseRequests(forms.ModelForm):
    reason = forms.CharField(max_length=500, required=True)

    class Meta:
        model = RequestCategory
        fields = ('reason',)

    def clean(self):
        data = self.cleaned_data
        return data

class AcceptRequests(forms.ModelForm):

    class Meta:
        model = RequestCategory
        fields = ('category_related',)

    def clean(self):
        data = self.cleaned_data
        return data