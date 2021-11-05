$(function() {
    function buildContainer(data) {
        var pu = document.getElementById('pu');
        pu.setAttribute("style", "display: none;");
        var container = document.getElementById("ward");
        var select = document.createElement("select");
        select.setAttribute("class", "form-control show-tick ward-select");
        select.setAttribute("data-live-search", "true");
        select.setAttribute("id", "ward-select");
        var option_blank = document.createElement("option");
        option_blank.value = "";
        option_blank.appendChild(document.createTextNode("-----Select an option-----"));
        select.appendChild(option_blank);
        for (let ward of data.wards) {
            var option = document.createElement("option");
            option.setAttribute("class", "m-l-20 ward-option");
            option.setAttribute("value", String(ward.ward_id));
            option.appendChild(document.createTextNode(ward.ward_name));
            select.appendChild(option);
        }
        if (data.wards.length == 0) {
            var option = document.createElement("option");
            option.setAttribute("class", "m-l-20 ward-option");
            option.appendChild(document.createTextNode("No wards available"));
            select.setAttribute("disabled", "disabled")
            select.appendChild(option);
        }
        container.appendChild(select);
        container.setAttribute("style", "display: block;")
        addWardEventListener()
    }

    function buildPuContainer(data) {
        var container = document.getElementById("pu");
        var select = document.createElement("select");
        select.setAttribute("class", "form-control show-tick ward-select");
        select.setAttribute("data-live-search", "true");
        select.setAttribute("id", "pu-select");
        for (let pu of data.polling_units) {
            var option = document.createElement("option");
            option.setAttribute("class", "m-l-20 ward-option");
            option.setAttribute("value", String(pu.pu_id));
            option.appendChild(document.createTextNode(pu.pu_name));
            select.appendChild(option);
        }
        if (data.polling_units.length == 0) {
            // option_blank.remove()
            var option = document.createElement("option");
            option.setAttribute("class", "m-l-20 ward-option");
            option.appendChild(document.createTextNode("No Polling units available"));
            select.setAttribute("disabled", "disabled")
            select.appendChild(option);
        }
        container.appendChild(select);
        container.setAttribute("style", "display: block;");
        addWardEventListener();
    }

    function getData(data_type, data) {
        const MAPP = {
            "lga": "ward",
            "ward": "pu",
        }
        $.ajax({
            "url": `/api/${data_type}/${data}/${MAPP[data_type]}/`,
            "dataType": "json"
        }).done(function(data) {
            if (data_type == "ward") {
                buildPuContainer(data);
                return
            }
            buildContainer(data)
            console.log(document.getElementById("ward"));
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert("Error. please retry")
        })
    }
    var lgaSelect = document.getElementById("lga-select");
    lgaSelect.addEventListener("change", (e) => {
        var data = e.srcElement.value;
        if (data === "") {
            var ward = document.getElementById('ward');
            ward.setAttribute("style", "display: none;");
            var pu = document.getElementById("pu");
            pu.setAttribute("style", "display: none;")
            return
        }
        var ward_opts = document.querySelector(".ward-select")
        ward_opts.remove();
        var data_type = "lga"
        getData(data_type, data)
    })

    function addWardEventListener () {
        var wardSelect = document.getElementById("ward-select");
        wardSelect.addEventListener("change", (e) => {
            var data = e.srcElement.value;
            if (data == "") {
                var pu = document.getElementById("pu");
                pu.setAttribute("style", "display: none;")
                return
            }
            var pu_select =document.getElementById("pu-select");
            pu_select.remove()
            var data_type = "ward"
            getData(data_type, data);
        })
    }

    function submitBtnEvent(e) {
        e.preventDefault();
        var poll_unit = document.getElementById("pu-select");
        var poll_unit_container = document.getElementById("pu")
        var poll_unit_style = window.getComputedStyle(poll_unit_container);
        if (poll_unit_style.display == "none") {
            alert("select a polling unit");
        }
        else {
            if (!Number(poll_unit.value)) {
                alert("You cannot add results to a non-existent polling unit");
                return
            }
            var hidden_field = document.getElementById("hidden_field");
            hidden_field.value = poll_unit.value;
            console.log(hidden_field)
            submit_btn.removeEventListener("click", submitBtnEvent)
            submit_btn.click()
        }
    }

    var submit_btn = document.getElementById("submit-btn");
    submit_btn.addEventListener("click", submitBtnEvent);
});