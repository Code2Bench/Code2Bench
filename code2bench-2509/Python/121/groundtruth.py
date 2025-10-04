

def clean_ddl_for_pglite(ddl):
    """Clean DDL statements for PGlite compatibility"""

    # Remove PostgreSQL-specific extensions and features that PGlite doesn't support
    replacements = [
        # Remove vector column types (PGlite doesn't support pgvector)
        ('vector(1536)', 'TEXT'),  # Replace vector columns with TEXT for now
        ('vector(3072)', 'TEXT'),
        ('vector(4096)', 'TEXT'),

        # Remove GIN indexes (not supported in PGlite)
        ('USING gin', ''),

        # Simplify constraint names
        ('CONSTRAINT ', ''),

        # Remove some PostgreSQL-specific column constraints
        ('::text', ''),

        # Remove timezone from TIMESTAMP
        ('TIMESTAMP WITH TIME ZONE', 'TIMESTAMP'),

        # Simplify SERIAL to INTEGER with autoincrement
        ('BIGSERIAL', 'INTEGER'),
        ('SERIAL', 'INTEGER'),
    ]

    for old, new in replacements:
        ddl = ddl.replace(old, new)

    # Remove any lines that contain unsupported PostgreSQL features
    lines = ddl.split('\n')
    filtered_lines = []

    for line in lines:
        # Skip lines with unsupported features
        if any(unsupported in line.lower() for unsupported in [
            'gin', 'gist', 'tsvector', 'to_tsvector', 'pg_trgm',
            'btree_gin', 'btree_gist'
        ]):
            continue
        filtered_lines.append(line)

    return '\n'.join(filtered_lines)