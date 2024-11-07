function tabla_de_registros(selector, language_url) {
    $(selector).DataTable({
        responsive: true,
        language: {
            url: language_url
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'mostrar_datos': 'mostrar'
            },
            dataSrc: '',
        },
        columns: [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'direccion'},
            {'data': 'telefono'},
            {'data': 'correo_electronico'},
            {'data': 'nombre'},
        ],
        columnDefs: [
            {
                targets: [-1],
                render: function(data, type, row){
                    var botones = '<a class="btn btn-md" style="color: #007bff" href="editar-proveedor/'+ row.id +'/"><i class="fa-solid fa-pen-to-square"></i></a>';
                    botones += '<a class="btn btn-md" style="color: #007bff" href="eliminar-proveedor/' + row.id + '/"><i class="fas fa-trash-alt"></i></a>';
                    return botones
                }
            }
        ]
    })
}