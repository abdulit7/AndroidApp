import flet as ft
import datetime
from escpos.printer import Serial
import time

COM_PORT = "COM3"

def order_view(page: ft.Page, db: 'Database'):
    page.title = "Orders"
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0

    # DatePicker for date selection
    selected_date = datetime.datetime.now()

    def update_orders_by_date(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_picker.open = False
        update_orders_display()
        page.update()

    date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2000, month=1, day=1),
        last_date=datetime.datetime(year=2050, month=12, day=31),
        value=selected_date,
        on_change=update_orders_by_date,
        on_dismiss=lambda e: page.update()
    )

    def show_date_picker(e):
        page.dialog = date_picker
        date_picker.open = True
        page.overlay.append(date_picker)
        page.update()

    date_picker_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_700, size=20),
                ft.Text("Pick Date", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.WHITE,
            padding=10,
            elevation={"pressed": 2, "": 6},
        ),
        on_click=show_date_picker,
        opacity=1.0,
        on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
    )

    # Display orders
    orders_list = ft.ListView(
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    def print_customer_bill(order_id, items, table_number=None, customer_name=None, customer_number=None, address=None):
        if not items:
            page.snack_bar = ft.SnackBar(ft.Text("No items in order!", color=ft.Colors.RED_500), open=True)
            page.update()
            return
        try:
            p = Serial(devfile=COM_PORT, baudrate=9600, timeout=5)
            order_type = next((o["order_type"] for o in db.get_orders_by_date(selected_date.strftime("%Y-%m-%d")) if o["order_id"] == order_id), "Unknown")
            p.text(f"{order_type.replace('_', ' ').title()} Bill\n")
            p.text(f"Order ID: {order_id}\n")
            p.text(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            if table_number:
                p.text(f"Table Number: {table_number}\n")
            if customer_name:
                p.text(f"Customer Name: {customer_name}\n")
            if customer_number:
                p.text(f"Customer Number: {customer_number}\n")
            if address:
                p.text(f"Address: {address}\n")
            p.text("------------------------\n")
            subtotal = 0.0
            for item in items:
                item_total = item["quantity"] * item["price"]
                subtotal += item_total
                p.text(f"{item['item_name']} x {item['quantity']} - Rs{item_total:.2f}\n")
            p.text("------------------------\n")
            p.text(f"Total: Rs{subtotal:.2f}\n")
            p.text("------------------------\n")
            p.text("Thank you for your order!\n")
            p.cut()
            p.close()
            page.snack_bar = ft.SnackBar(ft.Text("Customer bill printed!", color=ft.Colors.GREEN_600), open=True)
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error printing: {str(ex)}", color=ft.Colors.RED_500), open=True)
            page.update()

    def show_order_details(e, order):
        items = db.get_order_items(order["order_id"])
        items_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Order Items", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    ft.ListView(
                        controls=[
                            ft.Row(
                                [
                                    ft.Text(f"{item['item_name']} x {item['quantity']}", size=14, color=ft.Colors.BLACK87),
                                    ft.Text(f"Rs{item['total']:.2f}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ) for item in items
                        ],
                        spacing=5,
                        padding=10,
                        auto_scroll=True,
                    ),
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.PRINT, color=ft.Colors.BLUE_700),
                                ft.Text("Print Bill", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            elevation={"pressed": 2, "": 6},
                        ),
                        on_click=lambda e: print_customer_bill(
                            order["order_id"],
                            items,
                            order["table_number"],
                            order["customer_name"],
                            order["customer_number"],
                            order["address"]
                        ),
                        opacity=1.0,
                        on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                    ),
                ],
                spacing=10,
            ),
            bgcolor=ft.Colors.WHITE,
            padding=10,
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
            margin=ft.margin.only(left=10, right=10, top=5),
            visible=False,
        )

        def toggle_details(e):
            items_container.visible = not items_container.visible
            page.update()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                f"Order ID: {order['order_id'][:8]}... | {order['order_type'].replace('_', ' ').title()} | {order['order_date']}",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.BLACK87,
                            ),
                            ft.Text(
                                f"Total: Rs{order['total']:.2f}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_700,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(
                        f"Table: {order['table_number'] or 'N/A'} | Name: {order['customer_name'] or 'N/A'} | Number: {order['customer_number'] or 'N/A'}",
                        size=12,
                        color=ft.Colors.BLACK54,
                    ),
                    items_container,
                ],
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            padding=10,
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
            on_click=toggle_details,
        )

    def update_orders_display():
        orders_list.controls.clear()
        orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
        if orders:
            for order in orders:
                orders_list.controls.append(show_order_details(None, order))
        else:
            orders_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No orders for this date",
                        size=14,
                        color=ft.Colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=10,
                )
            )
        page.update()

    # Initial display
    update_orders_display()

    # Gradient background
    background = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[ft.Colors.ORANGE_200, ft.Colors.ORANGE_400, ft.Colors.ORANGE_600],
        ),
        expand=True,
    )

    # Main content container
    orders_content = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Orders by Date",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        font_family="Roboto",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    shadow=ft.BoxShadow(
                        blur_radius=8,
                        spread_radius=1,
                        color=ft.Colors.BLACK26,
                    ),
                    padding=8,
                ),
                date_picker_button,
                ft.Container(
                    content=orders_list,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=10,
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        spread_radius=3,
                        color=ft.Colors.BLACK26,
                    ),
                    margin=ft.margin.symmetric(horizontal=10, vertical=20),
                    height=400,
                ),
                # ft.ElevatedButton(
                #     content=ft.Row(
                #         [
                #             ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_700, size=20),
                #             ft.Text("Back to Dashboard", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
                #         ],
                #         alignment=ft.MainAxisAlignment.CENTER,
                #         spacing=8,
                #     ),
                #     style=ft.ButtonStyle(
                #         shape=ft.RoundedRectangleBorder(radius=10),
                #         bgcolor=ft.Colors.WHITE,
                #         padding=10,
                #         elevation={"pressed": 2, "": 6},
                #     ),
                #     on_click=lambda e: page.go("/dashboard"),
                #     opacity=1.0,
                #     on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                # ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        width=min(page.width, 360),
        alignment=ft.alignment.center,
    )

    # Stack the gradient background and content
    return ft.Stack(
        [
            background,
            orders_content,
        ],
        expand=True,
    )