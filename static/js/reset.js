$(document).ready(function () {
    $('#resetpass').on('submit', function (e) {
        e.preventDefault();
        var data = $("#resetpass").serializeJSON();
        data["subject"] = "resetpass";

        if (data["newpass"] == data["newpass2"]) {

            $.ajax({
                type: 'POST',
                url: "/",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: 'json',
                success: function (err, req, resp) {

                    msg = JSON.parse(resp["responseText"]);


                    if (msg["status"] == "success") {
                        $("#success").attr("hidden", false);
                        $("#hbutton").attr("hidden", false);
                        $("#error").text("");
                        $("#success").text("Reset Successful");

                    }
                    else if (msg["status"] == "nouser") {
                        $("#error").text("Username does not exists");
                        $("#success").text("");
                    }
                    else if (msg["status"] == "badpass") {
                        $("#error").text("password is wrong");
                    }
                    else {
                        $("#error").text(msg["status"]);
                    }
                }
            });
        }
        else {
            $("#error").text("New password does not match");
        }
    })
})

$("#hbutton").click(function () {
    window.location.href = "/";
})

function send_form(action, params) {
    var form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', action);

    for (var key in params) {
        if (params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


