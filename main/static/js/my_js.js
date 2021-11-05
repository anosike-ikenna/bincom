$(function() {
    var view_btn = document.getElementById("view-btn");
    view_btn.addEventListener("click", (e) => {
        var pu_select = document.getElementById("pu-select");
        view_btn.setAttribute("href", `/pu/${pu_select.value}/`);
    })
    function buildContainer(data) {
        view_btn.setAttribute("style", "display: none;")
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
        // var option_blank = document.createElement("option");
        // option_blank.value = "";
        // option_blank.appendChild(document.createTextNode("-----Select an option-----"));
        // select.appendChild(option_blank);
        view_btn.setAttribute("style", "display: inline;");
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
            view_btn.setAttribute("style", "display: none;");
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
        view_btn.setAttribute("style", "display: none;");
        var data = e.srcElement.value;
        if (data === "") {
            var ward = document.getElementById('ward');
            ward.setAttribute("style", "display: none;");
            var pu = document.getElementById("pu");
            pu.setAttribute("style", "display: none;")
            return
        }
        view_btn.setAttribute("style", "display: none;");
        var ward_opts = document.querySelector(".ward-select")
        ward_opts.remove();
        var data_type = "lga"
        getData(data_type, data)
    })

    function addWardEventListener () {
        var wardSelect = document.getElementById("ward-select");
        wardSelect.addEventListener("change", (e) => {
            view_btn.setAttribute("style", "display: none;");
            var data = e.srcElement.value;
            if (data == "") {
                view_btn.setAttribute("style", "display: none")
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
});