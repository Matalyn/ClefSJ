CREATE TABLE opens (
  keyNumber varchar(32) NOT NULL,
  description varchar(100) NOT NULL,
  FOREIGN KEY keyNumber REFERENCES clef(keyNumber) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO opens(keyNumber)
SELECT DISTINCT keyNumber, opens FROM clef;

UPDATE opens SET description = 'Door' WHERE description = 'door';
UPDATE opens SET description = 'Mailbox' WHERE description = 'mailBox'

ALTER TABLE clef DROP COLUMN opens;