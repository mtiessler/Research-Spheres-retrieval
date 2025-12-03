import pytest
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from config.settings import get_settings

load_dotenv()


@pytest.fixture(scope='module')
def neo4j_driver():
    settings = get_settings()

    driver = GraphDatabase.driver(
        settings.get('neo4j', 'uri'),
        auth=(
            settings.get('neo4j', 'user'),
            os.getenv('NEO4J_PASSWORD')
        )
    )

    yield driver

    driver.close()


def test_neo4j_connection(neo4j_driver):
    with neo4j_driver.session() as session:
        result = session.run("RETURN 1 as test")
        record = result.single()
        assert record is not None
        assert record['test'] == 1

    print("Neo4j connection successful")


def test_neo4j_version(neo4j_driver):
    with neo4j_driver.session() as session:
        result = session.run("CALL dbms.components() YIELD versions RETURN versions[0] as version")
        record = result.single()
        version = record['version']
        print(f"Neo4j version: {version}")
        assert version is not None


def test_publications_exist(neo4j_driver):
    with neo4j_driver.session() as session:
        result = session.run("MATCH (p:publication) RETURN count(p) as count")
        count = result.single()['count']

        assert count > 0, "No Publication nodes found in database. Load data first."
        print(f"Found {count} publications in Neo4j")


def test_publications_have_required_properties(neo4j_driver):
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (p:publication)
            RETURN p.id as id, p.title as title, p.abstract as abstract
            LIMIT 1
        """)

        record = result.single()
        assert record is not None, "No publications found"

        pub_id = record['id']
        title = record['title']
        abstract = record['abstract']

        assert pub_id is not None, "Publication missing 'id' property"
        assert title is not None, "Publication missing 'title' property"

        print(f"Sample publication ID: {pub_id}")
        print(f"Sample publication title: {title[:50]}...")

        if abstract:
            print(f"Abstract available: {len(abstract)} characters")
        else:
            print("Warning: Sample publication has no abstract")


def test_publication_relationships(neo4j_driver):
    with neo4j_driver.session() as session:
        relationship_types = ['AUTHORED', 'CITES', 'PART_OF', 'HAS_TOPIC']

        for rel_type in relationship_types:
            result = session.run(f"""
                MATCH ()-[r:{rel_type}]->()
                RETURN count(r) as count
            """)
            count = result.single()['count']

            if count > 0:
                print(f"Found {count} {rel_type} relationships")


def test_author_nodes_exist(neo4j_driver):
    with neo4j_driver.session() as session:
        result = session.run("MATCH (a:Author) RETURN count(a) as count")
        count = result.single()['count']

        if count > 0:
            print(f"Found {count} authors in database")
        else:
            print("Warning: No Author nodes found")


def test_database_constraints(neo4j_driver):
    with neo4j_driver.session() as session:
        result = session.run("SHOW CONSTRAINTS")
        constraints = list(result)

        print(f"Database has {len(constraints)} constraints")

        for constraint in constraints:
            print(f"  - {constraint.get('name', 'unnamed')}")


def test_database_indexes(neo4j_driver):
    with neo4j_driver.session() as session:
        result = session.run("SHOW INDEXES")
        indexes = list(result)

        print(f"Database has {len(indexes)} indexes")

        for index in indexes:
            print(f"  - {index.get('name', 'unnamed')}")