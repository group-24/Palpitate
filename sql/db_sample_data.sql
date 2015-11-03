INSERT INTO batch (added,description) VALUES (now(),'test');
INSERT INTO feature(name) VALUES
('f1'),
('f2'),
('f3')
;
INSERT INTO data (subjectID, featureID, batchID, featureValue,timeslice) VALUES
--BPMs
(1,1,1,60,0),
(2,1,1,80,0),
(3,1,1,67,0),
(4,1,1,50,0),
(5,1,1,100,0),
(6,1,1,93,0),
--f1s
(1,2,1,0.34524,0),
(2,2,1,0.94723,0),
(3,2,1,0.89342,0),
(4,2,1,0.23534,0),
(5,2,1,0.64342,0),
(6,2,1,0.44563,0),
--f3s
(1,4,1,0.60231,0),
(2,4,1,0.80541,0),
(3,4,1,0.67264,0),
(4,4,1,0.50452,0),
(5,4,1,1.01231,0),
(6,4,1,0.93542,0)
;
