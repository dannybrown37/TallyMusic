$(document).ready(function(){
  $("#datefilter-container .js-command").click(function(){
    $(this).parent("#datefilter-container").find("#datefilter").toggleClass("open");
  });
});
