import reflex as rx
from reflex_google_auth import google_login, google_oauth_provider
from app.states.auth_state import AuthState

CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID_PLACEHOLDER"


def auth_layout(content: rx.Component) -> rx.Component:
    return google_oauth_provider(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("trending-up", class_name="w-10 h-10 text-blue-600 mb-4"),
                    rx.el.h1(
                        "StockDash", class_name="text-3xl font-bold text-gray-900 mb-2"
                    ),
                    rx.el.p(
                        "Professional Market Analytics",
                        class_name="text-gray-500 mb-8 font-medium",
                    ),
                    content,
                    class_name="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 w-full max-w-md flex flex-col items-center",
                ),
                class_name="flex flex-col items-center justify-center w-full max-w-md px-4",
            ),
            class_name="min-h-screen w-full flex items-center justify-center bg-slate-50 font-['Raleway'] relative overflow-hidden",
        ),
        client_id=CLIENT_ID,
    )


def login_page() -> rx.Component:
    return auth_layout(
        rx.el.div(
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="w-5 h-5 mr-2"),
                    rx.el.span(AuthState.error_message),
                    class_name="bg-red-50 text-red-600 p-3 rounded-lg text-sm flex items-center w-full mb-6 border border-red-100",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    placeholder="you@company.com",
                    on_change=AuthState.set_email,
                    class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-900 placeholder-gray-400",
                    default_value=AuthState.email,
                ),
                class_name="w-full mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    type="password",
                    placeholder="••••••••",
                    on_change=AuthState.set_password,
                    class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-900 placeholder-gray-400",
                    default_value=AuthState.password,
                ),
                class_name="w-full mb-6",
            ),
            rx.el.button(
                rx.cond(
                    AuthState.is_loading,
                    rx.el.div(
                        class_name="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mx-auto"
                    ),
                    "Sign In",
                ),
                on_click=AuthState.login,
                disabled=AuthState.is_loading,
                class_name="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all shadow-md hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed mb-4",
            ),
            rx.el.div(
                rx.el.div(class_name="h-px bg-gray-200 w-full"),
                rx.el.span(
                    "or",
                    class_name="text-xs text-gray-400 uppercase px-2 bg-white relative z-10",
                ),
                rx.el.div(class_name="h-px bg-gray-200 w-full"),
                class_name="flex items-center justify-between w-full my-4",
            ),
            rx.el.div(
                google_login(on_success=AuthState.handle_google_login),
                class_name="w-full flex justify-center mb-6",
            ),
            rx.el.div(
                "Don't have an account? ",
                rx.el.a(
                    "Create account",
                    href="/register",
                    class_name="text-blue-600 hover:text-blue-700 font-semibold hover:underline",
                ),
                class_name="text-sm text-gray-600 text-center w-full",
            ),
            class_name="w-full",
        )
    )


def register_page() -> rx.Component:
    return auth_layout(
        rx.el.div(
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="w-5 h-5 mr-2"),
                    rx.el.span(AuthState.error_message),
                    class_name="bg-red-50 text-red-600 p-3 rounded-lg text-sm flex items-center w-full mb-6 border border-red-100",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.label(
                    "Full Name",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    placeholder="John Doe",
                    on_change=AuthState.set_full_name,
                    class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-900 placeholder-gray-400",
                    default_value=AuthState.full_name,
                ),
                class_name="w-full mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    placeholder="you@company.com",
                    on_change=AuthState.set_email,
                    class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-900 placeholder-gray-400",
                    default_value=AuthState.email,
                ),
                class_name="w-full mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    type="password",
                    placeholder="••••••••",
                    on_change=AuthState.set_password,
                    class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-900 placeholder-gray-400",
                    default_value=AuthState.password,
                ),
                class_name="w-full mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Confirm Password",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    type="password",
                    placeholder="••••••••",
                    on_change=AuthState.set_confirm_password,
                    class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-900 placeholder-gray-400",
                    default_value=AuthState.confirm_password,
                ),
                class_name="w-full mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Role", class_name="block text-sm font-medium text-gray-700 mb-1.5"
                ),
                rx.el.select(
                    rx.el.option("Trader", value="Trader"),
                    rx.el.option("Admin", value="Admin"),
                    rx.el.option("Viewer", value="Viewer"),
                    value=AuthState.registration_role,
                    on_change=AuthState.set_registration_role,
                    class_name="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-900 cursor-pointer",
                ),
                class_name="w-full mb-6",
            ),
            rx.el.button(
                rx.cond(
                    AuthState.is_loading,
                    rx.el.div(
                        class_name="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mx-auto"
                    ),
                    "Create Account",
                ),
                on_click=AuthState.register,
                disabled=AuthState.is_loading,
                class_name="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all shadow-md hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed mb-4",
            ),
            rx.el.div(
                rx.el.div(class_name="h-px bg-gray-200 w-full"),
                rx.el.span(
                    "or",
                    class_name="text-xs text-gray-400 uppercase px-2 bg-white relative z-10",
                ),
                rx.el.div(class_name="h-px bg-gray-200 w-full"),
                class_name="flex items-center justify-between w-full my-4",
            ),
            rx.el.div(
                google_login(on_success=AuthState.handle_google_login),
                class_name="w-full flex justify-center mb-6",
            ),
            rx.el.div(
                "Already have an account? ",
                rx.el.a(
                    "Sign In",
                    href="/",
                    class_name="text-blue-600 hover:text-blue-700 font-semibold hover:underline",
                ),
                class_name="text-sm text-gray-600 text-center w-full",
            ),
            class_name="w-full",
        )
    )