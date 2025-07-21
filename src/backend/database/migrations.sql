-- Create schools table
CREATE TABLE schools (
    school_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL UNIQUE,
    address VARCHAR,
    city VARCHAR,
    state VARCHAR,
    contact_email VARCHAR UNIQUE,
    phone_number VARCHAR,
    admin_user_id UUID REFERENCES users(user_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_schools_name ON schools(name);
CREATE INDEX idx_schools_admin_user_id ON schools(admin_user_id);

-- Enhance users table
ALTER TABLE users
    ADD COLUMN role VARCHAR CHECK (role IN ('super_admin', 'school_admin', 'it_support', 'teacher', 'student', 'guardian', 'government', 'corporation', 'ngo_partner')) NOT NULL,
    ADD COLUMN school_id UUID REFERENCES schools(school_id),
    ADD COLUMN guardian_id UUID REFERENCES users(user_id);

CREATE INDEX idx_users_school_id ON users(school_id);
CREATE INDEX idx_users_guardian_id ON users(guardian_id);
