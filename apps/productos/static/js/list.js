function tabla_de_registros(selector, language_url) {
    $(selector).DataTable({
        destroy: true,
        responsive: true,
        deferRender: true,
        language: {
            url: language_url,
        },
        ajax: {
            url: window.location.pathname,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                mostrar_datos: "mostrar",
            },
            dataSrc: "",
        },
        columns: [
            { data: "id" },
            { data: "nombre" },
            { data: "descripcion" },
            { data: "categoria" },
            { data: "precio" },
            { data: "cantidad_en_stock" },
            { data: "nombre" },
        ],
        columnDefs: [
            {
                targets: [-1],
                render: function (data, type, row) {
                    var buttons =
                        '<a href="/productos/editar-producto/' +
                        row.id +
                        '/" class="btn btn-md" style="color: #007bff; padding-top:0; padding-bottom:0;"><i class="fas fa-edit"></i></a>';
                    buttons +=
                        '<a href="/productos/eliminar-producto/' +
                        row.id +
                        '/" class="btn btn-md" style="color: #007bff; padding-top:0; padding-bottom:0;"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                },
            },
            {
                targets: [-2],
                render: function (data, type, row) {
                    var stock;
                    if (data <= 10) {
                        stock =
                            '<span class="badge rounded-pill bg-danger">' +
                            row.cantidad_en_stock +
                            '</span>';
                    } else {
                        stock =
                            '<span class="badge rounded-pill bg-primary">' +
                            row.cantidad_en_stock +
                            '</span>';
                    }
                    return stock;
                },
            },
            {
                targets: [-3],
                render: function (data, type, row) {
                    var numero = parseFloat(data)
                    var numero_formateado = formatearNumero(numero)
                    return '$' + numero_formateado
                }
            }
        ],
    });
}
