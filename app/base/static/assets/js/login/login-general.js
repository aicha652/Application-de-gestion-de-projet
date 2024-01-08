"use strict";

function get_data_from_form(form) {
    var serialized = form.serializeArray();
    var data = {};
    $.each(serialized,
        function (i, v) {
            data[v.name] = v.value;
        });
    // console.log(data)
    return data;
}

// Class Definition
var KTLogin = function () {
    var _login;

    var showErrorMsg = function (form, type, msg) {
        var alert = $('<div class="alert alert-' + type + ' alert-dismissible" role="alert">\
      <div class="alert-text">' + msg + '</div>\
                <i class="flaticon2-cross kt-icon-sm close" data-dismiss="alert"></i>\
    </div>');


        alert.prependTo(form);
        // alert.appendTo(form);
        // alert.animateClass('fadeIn animated');
        KTUtil.animateClass(alert[0], 'fadeIn animated');
        alert.find('span').html(msg)
    }

    var _showForm = function (form) {
        var cls = 'login-' + form + '-on';
        var form = 'kt_login_' + form + '_form';

        _login.removeClass('login-forgot-on');
        _login.removeClass('login-signin-on');
        _login.removeClass('login-signup-on');

        _login.addClass(cls);

        // KTUtil.animateClass(KTUtil.getById(form), 'animate__animated animate__backInUp');
    }

    var _handleSignInForm = function () {
        var validation;

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            KTUtil.getById('kt_login_signin_form'), {
                fields: {
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'Veuillez saisir votre Email'
                            },
                            emailAddress: {
                                message: 'Veuillez saisir une adresse Email valide'
                            }
                        }
                    },
                    password: {
                        validators: {
                            notEmpty: {
                                message: 'Veuillez saisir votre mot de passe'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    submitButton: new FormValidation.plugins.SubmitButton(),
                    //defaultSubmit: new FormValidation.plugins.DefaultSubmit(), // Uncomment this line to enable normal button submit after form validation
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        $('#kt_login_signin_submit').on('click', function (e) {
            e.preventDefault();
            // var btn = $(this);
            var btn = KTUtil.getById("kt_login_signin_submit");

            var form = $(this).closest('form');
            validation.validate().then(function (status) {
                if (status != 'Valid') {
                    return;
                }

                KTUtil.btnWait(btn, "spinner spinner-right spinner-white pr-15", "Envoi");
                form.find('.alert').remove();
                $.ajax({
                    url: HOST_URL + 'api/auth/login',
                    method: 'POST',
                    data: JSON.stringify(get_data_from_form(form)),
                    contentType: 'application/json; charset=utf-8',
                    success: function (response, status, xhr, $form) {
                        // similate 2s delay
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
                            showErrorMsg(form, 'danger', 'Erreur serveur veuillez réssayer plutard !');
                        }
                    }
                });
            })
        });

        // Handle forgot button
        $('#kt_login_forgot').on('click', function (e) {
            e.preventDefault();
            _showForm('forgot');
        });

        // Handle signup
        $('#kt_login_signup').on('click', function (e) {
            e.preventDefault();
            _showForm('signup');
        });
    }

    var _handleSignUpForm = function (e) {
        var validation;
        var form = KTUtil.getById('kt_login_signup_form');

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            form, {
                fields: {
                    username: {
                        validators: {
                            notEmpty: {
                                message: "Le nom d'utilisateur est obligatoire"
                            },
                            stringLength: {
                                min: 3,
                                message: 'Doit contenir plus que 2 caractère'
                            }
                        }
                    },
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'Veuillez saisir votre email'
                            },
                            emailAddress: {
                                message: 'Le format de votre email est invalide'
                            }
                        }
                    },
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
                            notEmpty: {
                                message: 'Veuillez saisir la confirmation de votre mot de passe'
                            },
                            identical: {
                                compare: function () {
                                    return form.querySelector('[name="password"]').value;
                                },
                                message: 'Doit être identique au mot de passe saisi'
                            }


                        }
                    },


                    agree: {
                        validators: {
                            notEmpty: {
                                message: 'Vous devez accepter les termes et les conditions'
                            }
                        }
                    },
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        $('#kt_login_signup_submit').on('click', function (e) {
            e.preventDefault();
            // var btn = $(this);
            var btn = KTUtil.getById("kt_login_signup_submit");

            var form = $(this).closest('form');
            validation.validate().then(function (status) {

                if (status != 'Valid') {
                    return;
                }
                form.find('.alert').remove();
                KTUtil.btnWait(btn, "spinner spinner-right spinner-white pr-15", "Envoi");

                $.ajax({
                    url: HOST_URL + 'api/auth/register',
                    method: 'POST',
                    data: JSON.stringify(get_data_from_form(form)),
                    contentType: 'application/json; charset=utf-8',
                    success: function (response, status, xhr, $form) {
                        // similate 2s delay
                        KTUtil.btnRelease(btn);
                        if (xhr.status === 201) {
                            form[0].reset();
                            validation.resetForm()

                            var signInForm = $('#kt_login_signin_form');


                            _showForm('signin');

                            showErrorMsg(signInForm, 'success', 'Compte créé! Veuillez vérifier votre boite email, afin de l\'activer !');
                            //

                            // setTimeout(function() {
                            //     btn.removeClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', false);
                            //     showErrorMsg(form, 'danger', 'Incorrect username or password. Please try again.');
                            //   }, 2000);
                        }
                    },
                    error: function (xhr, data) {
                        KTUtil.btnRelease(btn);
                        if (xhr.status === 400) {
                            // console.log(xhr);
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
                })
            });
            //   console.log('after status = Valid');
            //
            //
            // swal.fire({
            //   text: "All is cool! Now you submit this form",
            //   icon: "success",
            //   buttonsStyling: false,
            //   confirmButtonText: "Ok, got it!",
            //   customClass: {
            //     confirmButton: "btn font-weight-bold btn-light-primary"
            //   }
            // }).then(function() {
            //   KTUtil.scrollTop();
            // });
            // } else {
            //   swal.fire({
            //     text: "Sorry, looks like there are some errors detected, please try again.",
            //     icon: "error",
            //     buttonsStyling: false,
            //     confirmButtonText: "Ok, got it!",
            //     customClass: {
            //       confirmButton: "btn font-weight-bold btn-light-primary"
            //     }
            //   }).then(function() {
            //     KTUtil.scrollTop();
            //   });
            // }
            // });
        });

        // Handle cancel button
        $('#kt_login_signup_cancel').on('click', function (e) {
            e.preventDefault();

            _showForm('signin');
        });
    }

    var _handleForgotForm = function (e) {
        var validation;

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            KTUtil.getById('kt_login_forgot_form'), {
                fields: {
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'Veuillez saisir votre Email'
                            },
                            emailAddress: {
                                message: 'Le format de cet email est invalide'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        // Handle submit button
        $('#kt_login_forgot_submit').on('click', function (e) {
            e.preventDefault();
            // var btn = $(this);
            var btn = KTUtil.getById("kt_login_forgot_submit");

            var form = $(this).closest('form');
            validation.validate().then(function (status) {
                if (status != 'Valid') {
                    return;
                }
                form.find('.alert').remove();
                KTUtil.btnWait(btn, "spinner spinner-right spinner-white pr-15", "Envoi");

                $.ajax({
                    url: HOST_URL + 'api/auth/forgot',
                    method: 'POST',
                    data: JSON.stringify(get_data_from_form(form)),
                    contentType: 'application/json; charset=utf-8',
                    success: function (response, status, xhr, $form) {
                        // similate 2s delay
                        KTUtil.btnRelease(btn);
                        if (xhr.status === 200) {
                            form[0].reset();
                            validation.resetForm()

                            var signInForm = $('#kt_login_signin_form');


                            _showForm('signin');

                            showErrorMsg(signInForm, 'success', 'Les instructions de changement de mot de passe sont envoyées. Veuillez vérifier votre boite email !');
                            //

                            // setTimeout(function() {
                            //     btn.removeClass('kt-spinner kt-spinner--right kt-spinner--sm kt-spinner--light').attr('disabled', false);
                            //     showErrorMsg(form, 'danger', 'Incorrect username or password. Please try again.');
                            //   }, 2000);
                        }
                    },
                    error: function (xhr, data) {
                        KTUtil.btnRelease(btn);
                        if (xhr.status === 400) {
                            // console.log(xhr);
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
            });
        });

        // Handle cancel button
        $('#kt_login_forgot_cancel').on('click', function (e) {
            e.preventDefault();

            _showForm('signin');
        });
    }

    // Public Functions
    return {
        // public functions
        init: function () {
            _login = $('#kt_login');

            _handleSignInForm();
            _handleSignUpForm();
            _handleForgotForm();
        }
    };
}();

// Class Initialization
jQuery(document).ready(function () {
    KTLogin.init();
});
