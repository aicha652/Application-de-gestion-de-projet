"use strict";
// Class definition

var DevisListDatatable = function () {
    // Private functions

    var _initTable = function () {
        var dataUrl = $('#devis_datatable').attr('data-url');
        moment.locale('fr');
        $.get(dataUrl, function (data) {
            var datatable = $('#devis_datatable').KTDatatable({
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
                        field: 'numero',
                        title: 'numero',
                        sortable: 'asc',
                        width: 100,
                        selector: false,
                        textAlign: 'left',
                        autoHide: false,
                        template: function (data) {
                            return '<span class="font-weight-bolder">' + data.numero + '</span>';
                        }
                    }, {
                        field: 'status',
                        title: 'status',
                        sortable: 'asc',
                        width: 150,
                        selector: false,
                        textAlign: 'left',
                        autoHide: false,
                        template: function (data) {
                            return '<span class="font-weight-bolder">' + data.status + '</span>';
                        }
                    }, {
                        field: 'info',
                        title: 'info',
                        sortable: 'asc',
                        width: 250,
                        selector: false,
                        textAlign: 'left',
                        autoHide: false,
                        template: function (data) {
                            return '<span class="font-weight-bolder">' + data.info + '</span>';
                        }
                    }, {
                        field: 'montant_ht',
                        title: 'montant_ht',
                        sortable: 'asc',
                        width: 100,
                        selector: false,
                        textAlign: 'left',
                        autoHide: false,
                        template: function (data) {
                            return '<span class="font-weight-bolder">' + data.montant_ht + '</span>';
                        }
                    }, {
                        field: 'id',
                        title: 'id',
                        sortable: 'asc',
                        width: 200,
                        selector: false,
                        textAlign: 'left',
                        template: function (data) {
                            return '<span class="font-weight-bolder">' + data.id + '</span>';
                        }
                    }, {
                        field: 'projet',
                        title: 'projet',
                        sortable: 'asc',
                        width: 200,
                        selector: false,
                        textAlign: 'left',
                        template: function (data) {
                            return '<span class="font-weight-bolder">' + data.projet + '</span>';
                        }
                    },  {
                        field: 'Actions',
                        title: 'Actions',
                        sortable: false,
                        width: 100,
                        overflow: 'visible',
                        autoHide: false,
                        template: function (data) {
                            return '\
                             <a href="/editDevis/' + data.id + '" class="btn btn-sm btn-default btn-text-primary btn-hover-primary btn-icon mr-2" title="Edit details" style="background-color: green">\
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
                            <a href="/get_pdf/' + data.id + '/' + data.projet + '" class="btn btn-sm btn-default btn-text btn-hover btn-icon mr-2" title="Page projet" style="background-color: #008080">\
	                           <span class="svg-icon svg-icon-primary svg-icon-2x"><!--begin::Svg Icon | path:/var/www/preview.keenthemes.com/metronic/releases/2021-05-14-112058/theme/html/demo1/dist/../src/media/svg/icons/Files/Download.svg--><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">\
                                <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\
                                      <rect x="0" y="0" width="24" height="24"/>\
                                      <path d="M2,13 C2,12.5 2.5,12 3,12 C3.5,12 4,12.5 4,13 C4,13.3333333 4,15 4,18 C4,19.1045695 4.8954305,20 6,20 L18,20 C19.1045695,20 20,19.1045695 20,18 L20,13 C20,12.4477153 20.4477153,12 21,12 C21.5522847,12 22,12.4477153 22,13 L22,18 C22,20.209139 20.209139,22 18,22 L6,22 C3.790861,22 2,20.209139 2,18 C2,15 2,13.3333333 2,13 Z" fill="#000000" fill-rule="nonzero" opacity="0.3"/>\
                                      <rect fill="#000000" opacity="0.3" transform="translate(12.000000, 8.000000) rotate(-180.000000) translate(-12.000000, -8.000000) " x="11" y="1" width="2" height="14" rx="1"/>\
                                      <path d="M7.70710678,15.7071068 C7.31658249,16.0976311 6.68341751,16.0976311 6.29289322,15.7071068 C5.90236893,15.3165825 5.90236893,14.6834175 6.29289322,14.2928932 L11.2928932,9.29289322 C11.6689749,8.91681153 12.2736364,8.90091039 12.6689647,9.25670585 L17.6689647,13.7567059 C18.0794748,14.1261649 18.1127532,14.7584547 17.7432941,15.1689647 C17.3738351,15.5794748 16.7415453,15.6127532 16.3310353,15.2432941 L12.0362375,11.3779761 L7.70710678,15.7071068 Z" fill="#000000" fill-rule="nonzero" transform="translate(12.000004, 12.499999) rotate(-180.000000) translate(-12.000004, -12.499999) "/>\
                                </g>\
                                </svg><!--end::Svg Icon--></span>\
	                        </a>\
	                    ';
                        },
                    }],
            });
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
    DevisListDatatable.init();
});