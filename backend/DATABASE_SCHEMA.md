# Kids Pixel Pals - PostgreSQL Database Schema

## Overview
Comprehensive database schema for the Kids Pixel Pals application with proper relationships, data encryption, and audit logging.

## Database Tables

### 1. Users Table (`users`)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('ADMIN', 'PARENT', 'CHILD')),
    parent_id INTEGER REFERENCES users(id),
    approved_by_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Profiles Table (`profiles`)
```sql
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    display_name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Game Credentials Table (`game_credentials`)
```sql
CREATE TABLE game_credentials (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    game_name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    password_ciphertext BYTEA NOT NULL,  -- Encrypted with AES-256
    iv BYTEA NOT NULL,                   -- Initialization vector
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Conversations Table (`conversations`)
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    is_group BOOLEAN DEFAULT FALSE,
    title VARCHAR(200),
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Conversation Members Table (`conversation_members`)
```sql
CREATE TABLE conversation_members (
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_in_convo VARCHAR(20) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (conversation_id, user_id)
);
```

### 6. Messages Table (`messages`)
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users(id),
    type VARCHAR(10) NOT NULL CHECK (type IN ('text', 'audio', 'image', 'system')),
    content TEXT,
    media_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
```

### 7. Audit Logs Table (`audit_logs`)
```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    actor_id INTEGER NOT NULL REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER,
    before_json JSONB,
    after_json JSONB,
    ip VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Relationships Diagram

```
users
  ├──┬ profiles (1:1)
  │   └── game_credentials (1:many)
  ├──┬ children (self-referential, 1:many)
  └──┬ conversations (created_by)
      └── conversation_members (many:many)
          └── messages
```

## Indexes for Performance

```sql
-- Users table indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_parent_id ON users(parent_id);
CREATE INDEX idx_users_approved ON users(approved_by_admin);

-- Profiles table indexes
CREATE INDEX idx_profiles_user_id ON profiles(user_id);

-- Game credentials indexes
CREATE INDEX idx_game_creds_profile_id ON game_credentials(profile_id);
CREATE INDEX idx_game_creds_game_name ON game_credentials(game_name);

-- Conversations indexes
CREATE INDEX idx_conversations_created_by ON conversations(created_by);
CREATE INDEX idx_conversations_is_group ON conversations(is_group);

-- Conversation members indexes
CREATE INDEX idx_conv_members_user_id ON conversation_members(user_id);
CREATE INDEX idx_conv_members_conv_id ON conversation_members(conversation_id);

-- Messages indexes
CREATE INDEX idx_messages_conv_id ON messages(conversation_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_type ON messages(type);

-- Audit logs indexes
CREATE INDEX idx_audit_logs_actor_id ON audit_logs(actor_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
```

## Data Encryption Strategy

### Sensitive Data Fields
- `game_credentials.password_ciphertext`: AES-256 encrypted game passwords
- `users.password_hash`: Argon2 hashed user passwords

### Encryption Implementation
```python
# Using Fernet (AES-256) from cryptography library
from cryptography.fernet import Fernet
import base64

# Generate key from settings
encryption_key = base64.urlsafe_b64encode(settings.encryption_key.encode()[:32].ljust(32))
cipher_suite = Fernet(encryption_key)

def encrypt_game_password(password: str) -> tuple[bytes, bytes]:
    """Encrypt game password with unique IV"""
    encrypted_data = cipher_suite.encrypt(password.encode())
    return encrypted_data

def decrypt_game_password(encrypted_data: bytes) -> str:
    """Decrypt game password"""
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()
```

## Security Considerations

1. **Password Hashing**: Argon2 for user passwords (resistant to GPU attacks)
2. **Sensitive Data Encryption**: AES-256 for game credentials
3. **Role-Based Access Control**: ADMIN, PARENT, CHILD roles with proper permissions
4. **Audit Logging**: Comprehensive logging of all administrative actions
5. **Cascade Deletes**: Proper foreign key constraints with ON DELETE CASCADE
6. **Input Validation**: SQLAlchemy type validation and constraints

## Backup and Recovery

```bash
# Backup database
pg_dump kids_pixel_pals > backup_$(date +%Y%m%d).sql

# Restore database
psql kids_pixel_pals < backup_file.sql
```

## Monitoring and Maintenance

- Regular vacuum and analyze operations
- Monitor index usage and rebuild when necessary
- Set up connection pooling for better performance
- Implement database replication for high availability