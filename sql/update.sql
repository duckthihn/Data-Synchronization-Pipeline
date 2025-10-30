-- INSERT
INSERT INTO Users VALUES (1, 'alice', NULL, 'https://github.com/alice', NULL);
INSERT INTO Users VALUES (2, 'bob', 'abc123', 'https://github.com/bob', 'https://avatars.com/bob.png');
INSERT INTO Users VALUES (3, 'charlie', NULL, NULL, NULL);
INSERT INTO Users VALUES (4, 'dave', 'xyz789', 'https://github.com/dave', NULL);
INSERT INTO Users VALUES (5, 'eve', NULL, 'https://github.com/eve', 'https://avatars.com/eve.jpg');
INSERT INTO Users VALUES (6, 'frank', NULL, NULL, NULL);
INSERT INTO Users VALUES (7, 'grace', 'def456', 'https://github.com/grace', NULL);
INSERT INTO Users VALUES (8, 'heidi', NULL, 'https://github.com/heidi', 'https://avatars.com/heidi.png');
INSERT INTO Users VALUES (9, 'ivan', NULL, NULL, NULL);
INSERT INTO Users VALUES (10, 'judy', 'ghi789', 'https://github.com/judy', 'https://avatars.com/judy.jpg');

-- UPDATE
UPDATE Users SET login = 'alice_new' WHERE user_id = 1;
UPDATE Users SET gravatar_id = 'new_abc' WHERE user_id = 2;
UPDATE Users SET url = 'https://newsite.com/charlie' WHERE user_id = 3;
UPDATE Users SET avatar_url = 'https://avatars.com/dave_new.png' WHERE user_id = 4;
UPDATE Users SET login = 'eve_hacked', gravatar_id = 'hacked' WHERE user_id = 5;
UPDATE Users SET url = 'https://newsite.com/frank' WHERE user_id = 6;
UPDATE Users SET avatar_url = 'https://avatars.com/grace_new.png' WHERE user_id = 7;
UPDATE Users SET gravatar_id = NULL WHERE user_id = 8;
UPDATE Users SET login = 'ivan_updated', url = 'https://newsite.com/ivan' WHERE user_id = 9;
UPDATE Users SET avatar_url = NULL WHERE user_id = 10;

-- DELETE
DELETE FROM Users WHERE user_id = 1;
DELETE FROM Users WHERE user_id = 2;
DELETE FROM Users WHERE user_id = 3;
