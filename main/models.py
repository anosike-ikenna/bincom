from django.db import models


class States(models.Model):
    state_id = models.IntegerField(primary_key=True)
    state_name = models.CharField(max_length=50)

    class Meta:
        db_table = "states"

    def __str__(self):
        return self.state_name


class Lga(models.Model):
    uniqueid = models.BigAutoField(primary_key=True)
    lga_id = models.IntegerField()
    lga_name = models.CharField(max_length=50)
    state_id = models.ForeignKey(States, on_delete=models.CASCADE, db_column="state_id")
    lga_description = models.TextField(blank=True)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = "lga"

    def __str__(self):
        return self.lga_name


class Ward(models.Model):
    uniqueid = models.BigAutoField(primary_key=True)
    ward_id = models.IntegerField()
    ward_name = models.CharField(max_length=50)
    lga_id = models.IntegerField()
    ward_description = models.TextField(blank=True)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = "ward"

    def __str__(self):
        return self.ward_name


class PollingUnit(models.Model):
    uniqueid = models.BigAutoField(primary_key=True)
    polling_unit_id = models.IntegerField()
    ward_id = models.IntegerField()
    lga_id = models.IntegerField()
    uniquewardid = models.IntegerField(blank=True, null=True)
    # uniquewardid = models.ForeignKey(Ward, models.SET_NULL, null=True, db_column="uniquewardid")
    polling_unit_number = models.CharField(max_length=50, blank=True, null=True)
    polling_unit_name = models.CharField(max_length=50, blank=True, null=True)
    polling_unit_description = models.TextField(blank=True, null=True)
    lat = models.CharField(max_length=255, blank=True, null=True)
    long = models.CharField(max_length=255, blank=True, null=True)
    entered_by_user = models.CharField(max_length=50, blank=True, null=True)
    date_entered = models.DateTimeField(null=True)
    user_ip_address = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "polling_unit"

    def __str__(self):
        return self.polling_unit_name


# MyISAM table
class Party(models.Model):
    partyid = models.CharField(max_length=11)
    partyname = models.CharField(max_length=11)

    class Meta:
        db_table = "party"

    def __str__(self):
        return self.partyname


# MyISAM table
class AgentName(models.Model):
    name_id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=13)
    pollingunit_uniqueid = models.IntegerField()

    class Meta:
        db_table = "agentname"

    def __str__(self):
        return "{last_name}, {first_name}".format(
            last_name=self.lastname,
            first_name=self.firstname,
        )


class AnnouncedStateResults(models.Model):
    result_id = models.BigAutoField(primary_key=True)
    state_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = "announced_state_results"


class AnnouncedLgaResults(models.Model):
    result_id = models.BigAutoField(primary_key=True)
    lga_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = "announced_lga_results"


class AnnouncedWardResults(models.Model):
    result_id = models.BigAutoField(primary_key=True)
    ward_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = "announced_ward_results"


class AnnouncedPollingUnitResults(models.Model):
    result_id = models.BigAutoField(primary_key=True)
    polling_unit_uniqueid = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = "announced_pu_results"

    def __str__(self):
        return "{0} => {1}".format(self.party_abbreviation, self.party_score)