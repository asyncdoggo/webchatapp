var mid = 0;
var username = sessionStorage.getItem("from");
var touser = sessionStorage.getItem("touser");
var getdata = {};
var key = "";

const sleep = ms => new Promise(res => setTimeout(res, ms));

$(document).ready(function() {
    key = localStorage.getItem("key");
    var textarea = $("#textarea1");
    textarea.attr("readonly",true);
    getdata = {"subject":"getmsg","touser":touser,"fromuser":username,"key":key}


    console.log(username);

    $("#submit").click(function(){
        var textbox = $("#textbox1").val();
        var message = username + ":" + textbox + '\n';
        console.log(message);

        msgdata = {"subject":"sendmsg",
                    "message": message,
                    "touser":touser,
                    "fromuser":username,
                    "key":key
                }

        $.post("/",{
            all_data:JSON.stringify(msgdata)
        },function(err,req,resp){
            var res = resp["responseText"];
            console.log(res);
        })
    })


    $("#logout").click(function(){
        localStorage.clear();
        send_form("/logout",{"uname":username,"key":key});
    })


    getloop();
})


var getdata = {"subject":"getmsg",
            "touser":touser,
            "fromuser":username
                }

var msg  = "";

var count = 0
var prev = count;
async function getloop(){
        var textarea = $("#textarea1");
        while(true){
        await sleep(1000);

        $.post("/",{
            all_data:JSON.stringify(getdata)
        },function(err,req,resp){
            console.log(resp["responseText"])
            msg = JSON.parse(resp["responseText"]);
            count = Object.keys(msg).length;

            if (count > prev){
            textarea.val("");
            for (m in Object.keys(msg)){
            textarea.val(textarea.val() + msg[m]);
            prev = count;
        }
        }
        })
    }
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
