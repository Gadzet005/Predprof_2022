// Скрипт для получения суммы операции относительно выбранной базовой операции
let operations = document.getElementsByName("operation");
var amount_tr = document.getElementById("amount_tr");
var select = null;

var bal = document.getElementById("bal");
var bal_amount = bal.innerHTML
var bal_unit = document.getElementById("bal_unit");

// amount_data = {id операции: сумма операции, ...}
let amount_data = {};
for (var i = 0; i < operations.length; i++) {
    amount_data[operations[i].id] = operations[i].cells["amount"].innerHTML;
}

function SelectOperation () {
    if (select == this) {
        // Показываем абсолютную сумму
        this.className = "table-light";
        select = null;
        amount_tr.innerHTML = "Сумма, ₽";
        bal.innerHTML = bal_amount;
        bal_unit.innerHTML = "₽";
        
        let amount_list = document.getElementsByName("amount");
        for (var i = 0; i < amount_list.length; i++) {
            amount_list[i].innerHTML = amount_data[amount_list[i].parentElement.id];
        }
    }
    else {
        // Показываем относительную сумму
        if (select) {
            select.className = "table-light";
        }
        this.className = "spinner-border-sm border-warning";
        select = this
        amount_tr.innerHTML = "Сумма, отн.";

        // Изменяем значения у операций, относительно выбранной операции
        var select_amount = Math.abs(amount_data[this.id]);
        bal.innerHTML = (bal_amount / select_amount).toFixed(2);
        bal_unit.innerHTML = "отн.";
        let amount_list = document.getElementsByName("amount");
        for (var i = 0; i < amount_list.length; i++) {
            amount_list[i].innerHTML = (amount_data[amount_list[i].parentElement.id] / select_amount).toFixed(2);
        }
    }
}

for (var i in operations) {
    operations[i].onclick = SelectOperation;
}