DO $$ BEGIN
IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'shevark') THEN
    CREATE DATABASE shevark OWNER crm;
END IF;
END $$;
