keywords = {
    # Food & Drinks
    "coffee": "Food",
    "lunch": "Food",
    "dinner": "Food",
    "Burger": "Food",
    "restaurant": "Food",
    "supermarket": "Food",
    "groceries": "Food",
    "snack": "Food",
    "Coffee and lunch": "Food",

    # Transport
    "bus": "Transport",
    "train": "Transport",
    "taxi": "Transport",
    "uber": "Transport",
    "petrol": "Transport",
    "fuel": "Transport",
    "Bus ticket": "Transport",
    
    # Entertainment
    "Netflix": "Entertainment",
    "spotify": "Entertainment",
    "cinema": "Entertainment",
    "games": "Entertainment",
    "movie": "Entertainment",
    
    # Bills & Utilities
    "phone": "Bills",
    "electricity": "Bills",
    "water": "Bills",
    "gas": "Bills",
    "internet": "Bills",
    "rent": "Bills",
    "Phone bill": "Bills",

    # Shopping
    "clothes": "Shopping",
    "shoes": "Shopping",
    "amazon": "Shopping",
    "store": "Shopping",

    # Health & Fitness
    "gym": "Health",
    "doctor": "Health",
    "pharmacy": "Health",

    # Misc / Other
    "gift": "Other",
    "donation": "Other",
    "charity": "Other",
}
# categorizing the payments through a dictionary

currency_symbol = input("What currency symbol would you like?")
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
# importing modules to use later

food_amount = 0
transport_amount = 0
entertainment_amount = 0
bills_amount = 0
shopping_amount = 0
health_amount = 0
other_amount = 0
# to ensure that before anything happens that everything is 0, also to just create the variables that are gonna be used later in the code

df = pd.read_csv("spending.csv", skip_blank_lines= True)
# "reading" the .csv file by basicaly copying it into a database, which is what the rest of this code builds upon

df = df.dropna(axis = 1, how="all")
df = df.dropna(axis = 0, how="all")
#editing the database to remove fully blank columns and rows

print("CSV successfully read:")

required_columns = ["Date", "Description", "Amount"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"CSV missing required column: {col}")
    
if df["Amount"].isnull().any():
    raise ValueError("Error: Some rows in the Amount column are empty.")

if not pd.api.types.is_numeric_dtype(df["Amount"]):
    raise ValueError("Error: Amount column contains non-numeric values.")
#these if statements are for if you are missing a column, or if some rows are empty, or if you have like words under the column like amount

if "Category" not in df.columns:
    df["Category"] = ""
    category_column_index = df.columns.get_loc("Category")
    df["Category"] = df["Description"].map(keywords).fillna("Other")
    for description_row_index,content in enumerate(df["Description"]):
        df.iloc[description_row_index,category_column_index] = keywords[content]
else:
    category_column_index = df.columns.get_loc("Category")
    df["Category"] = df["Description"].map(keywords).fillna("Other")
    for description_row_index,content in enumerate(df["Description"]):
        df.iloc[description_row_index,category_column_index] = keywords[content]
# if statement is to split the cases where the user decides not to categorise their spenidng, for convenience
# on the case where they have categorised it then you locate the column index, to use that value so that when you loop for the rows
#under the description column it categorizes through a dictionary for the description, and then that outputted word is put onto the 
#same row but under the category column
# similar thing for if they haven't categorized it cause you just add a new column first called category, then do the same code as just now 

totals = df.groupby("Category")["Amount"].sum()
food_amount = totals.get("Food", 0)
transport_amount = totals.get("Transport", 0)
entertainment_amount = totals.get("Entertainment", 0)
bills_amount = totals.get("Bills", 0)
shopping_amount = totals.get("Shopping", 0)
health_amount = totals.get("Health", 0)
other_amount = totals.get("Other", 0)
total = food_amount + transport_amount + entertainment_amount + bills_amount + shopping_amount + health_amount + other_amount
#grouping the categories, and then summing the respective amounts for each category, then "fetching" those values, and also getting total

test = df.groupby("Date").sum().drop(["Description", "Category"], axis = 1).reset_index()
test["Day"] = ""
test = test.reindex(columns=["Date", "Day", "Amount"])
test = test.sort_values(by="Date").reset_index(drop=True)
day_column_index = test.columns.get_loc("Day")
for date_row_index,date_row_content in enumerate(test["Date"]):
    date_object = datetime.strptime(date_row_content, "%Y-%m-%d")
    test.iloc[date_row_index,day_column_index] = date_object.strftime("%A")
#making a new dataframe to use for spending trends, used for the line graph

avg_per_day = df.groupby("Date")["Amount"].sum().mean()
avg_per_day_rounded = Decimal(str(avg_per_day)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
#the code to get the average per day 

food_proportion = (food_amount / total)*100
transport_proportion = (transport_amount / total)*100
entertainment_proportion = (entertainment_amount / total)*100
bills_proportion = (bills_amount / total)*100
shopping_proportion = (shopping_amount / total)*100
health_proportion = (health_amount / total)*100
other_proportion = (other_amount / total)*100
#getting proportions for pie chart 

labels = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Health", "Other"]
sizes = [food_proportion, transport_proportion, entertainment_proportion, bills_proportion, shopping_proportion, health_proportion, other_proportion]
filtered_labels = [label for label, size in zip(labels, sizes) if size > 0]
filtered_sizes = [size for size in sizes if size > 0]
plt.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%')
plt.title("Pie Chart On Your Spending")
plt.axis('equal')
plt.figure()
#making labels for categories, and getting rid of the ones if they have no amount, and plotting a pie chart

x = []
y = []

for date_row_index,date_row_content in enumerate(test["Date"]):
    x.append(date_row_content)
for amount_row_index,amount_row_content in enumerate(test["Amount"]):
    y.append(amount_row_content)
highest_spending_amount = max(y)
highest_spending_amount_index = y.index(highest_spending_amount)
plt.plot(x, y, marker='o', linestyle='-', color='b',)
plt.xlabel("Date")
plt.ylabel("Amount (" + currency_symbol + ")")
plt.title("Daily Spending")
#line graph


test = test.rename(columns={"Amount": "Amount (" + currency_symbol + ")"})
df = df.rename(columns={"Amount": "Amount (" + currency_symbol + ")"})
print(df)
#adding the currency symbol to the "Amount" so it looks better

with open("summary.txt", "w") as f:
    f.write("Finance Summary\n\n")
    f.write("Here is your spending on this document:\n")
    f.write(f"Food: {currency_symbol}{float(food_amount)}\n")
    f.write(f"Transport: {currency_symbol}{float(transport_amount)}\n")
    f.write(f"Entertainment: {currency_symbol}{float(entertainment_amount)}\n")
    f.write(f"Bills: {currency_symbol}{float(bills_amount)}\n")
    f.write(f"Shopping: {currency_symbol}{float(shopping_amount)}\n")
    f.write(f"Health: {currency_symbol}{float(health_amount)}\n")
    f.write(f"Other: {currency_symbol}{float(other_amount)}\n")
    f.write(f"And in total you spent: {currency_symbol}{float(total)}\n")
    f.write("Here is how much you have spent per day:\n")
    f.write(test.to_string(index = False))
    f.write("\n\n")
    f.write(f"And the average amount you spent per day is: {currency_symbol}{float(avg_per_day_rounded)}\n")
    f.write(
    f"You spent the most on {datetime.strptime(x[highest_spending_amount_index], '%Y-%m-%d').strftime('%A')} "
    f"({x[highest_spending_amount_index]}), where you have spent {currency_symbol}{highest_spending_amount}\n") 
    f.write(f"Refer to the line and pie chart for spending trends")
plt.show()
plt.show()
#writing the text file summary and then showing the pie chart and line graph