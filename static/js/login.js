$(document).ready(function(){
    $('#login_form').on('submit', function(e) {
    e.preventDefault();
    var data = $("#login_form").serializeJSON();
    data["subject"] = "login"

    $.post("/",{
        all_data:JSON.stringify(data)
    },function(err,req,resp){
        if(resp["responseText"] == "success"){
            send_form("/interface","uname",data["uname"]);
        }
        else if(resp["responseText"] == "nouser"){
            $("#error").text("Username does not exists");
        }
        else if(resp["responseText"] == "badpasswd"){
            $("#error").text("password is wrong");
        }
});
})
})

function send_form(action,p1,p2){
        var form = document.createElement('form');
            form.setAttribute('method', 'post');
            form.setAttribute('action', action);

            var hiddenField = document.createElement('input');
            hiddenField.setAttribute('type', 'hidden');
            hiddenField.setAttribute('name', p1);
            hiddenField.setAttribute('value', p2);
            form.appendChild(hiddenField);
            document.body.appendChild(form);
            form.submit();
}

