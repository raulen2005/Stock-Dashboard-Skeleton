import reflex as rx
from app.states.market_state import MarketState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E5E7EB",
        "borderRadius": "0.5rem",
        "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "padding": "8px",
    },
    "item_style": {"fontSize": "12px", "fontWeight": "500", "color": "#1F2937"},
    "label_style": {"color": "#6B7280", "marginBottom": "4px", "fontSize": "11px"},
    "separator": "",
}


def stock_area_chart() -> rx.Component:
    return rx.recharts.area_chart(
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3", vertical=False, stroke="#E5E7EB"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.x_axis(
            data_key="date",
            axis_line=False,
            tick_line=False,
            tick={"fontSize": 12, "fill": "#9CA3AF"},
            min_tick_gap=30,
        ),
        rx.recharts.y_axis(
            domain=["auto", "auto"],
            orientation="right",
            axis_line=False,
            tick_line=False,
            tick={"fontSize": 12, "fill": "#9CA3AF"},
            allow_decimals=True,
        ),
        rx.recharts.area(
            type_="monotone",
            data_key="price",
            stroke="#3B82F6",
            stroke_width=2,
            fill_opacity=0.3,
            fill="#3B82F6",
            animation_duration=1000,
        ),
        data=MarketState.stock_data,
        width="100%",
        height=350,
    )