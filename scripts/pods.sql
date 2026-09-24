-- pods.sql: pretend schema, dump only (never queried for real)
CREATE TABLE pod_words (
    key     text PRIMARY KEY,
    word    text NOT NULL,
    clicks  integer DEFAULT 0
);

INSERT INTO pod_words (key, word, clicks)
VALUES ('spark', 'sparkle', 17),
       ('fern', 'fronds', 42),
       ('pod',  'cozy',   99);

SELECT word, clicks
FROM pod_words
WHERE clicks > 20
ORDER BY clicks DESC;