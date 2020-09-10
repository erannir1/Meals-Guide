

#########################################
# 1
#########################################


class Food:

    def __init__(self, name, price, calories, ingredients):
        self.name = name
        self.price = price
        self.calories = calories
        self.ingredients = ingredients
        if not self.validate():
            raise ValueError('Invalid input: calories and price input must be higher than zero')

    def validate(self):

        if self.price > 0 and self.calories > 0:
            return True
        else:
            return False

    def __repr__(self):
        return self.name + " costs " + str(self.price) + " NIS and contains: " + str(self.ingredients) +" (only " + str(self.calories) +" calories)"

    def __lt__(self, other):
        if self.price < other.price:
            return True
        elif self.price == other.price:
            if len(self.ingredients) < len(other.ingredients):
                return True
            else:
                return False
        else:
            return False

    def __eq__(self, other):
        if self.price == other.price and len(self.ingredients) == len(other.ingredients):
            return True
        else:
            return False

    def __le__(self, other):
        if self < other or self == other:
            return True
        else:
            return False

    def add_ingredient(self, ingredient, calories):
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)
        else:
            raise ValueError(ingredient +" already exists")
        if self.calories > 0:
            self.calories += calories
        else:
            raise ValueError('Calories input must be higher than zero')

    def remove_ingredient(self, ingredient, calories):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
        else:
            raise ValueError(ingredient + " doesn't exist")
        if self.calories > calories:
            self.calories -= calories
        else:
            raise ValueError("Calories value must br higher than zero!")

#########################################
# 2
#########################################


class Beverage:

    def __init__(self, name, price, is_diet):
        self.name = name
        self.price = price
        self.is_diet = is_diet
        if not self.validate():
            raise ValueError("Price must be higher than zero!")

    def validate(self):
        if self.price > 0:
            return True
        else:
            return False

    def __repr__(self):
        if self.is_diet:
            return self.name + " costs " + str(self.price) + " NIS (is diet)"
        else:
            return self.name + " costs " + str(self.price) + " NIS"

    def get_price(self, size="normal"):
        if size == "small":
            self.price *= 0.8
        elif size == "normal":
            self.price *= 1.0
        elif size == "big":
            self.price *= 1.2
        else:
            raise ValueError("Invalid size")
        return self.price

#########################################
# 3
#########################################


class Meal:

    def __init__(self, name, beverage, food):
        self.name = name
        self.beverage = beverage
        self.food = food

    def __repr__(self):
        if self.is_healthy():
            return self.name + " meal costs " + str(self.beverage.price + sum(i.price for i in self.food)) + " NIS (healthy!)"
        else:
            return self.name + " meal costs " + str(self.beverage.price + sum(i.price for i in self.food)) + " NIS"

    def get_price(self):
        meal_price = self.beverage.get_price("small")
        min_price_food = min(i.price for i in self.food)
        for i in self.food:
            if i.price != min_price_food:
                meal_price += i.price
        return meal_price

    def __contains__(self, ingredient):
        for i in self.food:
            for j in i.ingredients:
                if j == ingredient:
                    return True
        return False

    def is_healthy(self):
        flag = True
        if self.beverage.is_diet is False:
            flag = False
        sum_cal = 0
        for i in self.food:
            sum_cal += i.calories
        if sum_cal >= 800:
            flag = False
        return flag

#########################################
# 4
#########################################


def load_meal(file_name):
    try:
        with open(file_name, 'r') as y:
            x = y.readlines()
            food_lst = []
            for line in x:
                lx = line.rstrip("\n").split(",")
                if lx[0] != "food" and lx[0] != "beverage":
                    print "Row " + str(x.index(line)) + " is not valid"
                elif lx[0] == "beverage":
                    if lx[2] < 0 or lx[2].isalpha() is True or lx[2].isalnum() is False:
                        print "Row " + str(x.index(line)) + " is not valid"
                    elif lx[3] != "t" and lx[3] != "f":
                        print "Row " + str(x.index(line)) + " is not valid"
                    else:
                        if lx[3] == "t":
                            drink = Beverage(lx[1],float(lx[2]),True)
                        else:
                            drink = Beverage(lx[1], float(lx[2]), False)
                elif lx[0] == "food":
                    if lx[2] < 0 or lx[2].isalpha() is True or lx[2].isalnum() is False:
                        print "Row " + str(x.index(line)) + " is not valid"
                    elif lx[3] < 0 or lx[3].isdigit() is False:
                        print "Row " + str(x.index(line)) + " is not valid"
                    else:
                        food_lst.append(Food(lx[1], float(lx[2]), int(lx[3]), lx[4].split(";")))
            print str(file_name), "meal costs", Meal(file_name, drink, food_lst).get_price(), "NIS loaded successfully."

    except IOError:
        print "Cannot load menu due to IOError"
