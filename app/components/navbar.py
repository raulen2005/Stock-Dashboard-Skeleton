import reflex as rx
from app.states.auth_state import AuthState


def nav_link(text: str, url: str, icon: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-4 h-4 mr-2.5"),
            rx.el.span(text),
            class_name="flex items-center",
        ),
        href=url,
        class_name="flex items-center px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200",
    )


def user_menu_item(
    text: str, icon: str, href: str = None, on_click: rx.event.EventType = None
) -> rx.Component:
    common_classes = "flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
    content = rx.el.div(
        rx.icon(icon, class_name="w-4 h-4 mr-3"), text, class_name="flex items-center"
    )
    if href:
        return rx.el.a(content, href=href, class_name=common_classes)
    else:
        return rx.el.button(content, on_click=on_click, class_name=common_classes)


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("trending-up", class_name="w-6 h-6 text-white"),
                        class_name="bg-blue-600 p-2 rounded-lg shadow-md mr-3",
                    ),
                    rx.el.span(
                        "Mara",
                        class_name="text-xl font-bold text-gray-900 tracking-tight",
                    ),
                    href="/dashboard",
                    class_name="flex items-center hover:opacity-90 transition-opacity flex-shrink-0 mr-8",
                ),
                rx.el.div(
                    nav_link("Panel", "/dashboard", "layout-dashboard"),
                    nav_link("Mercado", "/market", "bar-chart-2"),
                    nav_link("Usuarios", "/users", "users"),
                    nav_link("Configuración", "/settings", "settings"),
                    class_name="hidden md:flex items-center space-x-2",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                nav_link("Panel", "/dashboard", "layout-dashboard"),
                nav_link("Mercado", "/market", "bar-chart-2"),
                nav_link("Usuarios", "/users", "users"),
                nav_link("Configuración", "/settings", "settings"),
                class_name="flex md:hidden items-center space-x-1 overflow-x-auto no-scrollbar mask-fade-right mx-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", class_name="w-5 h-5 text-gray-500"),
                    rx.el.span(
                        class_name="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"
                    ),
                    class_name="relative p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 rounded-full transition-colors mr-2",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.image(
                            src="https://api.dicebear.com/9.x/initials/svg?seed="
                            + AuthState.email,
                            class_name="w-8 h-8 rounded-full border-2 border-white shadow-sm",
                        ),
                        rx.el.div(
                            rx.el.p(
                                rx.cond(
                                    AuthState.full_name, AuthState.full_name, "Usuario"
                                ),
                                class_name="text-sm font-semibold text-gray-700 leading-none",
                            ),
                            rx.el.p(
                                "Plan Pro",
                                class_name="text-xs text-blue-600 font-medium mt-0.5 text-left",
                            ),
                            class_name="hidden md:flex flex-col items-start ml-3 mr-2",
                        ),
                        rx.icon("chevron-down", class_name="w-4 h-4 text-gray-400"),
                        on_click=AuthState.toggle_profile_menu,
                        class_name="flex items-center pl-2 pr-1 py-1.5 rounded-full hover:bg-gray-50 transition-colors border border-transparent hover:border-gray-200",
                    ),
                    rx.cond(
                        AuthState.is_profile_menu_open,
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    "Iniciado como",
                                    class_name="text-xs text-gray-500 uppercase font-semibold tracking-wider mb-1",
                                ),
                                rx.el.div(
                                    AuthState.email,
                                    class_name="text-sm font-medium text-gray-900 truncate",
                                ),
                                rx.el.div(
                                    AuthState.user_role,
                                    class_name="text-xs text-blue-600 font-semibold mt-1",
                                ),
                                class_name="px-4 py-3 border-b border-gray-100 bg-gray-50/50",
                            ),
                            rx.el.div(
                                user_menu_item("Mi Perfil", "user", href="/profile"),
                                user_menu_item(
                                    "Configuración", "settings", href="/settings"
                                ),
                                user_menu_item("Facturación", "credit-card", href="#"),
                                class_name="py-1",
                            ),
                            rx.el.div(
                                user_menu_item(
                                    "Cerrar Sesión",
                                    "log-out",
                                    on_click=AuthState.logout,
                                ),
                                class_name="py-1 border-t border-gray-100",
                            ),
                            class_name="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-xl ring-1 ring-black ring-opacity-5 py-0 overflow-hidden animate-scale-up z-50 origin-top-right",
                        ),
                        rx.fragment(),
                    ),
                    class_name="relative ml-3",
                ),
                class_name="flex items-center ml-auto",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-20",
        ),
        class_name="bg-white border-b border-gray-200 sticky top-0 z-40",
    )