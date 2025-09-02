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

    # Title (commented out to avoid AppBar conflict)
    # title = ft.Container(
    #     content=ft.Text(
    #         "AKBER TIKKA Dashboard",
    #         size=24,
    #         weight=ft.FontWeight.BOLD,
    #         color=ft.Colors.WHITE,
    #         text_align=ft.TextAlign.CENTER,
    #         font_family="Roboto",
    #     ),
    #     shadow=ft.BoxShadow(
    #         blur_radius=8,
    #         spread_radius=1,
    #         color=ft.Colors.BLACK26,
    #     ),
    #     padding=8,
    #     margin=ft.margin.only(top=10, bottom=10),
    # )

    # Card list in a Column
    card_list = ft.Column(
        controls=[
            ft.GestureDetector(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.RESTAURANT_MENU, color=ft.Colors.BLUE_700, size=30),
                                ft.Text("Order", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        width=340,
                    ),
                    elevation=6,
                    color=ft.Colors.BLUE_50,
                ),
                on_tap=lambda e: page.go("/menu"),
                on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
            ),
            ft.GestureDetector(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.MONETIZATION_ON, color=ft.Colors.GREEN_700, size=30),
                                ft.Text("Sale", color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD, size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        width=340,
                    ),
                    elevation=6,
                    color=ft.Colors.GREEN_50,
                ),
                on_tap=lambda e: page.go("/sale"),
                on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
            ),
            ft.GestureDetector(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.MONEY_OFF, color=ft.Colors.AMBER_700, size=30),
                                ft.Text("Expense", color=ft.Colors.AMBER_700, weight=ft.FontWeight.BOLD, size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        width=340,
                    ),
                    elevation=6,
                    color=ft.Colors.AMBER_50,
                ),
                on_tap=lambda e: page.go("/expense"),
                on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
            ),
            ft.GestureDetector(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.MENU_BOOK, color=ft.Colors.PURPLE_700, size=30),
                                ft.Text("Menu", color=ft.Colors.PURPLE_700, weight=ft.FontWeight.BOLD, size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        width=340,
                    ),
                    elevation=6,
                    color=ft.Colors.PURPLE_50,
                ),
                on_tap=lambda e: page.go("/menu"),
                on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
            ),
            ft.GestureDetector(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.ADD_SHOPPING_CART, color=ft.Colors.ORANGE_700, size=30),
                                ft.Text("Add Product", color=ft.Colors.ORANGE_700, weight=ft.FontWeight.BOLD, size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        width=340,
                    ),
                    elevation=6,
                    color=ft.Colors.ORANGE_100,
                ),
                on_tap=lambda e: page.go("/products"),
                on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
            ),
            ft.GestureDetector(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.LIST_ALT, color=ft.Colors.TEAL_700, size=30),
                                ft.Text("Orders", color=ft.Colors.TEAL_700, weight=ft.FontWeight.BOLD, size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        width=340,
                    ),
                    elevation=6,
                    color=ft.Colors.TEAL_50,
                ),
                on_tap=lambda e: page.go("/orders"),
                on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

    # Debug print
    print(f"Card list controls: {len(card_list.controls)} cards")

    # Main content container
    dashboard_content = ft.Container(
        content=ft.Column(
            [
                # title,  # Commented to avoid AppBar conflict
                ft.Container(
                    content=card_list,
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
