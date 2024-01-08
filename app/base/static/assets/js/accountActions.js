function get_data_from_form(form) {
    var serialized = form.serializeArray();
    var data = {};
    $.each(serialized,
        function (i, v) {
            data[v.name] = v.value;
        });
    console.log(data)
    return data;
}

var showErrorMsg = function (form, type, msg) {
    var alert = $('<div class="alert alert-' + type + ' alert-dismissible" role="alert">\
    <div class="alert-text">' + msg + '</div>\
              <i class="flaticon2-cross kt-icon-sm close" data-dismiss="alert"></i>\
  </div>');

    alert.prependTo(form);
    // alert.appendTo(form);
    //alert.animateClass('fadeIn animated');
    KTUtil.animateClass(alert[0], 'fadeIn animated');
    alert.find('span').html(msg)
}

var _handleActivationform = function () {
    var validation;
    console.log(KTUtil.getById('kt_activation_form'))
    validation = FormValidation.formValidation(
        KTUtil.getById('activation_form'), {
            fields: {
                activation_code: {
                    validators: {
                        notEmpty: {
                            message: "Veuillez saisir votre code d'activation"
                        }
                    }
                }
            }
            ,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                //defaultSubmit: new FormValidation.plugins.DefaultSubmit(), // Uncomment this line to enable normal button submit after form validation
                bootstrap: new FormValidation.plugins.Bootstrap()
            }
        }
    )

    $('#activation_submit').on('click', function (e) {
        e.preventDefault();
        var btn = KTUtil.getById("activation_submit");
        var form = $(this).closest('form');
        validation.validate().then(function (status) {
            if (status != 'Valid') {
                return;
            }
            form.find('.alert').remove();
            KTUtil.btnWait(btn, "spinner spinner-right spinner-white pr-15", "Envoi");
            $.ajax({
                url: HOST_URL + 'api/auth/activateAccount',
                method: 'POST',
                data: JSON.stringify(get_data_from_form(form)),
                contentType: 'application/json; charset=utf-8',
                success: function (response, status, xhr, $form) {
                    KTUtil.btnRelease(btn);
                    if (xhr.status === 200) {
                        form[0].reset();
                        validation.resetForm()
                        window.location.href = ('/');
                    }
                },
                error: function (xhr, data) {

                    KTUtil.btnRelease(btn);
                    if (xhr.status === 400) {
                        var errors = xhr.responseJSON.data.message;

                        jQuery.each(errors, function (index, value) {
                            if (value != '') {
                                showErrorMsg(form, 'danger', value)
                            }
                        });
                    } else {
                        showErrorMsg(form, 'danger', 'Serveur en maintenance veuillez réssayer plutard !');
                    }
                }
            });
        })
    });

}
var _handleResetPassword = function () {
    var validation;
    var form = KTUtil.getById('reset_password_form');

    validation = FormValidation.formValidation(
        form, {
            fields: {
                password: {
                    validators: {
                        notEmpty: {
                            message: 'Veuillez saisir un mot de passe'
                        },
                        stringLength: {
                            min: 8,
                            message: 'Votre mot de passe doit contenir plus que 8 caractère'
                        }
                    }
                },
                confirm_password: {
                    validators: {
                        notEmpty: {message: 'Veuillez saisir la confirmation de votre mot de passe'},
                        identical: {
                            compare: function () {
                                return form.querySelector('[name="password"]').value;
                            },
                            message: 'Ce champs doit être identique au mot de passe saisi'
                        }


                    }
                }
            }
            ,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                //defaultSubmit: new FormValidation.plugins.DefaultSubmit(), // Uncomment this line to enable normal button submit after form validation
                bootstrap: new FormValidation.plugins.Bootstrap()
            }
        }
    )

    $('#reset_password_submit').on('click', function (e) {
        e.preventDefault();
        // var btn = $(this);
        var btn = KTUtil.getById("reset_password_submit");
        var form = $(this).closest('form');
        validation.validate().then(function (status) {
            if (status != 'Valid') {
                return;
            }
            form.find('.alert').remove();
            KTUtil.btnWait(btn, "spinner spinner-right spinner-white pr-15", "Envoi");

            $.ajax({
                url: HOST_URL + 'api/auth/resetPassword',
                method: 'POST',
                data: JSON.stringify(get_data_from_form(form)),
                contentType: 'application/json; charset=utf-8',
                success: function (response, status, xhr, $form) {
                    KTUtil.btnRelease(btn);
                    if (xhr.status === 200) {
                        form[0].reset();
                        validation.resetForm()

                        window.location.href = ('/');
                    }
                },
                error: function (xhr, data) {
                    KTUtil.btnRelease(btn);
                    if (xhr.status === 401) {
                        var errors = xhr.responseJSON.data.message;

                        jQuery.each(errors, function (index, value) {
                            if (value != '') {
                                showErrorMsg(form, 'danger', value)
                            }
                        });
                    } else {
                        showErrorMsg(form, 'danger', 'Serveur en maintenance veuillez réssayer plutard !');
                    }
                }
            });
        })
    });

}
jQuery(document).ready(function () {
    // const activation_form = document.getElementById(activation_form)
    // const double_auth_form = document.getElementById(double_auth_form)
    if ($("#activation_form").length) {
        _handleActivationform();
    }
    if ($("#reset_password_form").length) {
        _handleResetPassword();
    }
});
