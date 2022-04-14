$(document).ready(function(){
    $('#reg_form').on('submit', function(e) {
    e.preventDefault();
    var senddata = $("#reg_form").serializeJSON();

    senddata["subject"] = "register";

    if (senddata["passwd1"] == senddata["passwd2"]){
        console.log("hello");

        $.ajax({
        type:'POST',
        url:"/",
        data:JSON.stringify(senddata),
        contentType: "application/json",
        dataType: 'json',
        success:function(err,req,resp){
            rmsg = JSON.parse(resp["responseText"]);
            if(rmsg["status"] == "success"){
                $("#success").text("Registration successful");
                $("#return").attr("hidden",false);
                $("#error").text("");
            }
            else if(rmsg["status"] == "alreadyuser"){
                $("#error").text("User already exists");
            }
            else if(rmsg["status"] == "alreadyemail"){
                $("#error").text("Email already exists");
            }
            else if(rmsg["status"] == "faliure"){
                $("#error").text("An unknown error occured");
            }
            else{
                $("#error").text(rmsg["status"]);
            }
        }
        });
    
    }
    else{
        $("#error").text("passwords do not match");
    }
    
    $("#return").click(function() {
        window.location.href = "/";
    })
});
})
