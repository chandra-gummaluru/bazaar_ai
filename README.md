# 🐪 Bazaar

**Bazaar** is a lightweight and extensible implementation of the board game *Jaipur*, designed specifically for training reinforcement learning (RL) agents. It simulates the core mechanics and strategic depth of the original game while offering a clean API for custom agents and learning environments.

## 🎯 Purpose

The library provides a fully functioning game loop for *Jaipur* with minimal dependencies and an object-oriented design. It focuses on:

- Modeling legal actions and transitions  
- Enforcing game rules (e.g. hand size, camel rules, bonus tokens)  
- Supporting self-play and agent-vs-agent training  
- Allowing custom agents

---

## 🧠 Why Jaipur?

*Jaipur* is a two-player trading game with:

- A small but rich action space  
- Partial observability  
- Long-term planning  
- Fast episode turnaround  

This makes it a great environment for RL research in small domains, especially for curriculum learning, zero-shot transfer, and strategy learning.

---

## ⚙️ Features

- ✅ Complete implementation of Jaipur rules  
- ✅ Action types: `Trade`, `Sell`, `Take` and `Herd`
- ✅ Reward structure via `Satchel` (points)  
- ✅ Legal action checking  
- ✅ Game state transition simulation  
- ✅ Easily serializable state for observation modeling  
- ✅ Modular object design (`Player`, `Market`, `Card`, `Trade`, `Purse`, etc.)  
- ✅ No UI (designed for programmatic play)  

---

## 🚀 Quick Start

```python
from bazaar import Game, RandomAgent

game = Game(agent1=RandomAgent(), agent2=RandomAgent())
winner, history = game.play()
print(f"Winner: {winner}")
```