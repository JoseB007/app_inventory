function tabla_de_registros(selector, language_url) {
    $(selector).DataTable({
        destroy: true,
        responsive: true,
        deferRender: true,
        language: {
            url: language_url,
        },
        ajax: {
            language: {
                url: url,
            },
            url: window.location.pathname,
            type: "POST",
            data: {
                mostrar_datos: "mostrar",
            },
            dataSrc: "",
        },
        columns: [
            { data: "id" },
            { data: "usuario" },
            { data: "documento_de_identidad" },
            { data: "telefono" },
            { data: "direccion" },
            { data: "correo_electronico" },
            { data: "fecha_contratacion" },
            { data: "usuario" },
        ],
        columnDefs: [
            {
                targets: [-1],
                render: function (data, type, row) {
                    var buttons =
                        '<a href="/empleados/editar-empleado/' +
                        row.id +
                        '/" class="btn btn-md" style="color: #007bff"><i class="fas fa-edit"></i></a> ';
                    buttons +=
                        '<a href="/empleados/eliminar-empleado/' +
                        row.id +
                        '/" class="btn btn-md" style="color: #007bff"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                },
            },
        ],
    });
}
