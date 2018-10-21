let s_interval;
let j_interval;
let pdf_interval;

$(document).ready(function() {

    $('select').material_select();

     $('.datepicker').pickadate({
        selectMonths: true,
        selectYears: 100,
        min: new Date(1950, 0, 1),
        max: new Date(),
        format: 'dd/mm/yyyy',
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        closeOnSelect: true,
        container: undefined,
     });

     running_s();
     running_j();
     running_pdf();

     $('#court-name-s').on('change', function() {
         $.ajax({
            type: 'GET',
            url: '/get-bench-list/' + this.value,
            success: function (data) {
                let option_list = "<option value='' disabled selected>Choose Bench</option>";

                if (!data)
                    option_list += "<option value='None' selected>NONE</option>";

                for (let i in data) {
                    option_list += "<option value='" + data[i].id + "'>" + data[i].name + "</option>";
                }
                $("#bench-s").html(option_list);
                $('select').material_select();

                Materialize.toast("Court selected!", 2000, 'light-green');
            },
            error: function (data) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
            }
        });
     });


     $('#submit-btn-s').on('click', function() {
         if (validate_s()) {
             const s_btn = $("#submit-btn-s");
             const l_btn = $("#btn-loading-s");
             const se_btn = $("#btn-send-s");

             s_btn.addClass("disabled");
             se_btn.addClass("d-none");
             l_btn.addClass("loading-btn");

             const court_name = $('#court-name-s').val();

             $.ajax({
                 type: 'POST',
                 url: '/start-scrap',

                 data: "court_name=" + court_name +
                     "&bench=" + $('#bench-s').val() +
                     "&start_date=" + $('#start-date-s').val() +
                     "&end_date=" + $('#end-date-s').val(),
                 success: function () {
                     Materialize.toast("Scrapping started!", 2000, 'light-green');

                 },
                 error: function (data) {
                 }
             });

             setTimeout(function () {
                 current_s(court_name);
                 l_btn.removeClass("loading-btn");
                 se_btn.removeClass("d-none");
                 s_btn.removeClass("disabled");
                 s_btn.addClass("d-none");
                 $('#cancel-btn-s').removeClass("d-none");
             }, 2000);

             s_interval = setInterval(function () {
                             current_s(court_name);
                         }, 10000);
         }
     });


     $('#cancel-btn-s').on('click', function() {
        const s_btn = $("#cancel-btn-s");
        const l_btn = $("#btn-close-loading-s");
        const se_btn = $("#btn-close-s");

        s_btn.addClass("disabled");
        se_btn.addClass("d-none");
        l_btn.addClass("loading-btn");

        const court_name = $('#current-court-s').text();

         $.ajax({
            type: 'GET',
            url: '/cancel-scrap/' + court_name,
            success: function () {
                Materialize.toast("Scrapping Aborted!", 2000, 'light-green');
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                s_btn.addClass("d-none");
                $('#submit-btn-s').removeClass("d-none");
            },
            error: function (data) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                s_btn.addClass("d-none");
                $('#submit-btn-s').removeClass("d-none");
            }
         });
     });


     $('#submit-btn-j').on('click', function() {
         if (validate_j()) {
             const s_btn = $("#submit-btn-j");
             const l_btn = $("#btn-loading-j");
             const se_btn = $("#btn-send-j");

             s_btn.addClass("disabled");
             se_btn.addClass("d-none");
             l_btn.addClass("loading-btn");

             const court_name = $('#court-name-j').val();

             $.ajax({
                 type: 'POST',
                 url: '/start-json',

                 data: "court_name=" + court_name +
                     "&start_date=" + $('#start-date-j').val() +
                     "&end_date=" + $('#end-date-j').val(),
                 success: function () {
                     Materialize.toast("JSON Creating started!", 2000, 'light-green');

                 },
                 error: function (data) {
                 }
             });

             setTimeout(function () {
                 current_j(court_name);
                 l_btn.removeClass("loading-btn");
                 se_btn.removeClass("d-none");
                 s_btn.removeClass("disabled");
                 s_btn.addClass("d-none");
                 $('#cancel-btn-j').removeClass("d-none");
             }, 2000);

             j_interval = setInterval(function () {
                             current_j(court_name);
                         }, 10000);
         }
     });


     $('#cancel-btn-j').on('click', function() {
        const s_btn = $("#cancel-btn-j");
        const l_btn = $("#btn-close-loading-j");
        const se_btn = $("#btn-close-j");

        s_btn.addClass("disabled");
        se_btn.addClass("d-none");
        l_btn.addClass("loading-btn");

        const court_name = $('#current-court-j').text();

         $.ajax({
            type: 'GET',
            url: '/cancel-json/' + court_name,
            success: function () {
                Materialize.toast("JSON process Aborted!", 2000, 'light-green');
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                s_btn.addClass("d-none");
                $('#submit-btn-j').removeClass("d-none");
            },
            error: function (data) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                s_btn.addClass("d-none");
                $('#submit-btn-j').removeClass("d-none");
            }
         });
     });


     $('#submit-btn-pdf').on('click', function() {
         if (validate_pdf()) {
             const s_btn = $("#submit-btn-pdf");
             const l_btn = $("#btn-loading-pdf");
             const se_btn = $("#btn-send-pdf");

             s_btn.addClass("disabled");
             se_btn.addClass("d-none");
             l_btn.addClass("loading-btn");

             const court_name = $('#court-name-pdf').val();

             $.ajax({
                 type: 'POST',
                 url: '/start-pdf',

                 data: "court_name=" + court_name,
                 success: function () {
                     Materialize.toast("PDF Download started!", 2000, 'light-green');

                 },
                 error: function (data) {
                 }
             });

             setTimeout(function () {
                 current_pdf();
                 l_btn.removeClass("loading-btn");
                 se_btn.removeClass("d-none");
                 s_btn.removeClass("disabled");
                 s_btn.addClass("d-none");
                 $('#cancel-btn-pdf').removeClass("d-none");
             }, 2000);

             pdf_interval = setInterval(function () {
                             current_pdf();
                         }, 10000);
         }
     });


     $('#cancel-btn-pdf').on('click', function() {
        const s_btn = $("#cancel-btn-pdf");
        const l_btn = $("#btn-close-loading-pdf");
        const se_btn = $("#btn-close-pdf");

        s_btn.addClass("disabled");
        se_btn.addClass("d-none");
        l_btn.addClass("loading-btn");

         $.ajax({
            type: 'GET',
            url: '/cancel-pdf',
            success: function () {
                Materialize.toast("PDF process Aborted!", 2000, 'light-green');
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                s_btn.addClass("d-none");
                $('#submit-btn-pdf').removeClass("d-none");
            },
            error: function (data) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                s_btn.addClass("d-none");
                $('#submit-btn-pdf').removeClass("d-none");
            }
         });
     });

});

function current_s(court_name) {
     const s_btn = $("#submit-btn-s");
     const l_btn = $("#btn-loading-s");
     const se_btn = $("#btn-send-s");

     $.ajax({
        type: 'GET',
        url: '/current-scrap/' + court_name,
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"9\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                $('#cancel-btn-s').addClass("d-none");
                s_btn.removeClass("d-none");
                clearInterval(s_interval);
            }
            else {
                tr_list += "<tr>";
                tr_list += "<td id='current-court-s'>" + data.Name + "</td>";
                tr_list += "<td>" + data.bench + "</td>";
                tr_list += "<td>" + data.Start_Date + "</td>";
                tr_list += "<td>" + data.End_Date + "</td>";
                tr_list += "<td>" + data.No_Cases + "</td>";
                tr_list += "<td>" + data.No_Error + "</td>";
                tr_list += "<td>" + data.No_Year_Error + "</td>";
                tr_list += "<td>" + data.No_Year_NoData + "</td>";
                tr_list += "<td>" + data.status + "</td>";
                tr_list += "</tr>";

                if ("IN_RUNNING" !== data.status){
                    $('#cancel-btn-s').addClass("d-none");
                    $('#submit-btn-s').removeClass("d-none");
                    clearInterval(s_interval);
                }
            }
            $("#current-s").html(tr_list);

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
     });
}


function current_j(court_name) {
     const s_btn = $("#submit-btn-j");
     const l_btn = $("#btn-loading-j");
     const se_btn = $("#btn-send-j");

     $.ajax({
        type: 'GET',
        url: '/current-json/' + court_name,
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"5\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                $('#cancel-btn-j').addClass("d-none");
                s_btn.removeClass("d-none");
                clearInterval(j_interval);
            }
            else {
                tr_list += "<tr>";
                tr_list += "<td id='current-court-j'>" + data.Name + "</td>";
                tr_list += "<td>" + data.Start_Date + "</td>";
                tr_list += "<td>" + data.End_Date + "</td>";
                tr_list += "<td>" + data.No_Files + "</td>";
                tr_list += "<td>" + data.status + "</td>";
                tr_list += "</tr>";

                if ("IN_RUNNING" !== data.status){
                    $('#cancel-btn-j').addClass("d-none");
                    $('#submit-btn-j').removeClass("d-none");
                    clearInterval(j_interval);
                }
                if ("IN_SUCCESS" === data.status){
                    get_files(court_name);
                    clearInterval(j_interval);
                }
            }
            $("#current-j").html(tr_list);

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
     });
}


function current_pdf() {
     const s_btn = $("#submit-btn-pdf");
     const l_btn = $("#btn-loading-pdf");
     const se_btn = $("#btn-send-pdf");

     $.ajax({
        type: 'GET',
        url: '/current-pdf',
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"5\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                $('#cancel-btn-pdf').addClass("d-none");
                s_btn.removeClass("d-none");
                clearInterval(pdf_interval);
            }
            else {
                tr_list += "<tr>";
                tr_list += "<td id='current-court-pdf'>" + data.Name + "</td>";
                tr_list += "<td>" + data.No_Files + "</td>";
                tr_list += "<td>" + data.status + "</td>";
                tr_list += "</tr>";

                if ("IN_RUNNING" !== data.status){
                    $('#cancel-btn-pdf').addClass("d-none");
                    $('#submit-btn-pdf').removeClass("d-none");
                    s_btn.removeClass("disabled");
                    l_btn.removeClass("loading-btn");
                    se_btn.removeClass("d-none");
                    clearInterval(pdf_interval);
                }
                if ("IN_SUCCESS" === data.status){
                    clearInterval(pdf_interval);
                }
            }
            $("#current-pdf").html(tr_list);

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
     });
}


function running_s() {
     const s_btn = $("#submit-btn-s");
     const l_btn = $("#btn-loading-s");
     const se_btn = $("#btn-send-s");

     s_btn.addClass("disabled");
     se_btn.addClass("d-none");
     l_btn.addClass("loading-btn");

     $.ajax({
        type: 'GET',
        url: '/running-scrap',
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"9\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
                 l_btn.removeClass("loading-btn");
                 se_btn.removeClass("d-none");
                 s_btn.removeClass("disabled");
                $('#cancel-btn-s').addClass("d-none");
                s_btn.removeClass("d-none");
                clearInterval(s_interval);
            }
            else {
                tr_list += "<tr>";
                tr_list += "<td id='current-court-s'>" + data.Name + "</td>";
                tr_list += "<td>" + data.bench + "</td>";
                tr_list += "<td>" + data.Start_Date + "</td>";
                tr_list += "<td>" + data.End_Date + "</td>";
                tr_list += "<td>" + data.No_Cases + "</td>";
                tr_list += "<td>" + data.No_Error + "</td>";
                tr_list += "<td>" + data.No_Year_Error + "</td>";
                tr_list += "<td>" + data.No_Year_NoData + "</td>";
                tr_list += "<td>" + data.status + "</td>";
                tr_list += "</tr>";

                if ("IN_RUNNING" === data.status){
                     l_btn.removeClass("loading-btn");
                     se_btn.removeClass("d-none");
                     s_btn.removeClass("disabled");
                     s_btn.addClass("d-none");
                     $('#cancel-btn-s').removeClass("d-none");
                     s_interval = setInterval(function () {
                                     current_s(data.Name);
                                 }, 10000);
                }
                else {
                    $('#cancel-btn-s').addClass("d-none");
                    $('#submit-btn-s').removeClass("d-none");
                    clearInterval(s_interval);
                }
            }
            $("#current-s").html(tr_list);

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
     });
}


function running_j() {
     const s_btn = $("#submit-btn-j");
     const l_btn = $("#btn-loading-j");
     const se_btn = $("#btn-send-j");

     s_btn.addClass("disabled");
     se_btn.addClass("d-none");
     l_btn.addClass("loading-btn");

     $.ajax({
        type: 'GET',
        url: '/running-json',
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"5\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
                 l_btn.removeClass("loading-btn");
                 se_btn.removeClass("d-none");
                 s_btn.removeClass("disabled");
                $('#cancel-btn-j').addClass("d-none");
                s_btn.removeClass("d-none");
                clearInterval(j_interval);
            }
            else {
                tr_list += "<tr>";
                tr_list += "<td id='current-court-j'>" + data.Name + "</td>";
                tr_list += "<td>" + data.Start_Date + "</td>";
                tr_list += "<td>" + data.End_Date + "</td>";
                tr_list += "<td>" + data.No_Files + "</td>";
                tr_list += "<td>" + data.status + "</td>";
                tr_list += "</tr>";

                if ("IN_RUNNING" === data.status){
                     l_btn.removeClass("loading-btn");
                     se_btn.removeClass("d-none");
                     s_btn.removeClass("disabled");
                     s_btn.addClass("d-none");
                     $('#cancel-btn-j').removeClass("d-none");
                     j_interval = setInterval(function () {
                                     current_j(data.Name);
                                 }, 10000);
                }
                else {
                    $('#cancel-btn-j').addClass("d-none");
                    $('#submit-btn-j').removeClass("d-none");
                    clearInterval(j_interval);
                }
                if ("IN_SUCCESS" === data.status){
                    get_files(data.Name);
                    clearInterval(j_interval);
                }
            }
            $("#current-j").html(tr_list);

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
     });
}


function running_pdf() {
     const s_btn = $("#submit-btn-pdf");
     const l_btn = $("#btn-loading-pdf");
     const se_btn = $("#btn-send-pdf");

     s_btn.addClass("disabled");
     se_btn.addClass("d-none");
     l_btn.addClass("loading-btn");

     $.ajax({
        type: 'GET',
        url: '/current-pdf',
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"5\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
                 l_btn.removeClass("loading-btn");
                 se_btn.removeClass("d-none");
                 s_btn.removeClass("disabled");
                $('#cancel-btn-pdf').addClass("d-none");
                s_btn.removeClass("d-none");
                clearInterval(pdf_interval);
            }
            else {
                tr_list += "<tr>";
                tr_list += "<td id='current-court-pdf'>" + data.Name + "</td>";
                tr_list += "<td>" + data.No_Files + "</td>";
                tr_list += "<td>" + data.status + "</td>";
                tr_list += "</tr>";

                if ("IN_RUNNING" === data.status){
                     l_btn.removeClass("loading-btn");
                     se_btn.removeClass("d-none");
                     s_btn.removeClass("disabled");
                     s_btn.addClass("d-none");
                     $('#cancel-btn-pdf').removeClass("d-none");
                     pdf_interval = setInterval(function () {
                                     current_pdf();
                                 }, 10000);
                }
                else {
                    $('#cancel-btn-pdf').addClass("d-none");
                    $('#submit-btn-pdf').removeClass("d-none");
                    clearInterval(pdf_interval);
                }
                if ("IN_SUCCESS" === data.status || "IN_ABORT" === data.status){
                    $('#cancel-btn-pdf').addClass("d-none");
                    $('#submit-btn-pdf').removeClass("d-none");
                    s_btn.removeClass("disabled");
                    l_btn.removeClass("loading-btn");
                    se_btn.removeClass("d-none");
                    clearInterval(pdf_interval);
                }
            }
            $("#current-pdf").html(tr_list);

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
     });
}


function get_files(court_name) {
    $.ajax({
        type: 'GET',
        url: '/get-json/' + court_name,
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"2\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
            }
            else {
                for(let i in data.Name) {
                    tr_list += "<tr>";
                    tr_list += "<td>" + data.Name[i] + "</td>";
                    tr_list += "<td><a href='/files/" + data.Name[i] + "' target='_blank' class='waves-effect waves-light btn green'>Download</a></td>";
                    tr_list += "</tr>";
                }
            }
            $("#files-j").html(tr_list);
            Materialize.toast('Files Ready for Download', 2000, 'light-green');

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
    });
}


function validate_s() {
    const court_name = $('#court-name-s').val();
    const bench= $('#bench-s').val();
    const start_date= $('#start-date-s').val();
    const end_date= $('#end-date-s').val();

    if (court_name === null || court_name.localeCompare("") === 0){
        Materialize.toast('Please select court name.', 4000, 'red');
        return false;
    }
    else if (bench === null || bench.localeCompare("") === 0){
        Materialize.toast('Please select bench.', 4000, 'red');
        return false;
    }
    else if (start_date === null || start_date.localeCompare("") === 0){
        Materialize.toast('Please select Start Date.', 4000, 'red');
        return false;
    }
    else if (end_date === null || end_date.localeCompare("") === 0){
        Materialize.toast('Please select End Date.', 4000, 'red');
        return false;
    }
    else
        return true;
}


function validate_j() {
    const court_name = $('#court-name-j').val();
    const start_date= $('#start-date-j').val();
    const end_date= $('#end-date-j').val();

    if (court_name === null || court_name.localeCompare("") === 0){
        Materialize.toast('Please select court name.', 4000, 'red');
        return false;
    }
    else if (start_date === null || start_date.localeCompare("") === 0){
        Materialize.toast('Please select Start Date.', 4000, 'red');
        return false;
    }
    else if (end_date === null || end_date.localeCompare("") === 0){
        Materialize.toast('Please select End Date.', 4000, 'red');
        return false;
    }
    else
        return true;
}


function validate_pdf() {
    const court_name = $('#court-name-pdf').val();

    if (court_name === null || court_name.localeCompare("") === 0){
        Materialize.toast('Please select court name.', 4000, 'red');
        return false;
    } else
        return true;
}
