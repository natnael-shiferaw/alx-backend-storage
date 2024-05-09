-- Define a stored procedure named ComputeAverageWeightedScoreForUser, which calculates and stores 
-- the average weighted score for a user.

DROP procedure IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
    IN user_id INT
)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(score) FROM corrections
        WHERE corrections.user_id = user_id
    )
    WHERE id = user_id;
END;
|
