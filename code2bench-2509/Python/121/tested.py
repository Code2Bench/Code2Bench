import re

def clean_ddl_for_pglite(ddl: str) -> str:
    # Replace vector column types with TEXT
    ddl = re.sub(r'(\bvector\b)', 'TEXT', ddl)
    
    # Remove GIN indexes
    ddl = re.sub(r'GIN\s+', '', ddl)
    
    # Simplify constraint names by removing the 'CONSTRAINT' keyword
    ddl = re.sub(r'CONSTRAINT\s+', '', ddl)
    
    # Remove PostgreSQL-specific column constraints like '::text'
    ddl = re.sub(r'\$\$text\$', '', ddl)
    
    # Convert TIMESTAMP WITH TIME ZONE to TIMESTAMP
    ddl = re.sub(r'TIMESTAMP WITH TIME ZONE', 'TIMESTAMP', ddl)
    
    # Replace SERIAL and BIGSERIAL types with INTEGER
    ddl = re.sub(r'SERIAL', 'INTEGER', ddl)
    ddl = re.sub(r'BIGSERIAL', 'INTEGER', ddl)
    
    # Remove unsupported PostgreSQL features
    ddl = re.sub(r'GIN\s+|GIST\s+|TSVECTOR\s+|TO_TSVECTOR\s+|PG_TRGM\s+|BTREE_GIN\s+|BTREE_GIST', '', ddl)
    
    return ddl