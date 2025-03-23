# 🐪 Bazaar

**Bazaar** is a lightweight, extensible simulation of the *Jaipur* board game, specifically designed for training reinforcement learning (RL) agents. It replicates the core mechanics and strategic depth of the original *Jaipur* game while providing a clean and easy-to-use API for custom agents, facilitating the development of RL environments.

## 🎯 Purpose

The library provides a fully functional, object-oriented implementation of the *Jaipur* game loop with minimal dependencies. It focuses on key aspects of game modeling and reinforcement learning, including:

- **Modeling  Actions and Transitions**: Accurately simulating possible player actions and game state transitions.
- **Enforcing All Game Rules**: Ensures all gameplay mechanics are adhered to.
- **Custom Agent Integration**: Supports easy integration of custom RL agents, enabling researchers to experiment with different strategies and learning techniques.

By providing a well-structured environment, **Bazaar** offers the flexibility and extensibility necessary to build and train RL agents in a dynamic and competitive setting.

---

## 🧠 Why Jaipur?

*Jaipur* is an engaging two-player trading game that makes it an ideal environment for RL research. Here’s why it’s particularly suitable:

- **Small but Rich Action Space**: While the game has a relatively small number of possible actions, these actions lead to complex decision-making and strategic depth.
- **Partial Observability**: Players don’t have access to the full game state at all times, forcing them to make decisions based on incomplete information, simulating real-world uncertainty.
- **Long-term Planning**: Success depends not only on immediate gains but on long-term strategy, perfect for testing agents that need to plan ahead.
- **Fast Episode Turnaround**: The game’s relatively short length makes it ideal for training agents quickly, with fast iterations and short training cycles.

These characteristics make *Jaipur* an excellent environment for RL research.

---

## ⚙️ Features

- ✅ **Complete Implementation of Jaipur Rules**: All major rules of the *Jaipur* board game are faithfully replicated, ensuring accurate game play.
- ✅ **Game State Transition Simulation**: Accurately models state transitions resulting from player actions, maintaining an up-to-date view of the game state.
- ✅ **Easily Serializable State**: The game state can be serialized to facilitate observation modeling for RL agents.
- ✅ **No UI**: This library is designed for programmatic play without any user interface, allowing for faster, automated training and experimentation.

---

## 🚀 Quick Start

To get started with **Bazaar**, simply import the library, set up your traders (agents), and start a game. Here's a minimal example of how to run a basic game between two random traders:

```python
from bazaar_ai import game, trader, market
from bazaar_ai.terms import GoodTypes, BonusTypes
import random

# Define the traders (players in the game)
# Here we create two traders who each play using a random policy. The Trader class can be extended to include more advanced policies.
trader1 = trader.Trader(
    name="Caveman",
    seed=321,
)
trader2 = trader.Trader(
    name="Villager",
    seed=247,
)

traders = [trader1, trader2]

# Initialize and play a classic game
g = game.ClassicGame(traders)
g.setup()
g.play(verbosity=game.Verbosity.ALL) 

# Display the stats after the game is completed
g.show_stats()
```

To implement custom agents, the `Trader` class can be extended.

```python
from bazaar_ai.trader import Trader

class CustomTrader(Trader):
    def __init__(self, seed, name):
        super()__init__(seed, name)
        
        # add additional data
        pass 
            
    def select_action(self, market_observation):
        """
        Method for selecting an action based on the market observation, the trader's
        hand, and his/her satchel.

        Args:
            market_observation (MarketObservation): The current state of the market.

        Returns:
            Action: The selected action.
        """
        actions = self.get_all_actions(market_observation)
        
        # choose an action
        # based on the market observation, the trader's hand, and his/her satchel
        # appropriate __eq__ functions have been defined for all of these objects
        # these objects also support serialization allowing training data to be saved
        
        pass
```

