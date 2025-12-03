#!/usr/bin/env python3
"""
Script to index all publications from Neo4j to ChromaDB
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from embeddings.indexing.index_publications import PublicationIndexer
from config.settings import get_settings
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    # Load environment
    load_dotenv()

    # Load settings
    settings = get_settings()

    # Create indexer
    indexer = PublicationIndexer(
        neo4j_uri=settings.get('neo4j', 'uri'),
        neo4j_user=settings.get('neo4j', 'user'),
        neo4j_password=settings.get('neo4j', 'password'),
        embedding_model=settings.get('embeddings', 'model_name'),
        chroma_dir=settings.get('vector_store', 'persist_dir')
    )

    try:
        # Index all publications
        print("Starting indexing process...")
        indexer.index_publications(
            batch_size=settings.get('embeddings', 'batch_size'),
            limit=None  # Index all
        )
        print("\nIndexing complete!")

    except Exception as e:
        print(f"\nError during indexing: {e}")
        raise
    finally:
        indexer.close()


if __name__ == '__main__':
    main()