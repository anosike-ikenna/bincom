$(function() {
    var pu = document.getElementById("pu");
    var pu_name = document.getElementById("pu-select");
    var pu_name_allowed = false
    pu_name.addEventListener("change", () => {
        puChecker(pu_name.value);
    })

    function puChecker(name) {
        $.ajax({
            "url": `/api/pu/${name}`,
            "dataType": "json"
        }).done(function(data) {
            if (data.exists) {
                pu_name_allowed = true;
            }
            else {
                alert("Polling unit name already exists")
            }
        }).fail(function(jqXHR, textStatus, errorThrown) {
            ;
        });
    }
    function hidePU() {
        pu.setAttribute("style", "display: none;");
    }

    function showPU() {
        pu.setAttribute("style", "display: block;");
    }

    function buildContainer(data) {
        hidePU();
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
            select.setAttribute("disabled", "disabled");
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
                showPU();
                return
            }
            buildContainer(data)
            console.log(document.getElementById("ward"));
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert("Error. please retry");
        })
    }
    var lgaSelect = document.getElementById("lga-select");
    lgaSelect.addEventListener("change", (e) => {
        var data = e.srcElement.value;
        if (data === "") {
            var ward = document.getElementById('ward');
            ward.setAttribute("style", "display: none;");
            hidePU()
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
                hidePU()
                return
            }
            showPU()
        })
    }

    function submitBtnEvent(e) {
        e.preventDefault();
        var ward = document.getElementById("ward-select");
        var poll_unit_container = document.getElementById("pu")
        var poll_unit_style = window.getComputedStyle(poll_unit_container);
        if (poll_unit_style.display == "none") {
            alert("Please select a ward");
        }
        else {
            var inputElements = document.querySelectorAll("#pu div input");
            var inputError = false;
            for (let element of inputElements) {
                if (element.value === "") {
                    inputError = true;
                    break
                }
            }
            if (inputError) {
                alert("Please fill in polling unit details");
                return
            }
            var hidden_field = document.getElementById("hidden_field");
            hidden_field.value = ward.value;
            submit_btn.removeEventListener("click", submitBtnEvent);
            // submit_btn.click();
        }
    }

    var submit_btn = document.getElementById("submit-btn");
    submit_btn.addEventListener("click", submitBtnEvent);
});