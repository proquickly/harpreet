import duckdb
DATA = "/Users/andy/data/duckdb/brie"
population = duckdb.read_csv(DATA + "/world_population.csv")
print(population.describe())
print(population.columns)
print(population.dtypes)
print(type(population))

con = duckdb.connect()
con.execute(
    f"CREATE TABLE population AS SELECT * FROM read_csv_auto('{DATA}/world_population.csv')")

result = con.execute("SELECT * FROM population").fetchall()

print(result)
con.execute(
    f"""drop 
            table if exists 
        population; 
        
        CREATE 
        TABLE population AS 
        SELECT 
            * 
        FROM read_csv_auto('{DATA}/world_population.csv')
"""
)
