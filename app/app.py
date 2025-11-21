import reflex as rx
from app.pages.index import index
from app.pages.auth_pages import login_page, register_page
from app.pages.dashboard import dashboard_page
from app.pages.users import users_page
from app.pages.settings import settings_page
from app.pages.profile import profile_page
from app.pages.market import market_page
from app.states.auth_state import AuthState
from app.states.market_state import MarketState

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/animations.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/home")
app.add_page(login_page, route="/", on_load=AuthState.check_public)
app.add_page(register_page, route="/register", on_load=AuthState.check_public)
app.add_page(
    dashboard_page,
    route="/dashboard",
    on_load=[AuthState.check_login, MarketState.on_mount],
)
app.add_page(users_page, route="/users", on_load=AuthState.check_login)
app.add_page(settings_page, route="/settings", on_load=AuthState.check_login)
app.add_page(profile_page, route="/profile", on_load=AuthState.check_login)
app.add_page(
    market_page, route="/market", on_load=[AuthState.check_login, MarketState.on_mount]
)