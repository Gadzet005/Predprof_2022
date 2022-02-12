var type_select = document.getElementById("type_select");
var cat_select = document.getElementById("cat_select");
let optionList = document.getElementById('cat_select').getElementsByTagName('option');
var categories = JSON.parse(document.getElementById('categories').textContent);

// Устанавливает категории в зависимости от типа
if (cat_select && type_select){
    function SortCategories(){
        for (i = 1; i < optionList.length; i++) {
            if (categories[optionList[i].value] == type_select.value) {
                optionList[i].setAttribute('style', 'display:block;')
            }
            else {
                optionList[i].setAttribute('style', 'display:none;')
            }
        }
    }

    SortCategories();

    type_select.addEventListener("change", SortCategories);
};