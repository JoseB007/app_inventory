function enviar_datos_ajax(url, parametros, url_redireccion) {
    $.confirm({
        title: "Confirmación!",
        theme: "modern",
        content: "¿Estas seguro de relizar esta acción?",
        type: "blue",
        typeAnimated: true,
        buttons: {
            info: {
                text: "Confirmar",
                btnClass: "btn-blue",
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname,
                        type: "POST",
                        data: parametros,
                        dataType: "json",
                    })
                    .done(function (data) {
                        /*Validar si la variable data no contiene una propiedad llamada error*/
                        if (!data.error) {
                            if (typeof url_redireccion === "function") {
                                url_redireccion(data);
                            } else {
                                location.href = url_redireccion;
                                return false;
                            }
                        } else {
                            message_error(data.error);
                        }
                    })
                    .fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ": " + errorThrown);
                    })
                    .always(function (data) { });
                },
            },
            danger: {
                text: "Cancelar",
                btnClass: "btn-red any-other-class",
            },
        },
    });
}

function message_error(obj) {
    var html = "";
    if (typeof obj === "object") {
        $.each(obj, function (key, value) {
            html += "<p>" + key + ": " + value + "</p>";
        });
    } else {
        html = "<p>" + obj + "</p>";
    }
    html += "</p>";
    Swal.fire({
        icon: "error",
        title: "Oops...",
        /*text: errores,*/
        html: html,
    });
}

// Capturar mensajes de la plantilla
$(function () {
    $(".messages li").each(function (index) {
        if ($(this).hasClass("info")) {
            message_exito($(this).text(), "Info", "info");
        } else if ($(this).hasClass("error")) {
            message_exito($(this).text(), "Error", "error");
        } else {
            message_exito($(this).text(), "Éxito", "success");
        }
    });
});

function message_exito(mensaje, info, icono) {
    Swal.fire({
        text: mensaje,
        title: info,
        icon: icono,
    });
}

function alertas_eliminar(def_eliminar) {
    $.confirm({
        title: "Atención!",
        theme: "modern",
        content:
            "¿Estas seguro de relizar esta acción? Esto no se podrá deshacer!",
        type: "blue",
        buttons: {
            info: {
                text: "Confirmar",
                btnClass: "btn-blue",
                action: function () {
                    def_eliminar();
                },
            },
            danger: {
                text: "Cancelar",
                btnClass: "btn-red any-other-class",
            },
        },
    });
}

function formatearNumero(numero, decimales = 0) {
    var num = numero.toFixed(decimales).split(".");
    num[0] = num[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return num.join(".");
}
