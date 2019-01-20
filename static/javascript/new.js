let new_interval;

$(document).ready(function() {

     running_new();

     $('#new-court-name').on('change', function() {
         $.ajax({
            type: 'GET',
            url: '/new/get-bench-list/' + this.value,
            success: function (data) {
                let option_list = "<option value='' disabled selected>Choose Bench</option>";

                if (!data)
                    option_list += "<option value='None' selected>NONE</option>";

                for (let i in data) {
                    option_list += "<option value='" + data[i].id + "'>" + data[i].name + "</option>";
                }
                $("#new-bench").html(option_list);
                $('select').material_select();

                Materialize.toast("Court selected!", 2000, 'light-green');
            },
            error: function (data) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
            }
        });
     });


     $('#new-submit-btn').on('click', function() {
         if (validate_new()) {
             const s_btn = $("#new-submit-btn");
             const l_btn = $("#new-btn-loading");
             const se_btn = $("#new-btn-send");

             s_btn.addClass("disabled");
             se_btn.addClass("d-none");
             l_btn.addClass("loading-btn");

             const court_name = $('#new-court-name').val();
             const bench = $('#new-bench').val();

             $.ajax({
                 type: 'POST',
                 url: '/new/start-scrap',
                 data: "court_name=" + court_name + "&bench=" + bench,
                 success: function () {
                     Materialize.toast("Scrapping started!", 2000, 'light-green');

                 },
                 error: function (data) {
                 }
             });

             setTimeout(function () {
                 current_new(court_name, bench);
                 l_btn.removeClass("loading-btn");
                 se_btn.removeClass("d-none");
                 s_btn.removeClass("disabled");
                 s_btn.addClass("d-none");
                 $('#new-cancel-btn').removeClass("d-none");
             }, 2000);

             new_interval = setInterval(function () {
                             current_new(court_name, bench);
                         }, 10000);
         }
     });


     $('#new-cancel-btn').on('click', function() {
        const s_btn = $("#new-cancel-btn");
        const l_btn = $("#new-btn-close-loading");
        const se_btn = $("#new-btn-close");

        s_btn.addClass("disabled");
        se_btn.addClass("d-none");
        l_btn.addClass("loading-btn");

        const court_name = $('#new-current-court').text();
        const bench = $('#new-current-bench').text();

         $.ajax({
            type: 'GET',
            url: '/new/cancel-scrap/' + court_name + '/' + bench,
            success: function () {
                Materialize.toast("Scrapping Aborted!", 2000, 'light-green');
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                s_btn.addClass("d-none");
                $('#new-submit-btn').removeClass("d-none");
            },
            error: function (data) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                s_btn.addClass("d-none");
                $('#new-submit-btn').removeClass("d-none");
            }
         });
     });

});

function current_new(court_name, bench) {
     const s_btn = $("#new-submit-btn");
     const l_btn = $("#new-btn-loading");
     const se_btn = $("#new-btn-send");

     $.ajax({
        type: 'GET',
        url: '/new/current-scrap/' + court_name + "/" + bench,
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"16\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
                l_btn.removeClass("loading-btn");
                se_btn.removeClass("d-none");
                s_btn.removeClass("disabled");
                $('#new-cancel-btn').addClass("d-none");
                s_btn.removeClass("d-none");
                clearInterval(new_interval);
            }
            else {
                tr_list += "<tr>";
                tr_list += "<td id='new-current-court'>" + data.court_name + "</td>";
                tr_list += "<td id='new-current-bench'>" + data.bench + "</td>";
                tr_list += "<td>" + data.end_date + "</td>";
                tr_list += "<td>" + data.no_tries + "</td>";
                tr_list += "<td>" + data.total_cases + "</td>";
                tr_list += "<td>" + data.inserted_cases + "</td>";
                tr_list += "<td>" + data.no_nodata + "</td>";
                tr_list += "<td>" + data.no_alerts + "</td>";
                tr_list += "<td>" + data.no_pdf + "</td>";
                tr_list += "<td>" + data.no_text + "</td>";
                tr_list += "<td>" + data.no_json + "</td>";
                tr_list += "<td>" + data.transferred_pdf + "</td>";
                tr_list += "<td>" + data.transferred_text + "</td>";
                tr_list += "<td>" + data.transferred_json + "</td>";
                tr_list += "<td>" + data.status + "</td>";
                tr_list += "</tr>";

                if ("IN_RUNNING" !== data.status){
                    $('#new-cancel-btn').addClass("d-none");
                    $('#new-submit-btn').removeClass("d-none");
                    clearInterval(new_interval);
                }
            }
            $("#new-current").html(tr_list);

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
     });
}

function running_new() {
     const s_btn = $("#new-submit-btn");
     const l_btn = $("#new-btn-loading");
     const se_btn = $("#new-btn-send");

     s_btn.addClass("disabled");
     se_btn.addClass("d-none");
     l_btn.addClass("loading-btn");

     $.ajax({
        type: 'GET',
        url: '/new/running-scrap',
        success: function (data) {
            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"16\"><h6 class='center-align grey-text text-darken-2'>" +
                    "No Process Running</h6></td></tr>";
                 l_btn.removeClass("loading-btn");
                 se_btn.removeClass("d-none");
                 s_btn.removeClass("disabled");
                $('#new-cancel-btn').addClass("d-none");
                s_btn.removeClass("d-none");
                clearInterval(new_interval);
            }
            else {
                tr_list += "<tr>";
                tr_list += "<td id='new-current-court'>" + data.court_name + "</td>";
                tr_list += "<td id='new-current-bench'>" + data.bench + "</td>";
                tr_list += "<td>" + data.end_date + "</td>";
                tr_list += "<td>" + data.no_tries + "</td>";
                tr_list += "<td>" + data.total_cases + "</td>";
                tr_list += "<td>" + data.inserted_cases + "</td>";
                tr_list += "<td>" + data.no_nodata + "</td>";
                tr_list += "<td>" + data.no_alerts + "</td>";
                tr_list += "<td>" + data.no_pdf + "</td>";
                tr_list += "<td>" + data.no_text + "</td>";
                tr_list += "<td>" + data.no_json + "</td>";
                tr_list += "<td>" + data.transferred_pdf + "</td>";
                tr_list += "<td>" + data.transferred_text + "</td>";
                tr_list += "<td>" + data.transferred_json + "</td>";
                tr_list += "<td>" + data.status + "</td>";
                tr_list += "</tr>";

                if ("IN_RUNNING" === data.status){
                     l_btn.removeClass("loading-btn");
                     se_btn.removeClass("d-none");
                     s_btn.removeClass("disabled");
                     s_btn.addClass("d-none");
                     $('#new-cancel-btn').removeClass("d-none");
                     new_interval = setInterval(function () {
                                     current_s(data.Name);
                                 }, 10000);
                }
                else {
                    $('#new-cancel-btn').addClass("d-none");
                    $('#new-submit-btn').removeClass("d-none");
                    clearInterval(new_interval);
                }
            }
            $("#new-current").html(tr_list);

        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
     });
}

function validate_new() {
    const court_name = $('#new-court-name').val();
    const bench= $('#new-bench').val();

    if (court_name === null || court_name.localeCompare("") === 0){
        Materialize.toast('Please select court name.', 4000, 'red');
        return false;
    }
    else if (bench === null || bench.localeCompare("") === 0){
        Materialize.toast('Please select bench.', 4000, 'red');
        return false;
    }
    else
        return true;
}
