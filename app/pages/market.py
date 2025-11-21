import reflex as rx
from app.components.layout import dashboard_layout
from app.states.market_state import MarketState
from app.components.charts import stock_composed_chart


def search_box() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2",
            ),
            rx.el.input(
                placeholder="Buscar símbolo (ej. AAPL)...",
                on_change=MarketState.set_search_query,
                class_name="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-shadow shadow-sm",
                default_value=MarketState.search_query,
            ),
            rx.cond(
                MarketState.search_results.length() > 0,
                rx.el.div(
                    rx.foreach(
                        MarketState.search_results,
                        lambda item: rx.el.button(
                            rx.el.div(
                                rx.el.span(
                                    item["symbol"],
                                    class_name="font-bold text-gray-900 w-16 text-left",
                                ),
                                rx.el.span(
                                    item["name"],
                                    class_name="text-gray-600 text-sm truncate",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.span(
                                item["sector"],
                                class_name="text-xs text-gray-400 bg-gray-50 px-2 py-1 rounded-md",
                            ),
                            on_click=MarketState.select_stock(item["symbol"]),
                            class_name="flex items-center justify-between w-full px-4 py-3 hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-0",
                        ),
                    ),
                    class_name="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50",
                ),
                rx.fragment(),
            ),
            class_name="relative max-w-xl w-full mx-auto mb-8",
        ),
        class_name="w-full",
    )


def market_stat_item(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-xs font-medium text-gray-500 uppercase tracking-wider mb-1",
        ),
        rx.el.p(value, class_name="text-lg font-semibold text-gray-900"),
        class_name="bg-gray-50 p-4 rounded-xl border border-gray-100",
    )


def time_range_button(label: str, range_value: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=MarketState.set_time_range(range_value),
        class_name=rx.cond(
            MarketState.time_range == range_value,
            "px-3 py-1.5 text-sm font-medium rounded-lg bg-blue-600 text-white shadow-sm transition-all",
            "px-3 py-1.5 text-sm font-medium rounded-lg text-gray-600 hover:bg-gray-100 transition-all",
        ),
    )


def market_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            search_box(),
            rx.cond(
                MarketState.error_message != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="w-5 h-5 mr-2"),
                    rx.el.span(MarketState.error_message),
                    class_name="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 mb-6 flex items-center",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h1(
                                MarketState.selected_ticker,
                                class_name="text-4xl font-bold text-gray-900 tracking-tight",
                            ),
                            rx.el.span(
                                MarketState.current_company_name,
                                class_name="text-lg text-gray-500 font-medium ml-3",
                            ),
                            class_name="flex items-baseline",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "$" + MarketState.current_price.to(str),
                                class_name="text-3xl font-bold text-gray-900 mr-3",
                            ),
                            rx.el.span(
                                MarketState.price_change.to(str)
                                + " ("
                                + MarketState.price_change_percent.to(str)
                                + "%)",
                                class_name=rx.cond(
                                    MarketState.is_positive_change,
                                    "text-green-600 font-semibold bg-green-50 px-2 py-1 rounded-lg",
                                    "text-red-600 font-semibold bg-red-50 px-2 py-1 rounded-lg",
                                ),
                            ),
                            class_name="flex items-center mt-2",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("star", class_name="w-5 h-5 mr-2"),
                            rx.cond(
                                MarketState.watchlist.contains(
                                    MarketState.selected_ticker
                                ),
                                "Siguiendo",
                                "Añadir a Lista",
                            ),
                            on_click=rx.cond(
                                MarketState.watchlist.contains(
                                    MarketState.selected_ticker
                                ),
                                MarketState.remove_from_watchlist(
                                    MarketState.selected_ticker
                                ),
                                MarketState.add_to_watchlist,
                            ),
                            class_name=rx.cond(
                                MarketState.watchlist.contains(
                                    MarketState.selected_ticker
                                ),
                                "flex items-center px-4 py-2 bg-yellow-50 text-yellow-700 border border-yellow-200 rounded-lg font-medium transition-colors",
                                "flex items-center px-4 py-2 bg-white text-gray-700 border border-gray-200 rounded-lg hover:bg-gray-50 font-medium transition-colors shadow-sm",
                            ),
                        ),
                        class_name="flex items-center mt-4 md:mt-0",
                    ),
                    class_name="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Historial de Precios",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.div(
                            time_range_button("1D", "1d"),
                            time_range_button("5D", "5d"),
                            time_range_button("1M", "1mo"),
                            time_range_button("6M", "6mo"),
                            time_range_button("1A", "1y"),
                            time_range_button("MAX", "max"),
                            class_name="flex space-x-1 bg-gray-100 p-1 rounded-lg",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.cond(
                        MarketState.is_loading,
                        rx.el.div(
                            rx.el.div(
                                class_name="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"
                            ),
                            class_name="h-[350px] w-full flex items-center justify-center bg-gray-50 rounded-xl",
                        ),
                        stock_composed_chart(),
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Comparar con:",
                            class_name="text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                MarketState.available_symbols,
                                lambda sym: rx.cond(
                                    sym != MarketState.selected_ticker,
                                    rx.el.button(
                                        sym,
                                        on_click=lambda: MarketState.toggle_comparison(
                                            sym
                                        ),
                                        class_name=rx.cond(
                                            MarketState.comparison_symbols.contains(
                                                sym
                                            ),
                                            "px-2 py-1 text-xs bg-blue-600 text-white rounded-full border border-blue-600 transition-colors",
                                            "px-2 py-1 text-xs bg-white text-gray-600 rounded-full border border-gray-200 hover:border-blue-400 transition-colors",
                                        ),
                                    ),
                                    rx.fragment(),
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="mt-6 pt-6 border-t border-gray-100",
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 mb-8",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Estadísticas Clave",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        market_stat_item(
                            "Cierre Anterior",
                            "$" + MarketState.stock_info["previousClose"].to(str),
                        ),
                        market_stat_item(
                            "Apertura", "$" + MarketState.stock_info["open"].to(str)
                        ),
                        market_stat_item(
                            "Rango Día",
                            "$"
                            + MarketState.stock_info["dayLow"].to(str)
                            + " - $"
                            + MarketState.stock_info["dayHigh"].to(str),
                        ),
                        market_stat_item(
                            "Volumen", MarketState.stock_info["volume"].to(str)
                        ),
                        market_stat_item(
                            "Cap. Mercado",
                            "$" + MarketState.stock_info["marketCap"].to(str),
                        ),
                        market_stat_item(
                            "Ratio P/E", MarketState.stock_info["trailingPE"].to(str)
                        ),
                        class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4",
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 mb-8",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Sobre la Empresa",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.p(
                        MarketState.stock_info["longBusinessSummary"],
                        class_name="text-gray-600 leading-relaxed",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Sector:", class_name="font-semibold text-gray-900 mr-2"
                            ),
                            rx.el.span(
                                MarketState.stock_info["sector"],
                                class_name="text-gray-600",
                            ),
                            class_name="mr-6",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Industria:",
                                class_name="font-semibold text-gray-900 mr-2",
                            ),
                            rx.el.span(
                                MarketState.stock_info["industry"],
                                class_name="text-gray-600",
                            ),
                        ),
                        class_name="flex mt-4 text-sm border-t border-gray-100 pt-4",
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
                ),
                class_name="w-full animate-fade-in",
            ),
            class_name="w-full max-w-7xl mx-auto",
        )
    )