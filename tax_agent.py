user_data = {
    "name": "John Smith",
    "ssn": "123-45-6789", 
    "filing status": "married filing jointly",  
    "w2 income": 40000,
    "income 1099": 10000,
    "dependents": 2,
    "deductions": 6000,
    "withholding": 3500
}
invalid_user_data = {
    "name": "John Smith",
   #"ssn": "123-45-6789", 
   #"filing_status": "single", 
    "w2 income": 40000,
    "income 1099": 10000, 
    "dependents": 2,
    "deductions": 6000,  
     "withholding": 3500
}

def validate_data(user_data):
    required_fields = ["name", "ssn", "filing status", "w2 income", "income 1099", "dependents", "deductions", "withholding"]
    is_valid = True
    
    for field in required_fields:
        if field not in user_data or user_data[field] == "" or user_data[field] is None:
            print(field + " is missing")
            is_valid = False

    return is_valid

def calculate_tax(user_data):
    w2_income = user_data["w2 income"]
    income_1099 = user_data["income 1099"]
    deductions = user_data["deductions"]
    dependents = user_data["dependents"] 
    filing_status = user_data["filing status"]
    withholding = user_data["withholding"]

    total_income = w2_income + income_1099
    taxable_income = total_income - deductions - (dependents * 2000)
    if taxable_income < 0:
        taxable_income = 0

    if filing_status == "single":
        tax_rate = 0.10
    elif filing_status == "married_filing_jointly":
        tax_rate = 0.08
    elif filing_status == "head_of_household":
        tax_rate = 0.09
    else:
        tax_rate = 0.10
    
    tax = taxable_income * tax_rate
    if withholding > tax:
        refund = withholding - tax
        amount_owed = 0
    else:
        refund = 0
        amount_owed = tax - withholding

    return total_income, taxable_income, tax, refund, amount_owed

def generate_summary(user_data, total_income, taxable_income, tax_amount, refund, amount_owed):
    print("-----------Tax Summary------------------")
    print("Name:", user_data["name"])
    print("Total Income:", total_income)
    print("Filing Status:", user_data["filing status"])
    print("Deductions:", user_data["deductions"])
    print("Dependents:", user_data["dependents"])
    print("Taxable Income:", taxable_income)
    print("Estimated Tax Owed:", tax_amount)
    print("Withholding:", user_data["withholding"])
    print("Estimated Refund:", refund)
    print("Amount Owed:", amount_owed)

if validate_data(user_data):
    print("Data is valid")
    total_income, taxable_income, tax_amount, refund, amount_owed = calculate_tax(user_data)
    generate_summary(user_data, total_income, taxable_income, tax_amount, refund, amount_owed)
else:
    print("Data is not valid")

print("\n--- Testing Invalid Data ---")

if validate_data(invalid_user_data):
    taxable_income, tax_amount, refund, amount_owed = calculate_tax(invalid_user_data)
    generate_summary(invalid_user_data, taxable_income, tax_amount, refund, amount_owed)
else:
    print("Data is not valid")