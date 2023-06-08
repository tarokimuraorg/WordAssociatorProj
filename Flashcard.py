from dataclasses import dataclass

@dataclass(frozen=True)
class Flashcard:
    
    head_word : str = ''
    tail_word : str = ''
    weight : int = 0
