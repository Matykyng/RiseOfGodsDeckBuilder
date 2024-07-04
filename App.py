import flet as ft
import csv
import Cython

def main(page: ft.Page):
    page.title = "Creador de Mazos TCG"
    page.theme_mode = "dark"

    # Cargar las cartas desde el CSV
    cards = []
    with open('RoG Base de Datos 0.3 by MatyKyng .xlsx - Datos Base.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cards.append(row)

    # Lista de cartas disponibles
    available_cards = ft.ListView(expand=1, spacing=10, padding=20)
    
    # Lista de cartas en el mazo
    deck_cards = ft.ListView(expand=1, spacing=10, padding=20)

    # Contador de cartas en el mazo
    deck_count = ft.Text("Cartas en el mazo: 0", size=20, weight="bold")

    def update_deck_count():
        count = sum(int(item.controls[1].controls[1].value) for item in deck_cards.controls)
        deck_count.value = f"Cartas en el mazo: {count}"
        page.update()

    def add_to_deck(card):
        for item in deck_cards.controls:
            if item.controls[0].value == f"{card['Nombre']} - {card['Tipo']}":
                increase_card_count(item.controls[1].controls[2])
                return
        
        deck_cards.controls.append(
            ft.Row([
                ft.Text(f"{card['Nombre']} - {card['Tipo']}"),
                ft.Row([
                    ft.IconButton(ft.icons.REMOVE, on_click=decrease_card_count),
                    ft.Text("1"),
                    ft.IconButton(ft.icons.ADD, on_click=increase_card_count),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, c=card: remove_from_deck(c)),
                ]),
                ft.IconButton(ft.icons.VISIBILITY, on_click=lambda _, c=card: view_card(c))
            ])
        )
        update_deck_count()

    def increase_card_count(e):
        row = e.control.parent
        count_text = row.controls[1]
        count = int(count_text.value)
        count_text.value = str(count + 1)
        update_deck_count()

    def decrease_card_count(e):
        row = e.control.parent
        count_text = row.controls[1]
        count = int(count_text.value)
        if count > 1:
            count_text.value = str(count - 1)
            update_deck_count()
        else:
            remove_from_deck(row.parent.controls[0].value.split(" - ")[0])

    def remove_from_deck(card):
        for item in deck_cards.controls:
            if item.controls[0].value.startswith(card['Nombre'] if isinstance(card, dict) else card):
                deck_cards.controls.remove(item)
                break
        update_deck_count()

    def view_card(card):
        def close_dlg(e):
            dlg.open = False
            page.update()

        content = ft.Column([ft.Text(f"{key}: {value}") for key, value in card.items() if value])
        dlg = ft.AlertDialog(
            title=ft.Text(card['Nombre']),
            content=content,
            actions=[
                ft.TextButton("Cerrar", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dlg
        dlg.open = True
        page.update()

    def copy_deck_to_clipboard(e):
        deck_list = []
        for item in deck_cards.controls:
            card_name = item.controls[0].value.split(" - ")[0]
            card_count = item.controls[1].controls[1].value
            deck_list.append(f"{card_count}x {card_name}")
        
        deck_text = "\n".join(deck_list)
        page.set_clipboard(deck_text)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Mazo copiado al portapapeles")))

    for card in cards:
        available_cards.controls.append(
            ft.Row([
                ft.Text(f"{card['Nombre']} - {card['Tipo']}"),
                ft.IconButton(ft.icons.ADD, on_click=lambda _, c=card: add_to_deck(c)),
                ft.IconButton(ft.icons.VISIBILITY, on_click=lambda _, c=card: view_card(c))
            ])
        )

    page.add(
        ft.Row([
            ft.Text("Creador de Mazos", size=30, weight="bold"),
            deck_count
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row(
            [
                ft.Column([ft.Text("Cartas Disponibles"), available_cards], expand=1),
                ft.VerticalDivider(width=1),
                ft.Column([ft.Text("Mazo"), deck_cards], expand=1),
            ],
            expand=True,
        ),
        ft.ElevatedButton("Copiar Mazo", on_click=copy_deck_to_clipboard)
    )

ft.app(target=main)
