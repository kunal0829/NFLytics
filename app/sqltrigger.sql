CREATE TRIGGER addTrig
    BEFORE UPDATE ON PlayersInfo
        SET @old_pos = (SELECT Position FROM PlayersInfo WHERE PlayerId = new.PlayerId);

        IF (@old_pos = 'QB')    THEN SET new.Position = 'QB'
    END IF;

    END;