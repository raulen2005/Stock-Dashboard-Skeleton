import reflex as rx
from app.components.layout import dashboard_layout
from app.states.market_state import MarketState
from app.components.charts import stock_composed_chart


def stat_card(title: str, value: str, change: str, is_positive: bool) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500 mb-1"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.span(
                change,
                class_name=rx.cond(
                    is_positive,
                    "bg-green-100 text-green-700 px-2.5 py-0.5 rounded-full text-xs font-medium",
                    "bg-red-100 text-red-700 px-2.5 py-0.5 rounded-full text-xs font-medium",
                ),
            ),
            class_name="mt-2",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow",
    )


def watchlist_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(item["symbol"], class_name="font-bold text-gray-900"),
            rx.el.div(
                rx.el.span(
                    "$" + item["price"].to(str),
                    class_name="text-sm font-medium text-gray-900 mr-2",
                ),
                rx.el.span(
                    item["change_percent"].to(str) + "%",
                    class_name=rx.cond(
                        item["is_positive"],
                        "text-xs font-medium text-green-600",
                        "text-xs font-medium text-red-600",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center w-full",
        ),
        on_click=MarketState.select_stock(item["symbol"]),
        class_name="p-4 hover:bg-gray-50 border-b border-gray-100 last:border-0 cursor-pointer transition-colors",
    )


def dashboard_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.div(
                stat_card("Valor del Portafolio", "$124,592.00", "+12.5%", True),
                stat_card("Beneficio Total", "$24,500.20", "+8.2%", True),
                stat_card("Ganancia Hoy", "-$1,203.00", "-1.2%", False),
                stat_card("Posiciones Activas", "12", "0", True),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Resumen de Mercado",
                            class_name="text-lg font-bold text-gray-800",
                        ),
                        rx.el.select(
                            rx.foreach(
                                MarketState.available_symbols,
                                lambda sym: rx.el.option(sym, value=sym),
                            ),
                            value=MarketState.selected_ticker,
                            on_change=MarketState.select_stock,
                            class_name="text-sm border-gray-200 rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2 bg-white border outline-none cursor-pointer min-w-[120px]",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.cond(
                        MarketState.is_loading,
                        rx.el.div(
                            rx.el.div(
                                class_name="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"
                            ),
                            class_name="w-full h-80 flex items-center justify-center bg-gray-50 rounded-xl",
                        ),
                        stock_composed_chart(),
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200 col-span-2",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Lista de Seguimiento",
                        class_name="text-lg font-bold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.cond(
                            MarketState.watchlist_data.length() > 0,
                            rx.foreach(MarketState.watchlist_data, watchlist_item),
                            rx.el.div(
                                "Sin acciones en la lista",
                                class_name="text-gray-400 text-center py-8 text-sm",
                            ),
                        ),
                        class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
            ),
            class_name="w-full animate-fade-in",
        )
    )