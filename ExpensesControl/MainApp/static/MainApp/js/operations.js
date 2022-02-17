let operations = document.getElementsByName("operation");
var amount_tr = document.getElementById("amount_tr");
var select = null;

// Формируем: id операции: сумма операции
let amount_data = {};
for (var i = 0; i < operations.length; i++) {
    amount_data[operations[i].id] = operations[i].cells["amount"].innerHTML;
}

function SelectOperation () {
    if (select == this) {
        this.className = "table-light";
        select = null;
        amount_tr.innerHTML = "Сумма, ₽";
        
        let amount_list = document.getElementsByName("amount");
        for (var i = 0; i < amount_list.length; i++) {
            amount_list[i].innerHTML = amount_data[amount_list[i].parentElement.id];
        }
    }
    else {
        if (select) {
            select.className = "table-light";
        }
        this.className = "spinner-border-sm border-warning";
        select = this
        amount_tr.innerHTML = "Сумма, отн.";

        // Изменяем значения у операций, относительно выбранной операции
        var select_amount = amount_data[this.id];
        let amount_list = document.getElementsByName("amount");
        for (var i = 0; i < amount_list.length; i++) {
            amount_list[i].innerHTML = (amount_data[amount_list[i].parentElement.id] / Math.abs(select_amount)).toFixed(2);
        }
    }
}

for (var i in operations) {
    operations[i].onclick = SelectOperation;
}