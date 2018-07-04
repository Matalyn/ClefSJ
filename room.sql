CREATE TABLE temp_room (
  id INT NOT NULL AUTO_INCREMENT,
  address varchar(255) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEAFULT CHARSET=utf8;

INSERT INTO temp_room (address)
VALUES (SELECT DISTINCT r1.room from room r1);

CREATE TABLE unlocks (
  keyNumber varchar(32) NOT NULL,
  roomID INT NOT NULL,
  FOREIGN KEY (keyNumber) REFERENCES clef(keyNumber) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (roomID) REFERENCES room(id) ON UPDATE CASCADE ON DELETE CASCADE,
  PRIMARY KEY (keyNumber, roomID)
) ENGINE=InnoDB DEAFULT CHARSET=utf8;

INSERT INTO unlocks (keyNumber, roomID)
VALUES (SELECT r1.keyNumber, t1.roomID from room r1 JOIN temp_room t1 ON r1.room = t1.address);

DROP TABLE room;

RENAME TABLE temp_room to room;