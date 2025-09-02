import flet as ft

MENU_ITEMS = []

def product_view(page: ft.Page, db: 'Database'):
    page.title = "Manage Products"
    page.bgcolor = ft.Colors.ORANGE_50
    page.padding = 5
    page.scroll = ft.ScrollMode.AUTO

    global MENU_ITEMS
    MENU_ITEMS = db.get_menu()

    # Input fields for adding new product
    name_field = ft.TextField(
        label="Product Name",
        width=300,
        text_size=14,
        color=ft.Colors.BLUE_GREY_900,
        border_color=ft.Colors.AMBER_400,
        focused_border_color=ft.Colors.AMBER_600,
    )
    price_field = ft.TextField(
        label="Price (Rs)",
        width=150,
        text_size=14,
        color=ft.Colors.BLUE_GREY_900,
        border_color=ft.Colors.AMBER_400,
        focused_border_color=ft.Colors.AMBER_600,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def add_product(e):
        name = name_field.value.strip()
        try:
            price = float(price_field.value.strip())
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Price must be a valid number!", color=ft.Colors.RED_500), open=True)
            page.update()
            return

        if not name:
            page.snack_bar = ft.SnackBar(ft.Text("Product name is required!", color=ft.Colors.RED_500), open=True)
            page.update()
            return
        if price <= 0:
            page.snack_bar = ft.SnackBar(ft.Text("Price must be greater than 0!", color=ft.Colors.RED_500), open=True)
            page.update()
            return

        try:
            db.initialize_menu([{"name": name, "price": price}])
            global MENU_ITEMS
            MENU_ITEMS = db.get_menu()
            update_product_table()
            name_field.value = ""
            price_field.value = ""
            page.snack_bar = ft.SnackBar(ft.Text(f"Added {name} to menu!", color=ft.Colors.GREEN_600), open=True)
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error adding product: {str(ex)}", color=ft.Colors.RED_500), open=True)
            page.update()

    # Product table
    product_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name", color=ft.Colors.BROWN_800, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Price (Rs)", color=ft.Colors.BROWN_800, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Actions", color=ft.Colors.BROWN_800, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        heading_row_color=ft.Colors.ORANGE_200,
        border=ft.BorderSide(1, ft.Colors.GREY_400),
        divider_thickness=1,
    )

    def update_product_table():
        global MENU_ITEMS
        MENU_ITEMS = db.get_menu()
        product_table.rows.clear()
        for item in MENU_ITEMS:
            product_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["name"], color=ft.Colors.DEEP_ORANGE_900)),
                        ft.DataCell(ft.Text(f"Rs{item['price']:.2f}", color=ft.Colors.AMBER_800)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        icon_color=ft.Colors.BLUE_500,
                                        tooltip="Edit",
                                        on_click=lambda e, name=item["name"]: show_edit_dialog(name),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE,
                                        icon_color=ft.Colors.RED_500,
                                        tooltip="Delete",
                                        on_click=lambda e, name=item["name"]: show_delete_dialog(name),
                                    ),
                                ],
                                spacing=5,
                            )
                        ),
                    ]
                )
            )
        page.update()

    def show_edit_dialog(name):
        item = next((i for i in MENU_ITEMS if i["name"] == name), None)
        if not item:
            page.snack_bar = ft.SnackBar(ft.Text("Product not found!", color=ft.Colors.RED_500), open=True)
            page.update()
            return

        edit_name_field = ft.TextField(
            label="Product Name",
            value=item["name"],
            width=300,
            text_size=14,
            color=ft.Colors.BLUE_GREY_900,
            border_color=ft.Colors.AMBER_400,
            focused_border_color=ft.Colors.AMBER_600,
        )
        edit_price_field = ft.TextField(
            label="Price (Rs)",
            value=str(item["price"]),
            width=150,
            text_size=14,
            color=ft.Colors.BLUE_GREY_900,
            border_color=ft.Colors.AMBER_400,
            focused_border_color=ft.Colors.AMBER_600,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        def save_edit(e):
            new_name = edit_name_field.value.strip()
            try:
                price = float(edit_price_field.value.strip())
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Price must be a valid number!", color=ft.Colors.RED_500), open=True)
                page.update()
                return

            if not new_name:
                page.snack_bar = ft.SnackBar(ft.Text("Product name is required!", color=ft.Colors.RED_500), open=True)
                page.update()
                return
            if price <= 0:
                page.snack_bar = ft.SnackBar(ft.Text("Price must be greater than 0!", color=ft.Colors.RED_500), open=True)
                page.update()
                return

            try:
                db.edit_product(name, new_name, price)
                global MENU_ITEMS
                MENU_ITEMS = db.get_menu()
                update_product_table()
                dialog.open = False
                # page.overlay.remove(dialog)
                page.snack_bar = ft.SnackBar(ft.Text(f"Updated {new_name}!", color=ft.Colors.GREEN_600), open=True)
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error updating product: {str(ex)}", color=ft.Colors.RED_500), open=True)
                page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Edit Product: {name}", color=ft.Colors.BROWN_800, size=16),
            content=ft.Column(
                [
                    edit_name_field,
                    edit_price_field,
                ],
                tight=True,
                spacing=10,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(dialog)),
                ft.TextButton("Save", on_click=save_edit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def show_delete_dialog(name):
        def confirm_delete(e):
            try:
                db.delete_product(name)
                global MENU_ITEMS
                MENU_ITEMS = db.get_menu()
                update_product_table()
                dialog.open = False
                # page.overlay.remove(dialog)
                page.snack_bar = ft.SnackBar(ft.Text(f"Deleted {name}!", color=ft.Colors.GREEN_600), open=True)
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error deleting product: {str(ex)}", color=ft.Colors.RED_500), open=True)
                page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Delete Product: {name}", color=ft.Colors.BROWN_800, size=16),
            content=ft.Text(f"Are you sure you want to delete {name}?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(dialog)),
                ft.TextButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED_500)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        # page.overlay.remove(dialog)
        page.update()

    # Initialize product table
    update_product_table()

    # Layout
    content = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("Manage Products", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                    padding=8,
                    bgcolor=ft.Colors.ORANGE_300,
                    border_radius=8,
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Add New Product", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                            name_field,
                            price_field,
                            ft.ElevatedButton(
                                "Add Product",
                                icon=ft.Icons.ADD,
                                color=ft.Colors.GREEN_600,
                                on_click=add_product,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Container(
                    content=ft.Text("Product List", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                    padding=8,
                    bgcolor=ft.Colors.ORANGE_300,
                    border_radius=8,
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Container(
                    content=ft.ListView(
                        controls=[product_table],
                        expand=1,
                        auto_scroll=True,
                    ),
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
                    margin=ft.margin.only(bottom=10),
                ),
                # ft.ElevatedButton(
                #     "Back to Dashboard",
                #     icon=ft.Icons.ARROW_BACK,
                #     color=ft.Colors.BLUE_500,
                #     on_click=lambda e: page.go("/dashboard"),
                #     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                # ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=min(page.width, 360),
        alignment=ft.alignment.center,
    )

    return content