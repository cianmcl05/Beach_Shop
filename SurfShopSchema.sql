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
