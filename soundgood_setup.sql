
DROP TABLE IF EXISTS contact_details CASCADE;
CREATE TABLE contact_details (
 id INT GENERATED ALWAYS AS IDENTITY,
 email VARCHAR(50) UNIQUE NOT NULL
);

ALTER TABLE contact_details ADD CONSTRAINT PK_contact_details PRIMARY KEY (id);


DROP TABLE IF EXISTS personal_details CASCADE;
CREATE TABLE personal_details (
 id INT GENERATED ALWAYS AS IDENTITY,
 ssn VARCHAR(30) UNIQUE NOT NULL,
 name VARCHAR(50),
 street VARCHAR(30),
 city VARCHAR(30),
 zip VARCHAR(10)
);

ALTER TABLE personal_details ADD CONSTRAINT PK_personal_details PRIMARY KEY (id);


DROP TABLE IF EXISTS phone CASCADE;
CREATE TABLE phone (
 contact_details_id INT,
 phone VARCHAR(20) NOT NULL
);

ALTER TABLE phone ADD CONSTRAINT PK_phone PRIMARY KEY (contact_details_id,phone);


DROP TABLE IF EXISTS rental_instrument CASCADE;
CREATE TABLE rental_instrument (
 id INT GENERATED ALWAYS AS IDENTITY,
 type VARCHAR(50) NOT NULL,
 brand VARCHAR(30),
 price FLOAT(10) NOT NULL CHECK (price >= 0),
 quantity INT NOT NULL CHECK (quantity >= 0)
);

ALTER TABLE rental_instrument ADD CONSTRAINT PK_rental_instrument PRIMARY KEY (id);


DROP TABLE IF EXISTS student CASCADE;
CREATE TABLE student (
 id INT GENERATED ALWAYS AS IDENTITY,
 instrument VARCHAR(50),
 ensemble VARCHAR(50) CHECK (instrument IS NOT NULL OR ensemble IS NOT NULL),
 skill_level VARCHAR(12) NOT NULL,
 personal_details_id INT,
 contact_details_id INT,
 parent_contact_details_id INT
);

ALTER TABLE student ADD CONSTRAINT PK_student PRIMARY KEY (id);


DROP TABLE IF EXISTS time_period CASCADE;
CREATE TABLE time_period (
 id INT GENERATED ALWAYS AS IDENTITY,
 start_time TIMESTAMP(6) NOT NULL,
 end_time TIMESTAMP(6) NOT NULL
);

ALTER TABLE time_period ADD CONSTRAINT PK_time_period PRIMARY KEY (id);


DROP TABLE IF EXISTS application CASCADE;
CREATE TABLE application (
 id INT GENERATED ALWAYS AS IDENTITY,
 student_id INT,
 enrollment_offered BOOLEAN,
 accepted BOOLEAN
);

ALTER TABLE application ADD CONSTRAINT PK_application PRIMARY KEY (id);


DROP TABLE IF EXISTS instructor CASCADE;
CREATE TABLE instructor (
 id INT GENERATED ALWAYS AS IDENTITY,
 personal_details_id INT,
 contact_details_id INT
);

ALTER TABLE instructor ADD CONSTRAINT PK_instructor PRIMARY KEY (id);


DROP TABLE IF EXISTS instructor_ensemble CASCADE;
CREATE TABLE instructor_ensemble (
 instructor_id INT,
 ensemble VARCHAR(50) NOT NULL
);

ALTER TABLE instructor_ensemble ADD CONSTRAINT PK_instructor_ensemble PRIMARY KEY (instructor_id,ensemble);


DROP TABLE IF EXISTS instructor_instrument CASCADE;
CREATE TABLE instructor_instrument (
 instructor_id INT,
 instrument VARCHAR(50) NOT NULL
);

ALTER TABLE instructor_instrument ADD CONSTRAINT PK_instructor_instrument PRIMARY KEY (instructor_id,instrument);


DROP TABLE IF EXISTS instructor_time_period CASCADE;
CREATE TABLE instructor_time_period (
 instructor_id INT,
 time_period_id INT
);

ALTER TABLE instructor_time_period ADD CONSTRAINT PK_instructor_time_period PRIMARY KEY (instructor_id,time_period_id);


DROP TABLE IF EXISTS lesson CASCADE;
CREATE TABLE lesson (
 id INT GENERATED ALWAYS AS IDENTITY,
 instrument VARCHAR(50),
 ensemble VARCHAR(50) CHECK (instrument IS NOT NULL OR ensemble IS NOT NULL),
 skill_level VARCHAR(12) NOT NULL,
 min_slots INT NOT NULL,
 max_slots INT NOT NULL CHECK (max_slots >= min_slots),
 instructor_id INT,
 time_period_id INT,
 price FLOAT(10) NOT NULL
);

ALTER TABLE lesson ADD CONSTRAINT PK_lesson PRIMARY KEY (id);


DROP TABLE IF EXISTS rental CASCADE;
CREATE TABLE rental (
 id INT GENERATED ALWAYS AS IDENTITY,
 student_id INT,
 rental_instrument_id INT,
 time_period_id INT,
 terminated BOOLEAN DEFAULT FALSE
);

ALTER TABLE rental ADD CONSTRAINT PK_rental PRIMARY KEY (id);


DROP TABLE IF EXISTS booking CASCADE;
CREATE TABLE booking (
 id INT GENERATED ALWAYS AS IDENTITY,
 student_id INT,
 lesson_id INT
);

ALTER TABLE booking ADD CONSTRAINT PK_booking PRIMARY KEY (id);


ALTER TABLE phone ADD CONSTRAINT FK_phone_0 FOREIGN KEY (contact_details_id) REFERENCES contact_details (id) ON DELETE CASCADE;


ALTER TABLE student ADD CONSTRAINT FK_student_0 FOREIGN KEY (personal_details_id) REFERENCES personal_details (id) ON DELETE CASCADE;
ALTER TABLE student ADD CONSTRAINT FK_student_1 FOREIGN KEY (contact_details_id) REFERENCES contact_details (id) ON DELETE CASCADE;
ALTER TABLE student ADD CONSTRAINT FK_student_2 FOREIGN KEY (parent_contact_details_id) REFERENCES contact_details (id) ON DELETE CASCADE;


ALTER TABLE application ADD CONSTRAINT FK_application_0 FOREIGN KEY (student_id) REFERENCES student (id) ON DELETE CASCADE;


ALTER TABLE instructor ADD CONSTRAINT FK_instructor_0 FOREIGN KEY (personal_details_id) REFERENCES personal_details (id) ON DELETE CASCADE;
ALTER TABLE instructor ADD CONSTRAINT FK_instructor_1 FOREIGN KEY (contact_details_id) REFERENCES contact_details (id) ON DELETE CASCADE;


ALTER TABLE instructor_ensemble ADD CONSTRAINT FK_instructor_ensemble_0 FOREIGN KEY (instructor_id) REFERENCES instructor (id) ON DELETE CASCADE;


ALTER TABLE instructor_instrument ADD CONSTRAINT FK_instructor_instrument_0 FOREIGN KEY (instructor_id) REFERENCES instructor (id) ON DELETE CASCADE;


ALTER TABLE instructor_time_period ADD CONSTRAINT FK_instructor_time_period_0 FOREIGN KEY (instructor_id) REFERENCES instructor (id) ON DELETE CASCADE;
ALTER TABLE instructor_time_period ADD CONSTRAINT FK_instructor_time_period_1 FOREIGN KEY (time_period_id) REFERENCES time_period (id) ON DELETE CASCADE;


ALTER TABLE lesson ADD CONSTRAINT FK_lesson_0 FOREIGN KEY (instructor_id) REFERENCES instructor (id) ON DELETE CASCADE;
ALTER TABLE lesson ADD CONSTRAINT FK_lesson_1 FOREIGN KEY (time_period_id) REFERENCES time_period (id) ON DELETE CASCADE;


ALTER TABLE rental ADD CONSTRAINT FK_rental_0 FOREIGN KEY (student_id) REFERENCES student (id) ON DELETE CASCADE;
ALTER TABLE rental ADD CONSTRAINT FK_rental_1 FOREIGN KEY (rental_instrument_id) REFERENCES rental_instrument (id) ON DELETE CASCADE;
ALTER TABLE rental ADD CONSTRAINT FK_rental_2 FOREIGN KEY (time_period_id) REFERENCES time_period (id) ON DELETE CASCADE;


ALTER TABLE booking ADD CONSTRAINT FK_booking_0 FOREIGN KEY (student_id) REFERENCES student (id) ON DELETE CASCADE;
ALTER TABLE booking ADD CONSTRAINT FK_booking_1 FOREIGN KEY (lesson_id) REFERENCES lesson (id) ON DELETE CASCADE;


