from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import *
from .forms import PollingUnitForm, AnnouncedPollingUnitResultsForm
import json


def home_page(request):
    return redirect("question_one")

def question_one(request):
    states = States.objects.filter(state_id=25)
    lgas = Lga.objects.filter(state_id=25)
    wards = Ward.objects.filter(lga_id=lgas.first().lga_id)
    polling_units = PollingUnit.objects.filter(uniquewardid=wards.first().uniqueid)
    return render(
        request,
        "main/question1.html", 
        {
            "states": states,
            "lgas": lgas,
            "wards": wards,
            "polling_units": polling_units,
        }
    )

def polling_unit_detail(request, id):
    polling_unit = get_object_or_404(PollingUnit, uniqueid=id)
    ann_poll_unit_results = AnnouncedPollingUnitResults.objects.filter(
        polling_unit_uniqueid=id
    )
    return render(
        request, 
        "main/pu_list.html", 
        {
        "polling_unit": polling_unit,
        "ann_poll_unit_results": ann_poll_unit_results.order_by("party_abbreviation")
        }
    )

def polling_unit_delete(request, id):
    polling_unit = get_object_or_404(PollingUnit, uniqueid=id)
    polling_unit.delete()
    return redirect("question_three_b")

def wards_list(request, lga_id):
    wards = Ward.objects.filter(lga_id=lga_id)
    wards_dict = [
        {
            "ward_id": ward.uniqueid,
            "ward_name": ward.ward_name,
        }
        for ward in list(wards.order_by("ward_name"))
    ]
    json_data = {"wards": wards_dict}
    return HttpResponse(
        json.dumps(json_data),
        content_type="application/json",
    )

def pu_list(request, uward_id):
    polling_units = PollingUnit.objects.filter(uniquewardid=uward_id)
    polling_units_dict = [
        {
            "pu_id": polling_unit.uniqueid,
            "pu_name": polling_unit.polling_unit_name,
        }
        for polling_unit in list(polling_units.order_by("polling_unit_name"))
    ]
    json_data = {"polling_units": polling_units_dict}
    return HttpResponse(
        json.dumps(json_data),
        content_type="application/json"
    )

def question_two(request):
    states = States.objects.filter(state_id=25)
    lgas = Lga.objects.filter(state_id=25)
    return render(
        request, 
        "main/question2.html", 
        {
            "lgas": lgas,
            "states": states,
        }
    )

def lga_result(request, id):
    lga = get_object_or_404(Lga, lga_id=id)
    party_abbr = {"PDP", "DPP", "ACN", "PPA", "CDC", "JP", "ANPP", "LABO", "CPP"}
    poll_units = PollingUnit.objects.filter(lga_id=id).order_by("polling_unit_name")
    context = [[item.uniqueid, item.polling_unit_name] for item in poll_units]
    total_votes = {key: 0 for key in sorted(list(party_abbr))}
    for polling_unit_combo in context:
        results = AnnouncedPollingUnitResults.objects.filter(
            polling_unit_uniqueid=polling_unit_combo[0])
        result_parties = set()
        result_temp = []
        polling_unit_combo.pop(0)
        if not results:
            polling_unit_combo.extend([0] * len(party_abbr))
            continue
        if len(results) > len(party_abbr):
            return HttpResponse(
                "One or more parties have multiple results for this polling unit"
            )
        for result in results:
            party_abbreviation = result.party_abbreviation
            party_score = result.party_score
            result_parties.add(party_abbreviation)
            result_temp.append([party_abbreviation, party_score])
            total_votes[party_abbreviation] += party_score
        missing_result = party_abbr - result_parties
        result_temp.extend([[party, 0] for party in missing_result])
        result_temp.sort()
        for temp in range(len(result_temp)):
            polling_unit_combo.append(result_temp[temp][1])
    
    return render(
        request, 
        "main/lga_result.html",
        {
            "lga": lga,
            "context": context,
            "parties": sorted(list(party_abbr)),
            "total_votes": total_votes,
        }
    )

def question_three(request):
    return render(request, "main/question3.html")

def question_three_a(request):
    parties = Party.objects.all()
    form = AnnouncedPollingUnitResultsForm()
    PARTY_DICT = {
        "PDP": "PDP",
        "DPP": "DPP",
        "ACN": "ACN",
        "PPA": "PPA",
        "CDC": "CDC",
        "JP": "JP",
        "ANPP": "ANPP",
        "LABOUR": "LABO",
        "CPP": "CPP",
    }
    if request.method == "POST":
        polling_unit_uniqueid = request.POST["uniqueid"]
        results = AnnouncedPollingUnitResults.objects.filter(
            polling_unit_uniqueid=polling_unit_uniqueid)
        if results:
            return HttpResponse("This polling unit already has results")
        party_results = []
        for party in parties:
            my_dict = {
                'polling_unit_uniqueid': request.POST["uniqueid"],
                'party_abbreviation': PARTY_DICT[party.partyname],
                'party_score': request.POST[str(party.id)],
                'entered_by_user': request.POST["user_name"],
                'user_ip_address': request.POST["user_ip"],
            }
            form = AnnouncedPollingUnitResultsForm(my_dict)
            if form.is_valid():
                party_results.append(form)
            else:
                return HttpResponse("An Error occured, please try again")
        [form.save() for form in party_results]
        redirect_url = reverse("pu_detail", kwargs={"id": polling_unit_uniqueid})
        return redirect(redirect_url)
    states = States.objects.filter(state_id=25)
    lgas = Lga.objects.filter(state_id=25)
    wards = Ward.objects.filter(lga_id=lgas.first().lga_id)
    polling_units = PollingUnit.objects.filter(uniquewardid=wards.first().uniqueid)
    return render(
        request,
        "main/question3a.html", 
        {
            "states": states,
            "lgas": lgas,
            "wards": wards,
            "polling_units": polling_units,
            "form": form,
            "parties": parties,
        }
    )

######### Not used #########
def pu_exists(request, name):
    data = {"exists": False}
    try:
        PollingUnit.objects.get(polling_unit_name=name)
    except PollingUnit.DoesNotExist:
        pass
    else:
        data["exists"] = False
    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )

def question_three_b(request):
    states = States.objects.filter(state_id=25)
    lgas = Lga.objects.filter(state_id=25)
    wards = Ward.objects.filter(lga_id=lgas.first().lga_id)
    polling_units = PollingUnit.objects.filter(uniquewardid=wards.first().uniqueid)
    parties = Party.objects.all()
    if request.method == "POST":
        form = PollingUnitForm(request.POST)
        if form.is_valid():
            ward = Ward.objects.get(uniqueid=request.POST["uniqueid"])
            pu = form.save(ward=ward)
            success_url = reverse("add_results", kwargs={"pu_u_id": pu.uniqueid})
            return redirect(success_url)
        else:
            return HttpResponse("An error occured, please try again!")
    return render(
        request,
        "main/question3b.html", 
        {
            "states": states,
            "lgas": lgas,
            "wards": wards,
            "polling_units": polling_units,
            "parties": parties,
        }
    )

def add_results(request, pu_u_id):
    polling_unit = get_object_or_404(PollingUnit, uniqueid=pu_u_id)
    state = States.objects.get(state_id=25)
    lga = Lga.objects.get(lga_id=polling_unit.lga_id)
    ward = Ward.objects.get(uniqueid=polling_unit.uniquewardid)
    parties = Party.objects.all()
    return render(
        request, 
        "main/add_pu_results.html",
        {
            "state": state,
            "lga": lga,
            "ward": ward,
            "polling_unit": polling_unit,
            "parties": parties,
        }
    )