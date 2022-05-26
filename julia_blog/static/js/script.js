$(document).ready(function () {
  $(".save-comment").on("click", function (e) {
    e.preventDefault();
    let _comment = $(".comment-text").val();
    let _postid = $(this).data("post");
    let $crf_token = $('[name="csrfmiddlewaretoken"]').attr("value");
    $.ajax({
      url: $(this).data("url"),
      type: "post",
      headers: { "X-CSRFToken": $crf_token },
      data: {
        comment: _comment,
        postid: _postid,
        csrfmiddlewaretoken: "CSRF-TOKEN-VALUE",
      },
      dataType: "json",
      beforeSend: function () {
        $(".save-comment").addClass("disabled").text("saving...");
        console.log(_comment);
      },
      success: function (res) {
        $(".save-comment").removeClass("disabled").text("Submit");
      },
    });
  });
});
