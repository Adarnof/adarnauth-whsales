from django import forms
from whsales.models import System, Listing, Wormhole, Effect

class ListingAddForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['price', 'notes']
    system_name = forms.CharField(max_length=10, required=False)

    def clean_system_name(self):
        try:
            system = System.objects.get(name=self.cleaned_data['system_name'])
            return self.cleaned_data['system_name']
        except System.DoesNotExist:
            raise forms.ValidationError("Unrecognized wormhole system name.")

try:
    MAX_CLASS = System.objects.order_by('-wormhole_class')[0].wormhole_class
except:
    MAX_CLASS = 1

class ListingSearchForm(forms.Form):

    wormhole_class = forms.IntegerField(min_value=1, max_value=MAX_CLASS, required=False)
    system_name = forms.CharField(max_length=7, required=False)
    effect = forms.ModelChoiceField(required=False, queryset=Effect.objects.all())
    statics = forms.ModelMultipleChoiceField(required=False, queryset=Wormhole.objects.all())
    shattered = forms.BooleanField(required=False)
    include_sold = forms.BooleanField(required=False)
