CREATE TABLE Actors (
    actor_id BIGINT PRIMARY KEY,
    login VARCHAR(255) NOT NULL,
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255)
);

CREATE TABLE Repositories (
    repo_id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL
);

CREATE TABLE Issues (
    issue_id BIGINT PRIMARY KEY,
    issue_number INT,
    title VARCHAR(255),
    body TEXT,
    state VARCHAR(20),
    locked BOOLEAN,
    html_url VARCHAR(255),
    comments_count INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    closed_at TIMESTAMP,
    user_id BIGINT,
    repo_id BIGINT,
    FOREIGN KEY (user_id) REFERENCES Actors(actor_id),
    FOREIGN KEY (repo_id) REFERENCES Repositories(repo_id)
);

CREATE TABLE Comments (
    comment_id BIGINT PRIMARY KEY,
    issue_id BIGINT,
    user_id BIGINT,
    body TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES Issues(issue_id),
    FOREIGN KEY (user_id) REFERENCES Actors(actor_id)
);

CREATE TABLE Payloads (
    payload_id BIGINT PRIMARY KEY,
    action VARCHAR(50),
    issue_id BIGINT,
    comment_id BIGINT,
    FOREIGN KEY (issue_id) REFERENCES Issues(issue_id),
    FOREIGN KEY (comment_id) REFERENCES Comments(comment_id)
);
