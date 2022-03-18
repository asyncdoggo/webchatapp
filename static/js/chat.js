var mid = 0;

$(document).ready(function() {
    var textarea = $("#textarea1");
    textarea.attr("readonly",true);
    var username = $("#username").text();
    console.log(username);

    $("#submit").click(function(){
        var textbox = $("#textbox1").val();
        var message = username + ":" + textbox + '\n';
        console.log(message);

        msgdata = {"subject":"sendmsg",
                    "message": message,
                }

        $.post("/",{
            all_data:JSON.stringify(msgdata)
        },function(err,req,resp){
        })
    })


    $("#logout").click(function(){
        send_form("/logout","uname",username);
    })


    getloop();
})

var msg  = "";
var mid1 = 0;
    async function getloop(){
        while(true){
        await sleep(1000);
        $.post("/",{
            all_data:"{\"subject\":\"getmsg\"}"
        },function(err,req,resp){
            msg = JSON.parse(resp["responseText"]);

            console.log(resp["responseText"])

            mes = msg["message"];
            mid = msg["mid"];

            if(mid != mid1){
                textarea1.append(mes);
                mid1=mid;
            }
        })
    }
    }

    const sleep = ms => new Promise(res => setTimeout(res, ms));
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
