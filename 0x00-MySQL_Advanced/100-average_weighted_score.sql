DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    
    -- Calculate the total weighted score for the user
    SELECT SUM(score * weight) INTO total_score
    FROM corrections AS c
    JOIN projects AS p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Calculate the total weight of projects for the user
    SELECT SUM(weight) INTO total_weight
    FROM corrections AS c
    JOIN projects AS p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Update the average_score for the user
    UPDATE users
    SET average_score = total_score / total_weight
    WHERE id = user_id;
    
END$$

DELIMITER ;
