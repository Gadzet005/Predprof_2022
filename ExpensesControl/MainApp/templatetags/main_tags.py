from django import template

register = template.Library()

"""
    0 - Неавторизован;
    1 - Авторизован;
"""

main_menu = [
        {"title": "Главная", "url_name": "home", "access_levels": [0, 1]}, 

        {"title": "Операции", "url_name": "operations", "access_levels": [1]}, 
        
        {"title": "Вход/Регистрация", "access_levels": [0],
         "submenu": [{"title": "Вход", "access_levels": [0], "url_name": "login"},
                     {"title": "Регистрация", "access_levels": [0], "url_name": "register"}
         ]},

        {"title": "Личный кабинет", "access_levels": [1],
         "submenu": [{"title": "Редактировать данные", "access_levels": [1], "url_name": "edit_user_data"},
                     {"title": "Изменить пароль", "access_levels": [1], "url_name": "change_password"},
                     {"title": "Выход", "access_levels": [1], "url_name": "logout"}]
         },
    ]

@register.inclusion_tag('MainApp/main_menu.html')
def show_main_menu(request, title):
    access_level = 0
    if request.user.is_authenticated:
        access_level = 1

    # Формирование главного меню (зависит от уровня доступа пользователя)
    user_menu = []
    for elem in main_menu:
        if access_level in elem["access_levels"]:
            # Выбран ли элемент меню
            if title == elem["title"]:
                elem["selected"] = True
            else:
                elem["selected"] = False
            # Формирование выпадающих элементов
            if "submenu" in elem:
                submenu = []
                for sub_elem in elem["submenu"]:
                    if access_level in sub_elem["access_levels"]:
                        submenu.append(sub_elem)
                        if title == sub_elem["title"]:
                            elem["selected"] = True
                elem["submenu"] = submenu
            
            user_menu.append(elem)
            
    return {"main_menu": user_menu}