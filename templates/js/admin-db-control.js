let cmd_endpoint = '{{ url_for("admin.populate_database") }}';
let status_div = $("#task-status");

function _addToStatus(message, newline= true) {

    let newStatus = status_div.html() + "<br/>" + message.replace("\n", "<br/>");

    if (newline) {
        newStatus += "<br/>";
    }

    status_div.html(newStatus);
}

// function _callDbCmd(cmd, capture_sdout, callback){
//     return $.post('{{ url_for("admin.populate_database") }}', {'cmd': cmd, 'capture_sdout': capture_sdout}, callback).;
// }

function populate_db_cmd(cmd) {
    _addToStatus("processing " + cmd);
    // let capture_sdout = ($('#capture_sdout').prop('checked'));

    console.log();
    return $.post(cmd_endpoint, {'cmd': cmd, 'capture_sdout': true}, function(data){
        console.log(data);

        // _addToStatus(data['success'] ? "Success" : "ERROR");
        //         _addToStatus("Success" + data['success']);

        // _addToStatus(data['output'])
        _addToStatus(data)

        // if (data['output'] !== "") {
        //
        // }


    });
}

function populate_db_full() {
    populate_db_cmd("clear_db")
        .then(() => populate_db_cmd("populate_users"))
        .then(() => populate_db_cmd("populate_users"))
        .then(() => populate_db_cmd("populate_stocks"))
        .then(() => populate_db_cmd("clean_stocks"))
        .then(() => populate_db_cmd("populate_stock_history"))
        .then(() => populate_db_cmd("generate_portfolios"))


}