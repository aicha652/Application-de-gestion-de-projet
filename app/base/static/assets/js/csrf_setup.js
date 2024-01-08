
  var csrf_token = $('meta[name=csrf-token]').attr('content');
  console.log(csrf_token);
  $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  jqXHR.setRequestHeader('X-CSRF-Token', csrf_token);
  });
