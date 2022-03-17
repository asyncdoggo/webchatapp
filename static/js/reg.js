$(document).ready(function(){
    $('#reg_form').on('submit', function(e) {
    e.preventDefault();
    var data = $("#reg_form").serializeJSON();

    data["subject"] = "register";

    $.post("/",{
        all_data:JSON.stringify(data)
    },function(err,req,resp){

        rmsg = resp["responseText"]
        if(rmsg == "success"){
            $("#success").text("Rgistration successful")
            $("#return").attr("hidden",false)    
        }
        if(rmsg == "already"){
            $("#error").text("User already exists")
        }
        if(rmsg == "faliure"){
            $("#error").text("An unknown error occured")
        }
    })

    $("#return").click(function() {
        window.location.href = "/";
    })
});
})
