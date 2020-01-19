# Battleships

This is a simple online python game using pygame. I developed it to get a feel for sockets so 
and threading that I could use them in a chess game I was working on. As it turned out, the networking involved 
for battleships was (slightly) more complicated than I would have needed for a chess client.

### Prerequisites

- pygame

### Installing

- clone the repo
- run server.py
- run main.py to join

### Joining a Game

At the moment, the game is configured to play on the same machine. To play on different machines,
you must manually set the server IP in client.py. The port is set to 33000.