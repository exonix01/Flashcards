import os
import random
import argparse


class Card:

    def __init__(self, card, definition, errors=0):
        self.card = card
        self.definition = definition
        self.errors = int(errors)

    def check_answer(self, cards, logs):
        answer = input_and_logs(logs)
        if self.definition == answer:
            print_and_logs(logs, 'Your answer is correct!')
            return
        for card in cards:
            if answer == card.definition:
                print_and_logs(logs,
                               f'Your answer is wrong! The right answer is {self.definition}, but your definition is '
                               f'correct for "{card.card}"')
                self.errors += 1
                return
        print_and_logs(logs, f'Your answer is wrong! The right answer is {self.definition}')
        self.errors += 1

    def ask_user(self, logs):
        print_and_logs(logs, f'Print the definition of "{self.card}"')

    def wrongs_reset(self):
        self.errors = 0


def print_and_logs(logs, text):
    print(text)
    logs.append(text)


def input_and_logs(logs):
    answer = input()
    logs.append(answer)
    return answer


def input_term(cards, logs):
    print_and_logs(logs, 'The card:')
    card_names = [card.card for card in cards]
    while True:
        term = input_and_logs(logs)
        if term in card_names:
            print_and_logs(logs, f'The card "{term}" already exists. Try again:')
            continue
        return term


def input_definition(cards, logs):
    print_and_logs(logs, 'The definition of the card')
    card_names = [card.definition for card in cards]
    while True:
        definition = input_and_logs(logs)
        if definition in card_names:
            print_and_logs(logs, f'The definition "{definition}" already exists. Try again:')
            continue
        return definition


def input_card(cards, logs):
    term = input_term(cards, logs)
    definition = input_definition(cards, logs)
    cards.append(Card(term, definition))
    print_and_logs(logs, f'The pair ("{term}":"{definition}") has been added')


def remove_card(cards, logs):
    print_and_logs(logs, 'Which card?')
    card_for_remove = input_and_logs(logs)
    card_names = [card.card for card in cards]
    if card_for_remove in card_names:
        x = 0
        for card in cards:
            if card_for_remove == card.card:
                break
            x += 1
        cards.pop(x)
        print_and_logs(logs, 'The card has been removed')
    else:
        print_and_logs(logs, f"Can't remove \"{card_for_remove}\" card: there is no such card.")
    return cards


def check_user(card, cards, logs):
    card.ask_user(logs)
    card.check_answer(cards, logs)


def import_cards(cards, logs, path=''):
    print_and_logs(logs, 'File name:')
    if not path:
        path = input_and_logs(logs)
    card_names = [c.card for c in cards]
    if os.path.isfile(path):
        with open(path, 'r') as file:
            n = 0
            for card in file:
                card = card.split()
                if card[0] in card_names:
                    x = 0
                    for c in cards:
                        if c.card == card[0]:
                            break
                        x += 1
                    cards.pop(x)
                    cards.insert(x, Card(*card))
                else:
                    cards.append(Card(*card))
                n += 1
        print_and_logs(logs, f'{n} cards have been loaded.')
    else:
        print_and_logs(logs, 'File not found.')
    return cards


def export_cards(cards, logs, path=''):
    print_and_logs(logs, 'File name:')
    if not path:
        path = input_and_logs(logs)
    with open(path, 'w') as file:
        n = 0
        for card in cards:
            file.write(f'{card.card} {card.definition} {card.errors}\n')
            n += 1
    print_and_logs(logs, f'{n} cards have been saved.')


def ask_user(cards, logs):
    print_and_logs(logs, 'How many times to ask?')
    n = int(input_and_logs(logs))
    for _ in range(n):
        check_user(random.choice(cards), cards, logs)


def save_logs(logs):
    print_and_logs(logs, 'File name:')
    path = input_and_logs(logs)
    print_and_logs(logs, 'The log has been saved.')
    with open(path, 'w') as file:
        for log in logs:
            file.write(str(log) + '\n')


def hardest_card(cards, logs):
    if len(cards) == 0:
        print_and_logs(logs, 'There are no cards with errors.')
    else:
        wrongs = max([int(card.errors) for card in cards])
        hardest_cards = [card for card in cards if int(card.errors) == wrongs]
        if wrongs == 0:
            print_and_logs(logs, 'There are no cards with errors.')
        elif len(hardest_cards) == 1:
            print_and_logs(logs,
                           f'The hardest card is "{hardest_cards[0].card}". You have {wrongs} errors, '
                           f'answering it.')
        else:
            name_hardest = [card.card for card in hardest_cards]
            print_and_logs(logs,
                           f'The hardest cards are {", ".join(name_hardest)}. You have {wrongs} errors, '
                           f'answering it.')


def reset_stats(cards, logs):
    for card in cards:
        card.errors = 0
    print_and_logs(logs, 'Cards statistics have been reset')


def main():
    cards = []
    logs = []

    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from')
    parser.add_argument('--export_to')
    args = parser.parse_args()
    if args.import_from:
        import_cards(cards, logs, args.import_from)


    while True:
        print_and_logs(logs, 'Input the action (add, remove, import, export, ask, exit, log, hardest card, '
                             'reset stats):')
        answer = input_and_logs(logs)
        if answer == 'add':
            input_card(cards, logs)
        elif answer == 'remove':
            cards = remove_card(cards, logs)
        elif answer == 'import':
            cards = import_cards(cards, logs)
        elif answer == 'export':
            export_cards(cards, logs)
        elif answer == 'ask':
            ask_user(cards, logs)
        elif answer == 'exit':
            if args.export_to:
                export_cards(cards, logs, args.export_to)
            print_and_logs(logs, 'Bye bye!')
            break
        elif answer == 'log':
            save_logs(logs)
        elif answer == 'hardest card':
            hardest_card(cards, logs)
        elif answer == 'reset stats':
            reset_stats(cards, logs)
        else:
            print_and_logs(logs, 'Incorrect action!')
        print_and_logs(logs, '')
        continue


if __name__ == '__main__':
    main()
