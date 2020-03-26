$(document).ready(function(){

    $('.change-status').click(function(){
        let Url = $(this).data("url");
        $.ajax({
            async: true,
            type: "GET",
            url: Url,
            success:function(data){
                $('#fetched-data').html(data);
            }
        });
    });

});
