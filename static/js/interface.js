var uname = "";
var key = ""
$(document).ready(function() {
    key = document.cookie;
    document.cookie = `${key};expires=Thu, 18 Dec 1990 12:00:00 UTC;path=/interface`;
    ullist = $("ul");
    uname = $('#uname').text();

    $.post("/",{
        all_data:`{"subject":"getusers","uname":"${uname}","key":${key}}`
    },function(err,req,resp){
        msg = JSON.parse(resp["responseText"]);
        ullist.empty();
        for(i in Object.keys(msg)){
        ullist.append(`<li><button id="${msg[i]}">${msg[i]}</button></li>`);
        document.getElementById(msg[i]).onclick = buttonclick;
        }
    })
});

function buttonclick(){
var other = $(this).text();
document.cookie = `${key};path=/chat`;
send_form('/chat',{"subject":"sendto","from":uname,"to":other,"key":key});
}


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