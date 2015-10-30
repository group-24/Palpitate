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
  PRIMARY KEY (subjectID, featureID, batchID)

);

