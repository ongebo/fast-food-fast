orders = list()
food_items = list()
customers = list()
admins = list()


class Order:
    def create_order(self, customer, items, cost):
        order = {'id': len(orders), 'customer': customer, 'items': items, 'cost': cost}
        orders.append(order)
        return order
    
    def read(self, id=None):
        if id == None:
            return orders
        else:
            return orders[id]
    
    def update_order(self, id, customer, items, cost):
        order = orders[id]
        order['customer'] = customer
        order['items'] = items
        order['cost'] = cost
    
    def delete_order(self, id):
        del orders[id]
        return True


class FoodItem:
    def create_food_item(self, item, unit, rate):
        food_item = {'id': len(food_items), 'item': item, 'unit': unit, 'rate': rate}
        return food_item
    
    def read_food_items(self, id=None):
        if id == None:
            return food_items
        for food in food_items:
            if food['id'] == id:
                return food
    
    def update_food_item(self, id, item, unit, rate):
        item_to_update = food_items[id]
        item_to_update['item'] = item
        item_to_update['unit'] = unit
        item_to_update['rate'] = rate
    
    def delete_food_item(self, id, item, unit, rate):
        del food_items[id]
        return True


class Customer:
    def create_customer(self, username, email, telephone, password):
        customer = {'username': username, 'email': email, 'telephone': telephone,
                    'password': password}
        if len(customers) != 0:
            customer['id'] = customers[len(customers) - 1]['id'] + 1
        else:
            customer['id'] = 0
        return customer
    
    def read_customers(self, id=None):
        if id == None:
            return customers
        for customer in customers:
            if customer['id'] == id:
                return customer
    
    def update_customer(self, id, username, email, telephone, password):
        customer_to_update = None
        for customer in customers:
            if customer['id'] == id:
                customer_to_update = customer
                break
        customer_to_update['username'] = username
        customer_to_update['email'] = email
        customer_to_update['telephone'] = telephone
        customer_to_update['password'] = password
    
    def delete_customer(self, id):
        index = None
        for i in range(len(customers)):
            if customers[i]['id'] == id:
                index = i
                break
        del customers[index]
        return True


class Admin:
    def create_admin(self, name, password):
        admin = {'name': name, 'password': password}
        if len(admins) == 0:
            admin['id'] = 0
        else:
            admin['id'] = admins[len(admins) - 1]['id'] - 1
        return admin
    
    def read_admins(self, id=None):
        if id == None:
            return admins
        else:
            for admin in admins:
                if admin['id'] == id:
                    return admin
    
    def update_admin(self, id, name, password):
        for admin in admins:
            if admin['id'] == id:
                admin['name'] = name
                admin['password'] = password
    
    def delete_admin(self, id):
        index = None
        for i in range(len(admins)):
            if admins[i]['id'] == id:
                index = i
                break
        del admins[index]
        return True
