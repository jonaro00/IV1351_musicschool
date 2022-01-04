
-- Total number of booked lessons per month and what type of lesson they were
DROP VIEW IF EXISTS lessons_per_month_this_year;
CREATE VIEW lessons_per_month_this_year AS
WITH val (year) AS (VALUES (EXTRACT(YEAR FROM CURRENT_DATE)))
SELECT * FROM (
    SELECT EXTRACT(MONTH FROM t.start_time) AS month, COUNT(DISTINCT l.id) AS "Total lessons"
    FROM booking AS b
        JOIN lesson AS l ON b.lesson_id = l.id
        JOIN time_period AS t ON l.time_period_id = t.id
        CROSS JOIN val AS v
    WHERE EXTRACT(YEAR FROM t.start_time) = v.year
    GROUP BY EXTRACT(MONTH FROM t.start_time)
    ORDER BY month
) AS foo1
NATURAL FULL JOIN (
    SELECT EXTRACT(MONTH FROM t.start_time) AS month, COUNT(DISTINCT l.id) AS "Individual lessons"
    FROM booking AS b
        JOIN lesson AS l ON b.lesson_id = l.id
        JOIN time_period AS t ON l.time_period_id = t.id
        CROSS JOIN val AS v
    WHERE EXTRACT(YEAR FROM t.start_time) = v.year AND l.instrument IS NOT NULL AND l.max_slots = 1
    GROUP BY EXTRACT(MONTH FROM t.start_time)
    ORDER BY month
) AS foo2
NATURAL FULL JOIN (
    SELECT EXTRACT(MONTH FROM t.start_time) AS month, COUNT(DISTINCT l.id) AS "Group lessons"
    FROM booking AS b
        JOIN lesson AS l ON b.lesson_id = l.id
        JOIN time_period AS t ON l.time_period_id = t.id
        CROSS JOIN val AS v
    WHERE EXTRACT(YEAR FROM t.start_time) = v.year AND l.instrument IS NOT NULL AND l.max_slots > 1
    GROUP BY EXTRACT(MONTH FROM t.start_time)
    ORDER BY month
) AS foo3
NATURAL FULL JOIN (
    SELECT EXTRACT(MONTH FROM t.start_time) AS month, COUNT(DISTINCT l.id) AS "Ensembles"
    FROM booking AS b
        JOIN lesson AS l ON b.lesson_id = l.id
        JOIN time_period AS t ON l.time_period_id = t.id
        CROSS JOIN val AS v
    WHERE EXTRACT(YEAR FROM t.start_time) = v.year AND l.ensemble IS NOT NULL
    GROUP BY EXTRACT(MONTH FROM t.start_time)
    ORDER BY month
) AS foo4
;
SELECT * FROM lessons_per_month_this_year;


-- Average number of lessons per month of each type
DROP VIEW IF EXISTS average_lessons_per_month_this_year;
CREATE VIEW average_lessons_per_month_this_year AS
WITH val (year) AS (VALUES (EXTRACT(YEAR FROM CURRENT_DATE)))
SELECT * FROM (
    SELECT CAST(COUNT(DISTINCT l.id) / 12.0 AS DECIMAL(10,2)) AS "Average total lessons per month"
    FROM booking AS b
        JOIN lesson AS l ON b.lesson_id = l.id
        JOIN time_period AS t ON l.time_period_id = t.id
        CROSS JOIN val AS v
    WHERE EXTRACT(YEAR FROM t.start_time) = v.year
) AS foo1, (
    SELECT CAST(COUNT(DISTINCT l.id) / 12.0 AS DECIMAL(10,2)) AS "Average individual lessons per month"
    FROM booking AS b
        JOIN lesson AS l ON b.lesson_id = l.id
        JOIN time_period AS t ON l.time_period_id = t.id
        CROSS JOIN val AS v
    WHERE EXTRACT(YEAR FROM t.start_time) = v.year AND l.instrument IS NOT NULL AND l.max_slots = 1
) AS foo2, (
    SELECT CAST(COUNT(DISTINCT l.id) / 12.0 AS DECIMAL(10,2)) AS "Average group lessons per month"
    FROM booking AS b
        JOIN lesson AS l ON b.lesson_id = l.id
        JOIN time_period AS t ON l.time_period_id = t.id
        CROSS JOIN val AS v
    WHERE EXTRACT(YEAR FROM t.start_time) = v.year AND l.instrument IS NOT NULL AND l.max_slots > 1
) AS foo3, (
    SELECT CAST(COUNT(DISTINCT l.id) / 12.0 AS DECIMAL(10,2)) AS "Average ensembles per month"
    FROM booking AS b
        JOIN lesson AS l ON b.lesson_id = l.id
        JOIN time_period AS t ON l.time_period_id = t.id
        CROSS JOIN val AS v
    WHERE EXTRACT(YEAR FROM t.start_time) = v.year AND l.ensemble IS NOT NULL
) AS foo4
;
SELECT * FROM average_lessons_per_month_this_year;


-- List all instructors who has given more than 0 lessons in January, ordered by lessons given
DROP VIEW IF EXISTS overworked_instructors;
CREATE VIEW overworked_instructors AS
SELECT p.name AS "Instructor", COUNT(DISTINCT l.id) AS "Lessons given"
FROM booking AS b
    JOIN lesson AS l ON b.lesson_id = l.id
    JOIN time_period AS t ON l.time_period_id = t.id
    JOIN instructor AS i ON l.instructor_id = i.id
    JOIN personal_details AS p ON i.personal_details_id = p.id
WHERE EXTRACT(YEAR FROM t.start_time) = EXTRACT(YEAR FROM CURRENT_DATE)
    AND EXTRACT(MONTH FROM t.start_time) = EXTRACT(MONTH FROM CURRENT_DATE)
GROUP BY p.name
HAVING COUNT(DISTINCT l.id) > 0
ORDER BY COUNT(DISTINCT l.id) DESC
;
SELECT * FROM overworked_instructors;


-- List all ensembles next week (Jan 10 - Jan 16), sorted by genre and weekday
DROP VIEW IF EXISTS ensembles_next_week;
CREATE VIEW ensembles_next_week AS
SELECT
    l.ensemble AS "Genre",
    t.start_time AS "Start",
    t.end_time AS "End",
    CASE
        WHEN nb.slots >= 3 THEN '3+ slots left'
        WHEN nb.slots = 2  THEN '2 slots left'
        WHEN nb.slots = 1  THEN '1 slot left'
        WHEN nb.slots = 0  THEN 'Fully booked'
        ELSE 'what?'
    END AS "Slots left"
FROM lesson AS l
    JOIN time_period AS t ON l.time_period_id = t.id
    FULL JOIN (
        SELECT
            l.id AS id,
            l.max_slots - COUNT(b.id) AS slots
        FROM lesson AS l
            FULL OUTER JOIN booking as b ON l.id = b.lesson_id
        GROUP BY l.id
    ) AS nb ON nb.id = l.id
WHERE t.start_time >= TIMESTAMP '2022-01-10'
    AND t.start_time < TIMESTAMP '2022-01-17'
    AND l.ensemble IS NOT NULL
ORDER BY l.ensemble, t.start_time
;
SELECT * FROM ensembles_next_week;

