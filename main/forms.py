from django import forms
from django.core.exceptions import ValidationError
from .models import PollingUnit, AnnouncedPollingUnitResults


PARTY_OPTS = {"PDP", "DPP", "ACN", "PPA", "CDC", "JP", "PDP", "ANPP", "LABO", "CPP"}

class PollingUnitForm(forms.ModelForm):

    class Meta:
        model = PollingUnit
        fields = (
            "polling_unit_id",
            "polling_unit_number",
            "polling_unit_name",
            "polling_unit_description",
            "lat",
            "long",
            "entered_by_user",
            "user_ip_address",
        )

    def save(self, ward):
        self.instance.uniquewardid = ward.uniqueid
        self.instance.ward_id = ward.ward_id
        self.instance.lga_id = ward.lga_id
        return super().save()


class AnnouncedPollingUnitResultsForm(forms.ModelForm):

    class Meta:
        model = AnnouncedPollingUnitResults
        fields = "__all__"

    def clean_party_abbreviation(self):
        new_party = self.cleaned_data["party_abbreviation"].upper()
        if new_party not in PARTY_OPTS:
            raise ValidationError(
                "Party abbr. not recognized, options are: "
                "{}".format(PARTY_OPTS)
            )
        return new_party