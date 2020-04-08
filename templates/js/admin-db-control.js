function populate_db(cmd) {
    $("#task-status").html("processing...");
    console.log($('#capture_sdout').prop('checked'));
    $.post('{{ url_for("admin.populate_database") }}', {'cmd': cmd, 'capture_sdout': $('#capture_sdout').prop('checked')}, function(data){
       console.log(data);
       $("#task-status").html(data);
    });
}