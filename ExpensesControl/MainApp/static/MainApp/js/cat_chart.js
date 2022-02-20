var cat_data = JSON.parse(document.getElementById('cat_data').textContent);
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

function drawChart() {

    let lst = [["Категории", "Процент"]]
    for (var i in cat_data) {
        lst.push([cat_data[i][0], cat_data[i][1]])
    }
    
    var data = google.visualization.arrayToDataTable(lst);
    var options = {
        title: 'Категории',
        is3D: false,
        pieResidueSliceLabel: 'Остальные'
    };
    var chart = new google.visualization.PieChart(document.getElementById('cat_chart'));
        chart.draw(data, options);
}