$(document).ready(function(){

    $('.change-status').click(function(){
        let status = $(this).val();
        console.log(status);
        $.get({
            url:`{% url 'printer:user_print_request_list' ${status} %}`,
            success:function(data){
                $('#fetched-data').html(data);
            }
        });
    });

});
