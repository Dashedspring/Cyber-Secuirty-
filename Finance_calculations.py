import math
# Printing the input options available on serperate lines. 
print("Investment - to calculate the amount of interest you'll earn on your investment,\nBond - to calculate the amount youll have to pay on a home load,\nEnter either 'investment' or 'bond' from the menu above to proceed")

#storing the decision as a variable.
Decision = (input("which option are you picking?"))

#Adding lower function to ensure data input is captured regardless of capitalizaion
if Decision.lower() == "investment":
# Capture the information requred for investment calculation as integer.
     investment = int(input("How much money are you deposesting?"))   
     interest_rate = int(input("What is the interest rate?")) 
     time = int(input("how many years are you planning on investing?"))

#capturing input compound or interest
     interest = (input("compound or simple?:"))

#If statement to decide on correct calculation based on input. storing the answer as a variable so that an output message can be displayed.
     if interest == "simple":
       Simple_int = (investment * (1 + (interest_rate/100)*time))      
       print("The Simple interest you will receive is {}.".format(Simple_int)) 
     if interest == "compound":
        Compound_int = float(investment * math.pow((1+(interest_rate/100)),time)),
        print("The compound interest you will receive is {}.".format("%.2f" % Compound_int)) 


# capture the information as a float to round up the months. Elif statement as input is different. 
elif Decision.lower() == "bond":
    House_value = float(input("How much is the present value of the house?"))
    interest_rate = float(input("What is the interest rate?")) 
    monthly_payment = float(input("How many months will you take to repay the bond?"))
    monthly_interest_rate = ((interest_rate/100)/12)
    repayment = float(monthly_interest_rate * House_value)/(1 - (1 + monthly_interest_rate)**(-monthly_payment))
    
# print the calculation to 2 decimal places. With a clear output message.    
    print ("The amount you will have to pay back each month is {}.".format("%.2f" % repayment))



# erorr message to be displayed if the user doesnt input correct values       
else:
  print("You must pick Investment or Bond")
