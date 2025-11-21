import reflex as rx
from app.components.layout import dashboard_layout
from app.states.auth_state import AuthState


def profile_stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-6 h-6 {color}"),
            class_name="p-3 bg-gray-50 rounded-lg mb-4 w-fit",
        ),
        rx.el.h4(title, class_name="text-sm font-medium text-gray-500"),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow",
    )


def profile_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.h1("My Profile", class_name="text-2xl font-bold text-gray-900 mb-6"),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.email}",
                                class_name="w-24 h-24 rounded-full border-4 border-white shadow-lg mb-4",
                            ),
                            rx.el.h2(
                                rx.cond(
                                    AuthState.full_name,
                                    AuthState.full_name,
                                    "User Name",
                                ),
                                class_name="text-xl font-bold text-gray-900",
                            ),
                            rx.el.p(
                                AuthState.bio, class_name="text-gray-500 text-sm mt-1"
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Pro Member",
                                    class_name="px-3 py-1 bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-xs font-bold rounded-full mt-3 inline-block shadow-sm",
                                ),
                                class_name="flex justify-center",
                            ),
                            class_name="flex flex-col items-center text-center mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Email",
                                    class_name="text-xs font-medium text-gray-500 uppercase tracking-wide",
                                ),
                                rx.el.p(
                                    AuthState.email,
                                    class_name="text-sm font-medium text-gray-900 mt-1",
                                ),
                                class_name="py-3 border-b border-gray-100",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Role",
                                    class_name="text-xs font-medium text-gray-500 uppercase tracking-wide",
                                ),
                                rx.el.p(
                                    "Administrator",
                                    class_name="text-sm font-medium text-gray-900 mt-1",
                                ),
                                class_name="py-3 border-b border-gray-100",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Joined",
                                    class_name="text-xs font-medium text-gray-500 uppercase tracking-wide",
                                ),
                                rx.el.p(
                                    "October 24, 2023",
                                    class_name="text-sm font-medium text-gray-900 mt-1",
                                ),
                                class_name="py-3",
                            ),
                            class_name="w-full px-6 text-left",
                        ),
                        class_name="bg-white rounded-xl shadow-sm border border-gray-200 pt-8 pb-2 overflow-hidden",
                    ),
                    rx.el.div(
                        profile_stat_card(
                            "Total Trades", "1,245", "activity", "text-blue-600"
                        ),
                        profile_stat_card(
                            "Win Rate", "68.5%", "trophy", "text-yellow-500"
                        ),
                        class_name="grid grid-cols-2 gap-4 mt-6",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Edit Profile",
                                class_name="text-lg font-semibold text-gray-900",
                            ),
                            rx.el.p(
                                "Update your personal information",
                                class_name="text-sm text-gray-500 mt-1",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Full Name",
                                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                                ),
                                rx.el.input(
                                    on_change=AuthState.set_full_name,
                                    class_name="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all",
                                    default_value=AuthState.full_name,
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Bio",
                                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                                ),
                                rx.el.textarea(
                                    on_change=AuthState.set_bio,
                                    rows="3",
                                    class_name="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none",
                                    default_value=AuthState.bio,
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Phone Number",
                                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                                ),
                                rx.el.input(
                                    on_change=AuthState.set_phone,
                                    class_name="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all",
                                    default_value=AuthState.phone,
                                ),
                                class_name="mb-6",
                            ),
                            class_name="border-b border-gray-100 pb-6 mb-6",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Preferences",
                                class_name="text-lg font-semibold text-gray-900 mb-4",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.h5(
                                            "Email Notifications",
                                            class_name="text-sm font-medium text-gray-900",
                                        ),
                                        rx.el.p(
                                            "Receive daily market summaries",
                                            class_name="text-xs text-gray-500 mt-0.5",
                                        ),
                                    ),
                                    rx.el.input(
                                        type="checkbox",
                                        checked=AuthState.notifications_enabled,
                                        on_change=AuthState.toggle_notifications,
                                        class_name="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 cursor-pointer",
                                    ),
                                    class_name="flex justify-between items-center py-3 border-b border-gray-50",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.h5(
                                            "Market Alerts",
                                            class_name="text-sm font-medium text-gray-900",
                                        ),
                                        rx.el.p(
                                            "Get notified when stocks hit targets",
                                            class_name="text-xs text-gray-500 mt-0.5",
                                        ),
                                    ),
                                    rx.el.input(
                                        type="checkbox",
                                        checked=AuthState.market_alerts_enabled,
                                        on_change=AuthState.toggle_market_alerts,
                                        class_name="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 cursor-pointer",
                                    ),
                                    class_name="flex justify-between items-center py-3 border-b border-gray-50",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.h5(
                                            "Two-Factor Authentication",
                                            class_name="text-sm font-medium text-gray-900",
                                        ),
                                        rx.el.p(
                                            "Secure your account with 2FA",
                                            class_name="text-xs text-gray-500 mt-0.5",
                                        ),
                                    ),
                                    rx.el.input(
                                        type="checkbox",
                                        checked=AuthState.two_factor_enabled,
                                        on_change=AuthState.toggle_two_factor,
                                        class_name="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 cursor-pointer",
                                    ),
                                    class_name="flex justify-between items-center py-3",
                                ),
                                class_name="flex flex-col",
                            ),
                            class_name="mb-8",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.cond(
                                    AuthState.is_loading,
                                    rx.el.div(
                                        class_name="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"
                                    ),
                                    rx.icon("save", class_name="w-4 h-4 mr-2"),
                                ),
                                "Save Changes",
                                disabled=AuthState.is_loading,
                                on_click=AuthState.save_profile,
                                class_name="flex items-center justify-center px-6 py-2.5 bg-gray-900 text-white rounded-lg hover:bg-gray-800 font-medium transition-colors disabled:opacity-70",
                            ),
                            class_name="flex justify-end",
                        ),
                        class_name="bg-white p-8 rounded-xl shadow-sm border border-gray-200",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-[350px_1fr] gap-8",
            ),
            class_name="w-full animate-fade-in",
        )
    )