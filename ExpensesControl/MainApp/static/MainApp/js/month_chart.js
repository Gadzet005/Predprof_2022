var month_data = JSON.parse(document.getElementById('month_data').textContent);
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

function drawChart() {
    let lst = [['Месяц', 'Доход', "Расход"]]
    for (var month in month_data) {
        lst.push([month, month_data[month][0], month_data[month][1]])
    }

    var data = google.visualization.arrayToDataTable(lst);
    var options = {
    title: 'Доходы и расходы за полгода',
    hAxis: {title: 'Период'},
    vAxis: {title: 'Рубль'},
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('month_data_chart'));
    chart.draw(data, options);
}