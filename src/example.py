from bazaar_ai.bazaar import BasicBazaar, Trader

trader1 = Trader(seed = 0,
                 name = "Caveman")
trader2 = Trader(seed = 0, 
                 name = "Villager")

traders = {
    trader1.id: trader1,
    trader2.id: trader2
}

game = BasicBazaar(
    seed = 0,
    players = traders,
)

game.play()


