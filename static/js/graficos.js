$(function () {
    const fecha_actual = new Date()
    const año = fecha_actual.getFullYear()

    function calcular_total_mes(orden) {
        let total_ordenes = 0
        $.each(totalMesesOrdenesVentas, function (index, mes) {
            total_ordenes += mes
        })
        return formatearNumero(total_ordenes)
    }
    
    const chart = Highcharts.chart('container', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Ventas para el año ' + año,
            align: 'right'
        },
        subtitle: {
            text:
                calcular_total_mes(totalMesesOrdenesVentas),
            align: 'right',
        },
        xAxis: {
            categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total ventas mensuales (TVM)'
            }
        },
        // tooltip: {
        //     valueSuffix: ' (1000 MT)'
        // },
        // plotOptions: {
        //     column: {
        //         pointPadding: 0.2,
        //         borderWidth: 0
        //     }
        // },
        series: [
            {
                name: 'Ventas',
                data: totalMesesOrdenesVentas
            },
        ]
    });
})