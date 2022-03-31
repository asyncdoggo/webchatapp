var uname = "";
var key = "";
$(document).ready(function() {
    key = localStorage.getItem("key");
    ullist = $("ul");
    uname = localStorage.getItem("uname");

    $("#logout").click(function(){
        localStorage.clear();
        send_form("/logout",{"uname":uname,"key":key});
    })

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
sessionStorage.setItem("touser",other);
sessionStorage.setItem("from",uname);
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