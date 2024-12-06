var tabla_datos;
function tabla_de_registros(selector, url) {
    tabla_datos = $(selector).DataTable({
        responsive: true,
        language: {
            url: url,
        },
        ajax: {
            url: window.location.pathname,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                action: "list_data",
            },
            dataSrc: "",
        },
        columns: [
            { data: "id" },
            { data: "nombre" },
            { data: "documento_identidad" },
            { data: "telefono" },
            { data: "correo_electronico" },
            { data: "direccion" },
            { data: "direccion" },
        ],
        columnDefs: [
            {
                targets: [-1],
                render: function(data, type, row) {
                    let botones = '<a href="/clientes/editar-cliente/'+ row.id +'/" class="btn btn-md" style="color: #007bff; padding-top:0; padding-bottom:0;"><i class="fas fa-edit"></i></a>'
                    botones += '<a href="/clientes/eliminar-cliente/'+ row.id +'/" class="btn btn-md" style="color: #007bff; padding-top:0; padding-bottom:0;"><i class="fas fa-trash"></i></a>'
                    return botones
                }
            }
        ]
    });
}
