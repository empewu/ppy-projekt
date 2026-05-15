class GameError(Exception):
    pass

class PlayerDeadError(GameError):
    pass

class InvalidMoveError(GameError):
    pass