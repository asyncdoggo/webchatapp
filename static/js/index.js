$(document).ready(function(){
    $("#register").click(function(){
        window.location.href = "/register"
    })

    $("#login").click(function(){
        window.location.href = "/login"
    })

    try{
    var key = localStorage.getItem("key");
    var uname = localStorage.getItem("uname");

    if(key.length){

        $.post("/",{
            all_data:`{"subject":"login","uname":"${uname}","key":"${key}"}`
        },function(err,req,resp){
            msg = resp["responseText"];
            if(msg == "success"){
                send_form("/interface",{"key":key,"uname":uname});
            }
        });
    }
    }
    catch(e){
    }
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