import reflex as rx
from typing import TypedDict, Optional
import asyncio
import random
import string
from datetime import datetime


class User(TypedDict):
    id: str
    name: str
    email: str
    role: str
    status: str
    joined_date: str
    avatar_seed: str


class UserState(rx.State):
    users: list[User] = [
        {
            "id": "USR-001",
            "name": "Alice Freeman",
            "email": "alice@example.com",
            "role": "Administrador",
            "status": "Activo",
            "joined_date": "2023-01-15",
            "avatar_seed": "Alice",
        },
        {
            "id": "USR-002",
            "name": "Bob Smith",
            "email": "bob@example.com",
            "role": "Operador",
            "status": "Activo",
            "joined_date": "2023-03-10",
            "avatar_seed": "Bob",
        },
        {
            "id": "USR-003",
            "name": "Charlie Davis",
            "email": "charlie@example.com",
            "role": "Espectador",
            "status": "Inactivo",
            "joined_date": "2023-06-22",
            "avatar_seed": "Charlie",
        },
        {
            "id": "USR-004",
            "name": "Diana Prince",
            "email": "diana@example.com",
            "role": "Operador",
            "status": "Activo",
            "joined_date": "2023-07-05",
            "avatar_seed": "Diana",
        },
        {
            "id": "USR-005",
            "name": "Evan Wright",
            "email": "evan@example.com",
            "role": "Espectador",
            "status": "Activo",
            "joined_date": "2023-08-14",
            "avatar_seed": "Evan",
        },
    ]
    search_query: str = ""
    filter_role: str = "Todos"
    filter_status: str = "Todos"
    is_modal_open: bool = False
    is_loading: bool = False
    current_user_id: str = ""
    form_name: str = ""
    form_email: str = ""
    form_role: str = "Operador"
    form_status: str = "Activo"

    @rx.var
    def filtered_users(self) -> list[User]:
        filtered = self.users
        if self.search_query:
            query = self.search_query.lower()
            filtered = [
                u
                for u in filtered
                if query in u["name"].lower() or query in u["email"].lower()
            ]
        if self.filter_role != "Todos":
            filtered = [u for u in filtered if u["role"] == self.filter_role]
        if self.filter_status != "Todos":
            filtered = [u for u in filtered if u["status"] == self.filter_status]
        return filtered

    @rx.var
    def total_users(self) -> int:
        return len(self.users)

    @rx.var
    def filtered_count(self) -> int:
        return len(self.filtered_users)

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_filter_role(self, role: str):
        self.filter_role = role

    @rx.event
    def set_filter_status(self, status: str):
        self.filter_status = status

    @rx.event
    def set_form_name(self, name: str):
        self.form_name = name

    @rx.event
    def set_form_email(self, email: str):
        self.form_email = email

    @rx.event
    def set_form_role(self, role: str):
        self.form_role = role

    @rx.event
    def set_form_status(self, status: str):
        self.form_status = status

    @rx.event
    def open_add_modal(self):
        self.current_user_id = ""
        self.form_name = ""
        self.form_email = ""
        self.form_role = "Operador"
        self.form_status = "Activo"
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, user: User):
        self.current_user_id = user["id"]
        self.form_name = user["name"]
        self.form_email = user["email"]
        self.form_role = user["role"]
        self.form_status = user["status"]
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    async def save_user(self):
        self.is_loading = True
        await asyncio.sleep(0.8)
        if self.current_user_id:
            new_users = []
            for u in self.users:
                if u["id"] == self.current_user_id:
                    u["name"] = self.form_name
                    u["email"] = self.form_email
                    u["role"] = self.form_role
                    u["status"] = self.form_status
                    u["avatar_seed"] = self.form_name
                new_users.append(u)
            self.users = new_users
        else:
            new_id = f"USR-{random.randint(100, 999)}"
            new_user: User = {
                "id": new_id,
                "name": self.form_name,
                "email": self.form_email,
                "role": self.form_role,
                "status": self.form_status,
                "joined_date": datetime.now().strftime("%Y-%m-%d"),
                "avatar_seed": self.form_name,
            }
            self.users.append(new_user)
        self.is_loading = False
        self.is_modal_open = False

    @rx.event
    def delete_user(self, user_id: str):
        self.users = [u for u in self.users if u["id"] != user_id]