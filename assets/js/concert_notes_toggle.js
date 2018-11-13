$(document).ready(function(){
  $(".concerts .concert .details").click(function(){
    $(this).find(".notes").toggleClass("open");
  });
});
