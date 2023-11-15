"""Player Profile module, provides player profile functionality in a class."""
from sqlite3 import connect

DATA = ("score", "hits", "crits", "crit_chance", "name")
FIELDS = ("player_id",) + DATA
FIELDS_COUNT = len(FIELDS)
DATABASE_FILENAME = "saves.db"
DATABASE_TABLENAME = "players"


class PlayerProfile:
    """This is where player data goes..."""

    def __init__(self, player_id=1, player_data=(0,0,0,10,"Bouncer")):
        self.player_id = player_id
        self.player_data = player_data
        # self.score = score
        # self.hits = hits
        # self.crits = crits
        # self.crit_chance = crit_chance
        # self.name = name

    def save(self):
        """save a player to database"""
        conn = connect("saves.db")
        cursor = conn.cursor()

        query = "SELECT * FROM " + DATABASE_TABLENAME + " WHERE player_id=?;"
        datas = (self.player_id,)
        print(f"query: {query} === data: {datas}")
        cursor.execute(query, datas)
        results = cursor.fetchall()

        if not results:
            query = (
                f"INSERT INTO {DATABASE_TABLENAME} VALUES ({"?, " * (FIELDS_COUNT - 1)}?);"
            )
            datas = (self.player_id,)+self.player_data
        else:
            query = (
                "UPDATE "
                + DATABASE_TABLENAME
                + " SET "
                + ("%s=?, " * (FIELDS_COUNT - 1))
                + "%s=? WHERE player_id=?;"
            )
            datas = (self.player_id,)+self.player_data+(self.player_id,)
            query = query % FIELDS
        print(f"query: {query} === data: {datas}")
        cursor.execute(query, datas)
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
        print(f"results: {results}")
        profile = PlayerProfile(results.player_id,
                                (results.score,
                                 results.hits,
                                 results.crits,
                                 results.crit_chance,
                                 results.name))
        return profile
