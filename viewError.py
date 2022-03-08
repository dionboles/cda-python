import pandas as pd
import sqlite3

conn = sqlite3.connect(".pymon")
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';",conn)
table_session = pd.read_sql_query("""
SELECT 
	ITEM_START_TIME,
	ITEM,
	KIND,
	MEM_USAGE,
	CPU_USAGE
FROM
	TEST_METRICS 
		LEFT JOIN 
		TEST_SESSIONS
		ON TEST_METRICS.SESSION_H = TEST_SESSIONS.SESSION_H

""",conn)

print(tables.head())
print(table_session)