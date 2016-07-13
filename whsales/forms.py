from django import forms
from whsales.models import System, Listing, Wormhole, Effect

class ListingAddForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['system', 'price', 'notes']
        widgets = {
            'system': forms.HiddenInput()
        }
    system_name = forms.CharField(max_length=10, disabled=True, required=False)
    system_id = forms.CharField(max_length=10, widget=forms.HiddenInput())

class ListingSearchForm(forms.Form):
    wormhole_class = forms.IntegerField(min_value=1, max_value=43, required=False)
    system_name = forms.CharField(max_length=10, required=False)
    effect = forms.ModelChoiceField(required=False, queryset=Effect.objects.all())
    statics = forms.ModelMultipleChoiceField(required=False, queryset=Wormhole.objects.all())
    include_sold = forms.BooleanField(required=False)
