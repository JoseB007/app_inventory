var tabla_datos;
function tabla_de_registros(selector, language_url) {
    tabla_datos = $(selector).DataTable({
        responsive: true,
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
            { data: "fecha_de_orden" },
            { data: "proveedor" },
            { data: "estado" },
            { data: "subtotal" },
            { data: "iva" },
            { data: "total" },
            { data: "id" },
        ],
        columnDefs: [
            {
                targets: [-1],
                class: "text-right",
                render: function (data, type, row) {
                    return '<button rel="detail" class="btn btn-md" style="color: #007bff; display:inline; padding-top:0; padding-bottom:0;"><i class="fas fa-search"></i></button>';
                },
            },
            {
                targets: [-2, -3, -4],
                render: function (data, type, row) {
                    var numero = parseFloat(data);
                    var numero_formateado = formatearNumero(numero);
                    return "$" + numero_formateado;
                },
            },
            {
                targets: [3],
                render: function (data, type, row) {
                    let estado;
                    if (data == "Cancelada") {
                        estado =
                            '<span class="badge badge-success">' +
                            data +
                            "</span>";
                    }
                    return estado;
                },
            },
        ],
    });
}

$(function () {
    $("#tabla_productos tbody").on(
        "click",
        'button[rel="detail"]',
        function () {
            var celda_tr = tabla_datos.cell($(this).closest("td")).index();
            var datos_tr = tabla_datos.row(celda_tr.row).data();
            $("#tabla_detail").DataTable({
                destroy: true,
                responsive: true,
                language: {
                    url: url,
                },
                ajax: {
                    url: window.location.pathname,
                    type: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    data: {
                        mostrar_datos: "detalle",
                        id: datos_tr.id,
                    },
                    dataSrc: "",
                },
                columns: [
                    { data: "producto" },
                    { data: "precio_unitario" },
                    { data: "cantidad" },
                    { data: "subtotal" },
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        render: function (data, type, row) {
                            var numero = parseFloat(data);
                            var numero_formateado = formatearNumero(numero);
                            return "$" + numero_formateado;
                        },
                    },
                ],
            });

            $("#modalDetail").modal("show");
        }
    );

    // Modal del busqueda avanzada (Filtos)
    $("#id_btnfiltros").on('click', function () {
        $("#modalfiltros").modal('show')
    })
});

function tabla_filtros(tabla_selector, datos, url) {
    tabla_datos = $(tabla_selector).DataTable({
        destroy: true,
        responsive: true,
        data: datos,
        language: {
            url: url,
        },
        columns: [
            { data: "id" },
            { data: "fecha_de_orden" },
            { data: "proveedor" },
            { data: "estado" },
            { data: "subtotal" },
            { data: "iva" },
            { data: "total" },
            { data: "total" },
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4],
                render: function (data, type, row) {
                    var numero = parseFloat(data);
                    var numero_formateado = formatearNumero(numero);
                    return "$" + numero_formateado;
                },
            },
            {
                targets: [-1],
                class: "text-right",
                render: function (data, type, row) {
                    let botones =
                        '<a href="/ventas/reportes/facturas/'+ row.id +'/" target="__blank" class="btn btn-md" style="color: #007bff; display:inline; padding-top:0; padding-bottom:0;"><i class="fa-solid fa-file-pdf"></i></a>';
                    botones +=
                        '<button rel="detail" class="btn btn-md" style="color: #007bff; display:inline; padding-top:0; padding-bottom:0;"><i class="fas fa-search"></i></button>';
                    return botones;
                },
            },
            {
                targets: [3],
                render: function (data, type, row) {
                    let estado;
                    if (data == "Cancelada") {
                        estado =
                            '<span class="badge badge-success">' +
                            data +
                            "</span>";
                    }
                    return estado;
                },
            },
        ],
    })
}
