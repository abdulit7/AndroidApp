

import flet as ft
import datetime

def expense_view(page: ft.Page, db: 'Database'):
    page.title = "Expenses"
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0

    def close_dialog(dialog):
        dialog.open = False
        # if dialog in page.overlay:
        #     page.overlay.remove(dialog)
        page.update()

    # Dialog for adding expense
    add_expense_dialog = ft.AlertDialog(
        title=ft.Text("Add Expense", color=ft.Colors.BROWN_800, size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column([
            ft.TextField(
                label="Category",
                value="",
                width=300,
                text_style=ft.TextStyle(size=14),
                color=ft.Colors.BLUE_GREY_900,
                border_color=ft.Colors.AMBER_400,
                focused_border_color=ft.Colors.AMBER_600,
            ),
            ft.TextField(
                label="Amount",
                keyboard_type=ft.KeyboardType.NUMBER,
                width=150,
                text_style=ft.TextStyle(size=14),
                color=ft.Colors.BLUE_GREY_900,
                border_color=ft.Colors.AMBER_400,
                focused_border_color=ft.Colors.AMBER_600,
            ),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Save",
                        icon=ft.Icons.SAVE,
                        color=ft.Colors.GREEN_600,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        on_click=lambda e: save_expense(e, page),
                        opacity=1.0,
                        on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                    ),
                    ft.ElevatedButton(
                        "Cancel",
                        icon=ft.Icons.CANCEL,
                        color=ft.Colors.RED_500,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        on_click=lambda e: close_dialog(add_expense_dialog),
                        opacity=1.0,
                        on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=10,
            ),
        ], tight=True, spacing=10),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(add_expense_dialog)

    def show_add_expense_dialog(e):
        add_expense_dialog.content.controls[0].value = ""  # Reset category
        add_expense_dialog.content.controls[1].value = ""  # Reset amount
        page.dialog = add_expense_dialog
        add_expense_dialog.open = True
        page.update()

    def save_expense(e, page):
        category = add_expense_dialog.content.controls[0].value.strip()
        amount_str = add_expense_dialog.content.controls[1].value.strip()
        
        if not category or not amount_str:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter both category and amount!", color=ft.Colors.RED_500), open=True)
            page.update()
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            db.add_expense(category, amount, datetime.datetime.now().strftime("%Y-%m-%d"))
            close_dialog(add_expense_dialog)
            update_expense_display()
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Expense '{category}: Rs{amount:.2f}' added!", color=ft.Colors.GREEN_600), open=True)
        except ValueError as ve:
            error_msg = str(ve) if str(ve) != "Amount must be positive" else "Please enter a valid positive amount!"
            page.snack_bar = ft.SnackBar(content=ft.Text(error_msg, color=ft.Colors.RED_500), open=True)
        page.update()

    # Dialog for editing expense
    def show_edit_expense_dialog(e, expense_id, category, amount):
        edit_category_field = ft.TextField(
            label="Category",
            value=category,
            width=300,
            text_style=ft.TextStyle(size=14),
            color=ft.Colors.BLUE_GREY_900,
            border_color=ft.Colors.AMBER_400,
            focused_border_color=ft.Colors.AMBER_600,
        )
        edit_amount_field = ft.TextField(
            label="Amount",
            value=str(amount),
            keyboard_type=ft.KeyboardType.NUMBER,
            width=150,
            text_style=ft.TextStyle(size=14),
            color=ft.Colors.BLUE_GREY_900,
            border_color=ft.Colors.AMBER_400,
            focused_border_color=ft.Colors.AMBER_600,
        )

        def save_edit(e):
            new_category = edit_category_field.value.strip()
            amount_str = edit_amount_field.value.strip()
            if not new_category or not amount_str:
                page.snack_bar = ft.SnackBar(content=ft.Text("Please enter both category and amount!", color=ft.Colors.RED_500), open=True)
                page.update()
                return
            try:
                new_amount = float(amount_str)
                if new_amount <= 0:
                    raise ValueError("Amount must be positive")
                db.edit_expense(expense_id, new_category, new_amount)
                close_dialog(edit_expense_dialog)
                update_expense_display()
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Expense '{new_category}: Rs{new_amount:.2f}' updated!", color=ft.Colors.GREEN_600), open=True)
            except ValueError as ve:
                error_msg = str(ve) if str(ve) != "Amount must be positive" else "Please enter a valid positive amount!"
                page.snack_bar = ft.SnackBar(content=ft.Text(error_msg, color=ft.Colors.RED_500), open=True)
            page.update()

        edit_expense_dialog = ft.AlertDialog(
            title=ft.Text(f"Edit Expense: {category}", color=ft.Colors.BROWN_800, size=18, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    edit_category_field,
                    edit_amount_field,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Save",
                                icon=ft.Icons.SAVE,
                                color=ft.Colors.GREEN_600,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                on_click=save_edit,
                                opacity=1.0,
                                on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                            ),
                            ft.ElevatedButton(
                                "Cancel",
                                icon=ft.Icons.CANCEL,
                                color=ft.Colors.RED_500,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                on_click=lambda e: close_dialog(edit_expense_dialog),
                                opacity=1.0,
                                on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                    ),
                ],
                tight=True,
                spacing=10,
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        # page.overlay.clear()
        page.overlay.append(edit_expense_dialog)
        page.dialog = edit_expense_dialog
        edit_expense_dialog.open = True
        page.update()

    # Dialog for deleting expense
    def show_delete_expense_dialog(e, expense_id, category):
        def confirm_delete(e):
            try:
                db.delete_expense(expense_id)
                close_dialog(delete_expense_dialog)
                update_expense_display()
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Expense '{category}' deleted!", color=ft.Colors.GREEN_600), open=True)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Error deleting expense: {str(ex)}", color=ft.Colors.RED_500), open=True)
            page.update()

        delete_expense_dialog = ft.AlertDialog(
            title=ft.Text(f"Delete Expense: {category}", color=ft.Colors.BROWN_800, size=18, weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Are you sure you want to delete '{category}'?"),
            actions=[
                ft.ElevatedButton(
                    "Delete",
                    icon=ft.Icons.DELETE,
                    color=ft.Colors.RED_500,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=confirm_delete,
                    opacity=1.0,
                    on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                ),
                ft.ElevatedButton(
                    "Cancel",
                    icon=ft.Icons.CANCEL,
                    color=ft.Colors.BLUE_700,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=lambda e: close_dialog(delete_expense_dialog),
                    opacity=1.0,
                    on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        # page.overlay.clear()
        page.overlay.append(delete_expense_dialog)
        page.dialog = delete_expense_dialog
        delete_expense_dialog.open = True
        page.update()

    # DatePicker for date selection
    selected_date = datetime.datetime.now()

    def update_expense_by_date(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_picker.open = False
        update_expense_display()
        page.update()

    date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2000, month=1, day=1),
        last_date=datetime.datetime(year=2050, month=12, day=31),
        value=selected_date,
        on_change=update_expense_by_date,
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

    # Display expenses
    expense_list = ft.ListView(
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    def update_expense_display():
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_expenses = db.get_expenses_today()
        selected_date_expenses = db.get_expenses_by_date(selected_date.strftime("%Y-%m-%d"))
        
        expense_list.controls.clear()
        expense_list.controls.append(
            ft.Text(
                f"Today's Expenses ({today}):",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK87,
            )
        )
        if today_expenses:
            for idx, (cat, amt) in enumerate(today_expenses):
                expense_id = f"{today}_{idx}"  # Workaround if expense_id is missing
                expense_list.controls.append(
                    ft.GestureDetector(
                        content=ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text(f"{cat}", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK87, max_lines=1),
                                    ft.Row(
                                        [
                                            ft.Text(f"Rs{amt:.2f}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                                            ft.IconButton(
                                                ft.Icons.EDIT,
                                                icon_color=ft.Colors.BLUE_500,
                                                icon_size=16,
                                                tooltip="Edit",
                                                on_click=lambda e, eid=expense_id, c=cat, a=amt: show_edit_expense_dialog(e, eid, c, a),
                                            ),
                                            ft.IconButton(
                                                ft.Icons.DELETE,
                                                icon_color=ft.Colors.RED_500,
                                                icon_size=16,
                                                tooltip="Delete",
                                                on_click=lambda e, eid=expense_id, c=cat: show_delete_expense_dialog(e, eid, c),
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.END,
                                        spacing=5,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            border_radius=8,
                            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
                            width=340,
                        ),
                        on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
                    )
                )
            expense_list.controls.append(
                ft.Text(
                    f"Total Today: Rs{sum(amt for _, amt in today_expenses):.2f}",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK87,
                    text_align=ft.TextAlign.RIGHT,
                )
            )
        else:
            expense_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No expenses today",
                        size=12,
                        color=ft.Colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=10,
                    width=340,
                )
            )

        expense_list.controls.append(
            ft.Text(
                f"Expenses on {selected_date.strftime('%Y-%m-%d')}:",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK87,
            )
        )
        if selected_date_expenses:
            for idx, (cat, amt) in enumerate(selected_date_expenses):
                expense_id = f"{selected_date.strftime('%Y-%m-%d')}_{idx}"  # Workaround if expense_id is missing
                expense_list.controls.append(
                    ft.GestureDetector(
                        content=ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text(f"{cat}", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK87, max_lines=1),
                                    ft.Row(
                                        [
                                            ft.Text(f"Rs{amt:.2f}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                                            ft.IconButton(
                                                ft.Icons.EDIT,
                                                icon_color=ft.Colors.BLUE_500,
                                                icon_size=16,
                                                tooltip="Edit",
                                                on_click=lambda e, eid=expense_id, c=cat, a=amt: show_edit_expense_dialog(e, eid, c, a),
                                            ),
                                            ft.IconButton(
                                                ft.Icons.DELETE,
                                                icon_color=ft.Colors.RED_500,
                                                icon_size=16,
                                                tooltip="Delete",
                                                on_click=lambda e, eid=expense_id, c=cat: show_delete_expense_dialog(e, eid, c),
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.END,
                                        spacing=5,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            border_radius=8,
                            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
                            width=340,
                        ),
                        on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
                    )
                )
            expense_list.controls.append(
                ft.Text(
                    f"Total: Rs{sum(amt for _, amt in selected_date_expenses):.2f}",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK87,
                    text_align=ft.TextAlign.RIGHT,
                )
            )
        else:
            expense_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No expenses on this date",
                        size=12,
                        color=ft.Colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=10,
                    width=340,
                )
            )
        page.update()

    def on_add_expense_click(e):
        show_add_expense_dialog(e)

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
    expense_content = ft.Container(
        content=ft.ListView(
            controls=[
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.ADD, color=ft.Colors.GREEN_700, size=20),
                            ft.Text("Add Expense", color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD, size=14),
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
                    on_click=on_add_expense_click,
                    opacity=1.0,
                    on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                ),
                date_picker_button,
                ft.Container(
                    content=expense_list,
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
                    width=340,
                ),
            ],
            expand=True,
            auto_scroll=True,
            spacing=10,
            padding=10,
        ),
        width=min(page.width, 360),
        alignment=ft.alignment.center,
    )

    # Initial update
    update_expense_display()

    # Stack the gradient background and content
    return ft.Stack(
        [
            background,
            expense_content,
        ],
        expand=True,
    )
