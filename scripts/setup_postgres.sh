#!/bin/bash

# Exit on error
set -e

# Database names
DB_NAMES=("audioink_prod" "audioink_dev" "audioink_test")

# Create databases and set up permissions
for DB_NAME in "${DB_NAMES[@]}"; do
    echo "Setting up database: $DB_NAME"
    
    # Create database if it doesn't exist
    psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    psql -U postgres -c "CREATE DATABASE $DB_NAME"

    # Set up permissions
    psql -U postgres -d "$DB_NAME" << EOF
    -- Revoke all permissions from public
    REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
    REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;
    REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;

    -- Grant necessary permissions to postgres user
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO postgres;

    -- Set up search path
    ALTER DATABASE $DB_NAME SET search_path TO public;

    -- Enable necessary extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
EOF

    echo "Database $DB_NAME setup completed"
done

echo "All databases have been set up successfully" 