$(document).ready(function() {
    ullist = $("ul");
    var uname = $('#uname').text();
    getusers(uname);
});


const sleep = ms => new Promise(res => setTimeout(res, ms));
async function getusers(uname){
    while(true){
    $.post("/",{
        all_data:`{"subject":"getusers","uname":"${uname}"}`
    },function(err,req,resp){
        msg = JSON.parse(resp["responseText"]);
        ullist.empty();
        for(i in Object.keys(msg)){
        ullist.append(`<li><a href="/${msg[i]}">${msg[i]}</li>`);
        }

    })
    await sleep(5000);
}
}