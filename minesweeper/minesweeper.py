import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other): 
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        '''works on the basis that is a set in knowledge has the same number of moves as the value of count then it knows for sure that those moves are mines'''

        if len(self.cells) == self.count:
            return set(self.cells)
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        '''when in runner a certain block is pressed and it reveals 0 then its neighbours are bound to be safe'''

        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        '''marks by removing cell from cells and then reducing the count'''
        if cell in self.cells:
            self.cells.remove(cell)
            if self.count>0:
                self.count-=1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        '''to prevent the function from running if move already made'''
        if cell in self.moves_made:
            return None

        self.moves_made.add(cell) # step1 add to moves_made
        self.mark_safe(cell) # step2 marking it safe 
            
        i,j = cell
        ''' this gets the neighbours of the cell that was clicked
            the grid of cells around the cell
            prevents the same cell from adding again and prevents out of bound cells''' 
        neighbours = set()
        for row in range(i-1, i+2):
            for column in range(j-1, j+2):
                if (0 <= row < self.height) and (0 <= column < self.width) and (row, column) != (i, j):
                    neighbours.add((row, column))

        new_count = count # for making a copy of count for manipulating ahead

        for safe in self.safes: # remove any cells from neighbours if they are already marked as safe
            if safe in neighbours:
                neighbours.remove(safe)

        for mine in self.mines: # remove any cells from neighbours if they are alreasy marked as mine
            if mine in neighbours:
                neighbours.remove(mine)
                if new_count>0:
                    new_count-=1

        s = Sentence(neighbours, new_count) #using the last data to make an object of Sentence() class

        if s.cells: # if 's' is not empty we append it to the knowledge base
            self.knowledge.append(s)
        
        ''' this loop runs until no new instance of safes or mines are left
            new_safes and new_mines are sets
            they are updated by the putting the known safes and mines in them for each sentence in knowledge base'''
        changed = True
        while changed:
            changed = False
            new_safes = set()
            new_mines = set()

            for sentence in self.knowledge:
                new_safes.update(sentence.known_safes())
                new_mines.update(sentence.known_mines())

            ''' this loop runs for all safe cells in new_safes
                then adds them in safes if they are not already present'''
                
            for sa in new_safes:
                if sa not in self.safes:
                    self.mark_safe(sa)
                    changed = True

            ''' this loop runs for all mine cells in new_mines
                then adds them in mines if they are not already present'''
            
            for m in new_mines:
                if m not in self.mines:
                    self.mark_mine(m)
                    changed = True

            #changed here is turned true all the time except when there are no new instances which means it remains false and the loop ends

        new_s = [] # this is a form of new knowledge base that will be added to self.knowledge

        ''' these loops run to check and compare all sentences in self.knowledge with eachother
            it works on the rule of subsets
            if cells of s2 are a subset of cells of s1, then we subtract them and remove from the count'''

        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 == s2:
                    continue

                if s1.cells.issubset(s2.cells):
                    inferred_cells = s2.cells - s1.cells
                    inferred_count = s2.count - s1.count

                    new_sentence = Sentence(inferred_cells, inferred_count)

                    if new_sentence not in self.knowledge and new_sentence.cells:
                        new_s.append(new_sentence)

        # after that is done we append that formed sentence to the knowledge base
        self.knowledge.extend(new_s)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        choices = []

        # forms a list of choices that are not known mines and are not already made moves
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.mines and (i,j) not in self.moves_made:
                    choices.append((i,j))

        # if choices is not empty then we return a random move
        if choices:
            return random.choice(choices)
        return None
