"""Player Profile module, provides player profile functionality in a class."""
from sqlite3 import connect

DATA = ("score", "hits", "crits", "crit_chance", "name")
FIELDS = ("player_id",) + DATA
FIELDS_COUNT = len(FIELDS)
DATABASE_FILENAME = "saves.db"
DATABASE_TABLENAME = "players"


class PlayerProfile:
    """This is where player data goes..."""
    player_id=0
    score=0
    hits=0
    crits=0
    crit_chance=0
    name="Bouncer"

    def __init__(self, player_id=0, score=0, hits=0, crits=0, crit_chance=10, name="Bouncer"):
        self.player_id = player_id
        self.score = score
        self.hits = hits
        self.crits = crits
        self.crit_chance = crit_chance
        self.name = name

    def save(self):
        """save a player to database"""
        conn = connect("saves.db")
        cursor = conn.cursor()

        query = "SELECT * FROM " + DATABASE_TABLENAME + " WHERE id=?;"
        data = (self.player_id,)
        cursor.execute(query, data)
        results = cursor.fetchall()

        if not results:
            query = (
                f"INSERT INTO {DATABASE_TABLENAME} VALUES ({"?, " * (FIELDS_COUNT - 1)}?);"
            )
        else:
            query = (
                "UPDATE "
                + DATABASE_TABLENAME
                + " SET "
                + ("%s=?, " * (FIELDS_COUNT - 1))
                + "%s=? WHERE ID=?;"
            )
            query = query % FIELDS
        data=encode(self)

        cursor.execute(query, data)
        conn.commit()
        conn.close()

    def load(self, player_id=1):
        """
        :return: player profile loaded from db
        """
        conn = connect(DATABASE_FILENAME)
        cursor = conn.cursor()

        query = (
            "CREATE TABLE IF NOT EXISTS "
            + DATABASE_TABLENAME
            + " ("
            + ("%s, " * (FIELDS_COUNT - 1))
            + "%s);"
        )
        query = query % FIELDS
        cursor.execute(query)
        conn.commit()

        query = "SELECT * FROM " + DATABASE_TABLENAME + " WHERE player_id=?;"
        cursor.execute(query, (player_id,))
        conn.commit()
        results = cursor.fetchall()
        if not results:
            self = PlayerProfile()
        else:
            decode()

        conn.close


    def decode():
        """turns database coded data into player data"""        

    def encode(self):
        """turns player data into database coded data"""
        return {
        "player_id": self.player_id,
        "score": self.score,
        "hits": self.hits,
        "crits": self.crits,
        "crit_chance": self.crit_chance,
            "name": self.name,
        }
