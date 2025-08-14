from cassandra.cluster import Cluster
import constants


def main():
    cluster = Cluster([constants.CASSANDRA_HOST], port=constants.CASSANDRA_PORT)
    session = cluster.connect()

    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {constants.CASSANDRA_KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}};
    """)
    session.set_keyspace(constants.CASSANDRA_KEYSPACE)

    session.execute(f"""
        CREATE TABLE IF NOT EXISTS {constants.CASSANDRA_TABLE} (
            user_id INT,
            domain TEXT,
            created_at TIMESTAMP,
            page_title TEXT,
            PRIMARY KEY (user_id, page_title)
        );
    """)
    print("cassandra: keyspace/table ready")

    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    main()
