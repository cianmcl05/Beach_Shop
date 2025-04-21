# Beach_Shop
Beach shop finances

---

###  STEPS TO RUN APP

- Use the `surfshop_demo_3` branch — it is the most recent.
- Run the **new schema**: `SurfShopSchema.sql`.
- To see all features, create **3 different accounts**:  
  - An employee  
  - A manager  
  - An owner  

- Manager key: `"manager"`  
- Owner key: `"owner"`

>  **Before running the app**, make sure to add stores to the database:  
> Copy and paste this SQL:

```sql
INSERT INTO Store (Location, Store_Name)
VALUES
    ('Clearwater', 'Clearwater Store'),
    ('St. Petersburg', 'St. Pete Store'),
    ('Siesta Key', 'Siesta Store');
```
When logging in, select the store where you want your account to be assigned.

TO START THE APP

Navigate to app.py and run it.

ABOUT THE APP

This app serves as:

An employee clock in/out system

A tool to manage:

Expenses

Sales

Profit

Invoices

Merchandise

Payroll

Bonuses based on sales

USER ROLES
Employees can:

Clock in/out

Input expenses

Submit end-of-day sales

Enter register content

Managers can:

Do everything employees can (except clocking in/out)

View/edit payroll

Manage stores

Generate profit summaries

Manage invoices

Audit employee activity

Owners can:

Do everything managers can

Withdraw money based on net profit

Excludes payroll + merchandise + expense reserves

ACCESS RESTRICTIONS
Managers can only view current month data.

Owners can view all historical data.

Each store's data is stored individually and reflected across pages.

