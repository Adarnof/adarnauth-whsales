from django import forms
from whsales.models import System, Listing, Wormhole, Effect, Wanted

class ListingAddForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['system', 'system_name', 'price', 'notes']
        widgets = {
            'system': forms.HiddenInput()
        }
    system_name = forms.CharField(max_length=10, disabled=True, required=False)

try:
    MAX_CLASS = System.objects.order_by('-wormhole_class')[0].wormhole_class
except:
    MAX_CLASS = 1

class ListingSearchForm(forms.Form):

    system_name = forms.CharField(max_length=7, required=False)
    wormhole_class = forms.IntegerField(min_value=1, max_value=MAX_CLASS, required=False)
    effect = forms.ModelChoiceField(required=False, queryset=Effect.objects.all())
    statics = forms.MultipleChoiceField(required=False, choices=Wormhole.DESTINATION_CHOICES)
    shattered = forms.BooleanField(required=False)
    include_sold = forms.BooleanField(required=False)

    def clean_system_name(self):
        if not self.cleaned_data['system_name']:
            return None
        try:
            System.objects.get(name=self.cleaned_data['system_name'])
            return self.cleaned_data['system_name']
        except System.DoesNotExist:
             raise forms.ValidationError("Unrecognized wormhole system.")

class WantedAddForm(forms.ModelForm):
    class Meta:
        model = Wanted
        fields = ['system_name', 'wormhole_class', 'effect', 'statics', 'shattered', 'offering', 'notes']

    system_name = forms.CharField(max_length=7, required=False, help_text="If specified, system detail fields are ignored.")
    wormhole_class = forms.IntegerField(min_value=1, max_value=MAX_CLASS, required=False)
    statics = forms.MultipleChoiceField(required=False, choices=Wormhole.DESTINATION_CHOICES)

    def clean_system_name(self):
        if not self.cleaned_data['system_name']:
            return None
        try:
            System.objects.get(name=self.cleaned_data['system_name'])
            return self.cleaned_data['system_name']
        except System.DoesNotExist:
             raise forms.ValidationError("Unrecognized wormhole system.")

    def clean_wormhole_class(self):
        if self.cleaned_data['wormhole_class']:
            if self.cleaned_data['wormhole_class'] > 6 and self.cleaned_data['wormhole_class'] != 13:
                raise forms.ValidationError("Invalid wormhole class.")
        return self.cleaned_data['wormhole_class']

    def clean_statics(self):
        if self.cleaned_data['statics']:
            if self.cleaned_data['wormhole_class']:
                for s in self.cleaned_data['statics']:
                    if not System.objects.filter(wormhole_class=self.cleaned_data['wormhole_class']).filter(statics__destination=s).exists():
                        raise forms.ValidationError("Static %s not valid for Class %s wormholes." % (s, self.cleaned_data['wormhole_class']))
            else:
                for s in self.cleaned_data['statics']:
                    if not System.objects.filter(statics__destination=s).exists():
                        raise forms.ValidationError("No systems with static %s found." % s)
        return self.cleaned_data['statics']
