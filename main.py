import random

class SolitaireEngine:
    def __init__(self):
        # %% PRELIM
        self.searches = 0
        self.move_counter = 0
        self.consecutive_draw_rotations = 0
        
        self.suits = ['Bs', 'Rh', 'Bc', 'Rd'] 
        self.values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        self.deck = []
        for suit_name in self.suits:
            for value_name in self.values:
                self.deck.append(value_name + suit_name)

        random.shuffle(self.deck)

        # Create piles
        self.pile1 = self.deck[0:1]
        self.pile2 = self.deck[1:3] 
        self.pile3 = self.deck[3:6] 
        self.pile4 = self.deck[6:10]
        self.pile5 = self.deck[10:15]
        self.pile6 = self.deck[15:21]
        self.pile7 = self.deck[21:28]
        self.piles = [self.pile1, self.pile2, self.pile3, self.pile4, self.pile5, self.pile6, self.pile7]

        # Draw pile
        self.draw = self.deck[28:]

        # Final stacks
        self.Spades = []
        self.Hearts = []
        self.Clubs = [] 
        self.Diamonds = []
        self.stacks = [self.Spades, self.Hearts, self.Clubs, self.Diamonds]
        self.stack_labels = ['Spades', 'Hearts', 'Clubs', 'Diamonds']

        self.stacks_dict = {
            'Spades': self.Spades,
            'Hearts': self.Hearts,
            'Clubs': self.Clubs,
            'Diamonds': self.Diamonds
        }

        # Face up cards logic
        self.revealed = []
        for p in self.piles:
            self.revealed.append(p[-1])
        if self.draw:
            self.revealed.append(self.draw[-1])

    # --- HELPER METHODS ---

    def colour(self, card):
        if card[-2] == 'B':
            return 'Black'
        else:
            return 'Red'

    def suit(self, card):
        if card[-1] == 's':
            return 'Spades'
        elif card[-1] == 'h':
            return 'Hearts'
        elif card[-1] == 'c':
            return 'Clubs'
        elif card[-1] == 'd':
            return 'Diamonds'

    def value(self, card):
        return card[:-2]

    def stack_lookup(self, suit_name):
        return self.stacks_dict[suit_name]

    def revealed_list(self, pile):
        print_pile = []
        for card in pile:
            if card in self.revealed:
                print_pile.append(card)
            else:
                print_pile.append('X') 
        return print_pile

    def draw_rotation(self):
        self.draw.insert(0, self.draw.pop())
        self.revealed.append(self.draw[-1])

    def move_card(self, pile1, pile2, depth):
        chunk = pile1[-depth:]
        pile2.extend(chunk)
        del pile1[-depth:]
        if pile1:
            if pile1[-1] not in self.revealed:
                self.revealed.append(pile1[-1])

    def show_table(self):
        for index, val in enumerate(self.stacks):
            print(f'{self.stack_labels[index]}: {val}')
        print('\nDraw:')
        if len(self.draw) > 12:
            print(self.revealed_list(self.draw[:12]))
            print(self.revealed_list(self.draw[12:]))
        else:
            print(self.revealed_list(self.draw))
        print('\n')
        for index, val in enumerate(self.piles):
            print(f'{index+1}: {self.revealed_list(val)}')
        print('\n')

    def neighbouring_values(self, card1, card2):
        index1 = self.values.index(self.value(card1))
        index2 = self.values.index(self.value(card2))
        return (index2 - index1) == 1
        
    def opposite_colours(self, card1, card2):
        return self.colour(card1) != self.colour(card2)
        
    def move_to_stack(self, pile, suit1):
        target_stack = self.stacks_dict[suit1]
        self.move_card(pile, target_stack, 1)
        if pile == self.draw:
            print(f'Next card moved to {suit1}')
        else:
            print(f'Pile {self.piles.index(pile)+1} end card moved to {suit1}')

    def num_revealed(self, pile):
        if not pile: return 0
        count = [card for card in pile if card in self.revealed]
        return len(count)

    def head_card(self, pile):
        if pile:
            if pile == self.draw:
                return self.draw[-1], 1
            else:
                depth = self.num_revealed(pile)
                return pile[-depth], depth
        return None, 0

    # --- MAIN ENGINE LOGIC ---

    def alpha_go_solitaire(self):
        self.searches += 1

        # 1. Draw card is Ace
        if self.draw and self.value(self.draw[-1]) == 'A':
            self.move_counter += 1
            self.consecutive_draw_rotations = 0
            self.move_to_stack(self.draw, self.suit(self.draw[-1]))
            return

        # 2. Pile card is Ace
        for pile in self.piles:
            if pile and self.value(pile[-1]) == 'A':
                self.move_counter += 1
                self.move_to_stack(pile, self.suit(pile[-1]))
                return
                
        # 3. King to empty pile
        for pile in self.piles:
            if not pile:
                piles2 = self.piles.copy()
                piles2.remove(pile)
                piles2.append(self.draw)
                for pile2 in list(reversed(piles2)):
                    h_card, depth = self.head_card(pile2)
                    if h_card and self.value(h_card) == 'K' and pile2[0] != h_card:
                        self.move_counter += 1
                        if pile2 == self.draw:
                            self.consecutive_draw_rotations = 0
                        self.move_card(pile2, pile, depth)
                        print(f"King card(s) moved to Pile {self.piles.index(pile)+1}")
                        return

        # 4-10 (Generalized Loop for 2 through K)
        rank_logic = ['2','3','4','5','6','7','8','9','10','J','Q','K']
        for i, rank in enumerate(rank_logic):
            required_len = i + 1 # 2 needs len 1, 3 needs len 2, etc.
            
            if self.draw and self.value(self.draw[-1]) == rank and len(self.stack_lookup(self.suit(self.draw[-1]))) == required_len:
                self.move_counter += 1
                self.consecutive_draw_rotations = 0
                self.move_to_stack(self.draw, self.suit(self.draw[-1]))
                return
            
            for pile in self.piles:
                if pile and self.value(pile[-1]) == rank and len(self.stack_lookup(self.suit(pile[-1]))) == required_len:
                    self.move_counter += 1
                    self.move_to_stack(pile, self.suit(pile[-1]))
                    # Check win condition specifically on King move
                    if rank == 'K':
                        if all(len(s) == 13 for s in self.stacks):
                            print('\n')
                            self.show_table()
                            self.searches += 1 
                            print(f'\nWon in {self.move_counter} moves, you go girl :)')
                    return

        # 6 & 7. Move cards between piles
        piles1 = self.piles.copy()
        for pile01 in list(reversed(piles1)):
            piles2 = self.piles.copy()
            piles2.remove(pile01)
            for pile02 in list(reversed(piles2)):
                if not pile01 or not pile02: continue
                
                # Single card move
                if (len(pile01) == 1 or (len(pile01) > 1 and pile01[-2] not in self.revealed)) \
                    and self.neighbouring_values(pile01[-1], pile02[-1]) \
                    and self.opposite_colours(pile01[-1], pile02[-1]):
                    self.move_counter += 1
                    self.move_card(pile01, pile02, 1)
                    print(f'Pile {self.piles.index(pile01)+1} end card moved to Pile {self.piles.index(pile02)+1}')
                    return
                
                # Chunk move
                h_card, depth = self.head_card(pile01)
                if h_card and self.neighbouring_values(h_card, pile02[-1]) \
                    and self.opposite_colours(h_card, pile02[-1]):
                    self.move_counter += 1
                    self.move_card(pile01, pile02, depth)
                    print(f"chunk moved to pile {self.piles.index(pile02)+1}")
                    return

        # 8. Draw card down to pile
        for pile in self.piles:
            if pile and self.draw and self.neighbouring_values(self.draw[-1], pile[-1]) \
                and self.opposite_colours(self.draw[-1], pile[-1]):
                self.move_counter += 1
                self.consecutive_draw_rotations = 0
                self.move_card(self.draw, pile, 1)
                print('Draw card moved to Pile', self.piles.index(pile)+1)
                return

        # Rotation if no moves found
        if self.searches > self.move_counter:
            self.consecutive_draw_rotations += 1
            self.move_counter += 1
            if self.draw:
                self.draw_rotation()
                print("Next draw card")
                return

def main():
    game = SolitaireEngine()
    game.show_table()

    # Game loop
    while game.searches == game.move_counter and game.consecutive_draw_rotations <= len(game.draw):
        print('\n')
        game.show_table()
        game.alpha_go_solitaire()

if __name__ == "__main__":
    main()