
--parent 1
INSERT INTO contact_details (email) VALUES ('apparent@not.real');
INSERT INTO phone VALUES (1, '+4612345678');

--student 1
INSERT INTO contact_details (email) VALUES ('first_student@soundgood.music');
INSERT INTO phone VALUES (2, '+4612345678'), (2, '+4612345679');
INSERT INTO personal_details (ssn, name, street, city, zip) VALUES ('19970303-1234', 'Legvi McBoo', 'Road 1', 'Townsville', '1337');
INSERT INTO student (
    instrument,
    ensemble,
    skill_level,
    personal_details_id,
    contact_details_id,
    parent_contact_details_id
) VALUES (
    'Oboe',
    'Jazz',
    'Beginner',
    1,
    2,
    1
);

--student 2, a sibling to student 1 since they have the same parent contact details
INSERT INTO contact_details (email) VALUES ('second_student@soundgood.music');
INSERT INTO phone VALUES (3, '+4612345678'), (3, '+4612345680');
INSERT INTO personal_details (ssn, name, street, city, zip) VALUES ('19990403-1234', 'Kanad McBoo', 'Road 1', 'Townsville', '1337');
INSERT INTO student (
    instrument,
    ensemble,
    skill_level,
    personal_details_id,
    contact_details_id,
    parent_contact_details_id
) VALUES (
    'Flute',
    NULL,
    'Beginner',
    2,
    3,
    1
);

--instructor 1
INSERT INTO contact_details (email) VALUES ('the_boss@soundgood.music');
INSERT INTO phone VALUES (4, '+4612335632');
INSERT INTO personal_details (ssn, name, street, city, zip) VALUES ('19670201-1234', 'Krabi Macronn', 'Street 12', 'Townsville', '423');
INSERT INTO instructor (personal_details_id, contact_details_id) VALUES (3, 4);
INSERT INTO instructor_instrument VALUES
    (1, 'Guitar'),
    (1, 'Oboe'),
    (1, 'Otamatone'),
    (1, 'Drums')
;
INSERT INTO instructor_ensemble VALUES
    (1, 'RockBand'),
    (1, 'Orchestra')
;

--instructor 2
INSERT INTO contact_details (email) VALUES ('big_boi@soundgood.music');
INSERT INTO phone VALUES (5, '+4612335876');
INSERT INTO personal_details (ssn, name, street, city, zip) VALUES ('19770211-1234', 'Inka Lao', 'Street 15', 'Townsville', '424');
INSERT INTO instructor (personal_details_id, contact_details_id) VALUES (4, 5);
INSERT INTO instructor_instrument VALUES
    (2, 'Guitar'),
    (2, 'Drums'),
    (2, 'Flute'),
    (2, 'Violin')
;
INSERT INTO instructor_ensemble VALUES
    (2, 'Jazz')
;

--times
INSERT INTO time_period (start_time, end_time) VALUES
    (TIMESTAMP '2022-01-03 08:00', TIMESTAMP '2022-01-03 10:00'),
    (TIMESTAMP '2022-01-03 10:00', TIMESTAMP '2022-01-03 12:00'),
    (TIMESTAMP '2022-01-03 13:00', TIMESTAMP '2022-01-03 15:00'),
    (TIMESTAMP '2022-01-03 15:00', TIMESTAMP '2022-01-03 17:00'),
    (TIMESTAMP '2022-01-04 08:00', TIMESTAMP '2022-01-04 10:00'),
    (TIMESTAMP '2022-01-04 10:00', TIMESTAMP '2022-01-04 12:00'),
    (TIMESTAMP '2022-01-04 13:00', TIMESTAMP '2022-01-04 15:00'),
    (TIMESTAMP '2022-01-04 15:00', TIMESTAMP '2022-01-04 17:00'),
    (TIMESTAMP '2022-02-02 08:00', TIMESTAMP '2022-02-02 10:00'),
    (TIMESTAMP '2022-02-02 10:00', TIMESTAMP '2022-02-02 12:00'),
    (TIMESTAMP '2022-02-02 13:00', TIMESTAMP '2022-02-02 15:00'),
    (TIMESTAMP '2022-02-02 15:00', TIMESTAMP '2022-02-02 17:00')
;

--instructor times
INSERT INTO instructor_time_period (instructor_id, time_period_id) VALUES
    (1, 1),
    (1, 2),
    (1, 4),
    (1, 5),
    (1, 7),
    (1, 8),
    (2, 1),
    (2, 5),
    (2, 9)
;

--lesson 1: instructor 1 on 3 jan 08:00, booked by student 1
INSERT INTO lesson (
    instrument,
    ensemble,
    skill_level,
    min_slots,
    max_slots,
    instructor_id,
    time_period_id,
    price
) VALUES (
    'Oboe',
    NULL,
    'Beginner',
    1,
    1,
    1,
    1,
    100
);
INSERT INTO booking (student_id, lesson_id) VALUES (1, 1);

--lesson 2: instructor 2 on 2 feb 08:00, booked by student 2
INSERT INTO lesson (
    instrument,
    ensemble,
    skill_level,
    min_slots,
    max_slots,
    instructor_id,
    time_period_id,
    price
) VALUES (
    'Flute',
    NULL,
    'Beginner',
    1,
    1,
    2,
    9,
    100
);
INSERT INTO booking (student_id, lesson_id) VALUES (2, 2);

--parent 2
INSERT INTO contact_details (email) VALUES ('mama@not.real');
INSERT INTO phone VALUES (5, '+4612356784');

--student 3
INSERT INTO contact_details (email) VALUES ('smart_guy@soundgood.music');
INSERT INTO phone VALUES (6, '+4612000001');
INSERT INTO personal_details (ssn, name, street, city, zip) VALUES ('19900405-1234', 'Bing Chilling', 'Road 2', 'Townsville', '1337');
INSERT INTO student (
    instrument,
    ensemble,
    skill_level,
    personal_details_id,
    contact_details_id,
    parent_contact_details_id
) VALUES (
    'Saxophone',
    'Jazz',
    'Beginner',
    5,
    6,
    5
);

--lesson 3: Jazz ensemble with instructor 2 on 2 feb 13:00, booked by students 1 and 3
INSERT INTO lesson (
    instrument,
    ensemble,
    skill_level,
    min_slots,
    max_slots,
    instructor_id,
    time_period_id,
    price
) VALUES (
    NULL,
    'Jazz',
    'Beginner',
    2,
    4,
    2,
    11,
    150
);
INSERT INTO booking (student_id, lesson_id) VALUES (1, 3);
INSERT INTO booking (student_id, lesson_id) VALUES (3, 3);
