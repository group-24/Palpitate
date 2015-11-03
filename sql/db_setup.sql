CREATE TABLE feature
(
  featureID serial PRIMARY KEY,
  name varchar(10) not null
);

CREATE TABLE batch
(
  batchID serial PRIMARY KEY,
  added date not null,
  description text not null
);

CREATE TABLE data
(
  subjectID bigserial,
  featureID int REFERENCES feature,
  batchID int REFERENCES batch,
  featureValue numeric not null,
  timeslice int not null,
  PRIMARY KEY (subjectID, featureID, batchID, timeslice)

);

-- makes sure BPM always be feature with id 1
INSERT INTO feature(name) VALUES ('BPM') ;