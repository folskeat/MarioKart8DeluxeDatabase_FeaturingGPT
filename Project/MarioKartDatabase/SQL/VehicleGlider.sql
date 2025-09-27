CREATE TABLE VehicleGlider (
    VehicleGliderID INT PRIMARY KEY,
    VehicleGliderName VARCHAR(100) NOT NULL,
    Speed_Land DECIMAL(3,2) NOT NULL,
    Speed_AntiG DECIMAL(3,2) NOT NULL,
    Speed_Water DECIMAL(3,2) NOT NULL,
    Speed_Glide DECIMAL(3,2) NOT NULL,
    Acceleration DECIMAL(3,2) NOT NULL,
    WeightValue DECIMAL(3,2) NOT NULL,
    Handling_Land DECIMAL(3,2) NOT NULL,
    Handling_AntiG DECIMAL(3,2) NOT NULL,
    Handling_Water DECIMAL(3,2) NOT NULL,
    Handling_Glide DECIMAL(3,2) NOT NULL,
    Traction DECIMAL(3,2) NOT NULL,
    MiniTurbo DECIMAL(3,2) NOT NULL,
    Invincibility DECIMAL(3,2) NOT NULL
);

INSERT INTO VehicleGlider (VehicleGliderID, VehicleGliderName, Speed_Land, Speed_AntiG, Speed_Water, Speed_Glide, Acceleration, WeightValue, Handling_Land, Handling_AntiG, Handling_Water, Handling_Glide, Traction, MiniTurbo, Invincibility) VALUES
(1, 'Bowser Kite', -0.25, 0.25, -0.25, -0.25, 0.25, 0.00, 0.00, -0.25, 0.25, 0.25, -0.25, 0.25, -0.25),
(2, 'Cloud Glider', -0.25, 0.25, 0.00, -0.25, 0.25, -0.25, 0.00, 0.00, 0.00, 0.25, 0.00, 0.25, -0.25),
(3, 'Flower Glider', -0.25, 0.25, 0.00, -0.25, 0.25, -0.25, 0.00, 0.00, 0.00, 0.25, 0.00, 0.25, -0.25),
(4, 'Gold Glider', 0.00, 0.25, -0.25, 0.00, 0.00, 0.25, 0.00, -0.25, 0.25, 0.00, -0.25, 0.00, 0.00),
(5, 'Hylian Kite', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
(6, 'MKTV Parafoil', -0.25, 0.25, -0.25, -0.25, 0.25, 0.00, 0.00, -0.25, 0.25, 0.25, -0.25, 0.25, -0.25),
(7, 'Paper Glider', -0.25, 0.25, 0.00, -0.25, 0.25, -0.25, 0.00, 0.00, 0.00, 0.25, 0.00, 0.25, -0.25),
(8, 'Parachute', -0.25, 0.25, 0.00, -0.25, 0.25, -0.25, 0.00, 0.00, 0.00, 0.25, 0.00, 0.25, -0.25),
(9, 'Parafoil', -0.25, 0.25, -0.25, -0.25, 0.25, 0.00, 0.00, -0.25, 0.25, 0.25, -0.25, 0.25, -0.25),
(10, 'Paraglider', 0.00, 0.25, -0.25, 0.00, 0.00, 0.25, 0.00, -0.25, 0.25, 0.00, -0.25, 0.00, 0.00),
(11, 'Peach Parasol', -0.25, 0.25, -0.25, -0.25, 0.25, 0.00, 0.00, -0.25, 0.25, 0.25, -0.25, 0.25, -0.25),
(12, 'Plane Glider', 0.00, 0.25, -0.25, 0.00, 0.00, 0.25, 0.00, -0.25, 0.25, 0.00, -0.25, 0.00, 0.00),
(13, 'Super Glider', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
(14, 'Waddle Wing', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
(15, 'Wario Wing', 0.00, 0.25, -0.25, 0.00, 0.00, 0.25, 0.00, -0.25, 0.25, 0.00, -0.25, 0.00, 0.00);
