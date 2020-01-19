##TODO

- Message handling algorithm - DONE
  - Player 1 move: 1, MOVE, x, y
  - All players receive this message
  - Player 2 processes this and sends a response, Player 1 ignores it
  - Player 2 responds: 2, RESP, HIT, ship
  - The response is sent, and the opponent guesses are added when the response is received.
  - Player 1 receives the response, and updates its player guesses.
  - On receiving a response, the next turn is triggered.
  - If a ship is sunk, a SINK message is sent.
  - Player 1 receives the response, and updates its player guesses. Then adds a ship to its opponent ships.
  - Player 2 receives the response, and updates its opponents guesses. Can add a sunk ship here too.
 
 - ~~Need to decide the flow with responses. SINK can be incorporated into the RESP process.~~ DONE
 
 - ~~Ensure all dict keys are strings~~ DONE

 - ~~Tidy up _ship_tiles~~ DONE
 
 - Add a header row with info about the state of the game, e.g opponents turn.
 
 - Add menu screen
 
 - Add end game functionality
    - "You Win/Lose" icon
    - Return to main menu
    - The other player has left the game