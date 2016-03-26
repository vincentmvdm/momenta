$(function() {
  $("button").on("click", function() {
    id = this.id;
    $.ajax({
      url: '/challenge_user?user='+id,
      success: function(aa) {}
    });
  });
});
