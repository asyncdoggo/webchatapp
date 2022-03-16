$(document).ready(function(){
    $("#button1").click(function() {
        var uname = $("#username").val()

        var unamedata = {
            "subject":"login",
            "username":uname
        }

        $.post("/",{
            all_data:JSON.stringify(unamedata)
        },function(err,req,resp){
            console.log(resp);
            window.location.href = "/"+resp["responseText"];
        })
    })
})