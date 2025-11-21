import reflex as rx
from app.states.market_state import MarketState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E5E7EB",
        "borderRadius": "0.5rem",
        "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "padding": "12px",
    },
    "item_style": {"fontSize": "12px", "fontWeight": "500", "color": "#1F2937"},
    "label_style": {"color": "#6B7280", "marginBottom": "8px", "fontSize": "11px"},
    "separator": " : ",
}


def stock_composed_chart() -> rx.Component:
    return rx.recharts.composed_chart(
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3", vertical=False, stroke="#E5E7EB"
        ),
        rx.recharts.graphing_tooltip(
            **TOOLTIP_PROPS,
            cursor={"stroke": "#6B7280", "strokeWidth": 1, "strokeDasharray": "4 4"},
        ),
        rx.recharts.x_axis(
            data_key="date",
            axis_line=False,
            tick_line=False,
            tick={"fontSize": 12, "fill": "#9CA3AF"},
            min_tick_gap=30,
        ),
        rx.recharts.y_axis(
            y_axis_id="left",
            orientation="left",
            axis_line=False,
            tick_line=False,
            tick={"fontSize": 10, "fill": "#9CA3AF"},
            width=40,
            domain=["auto", "auto"],
        ),
        rx.recharts.y_axis(
            y_axis_id="right",
            orientation="right",
            axis_line=False,
            tick_line=False,
            tick={"fontSize": 12, "fill": "#9CA3AF"},
            domain=["auto", "auto"],
            allow_decimals=True,
        ),
        rx.recharts.area(
            data_key="price",
            y_axis_id="right",
            name="Cierre",
            type_="monotone",
            stroke="#3B82F6",
            stroke_width=2,
            fill_opacity=0.1,
            fill="#3B82F6",
            animation_duration=1000,
        ),
        rx.recharts.bar(
            data_key="volume",
            y_axis_id="left",
            name="Volumen",
            bar_size=20,
            fill="#E5E7EB",
        ),
        rx.recharts.line(
            data_key="open",
            name="Apertura",
            y_axis_id="right",
            stroke="transparent",
            stroke_width=0,
            dot=False,
            active_dot=False,
        ),
        rx.recharts.line(
            data_key="high",
            name="Máximo",
            y_axis_id="right",
            stroke="transparent",
            stroke_width=0,
            dot=False,
            active_dot=False,
        ),
        rx.recharts.line(
            data_key="low",
            name="Mínimo",
            y_axis_id="right",
            stroke="transparent",
            stroke_width=0,
            dot=False,
            active_dot=False,
        ),
        rx.foreach(
            MarketState.comparison_symbols,
            lambda sym, i: rx.recharts.line(
                data_key=sym,
                y_axis_id="right",
                name=sym,
                type_="monotone",
                stroke=MarketState.colors[i % 5],
                stroke_width=2,
                dot=False,
            ),
        ),
        data=MarketState.stock_data,
        width="100%",
        height=350,
    )