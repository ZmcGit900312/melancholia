$(document).ready(function(){
   //Write Code

    $("p").hover(
        function () {
            $(this).css('color','red');
            },
        function () {
            $(this).css('color','blue');
        }
        );

    $("#about-btn").click(
        function (event) {
            msgstr = $("#msg").html();
            msgstr = msgstr + 'ooo';
            $("#msg").html(msgstr);
        }
    );
});