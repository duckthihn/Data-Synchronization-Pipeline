-- Create log tables

CREATE TABLE IF NOT EXISTS Users_log_before (
    user_id BIGINT,
    login VARCHAR(255) NOT NULL,
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255),
    action_type VARCHAR(50),
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Users_log_after (
    user_id BIGINT,
    login VARCHAR(255) NOT NULL,
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255),
    action_type VARCHAR(50),
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BEFORE INSERT Trigger

CREATE TRIGGER before_users_insert
BEFORE INSERT ON Users
FOR EACH ROW

    INSERT INTO Users_log_before (
        user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp
    )
    VALUES (
        NEW.user_id, NEW.login, NEW.gravatar_id, NEW.url, NEW.avatar_url,
        'insert', NOW()
    );

-- AFTER INSERT Trigger

CREATE TRIGGER after_users_insert
AFTER INSERT ON Users
FOR EACH ROW

    INSERT INTO Users_log_after (
        user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp
    )
    VALUES (
        NEW.user_id, NEW.login, NEW.gravatar_id, NEW.url, NEW.avatar_url,
        'insert', NOW()
    );

-- BEFORE UPDATE Trigger

CREATE TRIGGER before_users_update
BEFORE UPDATE ON Users
FOR EACH ROW

    INSERT INTO Users_log_before (
        user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp
    )
    VALUES (
        OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url,
        'update', NOW()
    );

-- AFTER UPDATE Trigger

CREATE TRIGGER after_users_update
AFTER UPDATE ON Users
FOR EACH ROW

    INSERT INTO Users_log_after (
        user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp
    )
    VALUES (
        NEW.user_id, NEW.login, NEW.gravatar_id, NEW.url, NEW.avatar_url,
        'update', NOW()
    );

-- BEFORE DELETE Trigger

CREATE TRIGGER before_users_delete
BEFORE DELETE ON Users
FOR EACH ROW

    INSERT INTO Users_log_before (
        user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp
    )
    VALUES (
        OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url,
        'delete', NOW()
    );


-- AFTER DELETE Trigger

CREATE TRIGGER after_users_delete
AFTER DELETE ON Users
FOR EACH ROW

    INSERT INTO Users_log_after (
        user_id, login, gravatar_id, url, avatar_url, action_type, log_timestamp
    )
    VALUES (
        OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url,
        'delete', NOW()
    );



