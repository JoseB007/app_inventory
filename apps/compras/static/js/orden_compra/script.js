var tabla_productos;
var compra = {
    items: {
        proveedor: "",
        estado: "",
        subtotal: 0.0,
        iva: 0.0,
        total: 0.0,
        productos: [],
    },
    calcular_totales: function () {
        var cal_subtotal = 0;
        var iva_calculado = $("#id_iva").val();
        this.items.productos.forEach((element, index) => {
            element.subtotal = element.cantidad * element.precio;
            cal_subtotal += element.subtotal;
        });

        this.items.subtotal = cal_subtotal;
        this.items.iva = this.items.subtotal * iva_calculado;
        this.items.total = this.items.subtotal + this.items.iva;

        $("#id_subtotal").val(formatearNumero(this.items.subtotal));
        $("#id_iva_calulado").val(formatearNumero(this.items.iva));
        $("#id_total").val(formatearNumero(this.items.total));
    },
    agregar: function (item) {
        // let p;
        // $.each(this.items.productos, function (index, producto) {
        //     if (producto["id"] == item.id) {
        //         producto.cantidad += item.cantidad;
        //         p = true;
        //         return false
        //     }
        // });
        // if (!p) {
        //     this.items.productos.push(item);
        // }
        // this.lista();
        let productoExistente = this.items.productos.find(
            (producto) => producto.id === item.id
        );

        if (productoExistente) {
            // Si el producto ya existe, actualizamos su cantidad
            productoExistente.cantidad += item.cantidad;
        } else {
            // Si no existe, lo agregamos
            this.items.productos.push(item);
        }
        // Actualizamos la lista
        this.lista();
    },
    lista: function () {
        this.calcular_totales();
        tabla_productos = $("#tabla_productos").DataTable({
            destroy: true,
            responsive: true,
            language: {
                url: url_language,
            },
            data: this.items.productos,
            createdRow(row, data, dataIndex, cells) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 100000,
                    step: 1,
                });
            },
            columns: [
                { data: "nombre" },
                { data: "precio" },
                { data: "cantidad" },
                { data: "subtotal" },
                { data: "nombre" },
            ],
            columnDefs: [
                {
                    targets: [2],
                    render: function (data, type, row) {
                        return (
                            '<input type="text" name="cantidad" class="form-control form-control-sm" autocomplete="off" value="' +
                            row.cantidad +
                            '"></input>'
                        );
                    },
                },
                {
                    targets: [1, 3],
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
                        return '<a rel="remove" class="btn btn-lg" style="color: #007bff; display:inline"><i class="fas fa-trash-alt"></i></a>';
                    },
                },
            ],
        });
    },
};

$(function () {
    // $("#id_productos").on("change", function () {
    //     var id_categoria = $(this).val();
    //     var buscar_producto = $("#buscar_producto");

    //     if (id_categoria == "") {
    //         buscar_producto.val("---------");
    //         return false;
    //     }

    //     $.ajax({
    //         url: window.location.pathname,
    //         data: {
    //             mostrar_datos: "mostrar",
    //             id_producto: id_categoria,
    //         },
    //         type: "POST",
    //         dataType: "json",
    //         // código a ejecutar si la petición es satisfactoria;
    //         // la respuesta es pasada como argumento a la función
    //         success: function (data) {
    //             if (!data.error) {
    //                 buscar_producto.val(data.nombre);
    //             } else {
    //                 message_error(data.error);
    //             }
    //         },
    //         error: function (xhr, status) {
    //             alert(
    //                 "Disculpe, existió un problema.",
    //                 textStatus + ": " + errorThrown
    //             );
    //         },
    //     });
    // });

    $("#buscar_producto").autocomplete({
        minLength: 2,
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    accion: "buscar",
                    term: request.term,
                },
                type: "POST",
                dataType: "json",
                // código a ejecutar si la petición es satisfactoria la respuesta es pasada como argumento a la función
                success: function (data) {
                    if (data.length === 0) {
                        response([
                            {
                                value: "El producto no se encontró",
                            },
                        ]);
                    }
                    else if (!data.error) {
                        response(data);
                    } else {
                        message_error(response.error);
                    }
                },
                error: function (xhr, status) {
                    alert(
                        "Disculpe, existió un problema.",
                        status + ": " + xhr
                    );
                },
            });
        },
        select: function (event, ui) {
            event.preventDefault();
            if (
                ui.item.value !=
                "El producto no se encontró"
            ) {
            ui.item.cantidad = 1;
            ui.item.subtotal = 0.0;
            compra.agregar(ui.item);
            }
            $(this).val("");
        },
    });

    $("#id_iva")
        .TouchSpin({
            min: 0,
            max: 100,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            maxboostedstep: 10,
            postfix: "%",
        })
        .on("change", function () {
            compra.calcular_totales();
        })
        .val(0.0);

    $("#tabla_productos tbody")
        .on("click", 'a[rel="remove"]', function () {
            var fila_eliminada = tabla_productos
                .row(this.closest("tr"))
                .index();
            compra.items.productos.splice(fila_eliminada, 1);
            compra.lista();
        })
        .on("change", 'input[name="cantidad"]', function () {
            var cant = parseInt($(this).val());
            // // Obtner el index de la fila
            // var fila = tabla_productos.row(this.closest('tr')).index()
            // // Obtener los datos de la fila
            // var datos_fila = tabla_productos.row(fila).data();
            // datos_fila.cantidad = cant
            // // Calcular los totales
            // compra.calcular_totales()
            // // Obtener index columna
            // var columna = tabla_productos.column(this.closest('td')).index()
            // // Actualizar valor en la tabla
            var fila = tabla_productos.cell(this.closest("td")).index();
            compra.items.productos[fila.row].cantidad = cant;
            compra.calcular_totales();
            tabla_productos
                .cell(fila.row, fila.column + 1)
                .data(compra.items.productos[fila.row].subtotal)
                .draw();
        });

    $(".btn-deleteProducts").on("click", function () {
        if (compra.items.productos.length === 0) return false;
        alertas_eliminar(function () {
            compra.items.productos = [];
            compra.lista();
        });
    });

    $(".btn-addProveedor").on("click", function () {
        $("#modalAddProveedor").modal("show");
        setTimeout(function () {
            $("#modalAddProveedor").find("input:first").focus();
        }, 500);
    });

    // Enviar formulario proveedor
    $("#id_formulario_proveedor").on("submit", function (e) {
        e.preventDefault();
        var parametros = $(this).serializeArray();
        var url = "/proveedores/agregar-proveedor";

        enviar_datos_ajax(url, parametros, function (response) {
            if (!response.error) {
                $("#modalAddProveedor").modal("hide");

                // Limpiar datos del formulario modal
                var formProveedor = $("#id_formulario_proveedor input");
                $.each(formProveedor, function (index, campo) {
                    if ($(campo).is("input")) {
                        $(campo).val("");
                    }
                });

                const nuevoProveedor = $("<option>", {
                    value: response.proveedor.id,
                    text: response.proveedor.nombre,
                });

                $('select[name="proveedor"]').append(nuevoProveedor);
                $('select[name="proveedor"]').val(response.proveedor.id);

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

    $("#id_formulario_compra").on("submit", function (e) {
        e.preventDefault();
        if (compra.items.productos.length === 0) {
            message_error(
                "No se ha agregado ningún producto a la lista de compra"
            );
            return false;
        }
        compra.items.proveedor = $('select[name="proveedor"]').val();
        compra.items.estado = $('select[name="estado"]').val();
        // var parametros = {
        //     compra: JSON.stringify(compra.items),
        //     accion: $('input[name="accion"]').val(),
        // };
        var parametros = $(this).serializeArray()
        
        parametros.push({
            name: 'compra',
            value: JSON.stringify(compra.items)
        })

        enviar_datos_ajax(
        window.location.pathname,
        parametros,
        url_redireccion
        );
    });
});
