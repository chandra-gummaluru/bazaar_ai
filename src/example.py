from bazaar_ai.bazaar import BasicBazaar, Trader

trader1 = Trader(seed = 356,
                 name = "Caveman")
trader2 = Trader(seed = 12, 
                 name = "Villager")

traders = [trader1, trader2]

game = BasicBazaar(
    seed = 43646,
    players = traders,
)

game.play()


