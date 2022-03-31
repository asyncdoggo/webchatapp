$(document).ready(function(){
    $('#login_form').on('submit', function(e) {
    e.preventDefault();
    var data = $("#login_form").serializeJSON();
    data["subject"] = "login";

    $.post("/",{
        all_data:JSON.stringify(data)
    },function(err,req,resp){

        msg = JSON.parse(resp["responseText"]);

        if(msg["status"] == "success"){
            localStorage.setItem("uname",msg["uname"]);
            localStorage.setItem("key",msg["key"]);
            send_form("/interface",{"uname":msg["uname"],"key":msg["key"]});
        }
        else if(msg["status"] == "nouser"){
            $("#error").text("Username does not exists");
        }
        else if(msg["status"] == "badpasswd"){
            $("#error").text("password is wrong");
        }
});
})
})

function send_form(action,params){
        var form = document.createElement('form');
            form.setAttribute('method', 'post');
            form.setAttribute('action', action);

            for(var key in params) {
                if(params.hasOwnProperty(key)) {
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


