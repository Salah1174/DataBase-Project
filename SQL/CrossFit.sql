USE master;
GO
CREATE DATABASE CrossFit;

USE CrossFit;

CREATE TABLE Users
(
    UserID INT IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL,
    PasswordHash NVARCHAR(255) NOT NULL,
    Email NVARCHAR(100) UNIQUE,
    U_Address NVARCHAR(255),
    BirthDate DATE NOT NULL,
    RegistrationDate DATETIME DEFAULT GETDATE(),
    Age AS (DATEDIFF(YEAR, Birthdate, GETDATE())),
    CONSTRAINT USER_PK PRIMARY KEY (UserID)
);

CREATE TABLE [Trainee]
(
    [TraineeID] INT IDENTITY(1,1) ,
    [StartMembership] DATE NOT NULL,
    [EndMembership] DATE NULL,
    [UserID] INT NOT NULL,
    CONSTRAINT TRAINEE_PK PRIMARY KEY (TraineeID),
    CONSTRAINT FK_User_Trainee FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
GO

CREATE TABLE [Employee]
(
    [EmployeeID] INT IDENTITY(1,1),
    [EmployeeSalary] FLOAT NOT NULL,
    [UserID] int not null,
    CONSTRAINT EMPLOYEE_PK PRIMARY KEY (EmployeeID),
    CONSTRAINT FK_User_Employee FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
GO

CREATE TABLE [Trainer]
(
    [TrainerID] INT IDENTITY(1,1),
    [TrainerRole] NVARCHAR(255) NOT NULL,
    [UserID] INT NOT NULL,
    CONSTRAINT TRAINER_PK PRIMARY KEY (TrainerID),
    CONSTRAINT FK_User_Trainer FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
GO

CREATE TABLE [Equipment]
(
    [EquipmentID] INT IDENTITY(1,1) ,
    [EquipmentName] nvarchar(255) NOT NULL,
    [Condition] nvarchar(255) NULL,

    CONSTRAINT EQUIPMENT_PK PRIMARY KEY (EquipmentID)
)
GO

CREATE TABLE [Transactions]
(
    [TransactionsID] INT IDENTITY(1,1) ,
    [TransactionName] nvarchar(255) NOT NULL UNIQUE,
    [Amount] float NOT NULL,
    [Date] DATE,
    [TraineeID] int NOT NULL,
    [EmployeeID] int NOT NULL,

    CONSTRAINT TRANSACTIONS_PK PRIMARY KEY (TransactionsID),
    CONSTRAINT TRANSACTIONS_EMPLOYEE_FK FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    CONSTRAINT TRANSACTIONS_TRAINEE_FK FOREIGN KEY (TraineeID) REFERENCES Trainee(TraineeID)

)
GO

CREATE TABLE [MemberShip]
(
    [MembershipID] INT IDENTITY(1,1) ,
    [TraineeID] int NOT NULL,
    [start] DATE NOT NULL,
    [end] DATE NOT NULL,
    [type] nvarchar(255) NOT NULL,

    CONSTRAINT MEMBERSHIP_PK PRIMARY KEY (MembershipID),
    CONSTRAINT MEMBERSHIP_TRAINEE_FK FOREIGN KEY (TraineeID) REFERENCES Trainee (TraineeID)

)
GO

CREATE TABLE [Report]
(
    [ReportID] INT IDENTITY(1,1) ,
    [TraineeID] int NOT NULL,
    [Weight] float NOT NULL,
    [Height] int NOT NULL,
    [Description] TEXT NOT NULL,
    CONSTRAINT REPORT_PK PRIMARY KEY (ReportID),
    CONSTRAINT REPORT_TRAINEE_FK  FOREIGN KEY (TraineeID) REFERENCES Trainee (TraineeID)
)
GO

CREATE TABLE [Programs]
(
    [ProgramID] INT IDENTITY(1,1) ,
    [Name] nvarchar(255) NOT NULL UNIQUE,
    [description] nvarchar(255) NOT NULL,
    [Schedule] nvarchar(255) NOT NULL,
    [TrainerID] INT NOT NULL,
    [Capacity] int NOT NULL,

    CONSTRAINT PROGRAMS_PK PRIMARY KEY (ProgramID),
    CONSTRAINT PROGRAMS_TRAINER_FK FOREIGN KEY (TrainerID) REFERENCES Trainer (TrainerID)
)
GO

CREATE TABLE [Product]
(
    [ProductID] INT IDENTITY(1,1),
    [ProdcutName] nvarchar(255) NOT NULL UNIQUE,
    [ProductType] nvarchar(255) NOT NULL,
    [Price] float NOT NULL,
    [Quantity] int CHECK (Quantity >= 1) NULL,
    [ExpiryDate] DATE not null,
    [CafateriaID] int null,
    CONSTRAINT PRODUCT_PK PRIMARY KEY (ProductID)

)
GO

--ALTER TABLE [Product]
--ADD CONSTRAINT PRODUCT_CAFETERIA_FK
--FOREIGN KEY (CafeteriaID) REFERENCES Cafeteria(CafeteriaID);

CREATE TABLE [Cafateria]
(

    [CafateriaID] INT IDENTITY(1,1),
    [EmployeeID] int NOT NULL,
    [ProductID] int NOT NULL,
    [NumofTables] int NULL ,

    CONSTRAINT CAFATERIA_PK PRIMARY KEY (CafateriaID),
    CONSTRAINT CAFATERIA_EMPLOYEE_FK FOREIGN KEY (EmployeeID) REFERENCES Employee (EmployeeID),
    CONSTRAINT CAFATERIA_PRODUCT_FK FOREIGN KEY (ProductID) REFERENCES Product (ProductID)
)
GO

CREATE TABLE [Programs_Trainer]
(
    [ProgramID] int NOT NULL,
    [TrainerID] int NOT NULL,
    CONSTRAINT PROGRAMS_TRAINER_PK PRIMARY KEY ([ProgramID], [TrainerID]),
    CONSTRAINT PROGRAMS_TRAINER_ID_FK FOREIGN KEY (TrainerID) REFERENCES Trainer(TrainerID),
    CONSTRAINT PROGRAMS_PROGRAM_ID_FK FOREIGN KEY (ProgramID) REFERENCES Programs(ProgramID)

);
GO

CREATE TABLE [Programs_Trainee]
(
    [ProgramID] int NOT NULL,
    [TraineeID] int NOT NULL,

    CONSTRAINT PROGRAMS_TRAINEE_PK PRIMARY KEY  ([ProgramID], [TraineeID]),
    CONSTRAINT PROGRAMS_TRAINEE_PROGRAMID_FK FOREIGN KEY (ProgramID) REFERENCES Programs(ProgramID),
    CONSTRAINT PROGRAMS_TRAINEE_ID_FK FOREIGN KEY (TraineeID) REFERENCES Trainee(TraineeID)


);
GO

CREATE TABLE [Equipment_Programs]
(
    [EquipmentID] int NOT NULL,
    [ProgramID] int NOT NULL,

    CONSTRAINT EQUIPMENT_PROGRAMS_PK PRIMARY KEY ([EquipmentID], [ProgramID]),
    CONSTRAINT EQUIPMENT_PROGRAMS_EQUIPMENTID_FK FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID),
    CONSTRAINT EQUIPMENT_PROGRAMS_PROGRAMID_FK FOREIGN KEY (ProgramID) REFERENCES Programs(ProgramID),


);
GO
--Insertions

--Insert Into Users
INSERT INTO Users
    (Username, PasswordHash, Email, U_Address, BirthDate)
VALUES
    ('john_do', 'hashed_passwor', 'john.oe@example.com', '123 Main St', '1990-01-01');

--Insert Into Trainee
INSERT INTO Trainee
    (StartMembership, EndMembership, UserID)
SELECT '2024-04-23', '2025-04-23', 2
WHERE NOT EXISTS (
    SELECT 1
    FROM Trainer
    WHERE Trainer.UserID = 2
)AND NOT EXISTS (
    SELECT 1
    FROM Employee
    WHERE Employee.UserID = 5
);

--Insert into Employee
INSERT INTO Employee
    (EmployeeSalary, UserID)
SELECT 50000.00, 3
WHERE NOT EXISTS (
    SELECT 1
    FROM Trainee
    WHERE Trainee.UserID = 3
)AND NOT EXISTS (
    SELECT 1
    FROM Trainer
    WHERE Trainer.UserID = 3
);

--Insert into Trainer
INSERT INTO Trainer
    (TrainerRole, UserID)
SELECT 'Coach', 5
WHERE NOT EXISTS (
    SELECT 1
    FROM Trainee
    WHERE Trainee.UserID = 5
)
    AND NOT EXISTS (
    SELECT 1
    FROM Employee
    WHERE Employee.UserID = 5
);

--Insert Into Equipment
INSERT INTO Equipment
    (EquipmentName, [Condition])
VALUES
    ('Treadmill', 'Good');

--Insert into Transactions
INSERT INTO Transactions
    (TransactionName, Amount, Date, TraineeID, EmployeeID)
VALUES
    ('Membership Fee', 100.00, '2024-04-23', 1, 1);

--Insert Into Membership
INSERT INTO Membership
    (TraineeID, [start], [end], [type])
VALUES
    (1, '2024-04-23', '2025-04-23', 'Annual');

--Inserto into Report
INSERT INTO Report
    (TraineeID, Weight, Height, Description)
VALUES
    (1, 70.5, 175, 'Report description goes here.');

--Insert into Programs
INSERT INTO Programs
    (Name, description, Schedule, TrainerID, Capacity)
VALUES
    ('Weight Loss Program', 'This program focuses on weight loss through exercise and diet.', 'Monday to Friday, 6:00 PM - 7:00 PM', 1, 20);

--Insert into Product
INSERT INTO Product
    (ProdcutName, ProductType, Price, Quantity, ExpiryDate, CafeteriaID)
VALUES
    ('Product1', 'Type1', 10.99, 100, '2024-12-31', 1);

--Insert into Cafateria
INSERT INTO Cafeteria
    (EmployeeID, ProductID, NumofTables)
VALUES
    (1, 1, 10);

--Insert into Programs Trainer
INSERT INTO Programs_Trainer
    (ProgramID, TrainerID)
VALUES
    (1, 1);

--Insert into Programs Trainee
INSERT INTO Programs_Trainee
    (ProgramID, TraineeID)
VALUES
    (1, 1);

--Insert into Programs Equipment
INSERT INTO Equipment_Programs
    (EquipmentID, ProgramID)
VALUES
    (1, 1);



GO
--Filter Products By Type
CREATE PROCEDURE FilterProductsByType
    @p_ProductType NVARCHAR(255)
AS
BEGIN
    SELECT *
    FROM Product
    WHERE ProductType = @p_ProductType;
END;


-- Execute the stored procedure with a specific ProductType using EXECUTE
EXECUTE FilterProductsByType @p_ProductType = 'Type1';


GO
--Select User Name by User ID
CREATE PROCEDURE SelectUsernameByID
    @p_UserID INT
AS
BEGIN
    DECLARE @UserType NVARCHAR(50);

    -- Determine the user type based on the provided User ID
    SELECT @UserType = 
        CASE
            WHEN EXISTS (SELECT 1
        FROM Trainee
        WHERE Trainee.UserID = @p_UserID) THEN 'Trainee'
            WHEN EXISTS (SELECT 1
        FROM Employee
        WHERE Employee.UserID = @p_UserID) THEN 'Employee'
            WHEN EXISTS (SELECT 1
        FROM Trainer
        WHERE Trainer.UserID = @p_UserID) THEN 'Trainer'
            ELSE NULL
        END;

    -- Select the username based on the user type
    IF @UserType = 'Trainee'
    BEGIN
        SELECT Users.Username AS TraineeName
        FROM Users , Trainee
        WHERE Users.UserID = @p_UserID and Users.UserID = Trainee.UserID;
    END
    ELSE IF @UserType = 'Employee'
    BEGIN
        SELECT Users.Username AS EmployeeName
        FROM Users , Employee
        WHERE Users.UserID = @p_UserID and Users.UserID = Employee.UserID
    END
    ELSE IF @UserType = 'Trainer'
    BEGIN
        SELECT Users.Username AS TrainerName
        FROM Users , Trainer
        WHERE Users.UserID = @p_UserID and Users.UserID = Trainer.UserID
    END
    ELSE
    BEGIN
        -- Handle the case where the user type is not recognized
        PRINT 'User type not recognized.';
    END;
END;
GO


--Execute of Selected User Name by UserID 
EXECUTE SelectUsernameByID @p_UserID = 2;
GO


--Select Age
CREATE PROCEDURE SelectAge
    @p_UserID INT
AS
BEGIN
    DECLARE @UserType NVARCHAR(50);

    -- Determine the user type based on the provided User ID
    SELECT @UserType = 
        CASE
            WHEN EXISTS (SELECT 1
        FROM Trainee
        WHERE Trainee.UserID = @p_UserID) THEN 'Trainee'
            WHEN EXISTS (SELECT 1
        FROM Employee
        WHERE Employee.UserID = @p_UserID) THEN 'Employee'
            WHEN EXISTS (SELECT 1
        FROM Trainer
        WHERE Trainer.UserID = @p_UserID) THEN 'Trainer'
            ELSE NULL
        END;

    IF @UserType = 'Trainee' 
    BEGIN
        SELECT Users.Age as TraineeAge
        FROM Trainee , Users
        WHERE Users.UserID = @p_UserID and Users.UserID = Trainee.UserID;
    END
    ELSE IF @UserType = 'Trainer' 
    BEGIN
        SELECT Users.Age as TrainerAge
        FROM Trainer  , Users
        WHERE Users.UserID = @p_UserID and Users.UserID = Trainer.UserID;
    END
	ELSE IF @UserType = 'Employee'
    BEGIN
        SELECT Users.Age AS EmployeeAge
        FROM Users , Employee
        WHERE Users.UserID = @p_UserID and Users.UserID = Employee.UserID
    END
	ELSE
    BEGIN
        -- Handle the case where the user type is not recognized
        PRINT 'User type not recognized.';
    END;
END;
GO

--Execute Select Age User ID
EXECUTE SelectAge @p_UserID = 2;
GO




--Select address of trainee/trainer
CREATE PROCEDURE SelectAddress
    @p_UserID INT
AS
BEGIN
    DECLARE @UserType NVARCHAR(50);

    -- Determine the user type based on the provided User ID
    SELECT @UserType = 
        CASE
            WHEN EXISTS (SELECT 1
        FROM Trainee
        WHERE Trainee.UserID = @p_UserID) THEN 'Trainee'
            WHEN EXISTS (SELECT 1
        FROM Employee
        WHERE Employee.UserID = @p_UserID) THEN 'Employee'
            WHEN EXISTS (SELECT 1
        FROM Trainer
        WHERE Trainer.UserID = @p_UserID) THEN 'Trainer'
            ELSE NULL
        END;

    IF @UserType = 'Trainee' 
    BEGIN
        SELECT Users.U_Address as TraineeAddress
        FROM Trainee , Users
        WHERE Users.UserID = @p_UserID and Users.UserID = Trainee.UserID;
    END
    ELSE IF @UserType = 'Trainer' 
    BEGIN
        SELECT Users.U_Address as TrainerAddress
        FROM Trainer , Users
        WHERE Users.UserID = @p_UserID and Users.UserID = Trainer.UserID;
    END
	ELSE IF @UserType = 'Employee'
    BEGIN
        SELECT Users.U_Address AS EmployeeAddress
        FROM Users , Employee
        WHERE Users.UserID = @p_UserID and Users.UserID = Employee.UserID
    END
	ELSE
    BEGIN
        -- Handle the case where the user type is not recognized
        PRINT 'User type not recognized.';
    END;
END;

-- Execute Select Address
EXECUTE SelectAddress @p_UserID = 2;


