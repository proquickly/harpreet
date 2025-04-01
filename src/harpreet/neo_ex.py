# neo_ex.py
# A complete demo program showing the benefits of Neo4j graph database
import time
from neo4j import GraphDatabase
import networkx as nx

class GraphDatabaseDemo:
    def __init__(self, uri=None, username=None, password=None):
        # Default connection parameters if none provided
        self.uri = uri or "bolt://localhost:7687"
        self.username = username or "neo4j"
        self.password = password or "password"

        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            # Test the connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("Connected to Neo4j database successfully")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            self.driver = None
            raise  # Let the caller handle the exception

    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()
            print("Connection to Neo4j closed")

    def clear_database(self):
        """Clear all data from the database"""
        if not self.driver:
            print("No active database connection")
            return False

        try:
            with self.driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                print("Database cleared")
                return True
        except Exception as e:
            print(f"Failed to clear database: {e}")
            return False

    def create_social_network(self):
        """Create a social network dataset"""
        if not self.driver:
            print("No active database connection")
            return False

        try:
            with self.driver.session() as session:
                print("Creating social network dataset...")
                session.run("""
                    CREATE (alice:Person {name: 'Alice', age: 32, interests: ['Music', 'Travel', 'Reading']})
                    CREATE (bob:Person {name: 'Bob', age: 35, interests: ['Sports', 'Music', 'Cooking']})
                    CREATE (charlie:Person {name: 'Charlie', age: 28, interests: ['Travel', 'Photography']})
                    CREATE (david:Person {name: 'David', age: 41, interests: ['Technology', 'Reading']})
                    CREATE (emma:Person {name: 'Emma', age: 29, interests: ['Art', 'Music', 'Travel']})
                    CREATE (frank:Person {name: 'Frank', age: 33, interests: ['Sports', 'Movies']})
                    CREATE (grace:Person {name: 'Grace', age: 37, interests: ['Technology', 'Cooking']})
                    // Create friendships
                    CREATE (alice)-[:FRIEND {since: 2015}]->(bob)
                    CREATE (alice)-[:FRIEND {since: 2018}]->(emma)
                    CREATE (alice)-[:FRIEND {since: 2020}]->(grace)
                    CREATE (bob)-[:FRIEND {since: 2012}]->(charlie)
                    CREATE (bob)-[:FRIEND {since: 2019}]->(david)
                    CREATE (charlie)-[:FRIEND {since: 2017}]->(emma)
                    CREATE (charlie)-[:FRIEND {since: 2016}]->(frank)
                    CREATE (david)-[:FRIEND {since: 2014}]->(grace)
                    CREATE (emma)-[:FRIEND {since: 2021}]->(frank)
                    CREATE (frank)-[:FRIEND {since: 2018}]->(grace)
                    // Create locations
                    CREATE (nyc:City {name: 'New York City'})
                    CREATE (sf:City {name: 'San Francisco'})
                    CREATE (la:City {name: 'Los Angeles'})
                    CREATE (chicago:City {name: 'Chicago'})
                    CREATE (boston:City {name: 'Boston'})
                    // Create lived in relationships
                    CREATE (alice)-[:LIVES_IN {since: 2010}]->(nyc)
                    CREATE (bob)-[:LIVES_IN {since: 2015}]->(nyc)
                    CREATE (charlie)-[:LIVES_IN {since: 2012}]->(sf)
                    CREATE (david)-[:LIVES_IN {since: 2018}]->(la)
                    CREATE (emma)-[:LIVES_IN {since: 2019}]->(chicago)
                    CREATE (frank)-[:LIVES_IN {since: 2014}]->(boston)
                    CREATE (grace)-[:LIVES_IN {since: 2017}]->(sf)
                    // Create visit relationships
                    CREATE (alice)-[:VISITED {year: 2019}]->(sf)
                    CREATE (alice)-[:VISITED {year: 2021}]->(la)
                    CREATE (bob)-[:VISITED {year: 2020}]->(chicago)
                    CREATE (charlie)-[:VISITED {year: 2018}]->(nyc)
                    CREATE (emma)-[:VISITED {year: 2021}]->(nyc)
                    CREATE (emma)-[:VISITED {year: 2019}]->(sf)
                    CREATE (frank)-[:VISITED {year: 2017}]->(la)
                """)
                print("Social network dataset created successfully")
                return True
        except Exception as e:
            print(f"Failed to create social network: {e}")
            return False

    def create_movie_network(self):
        """Create a movie recommendation dataset"""
        if not self.driver:
            print("No active database connection")
            return False

        try:
            with self.driver.session() as session:
                print("Creating movie network dataset...")
                session.run("""
                    // Create users
                    CREATE (user1:User {name: 'User1', age: 25})
                    CREATE (user2:User {name: 'User2', age: 34})
                    CREATE (user3:User {name: 'User3', age: 29})
                    CREATE (user4:User {name: 'User4', age: 42})
                    CREATE (user5:User {name: 'User5', age: 31})
                    
                    // Create movies
                    CREATE (inception:Movie {title: 'Inception', year: 2010, genre: 'Sci-Fi'})
                    CREATE (darkKnight:Movie {title: 'The Dark Knight', year: 2008, genre: 'Action'})
                    CREATE (matrix:Movie {title: 'The Matrix', year: 1999, genre: 'Sci-Fi'})
                    CREATE (pulpFiction:Movie {title: 'Pulp Fiction', year: 1994, genre: 'Crime'})
                    CREATE (forrestGump:Movie {title: 'Forrest Gump', year: 1994, genre: 'Drama'})
                    CREATE (godfather:Movie {title: 'The Godfather', year: 1972, genre: 'Crime'})
                    CREATE (interstellar:Movie {title: 'Interstellar', year: 2014, genre: 'Sci-Fi'})
                    
                    // Create actors
                    CREATE (diCaprio:Actor {name: 'Leonardo DiCaprio'})
                    CREATE (bale:Actor {name: 'Christian Bale'})
                    CREATE (reeves:Actor {name: 'Keanu Reeves'})
                    CREATE (travolta:Actor {name: 'John Travolta'})
                    CREATE (jackson:Actor {name: 'Samuel L. Jackson'})
                    CREATE (hanks:Actor {name: 'Tom Hanks'})
                    CREATE (pacino:Actor {name: 'Al Pacino'})
                    CREATE (mcConaughey:Actor {name: 'Matthew McConaughey'})
                    
                    // Create directors
                    CREATE (nolan:Director {name: 'Christopher Nolan'})
                    CREATE (wachowski:Director {name: 'Lana Wachowski'})
                    CREATE (tarantino:Director {name: 'Quentin Tarantino'})
                    CREATE (zemeckis:Director {name: 'Robert Zemeckis'})
                    CREATE (coppola:Director {name: 'Francis Ford Coppola'})
                    
                    // Create acted_in relationships
                    CREATE (diCaprio)-[:ACTED_IN]->(inception)
                    CREATE (bale)-[:ACTED_IN]->(darkKnight)
                    CREATE (reeves)-[:ACTED_IN]->(matrix)
                    CREATE (travolta)-[:ACTED_IN]->(pulpFiction)
                    CREATE (jackson)-[:ACTED_IN]->(pulpFiction)
                    CREATE (hanks)-[:ACTED_IN]->(forrestGump)
                    CREATE (pacino)-[:ACTED_IN]->(godfather)
                    CREATE (mcConaughey)-[:ACTED_IN]->(interstellar)
                    CREATE (diCaprio)-[:ACTED_IN]->(interstellar)
                    
                    // Create directed relationships
                    CREATE (nolan)-[:DIRECTED]->(inception)
                    CREATE (nolan)-[:DIRECTED]->(darkKnight)
                    CREATE (nolan)-[:DIRECTED]->(interstellar)
                    CREATE (wachowski)-[:DIRECTED]->(matrix)
                    CREATE (tarantino)-[:DIRECTED]->(pulpFiction)
                    CREATE (zemeckis)-[:DIRECTED]->(forrestGump)
                    CREATE (coppola)-[:DIRECTED]->(godfather)
                    
                    // Create rated relationships - Complete ratings for all users
                    CREATE (user1)-[:RATED {rating: 5}]->(inception)
                    CREATE (user1)-[:RATED {rating: 4}]->(darkKnight)
                    CREATE (user1)-[:RATED {rating: 5}]->(matrix)
                    CREATE (user1)-[:RATED {rating: 3}]->(interstellar)
                    
                    CREATE (user2)-[:RATED {rating: 3}]->(inception)
                    CREATE (user2)-[:RATED {rating: 5}]->(pulpFiction)
                    CREATE (user2)-[:RATED {rating: 4}]->(godfather)
                    
                    CREATE (user3)-[:RATED {rating: 4}]->(inception)
                    CREATE (user3)-[:RATED {rating: 5}]->(matrix)
                    CREATE (user3)-[:RATED {rating: 4}]->(darkKnight)
                    CREATE (user3)-[:RATED {rating: 3}]->(forrestGump)
                    
                    CREATE (user4)-[:RATED {rating: 5}]->(godfather)
                    CREATE (user4)-[:RATED {rating: 4}]->(forrestGump)
                    CREATE (user4)-[:RATED {rating: 3}]->(pulpFiction)
                    
                    CREATE (user5)-[:RATED {rating: 5}]->(interstellar)
                    CREATE (user5)-[:RATED {rating: 4}]->(inception)
                    CREATE (user5)-[:RATED {rating: 3}]->(matrix)
                """)
                print("Movie network dataset created successfully")
                return True
        except Exception as e:
            print(f"Failed to create movie network: {e}")
            return False

    def demo_benefit_1_relationships(self):
        """Demonstrate the benefit of handling relationships in graph databases"""
        if not self.driver:
            print("No active database connection")
            return

        print("\n=== DEMO: BENEFIT 1 - NATURAL HANDLING OF RELATIONSHIPS ===")
        try:
            with self.driver.session() as session:
                print("\nFinding friends of friends for Alice (2nd degree connections):")
                result = session.run("""
                    MATCH (alice:Person {name: 'Alice'})-[:FRIEND]->(friend)-[:FRIEND]->(friendOfFriend)
                    WHERE friendOfFriend <> alice
                    RETURN DISTINCT friendOfFriend.name as name
                """)
                friends_of_friends = [record["name"] for record in result]
                print(f"Alice's friends of friends: {', '.join(friends_of_friends)}")

                print("\nFinding movie recommendations based on similar user ratings:")
                result = session.run("""
                    MATCH (user:User {name: 'User1'})-[r1:RATED]->(movie1:Movie)
                    MATCH (otherUser:User)-[r2:RATED]->(movie1)
                    WHERE user <> otherUser AND abs(r1.rating - r2.rating) <= 1
                    MATCH (otherUser)-[r3:RATED]->(recommendedMovie:Movie)
                    WHERE NOT EXISTS((user)-[:RATED]->(recommendedMovie))
                    RETURN DISTINCT recommendedMovie.title as title, AVG(r3.rating) as avgRating
                    ORDER BY avgRating DESC
                    LIMIT 3
                """)
                recommendations = [(record["title"], record["avgRating"]) for record in result]
                print("Movie recommendations for User1:")
                for movie, rating in recommendations:
                    print(f"  - {movie} (Average rating: {rating:.1f})")
        except Exception as e:
            print(f"Error in demo_benefit_1: {e}")

    def demo_benefit_2_pattern_matching(self):
        """Demonstrate the benefit of pattern matching in graph databases"""
        if not self.driver:
            print("No active database connection")
            return

        print("\n=== DEMO: BENEFIT 2 - COMPLEX PATTERN MATCHING ===")
        try:
            with self.driver.session() as session:
                print("\nFinding all actors who worked with director Christopher Nolan:")
                result = session.run("""
                    MATCH (actor:Actor)-[:ACTED_IN]->(:Movie)<-[:DIRECTED]-(director:Director {name: 'Christopher Nolan'})
                    RETURN DISTINCT actor.name as name
                """)
                actors = [record["name"] for record in result]
                print(f"Actors who worked with Christopher Nolan: {', '.join(actors)}")

                print("\nFinding all people who live in one city but visited another:")
                result = session.run("""
                    MATCH (person:Person)-[:LIVES_IN]->(homeCity:City)
                    MATCH (person)-[:VISITED]->(visitedCity:City)
                    WHERE homeCity <> visitedCity
                    RETURN person.name as name, homeCity.name as home, 
                           collect(DISTINCT visitedCity.name) as visited
                    ORDER BY name
                """)
                for record in result:
                    visited_cities = ", ".join(record["visited"])
                    print(f"{record['name']} lives in {record['home']} but visited {visited_cities}")
        except Exception as e:
            print(f"Error in demo_benefit_2: {e}")

    def demo_benefit_3_performance(self):
        """Demonstrate the benefit of performance for connected data in graph databases"""
        if not self.driver:
            print("No active database connection")
            return

        print("\n=== DEMO: BENEFIT 3 - PERFORMANCE FOR CONNECTED DATA ===")
        try:
            with self.driver.session() as session:
                print("\nFinding shortest path between two people:")

                # Measure performance of a complex graph traversal
                start_time = time.time()
                result = session.run("""
                    MATCH p=shortestPath((a:Person {name: 'Alice'})-[*]-(f:Person {name: 'Frank'}))
                    RETURN [node in nodes(p) | coalesce(node.name, node.title)] AS path
                """)
                path_nodes = result.single()["path"]
                duration = time.time() - start_time

                print(f"Shortest path found in {duration:.6f} seconds:")
                print(" -> ".join(path_nodes))

                # Run a complex query that would be difficult in SQL
                start_time = time.time()
                result = session.run("""
                    MATCH (person:Person)
                    OPTIONAL MATCH (person)-[:FRIEND]->(friend:Person)
                    WITH person, count(friend) as friendCount
                    MATCH (person)-[:LIVES_IN]->(city:City)
                    OPTIONAL MATCH (person)-[:VISITED]->(visitedCity:City)
                    RETURN person.name as name, 
                           friendCount,
                           city.name as home,
                           count(DISTINCT visitedCity) as citiesVisited
                    ORDER BY friendCount DESC
                """)
                duration = time.time() - start_time

                print(f"\nComplex social analysis completed in {duration:.6f} seconds:")
                for record in result:
                    print(f"{record['name']} has {record['friendCount']} friends, " +
                          f"lives in {record['home']}, and visited {record['citiesVisited']} cities")
        except Exception as e:
            print(f"Error in demo_benefit_3: {e}")

    def demo_benefit_4_schema_flexibility(self):
        """Demonstrate the benefit of schema flexibility in graph databases"""
        if not self.driver:
            print("No active database connection")
            return

        print("\n=== DEMO: BENEFIT 4 - SCHEMA FLEXIBILITY ===")
        try:
            with self.driver.session() as session:
                # Add a new property to an existing node
                print("\nAdding new properties to existing nodes:")
                session.run("""
                    MATCH (alice:Person {name: 'Alice'})
                    SET alice.occupation = 'Software Engineer', 
                        alice.languages = ['English', 'Spanish']
                """)

                # Create a new type of node and connect to existing nodes
                print("Adding a new type of node (Event) with connections to existing nodes:")
                session.run("""
                    CREATE (conference:Event {
                        name: 'Tech Conference 2023', 
                        date: '2023-11-15', 
                        location: 'San Francisco'
                    })
                    WITH conference
                    MATCH (person:Person)
                    WHERE person.name IN ['Alice', 'David', 'Grace']
                    CREATE (person)-[:ATTENDED {role: CASE 
                                                    WHEN person.name = 'Alice' THEN 'Speaker'
                                                    WHEN person.name = 'David' THEN 'Organizer'
                                                    ELSE 'Attendee' 
                                                 END}]->(conference)
                """)

                # Query the new structure
                result = session.run("""
                    MATCH (person:Person)-[r:ATTENDED]->(event:Event)
                    RETURN person.name as name, r.role as role, event.name as event
                """)

                print("\nPeople who attended the new event:")
                for record in result:
                    print(f"{record['name']} attended {record['event']} as a {record['role']}")

                # Show all data types for a node
                result = session.run("""
                    MATCH (alice:Person {name: 'Alice'}) 
                    RETURN alice
                """)

                alice_data = result.single()["alice"]
                print("\nAlice's flexible schema with added properties:")
                for key, value in alice_data.items():
                    print(f"  - {key}: {value}")
        except Exception as e:
            print(f"Error in demo_benefit_4: {e}")

    def demo_benefit_5_visualization(self):
        """Demonstrate the benefit of natural data visualization with graph databases"""
        if not self.driver:
            print("No active database connection")
            return

        print("\n=== DEMO: BENEFIT 5 - NATURAL DATA VISUALIZATION ===")
        try:
            # Create a NetworkX graph for visualization
            G = nx.Graph()

            # Get people and their friends
            with self.driver.session() as session:
                # Get all people
                result = session.run("""
                    MATCH (p:Person)
                    RETURN p.name as name
                """)
                for record in result:
                    G.add_node(record["name"], type="person")

                # Get friendships
                result = session.run("""
                    MATCH (p1:Person)-[:FRIEND]->(p2:Person)
                    RETURN p1.name as person1, p2.name as person2
                """)
                for record in result:
                    G.add_edge(record["person1"], record["person2"], type="friend")

                # Get cities
                result = session.run("""
                    MATCH (c:City)
                    RETURN c.name as name
                """)
                for record in result:
                    G.add_node(record["name"], type="city")

                # Get lives_in relationships
                result = session.run("""
                    MATCH (p:Person)-[:LIVES_IN]->(c:City)
                    RETURN p.name as person, c.name as city
                """)
                for record in result:
                    G.add_edge(record["person"], record["city"], type="lives_in")

            print("Building network visualization of people, their friendships, and cities...")

            # Create node colors based on type
            node_colors = []
            for node in G.nodes():
                if G.nodes[node].get("type") == "person":
                    node_colors.append("skyblue")
                else:
                    node_colors.append("lightgreen")

            # Create edge colors based on relationship type
            edge_colors = []
            for u, v in G.edges():
                if G.edges[u, v].get("type") == "friend":
                    edge_colors.append("gray")
                else:
                    edge_colors.append("red")

            # Position nodes using a layout algorithm
            pos = nx.spring_layout(G, seed=42)

            print("Network visualization is ready (would normally display a graph)")
            print("Graph contains:")
            print(f"- {sum(1 for _, attr in G.nodes(data=True) if attr.get('type') == 'person')} people")
            print(f"- {sum(1 for _, attr in G.nodes(data=True) if attr.get('type') == 'city')} cities")
            print(f"- {sum(1 for _, _, attr in G.edges(data=True) if attr.get('type') == 'friend')} friendship relationships")
            print(f"- {sum(1 for _, _, attr in G.edges(data=True) if attr.get('type') == 'lives_in')} lives_in relationships")

            # In a real application, you would display this graph:
            """
            plt.figure(figsize=(12, 10))
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1.5)
            
            # Draw labels
            nx.draw_networkx_labels(G, pos, font_size=10)
            
            plt.title("Social Network Graph")
            plt.axis("off")
            plt.tight_layout()
            plt.show()
            """
        except Exception as e:
            print(f"Error in demo_benefit_5: {e}")

def run_demo():
    """Run the complete Neo4j graph database demo"""
    # Connect to Neo4j
    demo = None
    try:
        # You should replace these with your actual Neo4j credentials
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "password"

        print("Starting Neo4j Graph Database Demo")
        print("==================================")
        print(f"Connecting to Neo4j at {uri}")

        demo = GraphDatabaseDemo(uri, username, password)

        # Clear existing data
        demo.clear_database()

        # Create sample datasets
        demo.create_social_network()
        demo.create_movie_network()

        # Run the demonstrations of graph database benefits
        demo.demo_benefit_1_relationships()
        demo.demo_benefit_2_pattern_matching()
        demo.demo_benefit_3_performance()
        demo.demo_benefit_4_schema_flexibility()
        demo.demo_benefit_5_visualization()

        print("\n==================================")
        print("Neo4j Graph Database Demo completed successfully!")

    except Exception as e:
        print(f"Demo failed: {e}")
    finally:
        # Ensure the database connection is closed
        if demo:
            demo.close()

if __name__ == "__main__":
    run_demo()
