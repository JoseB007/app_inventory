function tabla_de_registros(selector, url_language) {
    $(selector).DataTable({
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
                mostrar_datos: "mostrar",
            },
            dataSrc: "",
        },
        columns: [
            { data: "id" },
            { data: "username" },
            { data: "first_name" },
            { data: "last_name" },
            { data: "email" },
            { data: "groups" },
            { data: "is_superuser" },
            { data: "last_login" },
            { data: "date_joined" },
            { data: "id" },
        ],
        columnDefs: [
            {
                targets: [-1],
                render: function (data, type, row) {
                    var botones =
                        '<a class="btn btn-md" style="color: #007bff; padding-top:0; padding-bottom:0;" href="editar-usuario/' +
                        row.id +
                        '/"><i class="fa-solid fa-pen-to-square"></i></a>';
                    botones +=
                        '<a class="btn btn-md" style="color: #007bff; padding-top:0; padding-bottom:0;" href="eliminar-usuario/' +
                        row.id +
                        '/"><i class="fas fa-trash-alt"></i></a>';
                    return botones;
                },
            },
            {
                targets: [-5],
                render: function (data, type, row) {
                    var grupo = ""
                    $.each(row.groups, function (index, item) {
                        grupo += '<span class="badge badge-success">' + item + '</span>'
                    });
                    return grupo;
                },
            },
        ],
    });
}
