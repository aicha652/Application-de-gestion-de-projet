"use strict";
// Class definition

var UsersListDatatable = function () {
    // Private functions

    var _initTable = function () {
        var dataUrl = $('#users_datatable').attr('data-url');
        $.get(dataUrl, function (data) {
            var datatable = $('#users_datatable').KTDatatable({
                // datasource definition
                data: {
                    type: 'local',
                    source: data,
                    pageSize: 10, // display 20 records per page

                },

                // layout definition
                layout: {
                    scroll: false, // enable/disable datatable scroll both horizontal and vertical when needed.
                    footer: false, // display/hide footer
                },

                // column sorting
                sortable: true,

                pagination: true,

                search: {
                    input: $('#kt_subheader_search_form'),
                    delay: 400,
                    key: 'generalSearch'
                },

                // columns definition
                columns: [
                    {
                        field: 'id',
                        title: '#',
                        sortable: 'asc',
                        width: 40,
                        type: 'number',
                        selector: false,
                        textAlign: 'left',
                        template: function (data) {
                            return '<span class="font-weight-bolder">' + data.id + '</span>';
                        }
                    }, {
                        field: 'username',
                        title: "Nom de l'utilisateur",
                        width: 250,
                        template: function (data) {

                            var output = '';
                            var stateNo = KTUtil.getRandomInt(0, 7);
                            var states = [
                                'success',
                                'primary',
                                'danger',
                                'success',
                                'warning',
                                'dark',
                                'primary',
                                'info'];
                            var state = states[stateNo];
                            output = '<div class="d-flex align-items-center">' +
                                        '<div class="symbol symbol-40 symbol-light-' + state + ' flex-shrink-0">' +
                                            '<span class="symbol-label font-size-h4 font-weight-bold">' + data.first_name.substring(0, 1) + data.last_name.substring(0, 1) + '</span>' +
                                        '</div>' +
                                        '<div class="ml-4">' +
                                            '<div class="text-dark-75 font-weight-bolder font-size-lg mb-0">' + data.last_name + ' ' + data.first_name + '</div>' +
                                        '</div>' +
                                      '</div>';

                            return output;
                        }
                    }, {
                        field: 'email',
                        title: 'Email',
                        width: 220,
                        template: function (data) {
                            var output = '';

                            output += '<div class="font-weight-bolder font-size-lg mb-0">' + data.email + '</div>';

                            return output;
                        }
                    }, {
                        field: 'last_seen',
                        title: 'Visite',
                        width: 220,
                        template: function (data) {
                            var output = '';

                            output += '<div class="font-weight-bold text-muted">' + data.last_seen + '</div>';

                            return output;
                        }
                    }, {
                        field: 'is_admin',
                        title: 'Compte',
                        width: 120,
                        // callback function support for column rendering
                        template: function (data) {
                            var status = {
                                false: {'title': 'Utilisateur', 'class': ' label-light-primary'},
                                true: {'title': 'Administrateur', 'class': ' label-light-warning'},
                            };


                            return '<span class="label label-lg font-weight-bold ' + status[data.is_admin].class + ' label-inline">' + status[data.is_admin].title + '</span>';
                        }
                    }, {
                        field: 'is_active',
                        title: 'État',
                        width: 80,
                        // callback function support for column rendering
                        template: function (data) {
                            var status = {

                                false: {'title': 'Non Actif', 'class': ' label-light-danger'},
                                true: {'title': 'Actif', 'class': ' label-light-success'},

                            };
                            return '<span class="label label-lg font-weight-bold ' + status[data.is_active].class + ' label-inline">' + status[data.is_active].title + '</span>';
                        }
                    }, {
                        field: 'Actions',
                        title: 'Actions',
                        sortable: false,
                        width: 130,
                        overflow: 'visible',
                        autoHide: false,
                        template: function (data) {
                            return'\
	                        <a href="/editUser/' + data.id + '" class="btn btn-sm btn-default btn-text-primary btn-hover-primary btn-icon mr-2" title="Edit details" style="background-color: green">\
	                            <span class="svg-icon svg-icon-md">\
									<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">\
										<g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\
											<rect x="0" y="0" width="24" height="24"/>\
											<path d="M12.2674799,18.2323597 L12.0084872,5.45852451 C12.0004303,5.06114792 12.1504154,4.6768183 12.4255037,4.38993949 L15.0030167,1.70195304 L17.5910752,4.40093695 C17.8599071,4.6812911 18.0095067,5.05499603 18.0083938,5.44341307 L17.9718262,18.2062508 C17.9694575,19.0329966 17.2985816,19.701953 16.4718324,19.701953 L13.7671717,19.701953 C12.9505952,19.701953 12.2840328,19.0487684 12.2674799,18.2323597 Z" fill="#000000" fill-rule="nonzero" transform="translate(14.701953, 10.701953) rotate(-135.000000) translate(-14.701953, -10.701953) "/>\
											<path d="M12.9,2 C13.4522847,2 13.9,2.44771525 13.9,3 C13.9,3.55228475 13.4522847,4 12.9,4 L6,4 C4.8954305,4 4,4.8954305 4,6 L4,18 C4,19.1045695 4.8954305,20 6,20 L18,20 C19.1045695,20 20,19.1045695 20,18 L20,13 C20,12.4477153 20.4477153,12 21,12 C21.5522847,12 22,12.4477153 22,13 L22,18 C22,20.209139 20.209139,22 18,22 L6,22 C3.790861,22 2,20.209139 2,18 L2,6 C2,3.790861 3.790861,2 6,2 L12.9,2 Z" fill="#000000" fill-rule="nonzero" opacity="0.3"/>\
										</g>\
									</svg>\
	                            </span>\
	                        </a>\
	                        <button href="javascript:;" delete_url="/deleteUser/' + data.id + '" class="delete_user btn btn-sm btn-default btn-text-danger btn-hover-danger btn-icon" title="Delete" style="background-color:#FF0000">\
								<span class="svg-icon svg-icon-md">\
									<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">\
										<g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\
											<rect x="0" y="0" width="24" height="24"/>\
											<path d="M6,8 L6,20.5 C6,21.3284271 6.67157288,22 7.5,22 L16.5,22 C17.3284271,22 18,21.3284271 18,20.5 L18,8 L6,8 Z" fill="#000000" fill-rule="nonzero"/>\
											<path d="M14,4.5 L14,4 C14,3.44771525 13.5522847,3 13,3 L11,3 C10.4477153,3 10,3.44771525 10,4 L10,4.5 L5.5,4.5 C5.22385763,4.5 5,4.72385763 5,5 L5,5.5 C5,5.77614237 5.22385763,6 5.5,6 L18.5,6 C18.7761424,6 19,5.77614237 19,5.5 L19,5 C19,4.72385763 18.7761424,4.5 18.5,4.5 L14,4.5 Z" fill="#000000" opacity="0.3"/>\
										</g>\
									</svg>\
								</span>\
	                        </button>\
	                    ' ;
                        },
                    }],
            });

            $('#datatable_search_status').on('change', function () {
                datatable.search($(this).val().toLowerCase(), 'Status');
            });

            $('#datatable_search_type').on('change', function () {
                datatable.search($(this).val().toLowerCase(), 'Type');
            });

            $('#users_datatable').on('click', '.delete_user', function (event) {
                event.preventDefault();
                let delete_url = $(this).attr('delete_url');
                Swal.fire({
                    title: 'Supprimer ce compte?',
                    text: "Ceci supprimera tous les dossiers et fichiers associés !",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    cancelButtonText: 'Annuler',
                    confirmButtonText: 'Oui, supprimer!'
                }).then((result) => {
                    if (result.isConfirmed) {
                        $.post(delete_url, function (response) {
                            if (response.status === 'OK') {
                                Swal.fire(
                                    'Supprimé!',
                                    'Compte et données supprimés.',
                                    'success'
                                );
                                location.reload()
                            } else if (response.status === 'ERROR') {
                                Swal.fire(
                                    'Erreur !',
                                    response.message,
                                    'error'
                                )
                            } else {
                                Swal.fire(
                                    'Erreur !',
                                    'Réponse serveur',
                                    'error'
                                )
                            }

                        })

                    }
                })
            })
        });
    };

    return {
        // public functions
        init: function () {
            _initTable();
        },
    };
}();

jQuery(document).ready(function () {
    UsersListDatatable.init();
});
