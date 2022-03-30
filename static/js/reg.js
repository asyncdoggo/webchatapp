$(document).ready(function(){
    $('#reg_form').on('submit', function(e) {
    e.preventDefault();
    var data = $("#reg_form").serializeJSON();

    data["subject"] = "register";

    if (data["passwd1"] == data["passwd2"]){

        $.post("/",{
            all_data:JSON.stringify(data)
        },function(err,req,resp){
    
            rmsg = resp["responseText"]
            if(rmsg == "success"){
                $("#success").text("Registration successful")
                $("#return").attr("hidden",false)    
            }
            if(rmsg == "already"){
                $("#error").text("User already exists")
            }
            if(rmsg == "faliure"){
                $("#error").text("An unknown error occured")
            }
        })
    
    }
    else{
        $("#success").text("passwords do not match");
    }
    
    $("#return").click(function() {
        window.location.href = "/";
    })
});
})
