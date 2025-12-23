import pulp

# model
model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# variables
water = pulp.LpVariable('water', lowBound=0, cat='Continuous')
sugar = pulp.LpVariable('sugar', lowBound=0, cat='Continuous')
lemon_juice = pulp.LpVariable('lemon_juice', lowBound=0, cat='Continuous')
fruit_pure = pulp.LpVariable('fruit_pure', lowBound=0, cat='Continuous')

lemonade = pulp.LpVariable('lemonade', lowBound=0, cat='Continuous')
fruit_juice = pulp.LpVariable('fruit_juice', lowBound=0, cat='Continuous')

# constraints
model += 2*lemonade + 1*fruit_juice <= 100, "Water_Constraint"
model += 1*lemonade <= 50, "Sugar_Constraint"
model += 1*lemonade <= 30, "Lemon_Juice_Constraint"
model += 2*fruit_juice <= 40, "Fruit_Pure_Constraint"

# objective function
model += lemonade + fruit_juice, "Optimize_Production"

model.solve()

print(f"Status: {pulp.LpStatus[model.status]}")

for variable in model.variables():
    print(f"{variable.name} = {variable.varValue}")

print(f"Total production quantity = {pulp.value(model.objective)}")
