INSERT INTO batch (added,description) VALUES (now(),'test');
INSERT INTO feature(name) VALUES
('f1'),
('f2'),
('f3')
;
INSERT INTO data (subjectID, featureID, batchID, featureValue,timeslice) VALUES
(1,1,1,60,0),
(1,2,1,2.22453,0),
(1,3,1,0.36453,0),
(2,3,1,5.32471,0),
(2,2,1,4.72453,0),
(2,1,1,70,0),
(3,3,1,1.22451,0)
;
