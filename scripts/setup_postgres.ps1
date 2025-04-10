# Database names
$DB_NAMES = @("audioink_prod", "audioink_dev", "audioink_test")

# PostgreSQL connection parameters
$PG_USER = "postgres"
$PG_PASSWORD = "2135"

# Create databases and set up permissions
foreach ($DB_NAME in $DB_NAMES) {
    Write-Host "Setting up database: $DB_NAME"
    
    # Create database if it doesn't exist
    $dbExists = & "psql" -U $PG_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'"
    if (-not $dbExists) {
        & "psql" -U $PG_USER -c "CREATE DATABASE $DB_NAME"
    }

    # Set up permissions
    $sqlCommands = @"
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
"@

    & "psql" -U $PG_USER -d $DB_NAME -c $sqlCommands

    Write-Host "Database $DB_NAME setup completed"
}

Write-Host "All databases have been set up successfully" 