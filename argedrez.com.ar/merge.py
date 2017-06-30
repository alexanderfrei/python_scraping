import os
os.chdir("D:/chess_db/to_merge")

i = 0
with open('../2013.pgn', 'w') as db:
    for pgn in os.listdir():
        with open(pgn, 'r') as cur_db:
            db.write(cur_db.read())
            i += 1
            print("{}. {} done ".format(i, pgn))
