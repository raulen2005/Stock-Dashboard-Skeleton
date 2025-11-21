import reflex as rx
from app.components.layout import dashboard_layout
from app.states.user_state import UserState, User


def user_modal() -> rx.Component:
    return rx.cond(
        UserState.is_modal_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/50 backdrop-blur-sm transition-opacity",
                on_click=UserState.close_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            rx.cond(
                                UserState.current_user_id,
                                "Editar Usuario",
                                "Añadir Usuario",
                            ),
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        class_name="px-6 py-4 border-b border-gray-100 flex-shrink-0",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Nombre Completo",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                on_change=UserState.set_form_name,
                                placeholder="Juan Pérez",
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all",
                                default_value=UserState.form_name,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Correo Electrónico",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                on_change=UserState.set_form_email,
                                placeholder="juan@ejemplo.com",
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all",
                                default_value=UserState.form_email,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Rol",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.select(
                                    rx.el.option(
                                        "Administrador", value="Administrador"
                                    ),
                                    rx.el.option("Operador", value="Operador"),
                                    rx.el.option("Espectador", value="Espectador"),
                                    value=UserState.form_role,
                                    on_change=UserState.set_form_role,
                                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all",
                                ),
                                class_name="w-1/2 pr-2",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Estado",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.select(
                                    rx.el.option("Activo", value="Activo"),
                                    rx.el.option("Inactivo", value="Inactivo"),
                                    value=UserState.form_status,
                                    on_change=UserState.set_form_status,
                                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all",
                                ),
                                class_name="w-1/2 pl-2",
                            ),
                            class_name="flex mb-2",
                        ),
                        class_name="p-6 overflow-y-auto flex-1",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            on_click=UserState.close_modal,
                            class_name="px-4 py-2 text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg font-medium transition-colors mr-3 shadow-sm",
                        ),
                        rx.el.button(
                            rx.cond(
                                UserState.is_loading,
                                rx.el.div(
                                    class_name="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"
                                ),
                                "Guardar",
                            ),
                            disabled=UserState.is_loading,
                            on_click=UserState.save_user,
                            class_name="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center min-w-[100px] shadow-sm",
                        ),
                        class_name="flex justify-end px-6 py-4 bg-gray-50 border-t border-gray-100 rounded-b-xl flex-shrink-0",
                    ),
                    class_name="bg-white rounded-xl shadow-2xl w-full max-w-md relative z-10 animate-scale-up flex flex-col max-h-[85vh]",
                ),
                class_name="flex items-center justify-center min-h-screen p-4",
            ),
            class_name="fixed inset-0 z-[100] overflow-y-auto",
        ),
        rx.fragment(),
    )


def user_row(user: User) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src="https://api.dicebear.com/9.x/initials/svg?seed="
                    + user["avatar_seed"],
                    class_name="w-10 h-10 rounded-full bg-gray-100",
                ),
                rx.el.div(
                    rx.el.div(
                        user["name"], class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.div(user["email"], class_name="text-sm text-gray-500"),
                    class_name="ml-4",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                user["role"],
                class_name=rx.match(
                    user["role"],
                    (
                        "Administrador",
                        "px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800",
                    ),
                    (
                        "Operador",
                        "px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800",
                    ),
                    (
                        "Espectador",
                        "px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800",
                    ),
                    "px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                user["status"],
                class_name=rx.cond(
                    user["status"] == "Activo",
                    "px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
                    "px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            user["joined_date"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: UserState.open_edit_modal(user),
                    class_name="text-blue-600 hover:text-blue-900 p-2 hover:bg-blue-50 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: UserState.delete_user(user["id"]),
                    class_name="text-red-600 hover:text-red-900 p-2 hover:bg-red-50 rounded-lg transition-colors ml-2",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors",
    )


def users_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            user_modal(),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Gestión de Usuarios",
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Administre los miembros de su equipo y sus permisos.",
                        class_name="text-gray-500 mt-1 text-sm",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.span(
                        f"Total Usuarios: {UserState.total_users}",
                        class_name="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-xs font-medium border border-blue-100 mr-3",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-4 h-4 mr-2"),
                        "Añadir Usuario",
                        on_click=UserState.open_add_modal,
                        class_name="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm transition-colors shadow-sm hover:shadow",
                    ),
                    class_name="flex items-center mt-4 sm:mt-0",
                ),
                class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2",
                        ),
                        rx.el.input(
                            placeholder="Buscar usuarios...",
                            on_change=UserState.set_search_query.debounce(500),
                            class_name="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all",
                        ),
                        class_name="relative flex-1 min-w-[240px]",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Todos los Roles", value="Todos"),
                            rx.el.option("Administrador", value="Administrador"),
                            rx.el.option("Operador", value="Operador"),
                            rx.el.option("Espectador", value="Espectador"),
                            on_change=UserState.set_filter_role,
                            class_name="px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white text-gray-700 text-sm cursor-pointer hover:border-gray-300 transition-colors",
                        ),
                        rx.el.select(
                            rx.el.option("Todos los Estados", value="Todos"),
                            rx.el.option("Activo", value="Activo"),
                            rx.el.option("Inactivo", value="Inactivo"),
                            on_change=UserState.set_filter_status,
                            class_name="px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white text-gray-700 text-sm cursor-pointer hover:border-gray-300 transition-colors",
                        ),
                        class_name="flex gap-3",
                    ),
                    class_name="flex flex-col md:flex-row gap-4 mb-6 justify-between",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Usuario",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50/50",
                                ),
                                rx.el.th(
                                    "Rol",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50/50",
                                ),
                                rx.el.th(
                                    "Estado",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50/50",
                                ),
                                rx.el.th(
                                    "Fecha Ingreso",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50/50",
                                ),
                                rx.el.th(
                                    "Acciones",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50/50",
                                ),
                            ),
                            class_name="border-b border-gray-200",
                        ),
                        rx.el.tbody(
                            rx.foreach(UserState.filtered_users, user_row),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    rx.cond(
                        UserState.filtered_count == 0,
                        rx.el.div(
                            rx.icon("users", class_name="w-12 h-12 text-gray-300 mb-3"),
                            rx.el.h3(
                                "No se encontraron usuarios",
                                class_name="text-lg font-medium text-gray-900",
                            ),
                            rx.el.p(
                                "Intente ajustar su búsqueda o filtros.",
                                class_name="text-gray-500 mt-1",
                            ),
                            class_name="flex flex-col items-center justify-center py-12 bg-white",
                        ),
                        rx.fragment(),
                    ),
                    class_name="overflow-x-auto",
                ),
                class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden",
            ),
            class_name="w-full animate-fade-in",
        )
    )