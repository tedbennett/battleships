##TODO

- Redo message handling
  - Player 1 move: 1, MOVE, x, y
  - All players receive this message
  - Player 2 processes this and sends a response, Player 1 ignores it
  - Player 2 responds: 2, RESP, HIT, ship
  - During the response processing, the guess is added to the opponent guesses.
    - OR the response is sent, and the opponent guesses are added when the response is received.
  - Player 1 receives the response, and updates its player guesses.
  - On receiving a response, the next turn is triggered.
  - If a ship is sunk, a SINK message is sent.
  - Player 1 receives the response, and updates its player guesses. Then adds a ship to its opponent ships.
  - Player 2 receives the response, and updates its opponents guesses. Can add a sunk ship here too.
 
 - Need to decide the flow with responses. SINK can be incorporated into the RESP process.
 
 - Ensure all dict keys are strings