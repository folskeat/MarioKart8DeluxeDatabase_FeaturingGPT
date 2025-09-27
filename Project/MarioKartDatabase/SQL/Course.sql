CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CupID INT,
    CourseName VARCHAR(100),
    CupName VARCHAR(50),
    Origin VARCHAR(50)
);

INSERT INTO Course (CourseID, CupID, CourseName, CupName, Origin) VALUES
-- Mushroom Cup (CID = 1)
(1, 1, 'Mario Kart Stadium', 'Mushroom', 'Wii U'),
(2, 1, 'Water Park', 'Mushroom', 'Wii U'),
(3, 1, 'Sweet Sweet Canyon', 'Mushroom', 'Wii U'),
(4, 1, 'Thwomp Ruins', 'Mushroom', 'Wii U'),

-- Flower Cup (CID = 2)
(5, 2, 'Mario Circuit', 'Flower', 'Wii U'),
(6, 2, 'Toad Harbor', 'Flower', 'Wii U'),
(7, 2, 'Twisted Mansion', 'Flower', 'Wii U'),
(8, 2, 'Shy Guy Falls', 'Flower', 'Wii U'),

-- Star Cup (CID = 3)
(9, 3, 'Sunshine Airport', 'Star', 'Wii U'),
(10, 3, 'Dolphin Shoals', 'Star', 'Wii U'),
(11, 3, 'Electrodrome', 'Star', 'Wii U'),
(12, 3, 'Mount Wario', 'Star', 'Wii U'),

-- Special Cup (CID = 4)
(13, 4, 'Cloudtop Cruise', 'Special', 'Wii U'),
(14, 4, 'Bone-Dry Dunes', 'Special', 'Wii U'),
(15, 4, 'Bowser''s Castle', 'Special', 'Wii U'),
(16, 4, 'Rainbow Road', 'Special', 'Wii U'),

-- Shell Cup (CID = 5)
(17, 5, 'Moo Moo Meadows', 'Shell', 'Wii'),
(18, 5, 'Mario Circuit', 'Shell', 'GBA'),
(19, 5, 'Cheep Cheep Beach', 'Shell', 'DS'),
(20, 5, 'Toad''s Turnpike', 'Shell', 'N64'),

-- Banana Cup (CID = 6)
(21, 6, 'Dry Dry Desert', 'Banana', 'GCN'),
(22, 6, 'Donut Plains 3', 'Banana', 'SNES'),
(23, 6, 'Royal Raceway', 'Banana', 'N64'),
(24, 6, 'DK Jungle', 'Banana', '3DS'),

-- Leaf Cup (CID = 7)
(25, 7, 'Wario Stadium', 'Leaf', 'DS'),
(26, 7, 'Sherbet Land', 'Leaf', 'GCN'),
(27, 7, 'Music Park', 'Leaf', '3DS'),
(28, 7, 'Yoshi Valley', 'Leaf', 'N64'),

-- Lightning Cup (CID = 8)
(29, 8, 'Tick-Tock Clock', 'Lightning', 'DS'),
(30, 8, 'Piranha Plant Slide', 'Lightning', '3DS'),
(31, 8, 'Grumble Volcano', 'Lightning', 'Wii'),
(32, 8, 'Rainbow Road', 'Lightning', 'N64'),

-- Egg Cup (CID = 9)
(33, 9, 'Yoshi Circuit', 'Egg', 'GCN'),
(34, 9, 'Excitebike Arena', 'Egg', 'Wii U'),
(35, 9, 'Dragon Driftway', 'Egg', 'Wii U'),
(36, 9, 'Mute City', 'Egg', 'Wii U'),

-- Triforce Cup (CID = 10)
(37, 10, 'Wario''s Gold Mine', 'Triforce', 'Wii'),
(38, 10, 'Rainbow Road', 'Triforce', 'SNES'),
(39, 10, 'Ice Ice Outpost', 'Triforce', 'Wii U'),
(40, 10, 'Hyrule Circuit', 'Triforce', 'Wii U'),

-- Crossing Cup (CID = 11)
(41, 11, 'Baby Park', 'Crossing', 'GCN'),
(42, 11, 'Cheese Land', 'Crossing', 'GBA'),
(43, 11, 'Wild Woods', 'Crossing', 'Wii U'),
(44, 11, 'Animal Crossing', 'Crossing', 'Wii U'),

-- Bell Cup (CID = 12)
(45, 12, 'Neo Bowser City', 'Bell', '3DS'),
(46, 12, 'Ribbon Road', 'Bell', 'GBA'),
(47, 12, 'Super Bell Subway', 'Bell', 'Wii U'),
(48, 12, 'Big Blue', 'Bell', 'Wii U'),

-- Golden Dash Cup (CID = 13)
(49, 13, 'Paris Promenade', 'Golden Dash', 'Tour'),
(50, 13, 'Toad Circuit', 'Golden Dash', '3DS'),
(51, 13, 'Choco Mountain', 'Golden Dash', 'N64'),
(52, 13, 'Coconut Mall', 'Golden Dash', 'Wii'),

-- Lucky Cat Cup (CID = 14)
(53, 14, 'Tokyo Blur', 'Lucky Cat', 'Tour'),
(54, 14, 'Shroom Ridge', 'Lucky Cat', 'DS'),
(55, 14, 'Sky Garden', 'Lucky Cat', 'GBA'),
(56, 14, 'Ninja Hideaway', 'Lucky Cat', 'Tour'),

-- Turnip Cup (CID = 15)
(57, 15, 'New York Minute', 'Turnip', 'Tour'),
(58, 15, 'Mario Circuit 3', 'Turnip', 'SNES'),
(59, 15, 'Kalimari Desert', 'Turnip', 'N64'),
(60, 15, 'Waluigi Pinball', 'Turnip', 'DS'),

-- Propeller Cup (CID = 16)
(61, 16, 'Sydney Sprint', 'Propeller', 'Tour'),
(62, 16, 'Snow Land', 'Propeller', 'GBA'),
(63, 16, 'Mushroom Gorge', 'Propeller', 'Wii'),
(64, 16, 'Sky-High Sundae', 'Propeller', 'Tour'),

-- Rock Cup (CID = 17)
(65, 17, 'London Loop', 'Rock', 'Tour'),
(66, 17, 'Boo Lake', 'Rock', 'GBA'),
(67, 17, 'Rock Rock Mountain', 'Rock', '3DS'),
(68, 17, 'Maple Treeway', 'Rock', 'Wii'),

-- Moon Cup (CID = 18)
(69, 18, 'Berlin Byways', 'Moon', 'Tour'),
(70, 18, 'Peach Gardens', 'Moon', 'DS'),
(71, 18, 'Merry Mountain', 'Moon', 'Tour'),
(72, 18, 'Rainbow Road', 'Moon', '3DS'),

-- Fruit Cup (CID = 19)
(73, 19, 'Amsterdam Drift', 'Fruit', 'Tour'),
(74, 19, 'Riverside Park', 'Fruit', 'GBA'),
(75, 19, 'DK Summit', 'Fruit', 'Wii'),
(76, 19, 'Yoshi''s Island', 'Fruit', 'Tour'),

-- Boomerang Cup (CID = 20)
(77, 20, 'Bangkok Rush', 'Boomerang', 'Tour'),
(78, 20, 'Mario Circuit', 'Boomerang', 'DS'),
(79, 20, 'Waluigi Stadium', 'Boomerang', 'GCN'),
(80, 20, 'Singapore Speedway', 'Boomerang', 'Tour'),

-- Feather Cup (CID = 21)
(81, 21, 'Athens Dash', 'Feather', 'Tour'),
(82, 21, 'Daisy Cruiser', 'Feather', 'GCN'),
(83, 21, 'Moonview Highway', 'Feather', 'Wii'),
(84, 21, 'Squeaky Clean Sprint', 'Feather', 'Tour'),

-- Cherry Cup (CID = 22)
(85, 22, 'Los Angeles Laps', 'Cherry', 'Tour'),
(86, 22, 'Sunset Wilds', 'Cherry', 'GBA'),
(87, 22, 'Koopa Cape', 'Cherry', 'Wii'),
(88, 22, 'Vancouver Velocity', 'Cherry', 'Tour'),

-- Acorn Cup (CID = 23)
(89, 23, 'Rome Avanti', 'Acorn', 'Tour'),
(90, 23, 'DK Mountain', 'Acorn', 'GCN'),
(91, 23, 'Daisy Circuit', 'Acorn', 'Wii'),
(92, 23, 'Piranha Plant Cove', 'Acorn', 'Tour'),

-- Spiny Cup (CID = 24)
(93, 24, 'Madrid Drive', 'Spiny', 'Tour'),
(94, 24, 'Rosalina''s Ice World', 'Spiny', '3DS'),
(95, 24, 'Bowser Castle 3', 'Spiny', 'SNES'),
(96, 24, 'Rainbow Road', 'Spiny', 'Wii');
