let tabla;
let data;

function tabla_de_registros(selector, url_language) {
    tabla = $(selector).DataTable({
        destroy: true,
        responsive: true,
        deferRender: true,
        autoWidth: false,
        language: {
            url: url_language,
        },
        ajax: {
            url: window.location.pathname,
            type: "POST",
            data: {
                accion: "mostrar",
            },
            dataSrc: "",
        },
        columns: [
            { data: "id" },
            { data: "fecha" },
            { data: "total_ventas" },
            { data: "total_compras" },
            { data: "id" },
        ],
        columnDefs: [
            {
                targets: [-3, -2],
                render: function (data, type, row) {
                    let num = parseFloat(data);
                    let num_formateado = formatearNumero(num);
                    return "$" + num_formateado;
                },
            },
            {
                targets: [-1],
                render: function (data, type, row) {
                    let boton =
                        '<button rel="detail" class="btn btn-md" style="color: #007bff; display:inline"><i class="fas fa-search"></i></button>';
                    return boton;
                },
            },
        ],
    });
}

$(function () {
    $("#tabla_productos tbody").on(
        "click",
        "button[rel='detail']",
        function () {
            var fila = tabla.row($(this).closest("tr")).index();
            var datos_fila = tabla.row(fila).data();
            $.ajax({
                url: window.location.pathname,
                type: "POST",
                data: {
                    id: datos_fila.id,
                    accion: "detalle",
                },
                dataType: "json",
                success: function (response) {
                    data = response;
                    mostrar_orden(0);
                },
                error: function (xhr, status) {
                    alert(
                        "Disculpe, existió un problema.",
                        status + ": " + xhr
                    );
                },
            });
            $("#id_orden").text("(Órdenes de Venta)");
            $("button[id='btn-Ord_venta']").css("display", "none")
            $("button[id='btn-Ord_compra']").show();
            $("#modalDetallesOrdenes").modal("show");
        }
    );

    function mostrar_orden(orden) {
        $("#tabla_detail").DataTable({
            destroy: true,
            responsive: true,
            autoWidth: false,
            language: {
                url: url,
            },
            data: data[orden],
            columns: [
                { data: "id" },
                { data: "fecha" },
                { data: "estado" },
                { data: "total" },
                { data: "empleado" },
            ],
            columnDefs: [
                {
                    targets: [-2],
                    render: function (data, type, row) {
                        let num = parseFloat(data);
                        let num_formateado = formatearNumero(num);
                        return num_formateado;
                    },
                },
                {
                    targets: [-1],
                    class: "text-right",
                },
            ],
        });
    }

    $("button[id='btn-Ord_venta']").on("click", function () {
        $("#id_orden").text("(Órdenes de Venta)");
        mostrar_orden(0);
        $("button[id='btn-Ord_venta']").css("display", "none")
        $("button[id='btn-Ord_compra']").show();
    });

    $("button[id='btn-Ord_compra']").on("click", function () {
        $("#id_orden").text("(Órdenes de Compra)");
        mostrar_orden(1);
        $("button[id='btn-Ord_compra']").css("display", "none")
        $("button[id='btn-Ord_venta']").show();
    });
});

