from django import template

register = template.Library()


def get_access_level(user):
    """
    0 - Неавторизован;
    1 - Авторизован;
    """

    if user.is_authenticated:
        return 1
    return 0


class MenuElem:
    def __init__(self, title: str, url_name: str, access_levels: list, 
        submenu: list=None, include: list=None):

        self.title = title
        self.url_name = url_name
        self.access_levels = access_levels
        self.submenu = submenu
        self.selected = False
    
    def can_see(self, access_level):
        return access_level in self.access_levels


def get_menu_data(menu_name):
    main_menu = [
            MenuElem("Главная", "home", [0, 1]), 
            MenuElem("Операции", "operations", [1]), 
            MenuElem("Категории", "categories", [1]),
            MenuElem("Вход/Регистрация", None, [0], [
                MenuElem("Вход", "login", [0]),
                MenuElem("Регистрация", "register", [0])
            ]),
            MenuElem("Личный кабинет", None, [1], [
                MenuElem("Редактировать данные", "edit_user_data", [1]), 
                MenuElem("Изменить пароль", "change_password", [1]),
                MenuElem("Выход", "logout", [1])
            ])
        ]

    operation_menu = [
        MenuElem("Расходы", "add_expense", [1]), 
        MenuElem("Доходы", "add_income", [1]), 
    ]

    menu_list = {
        "main_menu": main_menu, 
        "operation_menu": operation_menu
        }

    return menu_list[menu_name]


@register.inclusion_tag('MainApp/menu.html')
def get_menu(request, menu_name):
    # selected - принудительно ставит выбраным элемент в меню
    current_url_name = request.resolver_match.url_name
    access_level = get_access_level(request.user)

    # Формирование главного меню (зависит от уровня доступа пользователя)
    menu = []
    for elem in get_menu_data(menu_name):
        if elem.can_see(access_level):

            # Выбран ли элемент меню
            if current_url_name == elem.url_name:
                elem.selected = True

            # Формирование выпадающих элементов
            if elem.submenu:
                submenu = []
                for sub_elem in elem.submenu:
                    if sub_elem.can_see(access_level):
                        submenu.append(sub_elem)
                        if current_url_name == sub_elem.url_name:
                            elem.selected = True
                elem.submenu = submenu
            
            menu.append(elem)

    return {"menu": menu}