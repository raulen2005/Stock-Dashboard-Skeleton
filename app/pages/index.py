import reflex as rx
from app.states.auth_state import AuthState


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("trending-up", class_name="w-16 h-16 text-blue-600 mb-6"),
                rx.el.h1(
                    "Mara",
                    class_name="text-5xl font-bold text-gray-900 mb-4 tracking-tight",
                ),
                rx.el.p(
                    "Plataforma Profesional de Análisis de Mercado",
                    class_name="text-xl text-gray-600 mb-8 font-medium max-w-lg mx-auto text-center",
                ),
                rx.el.div(
                    rx.el.a(
                        "Comenzar",
                        href="/dashboard",
                        class_name="inline-flex items-center px-8 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl mr-4",
                    ),
                    rx.el.a(
                        "Iniciar Sesión",
                        href="/",
                        class_name="inline-flex items-center px-8 py-3 bg-white text-gray-700 font-semibold rounded-xl border border-gray-200 hover:bg-gray-50 transition-all duration-200",
                    ),
                    class_name="flex flex-col sm:flex-row gap-4 justify-center items-center",
                ),
                class_name="text-center max-w-4xl mx-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "bar-chart-3", class_name="w-12 h-12 text-blue-600 mb-4"
                        ),
                        rx.el.h3(
                            "Datos en Tiempo Real",
                            class_name="text-xl font-semibold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Acceda a precios de acciones en vivo y datos de mercado impulsados por Yahoo Finance",
                            class_name="text-gray-600",
                        ),
                        class_name="text-center p-8 bg-white rounded-2xl shadow-sm border border-gray-100",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("users", class_name="w-12 h-12 text-green-600 mb-4"),
                        rx.el.h3(
                            "Gestión de Usuarios",
                            class_name="text-xl font-semibold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Administración completa de usuarios con control de acceso basado en roles",
                            class_name="text-gray-600",
                        ),
                        class_name="text-center p-8 bg-white rounded-2xl shadow-sm border border-gray-100",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "line-chart", class_name="w-12 h-12 text-purple-600 mb-4"
                        ),
                        rx.el.h3(
                            "Gráficos Avanzados",
                            class_name="text-xl font-semibold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Gráficos interactivos y herramientas de análisis técnico para decisiones informadas",
                            class_name="text-gray-600",
                        ),
                        class_name="text-center p-8 bg-white rounded-2xl shadow-sm border border-gray-100",
                    ),
                    class_name="w-full",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto mt-16",
            ),
            class_name="min-h-screen flex flex-col justify-center items-center px-4 py-16",
        ),
        class_name="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 font-['Raleway'] relative overflow-hidden",
    )