-- CREATE TABLE Users_log_before
CREATE TABLE IF NOT EXISTS Users_log_before (
    user_id BIGINT PRIMARY KEY,
    login VARCHAR(255) NOT NULL,
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255),
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TRIGGER

DELIMITER //

CREATE TRIGGER before_users_update
BEFORE UPDATE ON Users
FOR EACH ROW
BEGIN
    -- Insert old data into Users_log_before before the update
    INSERT INTO Users_log_before (user_id, login, gravatar_id, url, avatar_url, log_timestamp)
    VALUES (OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url);
END3//

DELIMITER ;
