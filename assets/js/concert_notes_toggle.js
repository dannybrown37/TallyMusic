$(document).ready(function(){
  $(".concerts .concert").click(function(){
    $(this).find(".details .notes").toggleClass("open");
  });
});
