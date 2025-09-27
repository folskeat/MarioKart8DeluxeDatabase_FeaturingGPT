# MarioKart8DeluxeDatabase_FeaturingGPT
For Records, Characters, Karts, and Courses!

### The purpose of this database is to allow users to query for world records, but also ask follow up questions!

![schema](https://github.com/folskeat/MarioKart8DeluxeDatabase_FeaturingGPT/blob/main/Project/MarioKartSchema.png?raw=true)

### Some Question, Query, and Response (working):

Ask a question about your database: When was the most recent world record acheived?

Generated SQL:

SELECT r.Date, r.Speed, r.Time, p.PlayerName, d.CharacterName, c.CourseName 
FROM Record r 
JOIN Player p ON r.PlayerID = p.PlayerID 
JOIN Driver d ON r.DriverID = d.DriverID 
JOIN Course c ON r.CourseID = c.CourseID 
ORDER BY r.Date DESC 
LIMIT 1;


Raw Query Result:
[('2025-09-25', 150, '1:57.797', 'Pii', 'Yoshi', 'Piranha Plant Slide')]

Friendly Result:
[{'Date': '2025-09-25', 'Speed': 150, 'Time': '1:57.797', 'PlayerName': 'Pii', 'CharacterName': 'Yoshi', 'CourseName': 'Piranha Plant Slide', 'DriverID': 9, 'Driver': 'Yoshi', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'CourseID': 30, 'Course': 'Piranha Plant Slide', 'PlayerID': 21, 'Player': 'Pii', 'Stats': {'Speed': {'Land': 3.75, 'Water': 4, 'AntiG': 3.5, 'Glide': 4.25}, 'Handling': {'Land': 3.75, 'Water': 3.25, 'AntiG': 3.75, 'Glide': 3.75}, 'Acceleration': 3.75, 'Weight': 3, 'Traction': 3.75, 'MiniTurbo': 4.25, 'Invincibility': 3}}]

Friendly Answer:
The most recent world record was set on September 25, 2025, on the course Piranha Plant Slide. It was done in 150cc with a time of 1:57.797 by a player named Pii racing as Yoshi. Isn't that cool? 🏁💨


### Some Question, Query, and Response (not working):

Ask a question about your database: What tires would best compliment Bowser?

Generated SQL:

SELECT vt.VehicleTireName
FROM Record r
JOIN Driver d ON r.DriverID = d.DriverID
JOIN VehicleTires vt ON r.VehicleTireID = vt.VehicleTireID
WHERE d.CharacterName = 'Bowser' COLLATE NOCASE
GROUP BY vt.VehicleTireName
ORDER BY COUNT(*) DESC
LIMIT 1;


Raw Query Result:
[]

Friendly Result:
[]

Friendly Answer:
Looks like Bowser doesn't have a specific favorite tire, so you can choose based on how you like to play! If you want more speed and weight, go for something like the Slick tires. But if you prefer better handling and traction, try something like the Sponge or Wood tires. It's all about finding the right balance that feels good for you! 🏎️💨

### A few more examples:

Ask a question about your database: Who has the most world records?

Generated SQL:

SELECT p.PlayerID, p.PlayerName, COUNT(*) AS RecordCount
FROM Record r
JOIN Player p ON r.PlayerID = p.PlayerID
GROUP BY p.PlayerID
ORDER BY RecordCount DESC
LIMIT 1;


Raw Query Result:
[(26, 'Vincent', 57)]

Friendly Result:
[{'PlayerID': 26, 'PlayerName': 'Vincent', 'RecordCount': 57, 'Driver': 'N/A Driver', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'Vincent', 'Stats': {'Speed': {'Land': 0.0, 'Water': 0.0, 'AntiG': 0.0, 'Glide': 0.0}, 'Handling': {'Land': 0.0, 'Water': 0.0, 'AntiG': 0.0, 'Glide': 0.0}, 'Acceleration': 0.0, 'Weight': 0.0, 'Traction': 0.0, 'MiniTurbo': 0.0, 'Invincibility': 0.0}}]

Friendly Answer:
The player with the most world records is Vincent! He's really fast and has set amazing times on 26 different tracks. It's like being the best at winning races again and again! 🏆🏎️

-

Ask a question about your database: What is the best build in the game?

Generated SQL:

SELECT 
    d.CharacterName, 
    vb.VehicleBodyName, 
    vt.VehicleTireName, 
    vg.VehicleGliderName, 
    COUNT(*) AS RecordCount
FROM 
    Record r
JOIN 
    Driver d ON r.DriverID = d.DriverID
JOIN 
    VehicleBody vb ON r.VehicleBodyID = vb.VehicleBodyID
JOIN 
    VehicleTires vt ON r.VehicleTireID = vt.VehicleTireID
JOIN 
    VehicleGlider vg ON r.VehicleGliderID = vg.VehicleGliderID
GROUP BY 
    r.DriverID, r.VehicleBodyID, r.VehicleTireID, r.VehicleGliderID
ORDER BY 
    RecordCount DESC
LIMIT 1;


Raw Query Result:
[('Yoshi', 'Biddybuggy', 'Azure Roller', 'Paper Glider', 27)]

Friendly Result:
[{'CharacterName': 'Yoshi', 'VehicleBodyName': 'Biddybuggy', 'VehicleTireName': 'Azure Roller', 'VehicleGliderName': 'Paper Glider', 'RecordCount': 27, 'DriverID': 9, 'Driver': 'Yoshi', 'VehicleBodyID': 4, 'VehicleBody': 'Biddybuggy', 'VehicleTireID': 2, 'VehicleTires': 'Azure Roller', 'VehicleGliderID': 7, 'VehicleGlider': 'Paper Glider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 3.75, 'Water': 4, 'AntiG': 3.5, 'Glide': 4.25}, 'Handling': {'Land': 3.75, 'Water': 3.25, 'AntiG': 3.75, 'Glide': 3.75}, 'Acceleration': 3.75, 'Weight': 3, 'Traction': 3.75, 'MiniTurbo': 4.25, 'Invincibility': 3}}]

Friendly Answer:
The best build in the game is like giving Yoshi a super speedy car! 🏎️✨ You put Yoshi in the Biddybuggy, with Azure Roller tires, and a Paper Glider. This combination has set 27 world records! It's a magical combo for zooming past everyone else! 🌟

-

Ask a question about your database: What is the best kart in the game?

Generated SQL:

SELECT vb.VehicleBodyName, COUNT(*) AS UsageCount
FROM Record r
JOIN VehicleBody vb ON r.VehicleBodyID = vb.VehicleBodyID
GROUP BY vb.VehicleBodyID
ORDER BY UsageCount DESC
LIMIT 1;


Raw Query Result:
[('Biddybuggy', 55)]

Friendly Result:
[{'VehicleBodyName': 'Biddybuggy', 'UsageCount': 55, 'Driver': 'N/A Driver', 'VehicleBodyID': 4, 'VehicleBody': 'Biddybuggy', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 0.0, 'Water': 0.0, 'AntiG': 0.0, 'Glide': 0.0}, 'Handling': {'Land': 0.0, 'Water': 0.0, 'AntiG': 0.0, 'Glide': 0.0}, 'Acceleration': 0.0, 'Weight': 0.0, 'Traction': 0.0, 'MiniTurbo': 0.0, 'Invincibility': 0.0}}]

Friendly Answer:
The best kart in the game is the Biddybuggy! It's a top choice for players because it has great handling and acceleration, helping you zip through the tracks and around corners easily.

-
Ask a question about your database: Which country has the most world records?

Generated SQL:

SELECT p.Nation, COUNT(*) as RecordCount
FROM Record r
JOIN Player p ON r.PlayerID = p.PlayerID
GROUP BY p.Nation
ORDER BY RecordCount DESC
LIMIT 1;


Raw Query Result:
[('USA', 73)]

Friendly Result:
[{'Nation': 'USA', 'RecordCount': 73, 'Driver': 'N/A Driver', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 0.0, 'Water': 0.0, 'AntiG': 0.0, 'Glide': 0.0}, 'Handling': {'Land': 0.0, 'Water': 0.0, 'AntiG': 0.0, 'Glide': 0.0}, 'Acceleration': 0.0, 'Weight': 0.0, 'Traction': 0.0, 'MiniTurbo': 0.0, 'Invincibility': 0.0}}]

Friendly Answer:
The country with the most Mario Kart 8 Deluxe world records is the USA, holding 73 of them! Imagine it as if the USA racers have the most golden trophies in this kart-racing competition! 🏆

-

Ask a question about your database: Which characters only have one world record?

Generated SQL:

SELECT d.CharacterName 
FROM Driver d
JOIN Record r ON d.DriverID = r.DriverID
GROUP BY d.CharacterName
HAVING COUNT(r.RecordID) = 1;


Raw Query Result:
[('Baby Peach',), ('Koopa Troopa',), ('Ludwig',), ('Mii_M',), ('Peach',), ('Tanooki Mario',)]

Friendly Result:
[{'CharacterName': 'Baby Peach', 'DriverID': 19, 'Driver': 'Baby Peach', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 2.5, 'Water': 2.75, 'AntiG': 2.25, 'Glide': 3}, 'Handling': {'Land': 5, 'Water': 4.5, 'AntiG': 5, 'Glide': 5}, 'Acceleration': 4, 'Weight': 2, 'Traction': 4.25, 'MiniTurbo': 4.5, 'Invincibility': 4.25}}, {'CharacterName': 'Koopa Troopa', 'DriverID': 11, 'Driver': 'Koopa Troopa', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 3, 'Water': 3.25, 'AntiG': 2.75, 'Glide': 3.5}, 'Handling': {'Land': 4.5, 'Water': 4, 'AntiG': 4.5, 'Glide': 4.5}, 'Acceleration': 4, 'Weight': 2.5, 'Traction': 4.25, 'MiniTurbo': 4.25, 'Invincibility': 3.75}}, {'CharacterName': 'Ludwig', 'DriverID': 36, 'Driver': 'Ludwig', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 4, 'Water': 4.25, 'AntiG': 3.75, 'Glide': 4.5}, 'Handling': {'Land': 3.5, 'Water': 3, 'AntiG': 3.5, 'Glide': 3.5}, 'Acceleration': 3.5, 'Weight': 3.5, 'Traction': 3.5, 'MiniTurbo': 4, 'Invincibility': 3.5}}, {'CharacterName': 'Mii_M', 'DriverID': 49, 'Driver': 'Mii_M', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 4, 'Water': 4.25, 'AntiG': 3.75, 'Glide': 4.5}, 'Handling': {'Land': 3.5, 'Water': 3, 'AntiG': 3.5, 'Glide': 3.5}, 'Acceleration': 3.5, 'Weight': 3.5, 'Traction': 3.5, 'MiniTurbo': 4, 'Invincibility': 3.5}}, {'CharacterName': 'Peach', 'DriverID': 3, 'Driver': 'Peach', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 3.75, 'Water': 4, 'AntiG': 3.5, 'Glide': 4.25}, 'Handling': {'Land': 3.75, 'Water': 3.25, 'AntiG': 3.75, 'Glide': 3.75}, 'Acceleration': 3.75, 'Weight': 3, 'Traction': 3.75, 'MiniTurbo': 4.25, 'Invincibility': 3}}, {'CharacterName': 'Tanooki Mario', 'DriverID': 6, 'Driver': 'Tanooki Mario', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 3.75, 'Water': 4, 'AntiG': 3.5, 'Glide': 4.25}, 'Handling': {'Land': 3.75, 'Water': 3.25, 'AntiG': 3.75, 'Glide': 3.75}, 'Acceleration': 3.75, 'Weight': 3.25, 'Traction': 3.25, 'MiniTurbo': 4.25, 'Invincibility': 3}}]

Friendly Answer:
Sure thing! These are the characters who have zoomed to the top of the world just once in Mario Kart 8 Deluxe:

- Baby Peach
- Koopa Troopa
- Ludwig
- Mii (Male)
- Peach
- Tanooki Mario

Each of them has one super special world record win! 🌟🏆

-

Ask a question about your database: Which cup would take the longest to complete?

Generated SQL:

SELECT c.CupName, SUM(r.Time) AS TotalTime
FROM Record r
JOIN Course c ON r.CourseID = c.CourseID
GROUP BY c.CupName
ORDER BY TotalTime DESC
LIMIT 1;


Raw Query Result:
[('Rock', 10.0)]

Friendly Result:
[{'CupName': 'Rock', 'TotalTime': 10.0, 'Driver': 'N/A Driver', 'VehicleBody': 'N/A VehicleBody', 'VehicleTires': 'N/A VehicleTires', 'VehicleGlider': 'N/A VehicleGlider', 'Course': 'N/A Course', 'Player': 'N/A Player', 'Stats': {'Speed': {'Land': 0.0, 'Water': 0.0, 'AntiG': 0.0, 'Glide': 0.0}, 'Handling': {'Land': 0.0, 'Water': 0.0, 'AntiG': 0.0, 'Glide': 0.0}, 'Acceleration': 0.0, 'Weight': 0.0, 'Traction': 0.0, 'MiniTurbo': 0.0, 'Invincibility': 0.0}}]

Friendly Answer:
The Rock Cup would take the longest to complete in Mario Kart 8 Deluxe. In total, it takes around 10 minutes for the best players in the world to race through it. So, if you like a challenge and enjoy longer cups, the Rock Cup is the one for you! 🏎️⏱️

-

## Prompting Strategies

I think I gave it enough to go off of where you don't have to be overly specific in your prompting strategies. But it does like certain key phrases better than others. Sometimes, just changing wording can help. You might get better results by saying "best" as in "most optimal for winning" for example.
