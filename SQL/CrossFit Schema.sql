CREATE TABLE [Trainee] (
  [TraineeID] int PRIMARY KEY,
  [TraineeName] nvarchar(255),
  [StartMembership] timestamp,
  [EndMembership] timestamp
)
GO

CREATE TABLE [Employee] (
  [EmployeeID] int PRIMARY KEY,
  [EmployeeName] nvarchar(255),
  [EmployeeSalary] float,
  [EmployeeRole] nvarchar(255)
)
GO

CREATE TABLE [Trainer] (
  [TrainerID] int PRIMARY KEY,
  [TrainerName] nvarchar(255),
  [TrainerRole] nvarchar(255)
)
GO

CREATE TABLE [Equipment] (
  [EquipmentID] int PRIMARY KEY,
  [EquipmentName] nvarchar(255),
  [Condition] nvarchar(255)
)
GO

CREATE TABLE [Transactions] (
  [TransactionsID] int PRIMARY KEY,
  [TransactionName] nvarchar(255),
  [Amount] float,
  [Date] timestamp,
  [TraineeID] int
)
GO

CREATE TABLE [MemberShip] (
  [MembershipID] int PRIMARY KEY,
  [TraineeID] int,
  [start] timestamp,
  [end] timestamp,
  [type] nvarchar(255)
)
GO

CREATE TABLE [Report] (
  [ReportID] int PRIMARY KEY,
  [ClientID] int,
  [Weight] float,
  [Height] int
)
GO

CREATE TABLE [Programs] (
  [ProgramID] int PRIMARY KEY,
  [Name] nvarchar(255),
  [description] nvarchar(255),
  [Schedule] nvarchar(255),
  [Trainer] nvarchar(255),
  [Capacity] int
)
GO

CREATE TABLE [Cafateria] (
  [CafateriaID] int PRIMARY KEY,
  [EmployeeID] int,
  [ProductID] int,
  [NumofTables] int
)
GO

CREATE TABLE [Product] (
  [ProductID] int PRIMARY KEY,
  [Supplement] nvarchar(255),
  [Price] float,
  [Qunatity] int,
  [ExpiryDate] timestamp
)
GO

ALTER TABLE [Trainee] ADD FOREIGN KEY ([TraineeID]) REFERENCES [Trainer] ([TrainerID])
GO

CREATE TABLE [Programs_Trainee] (
  [Programs_ProgramID] int,
  [Trainee_TraineeID] int,
  PRIMARY KEY ([Programs_ProgramID], [Trainee_TraineeID])
);
GO

ALTER TABLE [Programs_Trainee] ADD FOREIGN KEY ([Programs_ProgramID]) REFERENCES [Programs] ([ProgramID]);
GO

ALTER TABLE [Programs_Trainee] ADD FOREIGN KEY ([Trainee_TraineeID]) REFERENCES [Trainee] ([TraineeID]);
GO


CREATE TABLE [Programs_Trainer] (
  [Programs_ProgramID] int,
  [Trainer_TrainerID] int,
  PRIMARY KEY ([Programs_ProgramID], [Trainer_TrainerID])
);
GO

ALTER TABLE [Programs_Trainer] ADD FOREIGN KEY ([Programs_ProgramID]) REFERENCES [Programs] ([ProgramID]);
GO

ALTER TABLE [Programs_Trainer] ADD FOREIGN KEY ([Trainer_TrainerID]) REFERENCES [Trainer] ([TrainerID]);
GO


ALTER TABLE [Report] ADD FOREIGN KEY ([ReportID]) REFERENCES [Trainer] ([TrainerID])
GO

ALTER TABLE [MemberShip] ADD FOREIGN KEY ([MembershipID]) REFERENCES [Trainee] ([TraineeID])
GO

ALTER TABLE [Trainee] ADD FOREIGN KEY ([TraineeID]) REFERENCES [Report] ([ReportID])
GO

ALTER TABLE [Product] ADD FOREIGN KEY ([ProductID]) REFERENCES [Cafateria] ([CafateriaID])
GO

ALTER TABLE [Transactions] ADD FOREIGN KEY ([TransactionsID]) REFERENCES [Trainee] ([TraineeID])
GO

CREATE TABLE [Equipment_Programs] (
  [Equipment_EquipmentID] int,
  [Programs_ProgramID] int,
  PRIMARY KEY ([Equipment_EquipmentID], [Programs_ProgramID])
);
GO

ALTER TABLE [Equipment_Programs] ADD FOREIGN KEY ([Equipment_EquipmentID]) REFERENCES [Equipment] ([EquipmentID]);
GO

ALTER TABLE [Equipment_Programs] ADD FOREIGN KEY ([Programs_ProgramID]) REFERENCES [Programs] ([ProgramID]);
GO


ALTER TABLE [Employee] ADD FOREIGN KEY ([EmployeeID]) REFERENCES [Cafateria] ([CafateriaID])
GO

ALTER TABLE [Employee] ADD FOREIGN KEY ([EmployeeID]) REFERENCES [Transactions] ([TransactionsID])
GO
