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
        self.score=player_data[0]
        self.hits=player_data[1]
        self.crits=player_data[2]
        self.crit_chance=player_data[3]
        self.name=player_data[4]
        self.player_data = player_data

    def save(self):
        """save a player to database"""
        conn = connect("saves.db")
        cursor = conn.cursor()

        query = "SELECT * FROM " + DATABASE_TABLENAME + " WHERE player_id=?;"
        datas = (self.player_id,)
        cursor.execute(query, datas)
        results = cursor.fetchall()
        self.player_data = (self.score, self.hits, self.crits, self.crit_chance, self.name)

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
        profile = PlayerProfile(results[0][0],(
                                results[0][1],
                                 results[0][2],
                                 results[0][3],
                                 results[0][4],
                                 results[0][5]))
        return profile

    def setscore(self,newscore):
        """setter of score"""
        self.score = newscore

    def sethits(self,newhits):
        """setter of score"""
        self.hits = newhits
