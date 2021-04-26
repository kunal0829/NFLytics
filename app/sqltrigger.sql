DELIMITER //
DROP TRIGGER IF EXISTS addTrig//

CREATE TRIGGER addTrig
    BEFORE UPDATE ON PlayersInfo
    FOR EACH ROW
    BEGIN
        SET @old_pos = (SELECT Position FROM PlayersInfo WHERE PlayerId = new.PlayerId GROUP BY PlayerId);
        IF (@old_pos = 'QB')    THEN SET new.Position = 'QB';
        ELSEIF (@old_pos = 'WR'  AND  (new.Position != 'RB' AND new.Position != 'TE'))     THEN SET new.Position = 'WR';
        ELSEIF (@old_pos = 'RB') THEN SET new.Position = 'RB';
        ELSEIF (@old_pos = 'TE'  AND  (new.Position != 'WR' AND new.Position != 'OT'))     THEN SET new.Position = 'TE';
        ELSEIF (@old_pos = 'C'  AND  (new.Position != 'OL' AND new.Position != 'OT'))     THEN SET new.Position = 'C';
        ELSEIF (@old_pos = 'OL'  AND  (new.Position != 'OT' AND new.Position != 'C'))     THEN SET new.Position = 'OL';
        ELSEIF (@old_pos = 'OT'  AND  (new.Position != 'OL' AND new.Position != 'C'))     THEN SET new.Position = 'OT';
        ELSE SET new.Position = new.Position;
        END IF;
    END//

DELIMITER ;
