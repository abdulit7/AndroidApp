
import flet as ft
from dashboard import dashboard_view
from expense import expense_view
from sale import sale_view
from menu import menu_view
from product import product_view
from order import order_view
from database import Database

# Initialize database
db = Database()
MENU_ITEMS = db.get_menu()
EXPENSES = {"Rent": 5000, "Water": 500, "Fuel": 500, "Other": 400}
ORDERS = {"dine_in": {}, "takeaway": {}, "online": {}}
TOTAL_SALES = 0.0
TOTAL_EXPENSES = sum(EXPENSES.values())
NET_PROFIT = 0.0
COM_PORT = "COM3"  # Replace with Android device (e.g., '/dev/ttyS0') or printer IP

def main(page: ft.Page):
    page.title = "Asan Billing POS"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(top=30)  # Add top padding for Android status bar
    page.bgcolor = ft.Colors.ORANGE_100
    page.scroll = ft.ScrollMode.AUTO
    # Set mobile dimensions
    page.window.width = 360
    page.window.height = 640
    page.window.resizable = True

    # Top AppBar (set globally, not in view controls)
    page.appbar = ft.AppBar(
        title=ft.Text("Asan Billing", size=18, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.ORANGE_400,
        actions=[
            ft.IconButton(ft.Icons.DASHBOARD, tooltip="Dashboard", on_click=lambda e: page.go("/dashboard")),
        ],
    )
    print("AppBar initialized with title 'Asan Billing'")

    # Bottom AppBar (set globally, not in view controls)
    def on_fab_click(e):
        page.snack_bar = ft.SnackBar(content=ft.Text("Add new item!"), open=True)
        page.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=on_fab_click,
        bgcolor=ft.Colors.GREEN_600,
        mini=True,
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.BLUE_700,
        shape=ft.NotchShape.CIRCULAR,
        height=60,
        content=ft.Row(
            controls=[
                ft.IconButton(ft.Icons.MENU, icon_color=ft.Colors.WHITE, tooltip="Menu", on_click=lambda e: page.go("/menu")),
                ft.Container(expand=True),
                ft.IconButton(ft.Icons.MONETIZATION_ON, icon_color=ft.Colors.WHITE, tooltip="Expenses", on_click=lambda e: page.go("/expense")),
                ft.IconButton(ft.Icons.SHOW_CHART, icon_color=ft.Colors.WHITE, tooltip="Sales", on_click=lambda e: page.go("/sale")),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        ),
    )
    print("BottomAppBar initialized with Menu, Expenses, Sales buttons")

    # Route map
    def get_route_map(page):
        return {
            "/dashboard": lambda: dashboard_view(page, db),
            "/expense": lambda: expense_view(page, db),
            "/sale": lambda: sale_view(page, db),
            "/menu": lambda: menu_view(page, db),
            "/products": lambda: product_view(page, db),
            "/order": lambda: order_view(page, db),
            "/orders": lambda: order_view(page, db),
            "/": lambda: dashboard_view(page, db),
        }

    def route_change(e: ft.RouteChangeEvent):
        print(f"Navigating to route: {e.route}")
        route = e.route

        # Clear overlays to prevent dialog stacking
        if any(isinstance(c, ft.AlertDialog) for c in page.overlay):
            page.overlay.clear()
        page.snack_bar = None

        # Handle invalid or root route
        route_map = get_route_map(page)
        content_builder = route_map.get(route, lambda: ft.Text("404 - Page Not Found", color=ft.Colors.RED_600))

        # Build content
        content = content_builder()
        view_width = min(page.width, 360)

        # Create view without embedding AppBar/BottomAppBar in controls
        page.views.clear()
        page.views.append(
            ft.View(
                route=route,
                controls=[
                    ft.Container(
                        content=content,
                        width=view_width,
                        alignment=ft.alignment.center,
                        padding=ft.padding.symmetric(horizontal=10),
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                appbar=page.appbar,  # Reference global AppBar
                floating_action_button=page.floating_action_button,
                bottom_appbar=page.bottom_appbar,  # Reference global BottomAppBar
            )
        )
        print(f"View stack size: {len(page.views)}")
        print(f"AppBar status: {'visible' if page.appbar else 'not visible'}")
        print(f"BottomAppBar status: {'visible' if page.bottom_appbar else 'not visible'}")
        try:
            page.update()
        except Exception as e:
            print(f"Error updating page: {e}")
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Render error: {e}"), open=True)
            page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)
        else:
            page.go("/dashboard")  # Default to dashboard
        print(f"View stack after pop: {len(page.views)}")
        page.update()

    # Set routing handlers
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/dashboard")  # Start at dashboard
    print("Initial route set to /dashboard")

ft.app(target=main, assets_dir="assets")
