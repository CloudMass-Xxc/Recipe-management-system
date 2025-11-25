-- Clear user data SQL script
-- Note: This script preserves table structure, only deletes data

-- First, check table structure to find correct table names
\dt

-- Check users table structure
\d users

-- Try to truncate users table if we have permissions
TRUNCATE TABLE users CASCADE;

-- If truncate fails, try delete with specific where clause
-- DELETE FROM users WHERE id > 0;

-- Show result
SELECT COUNT(*) AS remaining_users FROM users;
