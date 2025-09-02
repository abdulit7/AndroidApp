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
COM_PORT = "COM3"  # Replace with your Bluetooth printer's COM port

def main(page: ft.Page):
    page.title = "AKBER TIKKA"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0  # Reduced padding to ensure AppBar visibility
    page.bgcolor = ft.Colors.ORANGE_100
    page.scroll = ft.ScrollMode.AUTO
    # Set mobile dimensions
    page.window.width = 360
    page.window.height = 640

    # Top AppBar
    page.appbar = ft.AppBar(
        title=ft.Text("AKBER TIKKA", size=18, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.ORANGE_400,
        actions=[
            ft.IconButton(ft.Icons.DASHBOARD, tooltip="Dashboard", on_click=lambda e: page.go("/dashboard")),
        ],
    )
    print("AppBar initialized with title 'AKBER TIKKA'")

    # Bottom AppBar
    def on_fab_click(e):
        page.go("/products")

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

    def route_change(route):
        print(f"Navigating to route: {page.route}")
        # Clear existing views to avoid stacking
        page.views.clear()
        view_width = min(page.width, 360)

        # Map routes to view functions
        route_to_view = {
            "/dashboard": lambda: dashboard_view(page, db),
            "/expense": lambda: expense_view(page, db),
            "/sale": lambda: sale_view(page, db),
            "/menu": lambda: menu_view(page, db),
            "/products": lambda: product_view(page, db),
            "/order": lambda: order_view(page, db),
            "/orders": lambda: order_view(page, db),
            "/": lambda: menu_view(page, db),
        }

        # Get the view content for the current route
        view_content = route_to_view.get(page.route, lambda: menu_view(page, db))()

        # Create a single view with constrained content
        page.views.append(
            ft.View(
                route=page.route,
                controls=[
                    ft.Container(
                        content=ft.ListView(
                            controls=[view_content],
                            expand=True,
                            auto_scroll=True,
                        ),
                        width=view_width,
                        alignment=ft.alignment.center,
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                appbar=page.appbar,  # Ensure AppBar is referenced
                floating_action_button=page.floating_action_button,  # Ensure FAB is referenced
                bottom_appbar=page.bottom_appbar,  # Ensure BottomAppBar is referenced
            )
        )

        print(f"AppBar status: {'visible' if page.appbar else 'not visible'}")
        print(f"BottomAppBar status: {'visible' if page.bottom_appbar else 'not visible'}")
        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)
        else:
            page.go("/dashboard")  # Default to dashboard if no views left

    # Set routing handlers
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/dashboard")  # Start at dashboard

    print("Initial route set to /dashboard")

ft.app(target=main)