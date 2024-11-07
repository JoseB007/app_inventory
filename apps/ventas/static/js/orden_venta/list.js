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
            data: {
                action: "list_data",
            },
            dataSrc: "",
        },
        columns: [
            { data: "id" },
            { data: "fecha" },
            { data: "cliente" },
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
                        '<a href="/ventas/'+ row.id +'/factura.pdf" class="btn btn-md" style="color: #007bff; display:inline"><i class="fas fa-search"></i></a>';
                    botones +=
                        '<button rel="detail" class="btn btn-md" style="color: #007bff; display:inline"><i class="fas fa-search"></i></button>';
                    return botones;
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
            $("#modalDetail").modal("show");
            var fila = tabla_datos.row($(this).closest("tr")).index();
            var datos_fila = tabla_datos.row(fila).data();
            // console.log(fila);
            // console.log(datos_fila);
            $("#tabla_detail").DataTable({
                destroy: true,
                responsive: true,
                language: {
                    url: url,
                },
                ajax: {
                    url: window.location.pathname,
                    type: "POST",
                    data: {
                        id: datos_fila.id,
                        action: "detail",
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
        }
    );
});
