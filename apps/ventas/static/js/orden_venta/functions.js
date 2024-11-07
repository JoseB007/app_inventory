var table_data;

var sale = {
    cliente: "",
    estado: "",
    subtotal: 0.0,
    iva: 0.0,
    total: 0.0,
    productos: [],
};

function add_sale(item) {
    sale.productos.push(item);
    calculate_totals();
    table_sale();
}

function calculate_totals() {
    var sale_subtotal = 0;
    var iva = $("#porcentaje_iva").val();
    sale.productos.forEach((producto) => {
        producto.subtotal = producto.cantidad * producto.precio;
        sale_subtotal += producto.subtotal;
    });

    sale.subtotal = sale_subtotal;
    sale.iva = sale_subtotal * iva;
    sale.total = sale.subtotal + sale.iva;

    $("#id_subtotal").val(formatearNumero(sale.subtotal));
    $("#id_iva").val(formatearNumero(sale.iva));
    $("#id_total").val(formatearNumero(sale.total));
}

function table_sale() {
    table_data = $("#tabla_ventas").DataTable({
        destroy: true,
        responsive: true,
        language: {
            url: url,
        },
        data: sale.productos,
        createdRow: function (row, data, dataIndex) {
            $(row).find('input[name="cantidad"]').TouchSpin({
                min: 1,
                max: 100000,
                step: 1,
            });
        },
        columns: [
            { data: "label" },
            { data: "precio" },
            { data: "cantidad" },
            { data: "subtotal" },
            { data: "label" },
        ],
        columnDefs: [
            {
                targets: [-3],
                render: function (data, type, row) {
                    return (
                        '<input type="text" class="form-control-sm" name="cantidad" value="' +
                        data +
                        '"></input>'
                    );
                },
            },
            {
                targets: [-2, -4],
                render: function (data, type, row) {
                    let numero = parseFloat(data)
                    let numero_formateado = formatearNumero(numero)
                    return "$" + numero_formateado;
                },
            },
            {
                targets: [-1],
                class: "text-right",
                render: function (data, type, row) {
                    return '<a rel="remove" class="btn btn-lg" style="color: #007bff; display:inline"><i class="fas fa-trash-alt"></i></a>';
                },
            },
        ],
    });
}

$(function () {
    // Agregar cliente por defecto
    // var cliDef = {
    //     valor: "1",
    //     nombre: "2222222222",
    // };
    // var cliente = $("<option>", {
    //     value: cliDef.valor,
    //     text: cliDef.nombre,
    //     selected: true,
    // });
    // $("#id_cliente").append(cliente);
    $("#id_cliente").on("change", function () {
        var cli = $(this).val();
        if (cli == "") {
            $(this).val("1");
        }
    });

    // Limpiar el input 'buscar_producto'
    $(".btnClear").on("click", function () {
        $("#buscar_producto").val("");
        $("#buscar_producto").focus();
    });

    // jQuery UI
    $("#buscar_producto").autocomplete({
        minLength: 2,
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: "POST",
                data: {
                    term: request.term,
                    action: "buscar",
                },
                dataType: "json",
                success: function (data) {
                    if (data.length === 0) {
                        response([
                            {
                                value: "El producto no se encontró o no existe suficiente inventario",
                            },
                        ]);
                    } else if (!data.error) {
                        response(data);
                    } else {
                        message_error(response.error);
                    }
                },
                error: function (xhr, status) {
                    alert(
                        "Disculpe, existió un problema.",
                        textStatus + ": " + errorThrown
                    );
                },
            });
        },
        select: function (event, ui) {
            event.preventDefault();
            if (
                ui.item.value !=
                "El producto no se encontró o no existe suficiente inventario"
            ) {
                ui.item["cantidad"] = 1;
                ui.item["subtotal"] = 0.0;
                add_sale(ui.item);
            }
            $(this).val("");
        },
    });

    // Agregar una nueva cantidad del producto selecionado
    $("#tabla_ventas tbody").on(
        "change",
        'input[name="cantidad"]',
        function () {
            var cant = parseInt($(this).val());
            var fila = table_data.row($(this).closest("tr")).index();
            sale.productos[fila].cantidad = cant;
            var columna = table_data.column($(this).closest("td")).index();
            calculate_totals();
            table_data
                .cell(fila, columna + 1)
                .data(sale.productos[fila].subtotal)
                .draw();
        }
    );

    // Eliminar un producto de la tabla de ventas
    $("#tabla_ventas tbody").on("click", 'a[rel="remove"]', function () {
        var fila_eliminada = table_data.row(this.closest("tr")).index();
        sale.productos.splice(fila_eliminada, 1);
        table_sale();
        calculate_totals();
    });

    // TouchSpin input 'IVA'
    $("#porcentaje_iva")
        .TouchSpin({
            min: 0,
            max: 1,
            step: 0.01,
            decimals: 2,
            postfix: "%",
        })
        .val(0.19)
        .on("change", function () {
            calculate_totals();
        });

    // Calcular efectivo
    $(".btn-save").on("click", function (e) {
        e.preventDefault();
        if (sale.productos.length === 0) {
            message_error(
                "No se ha agregado ningún producto a la lista de venta."
            );
            return false;
        }

        // $("#tablaFact tbody").empty();
        $("#id_efectivo").val("");
        $("#id_cambio").text("$0.00");
        $("#id_monto").text("$0.00");

        // $.each(sale.productos, function (index, item) {
        //     var nuevaFila = $("<tr>");
        //     nuevaFila.append($("<td>").text(item.label));
        //     nuevaFila.append($("<td>").text(item.cantidad));
        //     nuevaFila.append($("<td>").text("$" + item.subtotal));
        //     $("#tablaFact").append(nuevaFila);
        // });

        $("#id_totalVenta").text("$" + formatearNumero(sale.total));
        $("#modalFact").modal("show");
    });

    // Calcular el cambio
    function calcular_efectivo() {
        var efectivo = parseFloat($("#id_efectivo").val());
        var total = sale.total || 0;

        // Validar que efectivo sea un número válido antes de continuar
        if (isNaN(efectivo) || efectivo < 0) {
            $("#id_cambio").text("$0.00");
            $("#id_monto").text("$0.00");
            return false;
        }

        // Calcular el cambio
        var cambio = efectivo - total;
        $("#id_monto").text("$" + formatearNumero(efectivo));
        $("#id_cambio").text("$" + formatearNumero(cambio));
    }

    $("#id_efectivo").on("input", function () {
        var monto = parseFloat($(this).val());
        if (monto < sale.total) {
            $("#id_monto").css("color", "red");
        } else {
            $("#id_monto").css("color", "black");
        }
        calcular_efectivo();
    });

    // Enviar formulario de venta
    $("#id_formulario_venta").on("submit", function (e) {
        e.preventDefault();
        if (sale.productos.length === 0) {
            message_error(
                "No se ha agregado ningún producto a la lista de venta."
            );
            return false;
        }

        if (
            $("#id_efectivo").val() == "" ||
            $("#id_efectivo").val() < sale.total
        ) {
            message_error(
                "La cantidad en efectivo no puede ser menor que el total a pagar."
            );
            return false;
        }

        sale.cliente = $('select[name="cliente"]').val();
        sale.estado = $('select[name="estado"]').val();
        var parametros = {
            sale: JSON.stringify(sale),
            action: $('input[name="accion"]').val(),
        };
        console.log(parametros);
        enviar_datos_ajax(
            window.location.pathname,
            parametros,
            url_redireccion
        );
        // var formData = new FormData(this)
        // formData.append('productos', JSON.stringify(sale.productos))

        // formData.entries().forEach(element => {
        //     console.log(element[0]+ ": " + element[1])
        // });
    });

    $(".btn-addCliente").on("click", function () {
        $("#modalAddCliente").modal("show");
        setTimeout(function () {
            $("#modalAddCliente").find('input:first').focus();
        }, 500);
    });

    // Enviar formulario de cliente
    $("#id_formulario_cliente").on("submit", function (e) {
        e.preventDefault();
        var parametros = $(this).serializeArray();
        var url = "/clientes/agregar-cliente/";

        enviar_datos_ajax(url, parametros, function (response) {
            if (!response.error) {
                $("#modalAddCliente").modal("hide");

                var formCliente = $("#id_formulario_cliente input");
                $.each(formCliente, function (index, campo) {
                    if ($(campo).is("input")) {
                        $(campo).val("");
                    }
                });

                const nuevoCliente = $('<option>', {
                    value: response.cliente.id,
                    text: response.cliente.nombre
                });

                $('select[name="cliente"]').append(nuevoCliente);
                $('select[name="cliente"]').val(response.cliente.id);

                message_exito(
                    "El registro se ha creado exitosamente.",
                    "Éxito",
                    "success"
                );
            } else {
                message_error(response.error);
            }
        });
    });
});
