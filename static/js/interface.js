var uname = "";

$(document).ready(function() {
    ullist = $("ul");
    uname = $('#uname').text();

    $.post("/",{
        all_data:`{"subject":"getusers","uname":"${uname}"}`
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
send_form('/chat',"subject","sendto","from",uname,"to",other);
}


function send_form(action,p1,p2,p3,p4,p5,p6){
    var form = document.createElement('form');
        form.setAttribute('method', 'post');
        form.setAttribute('action', action);

        var f1 = document.createElement('input');
        f1.setAttribute('type', 'hidden');
        f1.setAttribute('name', p1);
        f1.setAttribute('value', p2);
        form.appendChild(f1);
        var f2 = document.createElement('input');
        f2.setAttribute('type', 'hidden');
        f2.setAttribute('name', p3);
        f2.setAttribute('value', p4);
        form.appendChild(f2);
        var f3 = document.createElement('input');
        f3.setAttribute('type', 'hidden');
        f3.setAttribute('name', p5);
        f3.setAttribute('value', p6);
        form.appendChild(f3);

        document.body.appendChild(form);
        form.submit();
}
