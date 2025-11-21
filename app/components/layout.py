import reflex as rx
from app.components.navbar import navbar
from app.components.sidebar import sidebar


def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            navbar(),
            sidebar(),
            rx.el.main(
                content,
                class_name="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 animate-fade-in flex-1",
            ),
            class_name="flex-1 flex flex-col min-h-screen w-full transition-all duration-200",
        ),
        class_name="min-h-screen bg-gray-50 font-['Raleway'] flex flex-col",
    )