let tabla;
let data;
let tabla_detalle;

function tabla_de_registros(selector, url_language) {
    tabla = $(selector).DataTable({
        destroy: true,
        responsive: true,
        deferRender: true,
        language: {
            url: url_language,
        },
        ajax: {
            url: window.location.pathname,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                accion: "mostrar",
            },
            dataSrc: "",
        },
        columns: [
            { data: "id" },
            { data: "fecha" },
            { data: "tl_ordenes.0" },
            { data: "tl_ordenes.1" },
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
                class: "text-right",
                render: function (data, type, row) {
                    let boton =
                        '<button rel="detail" class="btn btn-md" style="color: #007bff; display:inline; padding: 0;"><i class="fas fa-search"></i></button>';
                    return boton;
                },
            },
        ],
    });
}

function mostrar_orden(orden) {
    tabla_detalle = $("#tabla_detail").DataTable({
        destroy: true,
        responsive: true,
        deferRender: true,
        language: {
            url: url,
        },
        data: orden,
        columns: [
            { data: "id" },
            { data: "fecha" },
            { data: "estado" },
            { data: "productos" },
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
            {
                targets: [3],
                render: function (data, type, row) {
                    let productos = ""
                    $.each(data, function (index, producto) {
                        productos += "<p style='margin-bottom: .5rem;'>" + producto + "</p>";
                    })
                    return productos
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
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    id: datos_fila.id,
                    accion: "detalle",
                },
                dataType: "json",
                success: function (response) {
                    data = response
                    if (data[0].length > 0) {
                        mostrar_orden(data[0]);
                        $("#id_orden").text("(Órdenes de Venta)");
                        $("button[id='btn-Ord_venta']").css("display", "none");
                        $("button[id='btn-Ord_compra']").show();
                    }
                    else {
                        mostrar_orden(data[1]),
                        $("#id_orden").text("(Órdenes de Compra)");
                        $("button[id='btn-Ord_compra']").css("display", "none");
                        $("button[id='btn-Ord_venta']").show();
                    }
                },
                error: function (xhr, status) {
                    alert(
                        "Disculpe, existió un problema.",
                        status + ": " + xhr
                    );
                },
            });
            $("#modalDetallesOrdenes").modal("show");
        }
    );


    $("button[id='btn-Ord_venta']").on("click", function () {
        $("#id_orden").text("(Órdenes de Venta)");
        mostrar_orden(data[0]);
        $("button[id='btn-Ord_venta']").css("display", "none");
        $("button[id='btn-Ord_compra']").show();
    });

    $("button[id='btn-Ord_compra']").on("click", function () {
        $("#id_orden").text("(Órdenes de Compra)");
        mostrar_orden(data[1]);
        $("button[id='btn-Ord_compra']").css("display", "none");
        $("button[id='btn-Ord_venta']").show();
    });
});
