import reflex as rx
import asyncio


class AuthState(rx.State):
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    full_name: str = ""
    user_role: str = "Trader"
    registration_role: str = "Trader"
    is_loading: bool = False
    error_message: str = ""
    is_authenticated: bool = False

    @rx.event
    def set_email(self, value: str):
        self.email = value
        self.error_message = ""

    @rx.event
    def set_password(self, value: str):
        self.password = value
        self.error_message = ""

    @rx.event
    def set_confirm_password(self, value: str):
        self.confirm_password = value
        self.error_message = ""

    @rx.event
    def set_full_name(self, value: str):
        self.full_name = value
        self.error_message = ""

    @rx.event
    def set_registration_role(self, value: str):
        self.registration_role = value

    @rx.event
    def handle_google_login(self, data: dict):
        self.email = "google_user@example.com"
        self.full_name = "Usuario Google"
        self.user_role = "Operador"
        self.is_authenticated = True
        return rx.redirect("/dashboard")

    bio: str = "Analista de Mercado Senior & Operador"
    phone: str = "+1 (555) 123-4567"
    notifications_enabled: bool = True
    market_alerts_enabled: bool = False
    two_factor_enabled: bool = True

    @rx.event
    def set_bio(self, value: str):
        self.bio = value

    @rx.event
    def set_phone(self, value: str):
        self.phone = value

    @rx.event
    def toggle_notifications(self, value: bool):
        self.notifications_enabled = value

    @rx.event
    def toggle_market_alerts(self, value: bool):
        self.market_alerts_enabled = value

    @rx.event
    def toggle_two_factor(self, value: bool):
        self.two_factor_enabled = value

    is_profile_menu_open: bool = False

    @rx.event
    def toggle_profile_menu(self):
        self.is_profile_menu_open = not self.is_profile_menu_open

    @rx.event
    async def save_profile(self):
        self.is_loading = True
        await asyncio.sleep(1.0)
        self.is_loading = False

    @rx.event(background=True)
    async def login(self):
        async with self:
            self.is_loading = True
            self.error_message = ""
            if not self.email or not self.password:
                self.error_message = "Por favor complete todos los campos."
                self.is_loading = False
                return
            await asyncio.sleep(1.5)
            if self.email == "admin" and self.password == "admin":
                self.email = "admin@mara.com"
                self.full_name = "Administrador del Sistema"
                self.user_role = "Administrador"
                self.is_authenticated = True
                self.is_loading = False
            elif "error" in self.email:
                self.error_message = "Credenciales inválidas."
                self.is_loading = False
                return
            else:
                self.user_role = "Operador"
                self.is_authenticated = True
                self.is_loading = False
        if self.is_authenticated:
            yield rx.redirect("/dashboard")

    @rx.event(background=True)
    async def register(self):
        async with self:
            self.is_loading = True
            self.error_message = ""
            if (
                not self.email
                or not self.password
                or (not self.confirm_password)
                or (not self.full_name)
            ):
                self.error_message = "Todos los campos son obligatorios."
                self.is_loading = False
                return
            if self.password != self.confirm_password:
                self.error_message = "Las contraseñas no coinciden."
                self.is_loading = False
                return
            if len(self.password) < 6:
                self.error_message = "La contraseña debe tener al menos 6 caracteres."
                self.is_loading = False
                return
            await asyncio.sleep(1.5)
            self.user_role = self.registration_role
            self.is_authenticated = True
            self.is_loading = False
        yield rx.redirect("/dashboard")

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.email = ""
        self.password = ""
        self.full_name = ""
        return rx.redirect("/")

    @rx.event
    def check_login(self):
        if not self.is_authenticated:
            return rx.redirect("/")

    @rx.event
    def check_public(self):
        if self.is_authenticated:
            return rx.redirect("/dashboard")