import reflex as rx
from app.components.layout import dashboard_layout


def settings_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.h1(
                "Configuración", class_name="text-2xl font-bold text-gray-900 mb-6"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Configuración de Perfil",
                        class_name="text-lg font-semibold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Nombre para Mostrar",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(class_name="w-full p-2 border rounded-md"),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Correo Electrónico",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                class_name="w-full p-2 border rounded-md",
                                disabled=True,
                                default_value="user@example.com",
                                key="user@example.com",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.button(
                            "Guardar Cambios",
                            class_name="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 font-medium text-sm transition-colors",
                        ),
                        class_name="max-w-md",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Notificaciones",
                        class_name="text-lg font-semibold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(type="checkbox", class_name="mr-2"),
                            "Notificaciones por Correo",
                            class_name="flex items-center mb-2 text-gray-700",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="checkbox", class_name="mr-2", default_checked=True
                            ),
                            "Alertas de Mercado",
                            class_name="flex items-center mb-2 text-gray-700",
                        ),
                        class_name="max-w-md",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
                ),
                class_name="flex flex-col gap-6",
            ),
            class_name="w-full",
        )
    )