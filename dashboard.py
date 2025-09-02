import flet as ft

def dashboard_view(page: ft.Page, db: 'Database'):
    page.title = "Dashboard"
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0

  

    # Gradient background
    background = ft.Container(
        content=ft.Container(),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[ft.Colors.ORANGE_200, ft.Colors.ORANGE_400, ft.Colors.ORANGE_600],
        ),
        expand=True,
    )

    # Title with shadow via Container
    title = ft.Container(
        content=ft.Text(
            "Restaurant Dashboard",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER,
            font_family="Roboto",
        ),
        shadow=ft.BoxShadow(
            blur_radius=8,
            spread_radius=1,
            color=ft.Colors.BLACK26,
        ),
        padding=8,
    )

    # Button style with hover effect using opacity
    button_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=10),
        bgcolor=ft.Colors.WHITE,
        padding=10,
        elevation={"pressed": 2, "": 6},
    )

    # Grid of buttons
    button_grid = ft.GridView(
        runs_count=1,  # Single column for mobile
        max_extent=300,
        child_aspect_ratio=1.3,
        spacing=10,
        run_spacing=10,
        padding=10,
        controls=[
            ft.ElevatedButton(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.RESTAURANT_MENU, color=ft.Colors.BLUE_700, size=30),
                        ft.Text("Order", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                style=button_style,
                on_click=lambda e: page.go("/menu"),
                opacity=1.0,
                on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
            ),
            ft.ElevatedButton(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.MONETIZATION_ON, color=ft.Colors.GREEN_700, size=30),
                        ft.Text("Sale", color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD, size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                style=button_style,
                on_click=lambda e: page.go("/sale"),
                opacity=1.0,
                on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
            ),
            ft.ElevatedButton(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.MONEY_OFF, color=ft.Colors.AMBER_700, size=30),
                        ft.Text("Expense", color=ft.Colors.AMBER_700, weight=ft.FontWeight.BOLD, size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                style=button_style,
                on_click=lambda e: page.go("/expense"),
                opacity=1.0,
                on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
            ),
            ft.ElevatedButton(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.MENU_BOOK, color=ft.Colors.PURPLE_700, size=30),
                        ft.Text("Menu", color=ft.Colors.PURPLE_700, weight=ft.FontWeight.BOLD, size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                style=button_style,
                on_click=lambda e: page.go("/menu"),
                opacity=1.0,
                on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
            ),
            ft.ElevatedButton(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ADD_SHOPPING_CART, color=ft.Colors.ORANGE_700, size=30),
                        ft.Text("Add Product", color=ft.Colors.ORANGE_700, weight=ft.FontWeight.BOLD, size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                style=button_style,
                on_click=lambda e: page.go("/products"),
                opacity=1.0,
                on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
            ),
            ft.ElevatedButton(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.LIST_ALT, color=ft.Colors.TEAL_700, size=30),
                        ft.Text("Orders", color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD, size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                style=button_style,
                on_click=lambda e: page.go("/orders"),
                opacity=1.0,
                on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
            ),
        ],
    )

    # Debug print to confirm button grid creation
    print(f"Button grid controls: {len(button_grid.controls)} buttons")

    # Main content container
    dashboard_content = ft.Container(
        content=ft.Column(
            [
                # title,
                ft.Container(
                    content=button_grid,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=10,
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        spread_radius=3,
                        color=ft.Colors.BLACK26,
                    ),
                    margin=ft.margin.symmetric(horizontal=10, vertical=20),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        width=min(page.width, 360),
        alignment=ft.alignment.center,
    )

    # Stack the gradient background and content
    return ft.Stack(
        [
            background,
            dashboard_content,
        ],
        expand=True,
    )