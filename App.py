import reflex as rx
import csv

class Card(rx.Base):
    name: str
    type: str
    details: dict

class State(rx.State):
    cards: list[Card] = []
    deck: list[tuple[Card, int]] = []
    
    def __init__(self):
        super().__init__()
        self.load_cards()

    def load_cards(self):
        with open('RoG Base de Datos 0.3 by MatyKyng .xlsx - Datos Base.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.cards.append(Card(name=row['Nombre'], type=row['Tipo'], details=row))

    def add_to_deck(self, card: Card):
        for i, (deck_card, count) in enumerate(self.deck):
            if deck_card.name == card.name:
                self.deck[i] = (deck_card, count + 1)
                return
        self.deck.append((card, 1))

    def remove_from_deck(self, card: Card):
        self.deck = [(c, count) for c, count in self.deck if c.name != card.name]

    def increase_card_count(self, card: Card):
        self.deck = [(c, count + 1 if c.name == card.name else count) for c, count in self.deck]

    def decrease_card_count(self, card: Card):
        self.deck = [(c, count - 1 if c.name == card.name and count > 1 else count) for c, count in self.deck]
        self.deck = [(c, count) for c, count in self.deck if count > 0]

    def copy_deck_to_clipboard(self):
        deck_list = [f"{count}x {card.name}" for card, count in self.deck]
        return "\n".join(deck_list)

def card_view(card: Card):
    return rx.vstack(
        rx.text(f"{card.name} - {card.type}"),
        rx.hstack(
            rx.button("Añadir", on_click=lambda: State.add_to_deck(card)),
            rx.button("Ver", on_click=rx.window_alert(str(card.details))),
        )
    )

def deck_card_view(card: Card, count: int):
    return rx.hstack(
        rx.text(f"{card.name} - {card.type}"),
        rx.text(str(count)),
        rx.button("-", on_click=lambda: State.decrease_card_count(card)),
        rx.button("+", on_click=lambda: State.increase_card_count(card)),
        rx.button("Eliminar", on_click=lambda: State.remove_from_deck(card)),
    )

def index():
    return rx.vstack(
        rx.heading("Creador de Mazos TCG"),
        rx.hstack(
            rx.vstack(
                rx.heading("Cartas Disponibles"),
                rx.vstack(
                    rx.foreach(State.cards, card_view)
                )
            ),
            rx.vstack(
                rx.heading("Mazo"),
                rx.text(f"Cartas en el mazo: {sum(count for _, count in State.deck)}"),
                rx.vstack(
                    rx.foreach(State.deck, lambda item: deck_card_view(item[0], item[1]))
                ),
                rx.button(
                    "Copiar Mazo", 
                    on_click=rx.set_clipboard(State.copy_deck_to_clipboard())
                )
            )
        )
    )

app = rx.App(state=State)
app.add_page(index)
app._compile