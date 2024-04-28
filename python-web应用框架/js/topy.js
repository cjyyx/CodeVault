// function_name:String;parameters:array
function topy(function_name,parameters) {
    var return_result;
    $.ajax({
        url: "/topy",
        data: JSON.stringify([function_name,parameters]),
        type: "POST",
        async: false,
        success: function (result) {
            return_result = result;
        }
    });
    return JSON.parse(return_result);

}




