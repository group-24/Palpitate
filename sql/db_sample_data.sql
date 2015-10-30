INSERT INTO batch (added,description) VALUES (now(),'test');
INSERT INTO feature(name) VALUES
('f1'),
('f2'),
('f3')
;
INSERT INTO data (subjectID, featureID, batchID, featureValue) VALUES
(1,1,1,0.38453),
(1,2,1,2.22453),
(1,3,1,0.36453),
(2,3,1,5.32471),
(2,2,1,4.72453),
(2,1,1,3.32923),
(3,3,1,1.22451)
;
