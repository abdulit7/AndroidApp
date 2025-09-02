import flet as ft
from escpos.printer import Network  # Use Network for Android compatibility
import time
import uuid
from datetime import datetime

MENU_ITEMS = []
ORDERS = {"dine_in": {}, "takeaway": {}, "Delivery": {}}
TOTAL_SALES = 0.0
COM_PORT = "192.168.1.100"  # Replace with your printer's IP for Android

def menu_view(page: ft.Page, db: 'Database'):
    page.title = "Menu"
    page.bgcolor = ft.Colors.ORANGE_50
    page.padding = 5
    page.scroll = ft.ScrollMode.AUTO

    global MENU_ITEMS
    MENU_ITEMS = db.get_menu()
    current_order_type = "dine_in"
    current_order = ORDERS[current_order_type]
    order_items = {}

    ORDER_TYPES = ["dine_in", "takeaway", "Delivery"]

    def switch_order_type(e):
        nonlocal current_order_type, current_order
        current_order_type = ORDER_TYPES[e.control.selected_index]
        current_order = ORDERS[current_order_type]
        update_order_display()
        update_order_summary()

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tab_alignment=ft.TabAlignment.CENTER,
        indicator_color=ft.Colors.AMBER_400,
        label_color=ft.Colors.GREY_800,
        unselected_label_color=ft.Colors.GREY_500,
        tabs=[
            ft.Tab(text="Dine-In", icon=ft.Icons.RESTAURANT),
            ft.Tab(text="Takeaway", icon=ft.Icons.TAKEOUT_DINING),
            ft.Tab(text="Delivery", icon=ft.Icons.CALL),
        ],
        on_change=switch_order_type,
    )

    order_type_display = ft.Text(
        value=f"Current Mode: {current_order_type.replace('_', ' ').title()}",
        size=14,
        color=ft.Colors.BLUE_GREY_900,
        weight=ft.FontWeight.BOLD
    )

    def update_order_display():
        order_type_display.value = f"Current Mode: {current_order_type.replace('_', ' ').title()}"
        page.update()

    def print_kitchen_receipt(order_id, items, table_number=None, customer_name=None, customer_number=None, address=None):
        if not items:
            page.snack_bar = ft.SnackBar(ft.Text("No items in order!", color=ft.Colors.RED_500), open=True)
            page.update()
            return
        try:
            p = Network(COM_PORT)  # Use network printer for Android
            p.text(f"{current_order_type.replace('_', ' ').title()} Receipt\n")
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
            for item_name, qty in items.items():
                if qty > 0:
                    p.text(f"{item_name} x {qty}\n")
            p.text("------------------------\n")
            p.cut()
            p.close()
            page.snack_bar = ft.SnackBar(ft.Text("Kitchen receipt printed!", color=ft.Colors.GREEN_600), open=True)
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error printing: {str(ex)}", color=ft.Colors.RED_500), open=True)
            page.update()

    def print_customer_bill(order_id, items, table_number=None, customer_name=None, customer_number=None, address=None):
        if not items:
            page.snack_bar = ft.SnackBar(ft.Text("No items in order!", color=ft.Colors.RED_500), open=True)
            page.update()
            return
        try:
            p = Network(COM_PORT)  # Use network printer for Android
            p.text(f"{current_order_type.replace('_', ' ').title()} Bill\n")
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
            for item_name, qty in items.items():
                if qty > 0:
                    item = next((i for i in MENU_ITEMS if i["name"] == item_name), None)
                    if item:
                        item_total = qty * item["price"]
                        subtotal += item_total
                        p.text(f"{item_name} x {qty} - Rs{item_total:.2f}\n")
            p.text("------------------------\n")
            p.text(f"Total: Rs{subtotal:.2f}\n")
            p.cut()
            p.close()
            page.snack_bar = ft.SnackBar(ft.Text("Customer bill printed!", color=ft.Colors.GREEN_600), open=True)
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error printing: {str(ex)}", color=ft.Colors.RED_500), open=True)
            page.update()

    menu_title = ft.Text("Menu", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800)
    menu_container = ft.ListView(  # Replaced GridView with ListView for single-column layout
        expand=1,
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    def update_menu_container():
        global MENU_ITEMS
        MENU_ITEMS = db.get_menu()
        menu_container.controls.clear()
        for item in MENU_ITEMS:
            menu_container.controls.append(
                ft.Card(
                    elevation=4,
                    color=ft.Colors.WHITE,
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(item["name"], size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE_900, text_align=ft.TextAlign.CENTER),
                                ft.Text(f"Rs{item['price']:.2f}", size=12, color=ft.Colors.AMBER_800, text_align=ft.TextAlign.CENTER),
                                ft.ElevatedButton(
                                    "Select Quantity",
                                    icon=ft.Icons.ADD_SHOPPING_CART,
                                    color=ft.Colors.GREEN_500,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    on_click=lambda e, n=item["name"]: show_quantity_dialog(page, n),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=10,
                        width=340,  # Constrain card width for mobile
                    ),
                    key=item["name"],
                )
            )
        page.update()

    update_menu_container()

    display_value = ft.TextField(
        value="0",
        label="Quantity",
        text_size=14,
        text_align=ft.TextAlign.CENTER,
        read_only=True,
        color=ft.Colors.BLUE_GREY_900,
        border_color=ft.Colors.AMBER_400,
        focused_border_color=ft.Colors.AMBER_600,
        width=150,
        key="qty_display",
    )

    def update_display(e, digit):
        current = display_value.value
        if current == "0":
            display_value.value = digit
        else:
            display_value.value = current + digit
        page.update()

    def close_quantity_dialog(page, dialog):
        dialog.open = False
        display_value.value = "0"
        page.update()

    def add_quantity(page, dialog, item_name, qty):
        try:
            quantity = int(qty)
            if quantity <= 0:
                page.snack_bar = ft.SnackBar(ft.Text("Quantity must be greater than 0", color=ft.Colors.RED_500), open=True)
                page.update()
                return
            if item_name not in order_items:
                order_items[item_name] = 0
            order_items[item_name] = quantity
            page.snack_bar = ft.SnackBar(ft.Text(f"Added {quantity} {item_name} to order", color=ft.Colors.GREEN_600), open=True)
            update_order_summary()
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid number", color=ft.Colors.RED_500), open=True)
        close_quantity_dialog(page, dialog)

    def show_quantity_dialog(page, item_name):
        print(f"Opening dialog for {item_name}")
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Select Quantity for {item_name}", color=ft.Colors.BROWN_800, size=16),
            content=ft.Column(
                [
                    ft.Text("Enter quantity:", size=14, color=ft.Colors.GREY_800),
                    ft.Row(
                        [
                            ft.ElevatedButton("7", on_click=lambda e: update_display(e, "7"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ft.ElevatedButton("8", on_click=lambda e: update_display(e, "8"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ft.ElevatedButton("9", on_click=lambda e: update_display(e, "9"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("4", on_click=lambda e: update_display(e, "4"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ft.ElevatedButton("5", on_click=lambda e: update_display(e, "5"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ft.ElevatedButton("6", on_click=lambda e: update_display(e, "6"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("1", on_click=lambda e: update_display(e, "1"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ft.ElevatedButton("2", on_click=lambda e: update_display(e, "2"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ft.ElevatedButton("3", on_click=lambda e: update_display(e, "3"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("0", on_click=lambda e: update_display(e, "0"), color=ft.Colors.AMBER_400, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ft.ElevatedButton("OK", on_click=lambda e: add_quantity(page, dialog, item_name, display_value.value), color=ft.Colors.GREEN_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ft.ElevatedButton("Cancel", on_click=lambda e: close_quantity_dialog(page, dialog), color=ft.Colors.RED_500, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    display_value,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                width=300,
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        display_value.value = "0"
        page.update()

    order_title = ft.Text("Current Order", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800)
    order_list = ft.ListView(expand=1, spacing=8, padding=10)
    total_text = ft.Text(value="Total: Rs0.0", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)

    def update_order_summary():
        order_list.controls.clear()
        subtotal = 0.0
        for item_name, qty in order_items.items():
            if qty > 0:
                item = next((i for i in MENU_ITEMS if i["name"] == item_name), None)
                if item:
                    item_total = qty * item["price"]
                    subtotal += item_total
                    order_list.controls.append(
                        ft.Card(
                            elevation=4,
                            color=ft.Colors.WHITE,
                            content=ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(f"{item_name} x {qty}", size=14, color=ft.Colors.DEEP_ORANGE_900),
                                        ft.Text(f"Rs{item_total:.2f}", size=14, color=ft.Colors.AMBER_800),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=8,
                            ),
                        )
                    )
        total_text.value = f"Total: Rs{subtotal:.2f}"
        global TOTAL_SALES
        TOTAL_SALES = subtotal
        page.update()

    def show_order_details_dialog():
        table_number_field = ft.TextField(label="Table Number", width=200, visible=current_order_type == "dine_in")
        customer_name_field = ft.TextField(label="Customer Name", width=200, visible=current_order_type in ["takeaway", "Delivery"])
        customer_number_field = ft.TextField(label="Customer Number", width=200, visible=current_order_type == "Delivery")
        address_field = ft.TextField(label="Address", width=200, visible=current_order_type == "Delivery")

        def validate_and_complete(e):
            table_number = table_number_field.value.strip() if current_order_type == "dine_in" else None
            customer_name = customer_name_field.value.strip() if current_order_type in ["takeaway", "Delivery"] else None
            customer_number = customer_number_field.value.strip() or None if current_order_type == "Delivery" else None
            address = address_field.value.strip() or None if current_order_type == "Delivery" else None

            if current_order_type == "dine_in" and not table_number:
                page.snack_bar = ft.SnackBar(ft.Text("Table number is required for dine-in!", color=ft.Colors.RED_500), open=True)
                page.update()
                return
            if current_order_type == "takeaway" and not customer_name:
                page.snack_bar = ft.SnackBar(ft.Text("Customer name is required for takeaway!", color=ft.Colors.RED_500), open=True)
                page.update()
                return

            dialog.open = False
            page.update()

            complete_order_with_details(table_number, customer_name, customer_number, address)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Enter {current_order_type.replace('_', ' ').title()} Details", size=16),
            content=ft.Column(
                [
                    table_number_field,
                    customer_name_field,
                    customer_number_field,
                    address_field,
                ],
                tight=True,
                spacing=10,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_quantity_dialog(page, dialog)),
                ft.TextButton("OK", on_click=validate_and_complete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def complete_order_with_details(table_number, customer_name, customer_number, address):
        if not order_items:
            page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=ft.Colors.RED_500), open=True)
            page.update()
            return

        order_id = str(uuid.uuid4())
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_details = []
        for item_name, qty in order_items.items():
            if qty > 0:
                item = next((i for i in MENU_ITEMS if i["name"] == item_name), None)
                if item:
                    order_details.append({
                        "name": item_name,
                        "quantity": qty,
                        "price": item["price"],
                        "total": qty * item["price"]
                    })

        try:
            db.add_order(order_id, current_order_type, order_details, date_time, table_number, customer_name, customer_number, address)
            print_kitchen_receipt(order_id, order_items, table_number, customer_name, customer_number, address)
            print_customer_bill(order_id, order_items, table_number, customer_name, customer_number, address)
            order_items.clear()
            update_order_summary()
            page.snack_bar = ft.SnackBar(ft.Text(f"Order {order_id} completed!", color=ft.Colors.GREEN_600), open=True)
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error completing order: {str(ex)}", color=ft.Colors.RED_500), open=True)
            page.update()

    def complete_order(e):
        if not order_items:
            page.snack_bar = ft.SnackBar(ft.Text("No items to complete!", color=ft.Colors.RED_500), open=True)
            page.update()
            return
        show_order_details_dialog()

    menu_content = ft.Container(
        content=ft.Column(
            [
                tabs,
                order_type_display,
                ft.Container(
                    content=menu_title,
                    padding=8,
                    bgcolor=ft.Colors.ORANGE_300,
                    border_radius=8,
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Container(
                    content=menu_container,
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Container(
                    content=order_title,
                    padding=8,
                    bgcolor=ft.Colors.ORANGE_300,
                    border_radius=8,
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Container(
                    content=order_list,
                    padding=8,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Container(
                    content=total_text,
                    padding=8,
                    bgcolor=ft.Colors.ORANGE_200,
                    border_radius=8,
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Receipt",
                            icon=ft.Icons.PRINT,
                            color=ft.Colors.BLUE_500,
                            on_click=lambda e: show_order_details_dialog(),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        ),
                        ft.ElevatedButton(
                            "Bill",
                            icon=ft.Icons.RECEIPT,
                            color=ft.Colors.GREEN_600,
                            on_click=lambda e: show_order_details_dialog(),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        ),
                        ft.ElevatedButton(
                            "Complete",
                            icon=ft.Icons.DONE,
                            color=ft.Colors.PURPLE_500,
                            on_click=complete_order,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=min(page.width, 360),
        alignment=ft.alignment.center,
    )

    return menu_content
