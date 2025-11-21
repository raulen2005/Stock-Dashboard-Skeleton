import reflex as rx
from app.states.auth_state import AuthState


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("trending-up", class_name="w-16 h-16 text-blue-600 mb-6"),
                rx.el.h1(
                    "StockDash",
                    class_name="text-5xl font-bold text-gray-900 mb-4 tracking-tight",
                ),
                rx.el.p(
                    "Professional Market Analytics Platform",
                    class_name="text-xl text-gray-600 mb-8 font-medium max-w-lg mx-auto text-center",
                ),
                rx.el.div(
                    rx.el.a(
                        "Get Started",
                        href="/dashboard",
                        class_name="inline-flex items-center px-8 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl mr-4",
                    ),
                    rx.el.a(
                        "Sign In",
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
                            "Real-time Data",
                            class_name="text-xl font-semibold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Access live stock prices and market data powered by Yahoo Finance",
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
                            "User Management",
                            class_name="text-xl font-semibold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Complete user administration with role-based access control",
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
                            "Advanced Charts",
                            class_name="text-xl font-semibold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Interactive charts and technical analysis tools for informed decisions",
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