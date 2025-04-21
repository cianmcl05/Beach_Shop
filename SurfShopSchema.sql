
USE surfshop;


CREATE TABLE Store (
    Store_ID INT PRIMARY KEY AUTO_INCREMENT,
    Location VARCHAR(255) NOT NULL,
    Store_Name VARCHAR(255) NOT NULL
);

CREATE TABLE Employee (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Role ENUM('employee', 'manager', 'owner') DEFAULT 'employee',

    Password VARCHAR(255) NOT NULL -- Store hashed passwords
);

CREATE TABLE Employee_Time (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    EmpID INT,
    ClockIn DATETIME NOT NULL,
    ClockOut DATETIME NOT NULL,
    Register_In DECIMAL(10,2) DEFAULT 0.00,
    Register_Out DECIMAL(10,2) DEFAULT 0.00,
    StoreID INT,
    FOREIGN KEY (EmpID) REFERENCES Employee(ID) ON DELETE CASCADE,
    FOREIGN KEY (StoreID) REFERENCES Store(Store_ID) ON DELETE SET NULL
);

CREATE TABLE End_of_Day_Sales (
    Date DATETIME PRIMARY KEY,
    Reg DECIMAL(10,2) NOT NULL,
    Credit DECIMAL(10,2) NOT NULL,
    Cash_in_Envelope DECIMAL(10,2) NOT NULL,
    EmpID INT,
    StoreID INT,
    FOREIGN KEY (EmpID) REFERENCES Employee(ID) ON DELETE SET NULL,
    FOREIGN KEY (StoreID) REFERENCES Store(Store_ID) ON DELETE SET NULL
);

CREATE TABLE Expenses (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(255) NOT NULL,
    Value DECIMAL(10,2) NOT NULL,
    Date DATE NOT NULL,
    EmpID INT,
    Tax DECIMAL(10,2) DEFAULT 0.00,
    Cash DECIMAL(10,2) DEFAULT 0.00,
    Credit DECIMAL(10,2) DEFAULT 0.00,
    StoreID INT,
    FOREIGN KEY (EmpID) REFERENCES Employee(ID) ON DELETE SET NULL,
    FOREIGN KEY (StoreID) REFERENCES Store(Store_ID) ON DELETE SET NULL
);

CREATE TABLE Payroll (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE NOT NULL,
    EmpID INT,
    Payroll INT NOT NULL,
    FOREIGN KEY (EmpID) REFERENCES Employee(ID) ON DELETE CASCADE
);

CREATE TABLE Invoice (
    InvoiceID INT PRIMARY KEY AUTO_INCREMENT,
    InvoiceNumber VARCHAR(255) UNIQUE NOT NULL,
    Company VARCHAR(255) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Payment_Status ENUM('paid', 'not') DEFAULT 'not',
    Due_Date DATE NOT NULL,
    Company_Status ENUM('Active', 'Closed', 'Vendor', 'Client') DEFAULT 'Active',
    Payment_Type ENUM('check', 'cash', 'card', 'withdrawal') NOT NULL,
    StoreID INT,
    FOREIGN KEY (StoreID) REFERENCES Store(Store_ID) ON DELETE SET NULL
);

CREATE TABLE Merchandise (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Merch_Type VARCHAR(255) NOT NULL,
    Merch_Value DECIMAL(10,2) NOT NULL,
    Purchase_Date DATE NOT NULL,
    StoreID INT,
    FOREIGN KEY (StoreID) REFERENCES Store(Store_ID) ON DELETE SET NULL
);

CREATE TABLE Bonus (
    BonusID INT PRIMARY KEY AUTO_INCREMENT,
    EmpID INT,
    Bonus_Amount DECIMAL(10,2) DEFAULT 0.00,
    Sales DECIMAL(10,2) DEFAULT 0.00,
    Gross DECIMAL(10,2) DEFAULT 0.00,
    Bonus_Percentage DECIMAL(10,2) DEFAULT 0.00,
    Current_Bonus_Percentage DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (EmpID) REFERENCES Employee(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Summary_Balance (
    Month INT,
    Year INT,
    Opening_Balance DECIMAL(10,2),
    Net_Profit DECIMAL(10,2),
    Current_Balance DECIMAL(10,2),
    PRIMARY KEY (Month, Year)
);
ALTER TABLE Withdrawals
ADD COLUMN OwnerName VARCHAR(255) DEFAULT NULL;

CREATE TABLE Withdrawals (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    StoreID INT,
    FOREIGN KEY (StoreID) REFERENCES Store(Store_ID) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS Employee_Activity_Log (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    EmpID INT,
    Name VARCHAR(255),
    Role ENUM('employee', 'manager', 'owner'),
    Action_Type VARCHAR(100),
    Description TEXT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EmpID) REFERENCES Employee(ID) ON DELETE SET NULL
);
ALTER TABLE Payroll
ADD COLUMN StoreID INT,
ADD FOREIGN KEY (StoreID) REFERENCES Store(Store_ID) ON DELETE SET NULL;

ALTER TABLE Expenses
MODIFY COLUMN Date DATETIME NOT NULL;

ALTER TABLE Payroll
ADD COLUMN Pay_With_Bonus DECIMAL(10,2) DEFAULT 0.00;

SELECT * FROM Bonus WHERE EmpID = 2

ALTER TABLE Payroll ADD COLUMN BonusID INT;
ALTER TABLE Payroll ADD CONSTRAINT fk_bonus FOREIGN KEY (BonusID) REFERENCES Bonus(BonusID) ON DELETE SET NULL;
ALTER TABLE Payroll ADD COLUMN Bonus DECIMAL(10,2) DEFAULT 0.00;
ALTER TABLE Bonus ADD COLUMN Bonus_Date DATE AFTER Bonus_Amount;

ALTER TABLE Bonus ADD COLUMN CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP;

CREATE TRIGGER trg_withdrawals_amount_check_bi
BEFORE INSERT ON Withdrawals
FOR EACH ROW
BEGIN
  IF NEW.Amount < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Withdrawal amount cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_withdrawals_amount_check_bu
BEFORE UPDATE ON Withdrawals
FOR EACH ROW
BEGIN
  IF NEW.Amount < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Withdrawal amount cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_payroll_amount_check_bi
BEFORE INSERT ON Payroll
FOR EACH ROW
BEGIN
  IF NEW.Payroll < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Payroll amount cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_payroll_amount_check_bu
BEFORE UPDATE ON Payroll
FOR EACH ROW
BEGIN
  IF NEW.Payroll < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Payroll amount cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_expenses_value_check_bi
BEFORE INSERT ON Expenses
FOR EACH ROW
BEGIN
  IF NEW.Value < 0 OR NEW.Tax < 0 OR NEW.Cash < 0 OR NEW.Credit < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Expense fields (Value, Tax, Cash, Credit) cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_expenses_value_check_bu
BEFORE UPDATE ON Expenses
FOR EACH ROW
BEGIN
  IF NEW.Value < 0 OR NEW.Tax < 0 OR NEW.Cash < 0 OR NEW.Credit < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Expense fields (Value, Tax, Cash, Credit) cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_eods_check_bi
BEFORE INSERT ON End_of_Day_Sales
FOR EACH ROW
BEGIN
  IF NEW.Reg < 0 OR NEW.Credit < 0 OR NEW.Cash_in_Envelope < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'EOD Sales (Reg, Credit, Cash in Envelope) must be non-negative';
  END IF;
END;

CREATE TRIGGER trg_eods_check_bu
BEFORE UPDATE ON End_of_Day_Sales
FOR EACH ROW
BEGIN
  IF NEW.Reg < 0 OR NEW.Credit < 0 OR NEW.Cash_in_Envelope < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'EOD Sales (Reg, Credit, Cash in Envelope) must be non-negative';
  END IF;
END;

CREATE TRIGGER trg_merch_value_check_bi
BEFORE INSERT ON Merchandise
FOR EACH ROW
BEGIN
  IF NEW.Merch_Value < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Merchandise value cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_merch_value_check_bu
BEFORE UPDATE ON Merchandise
FOR EACH ROW
BEGIN
  IF NEW.Merch_Value < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Merchandise value cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_invoice_amount_check_bi
BEFORE INSERT ON Invoice
FOR EACH ROW
BEGIN
  IF NEW.Amount < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Invoice amount cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_invoice_amount_check_bu
BEFORE UPDATE ON Invoice
FOR EACH ROW
BEGIN
  IF NEW.Amount < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Invoice amount cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_clock_times_check_bi
BEFORE INSERT ON Employee_Time
FOR EACH ROW
BEGIN
  IF NEW.ClockOut <= NEW.ClockIn THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'ClockOut must be after ClockIn';
  END IF;
END;

CREATE TRIGGER trg_clock_times_check_bu
BEFORE UPDATE ON Employee_Time
FOR EACH ROW
BEGIN
  IF NEW.ClockOut <= NEW.ClockIn THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'ClockOut must be after ClockIn';
  END IF;
END;

CREATE TRIGGER trg_bonus_check_bi
BEFORE INSERT ON Bonus
FOR EACH ROW
BEGIN
  IF NEW.Bonus_Amount < 0 OR NEW.Sales < 0 OR NEW.Gross < 0 OR
     NEW.Bonus_Percentage < 0 OR NEW.Current_Bonus_Percentage < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Bonus fields cannot be negative';
  END IF;
END;

CREATE TRIGGER trg_bonus_check_bu
BEFORE UPDATE ON Bonus
FOR EACH ROW
BEGIN
  IF NEW.Bonus_Amount < 0 OR NEW.Sales < 0 OR NEW.Gross < 0 OR
     NEW.Bonus_Percentage < 0 OR NEW.Current_Bonus_Percentage < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Bonus fields cannot be negative';
  END IF;
END;
