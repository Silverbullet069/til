""" Run this script after build_database.py since it needs tils.db """

'''
@File    :   update_readme.py
@Time    :   2024-12-04 22:03:31
@Author  :   Silverbullet069
@Version :   1.0
@License :   MIT License
@Desc    :   Update README.md to reflect tils.db. Credit goes to Simon Willison for logic and Claude 3.5 Sonnet for comments
'''

import pathlib
import sqlite3
import sys
import re
root = pathlib.Path(__file__).parent.resolve()

# Compiles regular expressions to match the sections in README.md that need to be replaced:
# - toc_re matches the block containing the table of contents.
# - count_re matches the block containing the count of TILs.
# - index_re matches the block containing the index of topics.
toc_re = re.compile(
    r"<!\-\- toc starts \-\->.*<!\-\- toc ends \-\->", re.DOTALL)
index_re = re.compile(
    r"<!\-\- index starts \-\->.*<!\-\- index ends \-\->", re.DOTALL)
til_count_re = re.compile(
    r"<!\-\- til count starts \-\->.*<!\-\- til count ends \-\->", re.DOTALL)

# separate template from code, use .format()
COUNT_TEMPLATE = "<!-- count starts -->{}<!-- count ends -->"

if __name__ == "__main__":
    # Load db
    db_path = root / "tils.db"
    by_topic = {}

    with sqlite3.connect(db_path) as conn: # transaction
        conn.row_factory = (
            sqlite3.Row
        )
        cursor = conn.cursor()

        # create topic list by using GROUP command
        topic_count_rows = cursor.execute("SELECT topic, COUNT(*) as count FROM til GROUP BY topic").fetchall()

        if len(topic_count_rows) == 0:
            assert False, "There is not a single row inside your database! Plase run build_database.py for the first time!"

        topic_count = topic_count_rows[0]["count"]
        
    # Group db to create a dict whose keys are topics name
    # Traverse db to populate value for each key - an array of indexes with a predefined structure
    # Replace current ToC with dict's list of keys, sort by alphabet (if the db was sorted, this is not needed)
    # Replace current TIL count with the total number of entries inside tils.db
    # Replace current indexes with the dict's list of values, sort by alphabet (if the db was sorted, this is not needed)
    pass
