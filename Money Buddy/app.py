from flask import Flask, render_template, request, redirect

app = Flask(__name__)
namesOfAid = []
moneyFromAid = []
feesForCollege = 0

@app.route("/")
def home_page():
    global feesForCollege
    if feesForCollege <= 0:
        return redirect("/fees")
    else:
        return render_template("home.html", nameList=namesOfAid, moneyList=moneyFromAid, fees=format(feesForCollege, ".2f"))

@app.route("/add", methods=["GET", "POST"])
def add():
    global feesForCollege
    if request.method == "GET":
        return render_template("add.html", fees=feesForCollege)
    else:
        name = request.form.get("aidName")
        money = request.form.get("aidMoney")
        
        if money and name:
            namesOfAid.append(name)
            moneyFromAid.append(money)
            feesForCollege -= float(money)
        else:
            return render_template("add.html", fees=feesForCollege)
        return redirect("/")
    
@app.route("/fees", methods=["GET", "POST"])
def fees():
    global feesForCollege
    global namesOfAid
    global moneyFromAid
    if request.method == "GET":
        edit = request.args.get("edit")
        if edit:
            return render_template("fees.html")
        else:
            if feesForCollege > 0:
                return redirect("/")
            return render_template("fees.html")
    else:
        feesForCollege = request.form.get("fees")
        if feesForCollege:
            feesForCollege = float(feesForCollege)
            namesOfAid = []
            moneyFromAid = []
            return redirect("/")
        else:
            return render_template("fees.html")


@app.route("/debt", methods=["GET", "POST"])
def debt():
    global feesForCollege
    if feesForCollege <= 0:
        return redirect("/fees")
    else:
        if request.method == "GET":
            return render_template("debt.html")
        else:
            pay_amount = 0
            interest_rate = request.form.get("interest")
            years = request.form.get("years")

            if not interest_rate:
                outputString = "Please enter a valid rate!!"
                return render_template("debt.html", outputStr=outputString)
            
            if not years:
                outputString = "Please enter a valid term of the loan!!"
                return render_template("debt.html", outputStr=outputString)
            
            pay_amount = calculate_monthly(feesForCollege, interest_rate, years)

            outputString = f"You will have to pay ${round(pay_amount, 2)} in monthly payments"
            return render_template("debt.html", outputStr=outputString)                                 

def calculate_monthly(principle, rate, time):
    j = float(rate) / 1200
    n = 12 * float(time)
    answer = (1 + j) ** -n
    answer = (1 - answer)
    answer = j / answer
    return principle * answer

@app.route("/extra")
def extra():
    return render_template("extra.html")


if __name__ == "__main__":
    app.run()