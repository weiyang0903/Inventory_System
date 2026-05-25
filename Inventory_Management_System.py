'''
INVENTORY MANAGEMENT SYSTEM (Stationery Store)
Developed by: Chin Wei Yang
'''
import os
import time

# count length of object
def custom_len(obj):
    count = 0
    try:
        for _ in obj:
            count += 1
    except TypeError:
        return 0
    return count

# File Declarations
PRODUCTS_FILE = "products.txt"
CATEGORIES_FILE = "categories.txt"

# ID transfer functions
def generate_id(category_id = None, product_id = None):
    if category_id is not None:
        return f"CA{category_id}"
    if product_id is not None:
        return f"PR{product_id}"
    return None

# Categories class
class Category:
    def __init__(self, category_id, name, activation=True):
        self.category_id = category_id
        self.name = name
        self.activation = bool(int(activation))

    def __str__(self):
        return f"{self.category_id}|{self.name}|{int(self.activation)}"

    @classmethod
    def from_string(cls, string):
        parts = string.strip().split("|")
        if custom_len(parts) == 3:
            return cls(
                category_id = parts[0].strip(),
                name = parts[1].strip(),
                activation = bool(int(parts[2].strip()))
            )
        return None
    
# Products Class
class Product:
    def __init__(self, product_id, name, category, price, stock, activation=True):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = float(price)
        self.stock = int(stock)
        self.activation = bool(int(activation))

    def __str__(self):
        return f"{self.product_id}|{self.name}|{self.category}|{self.price}|{self.stock}|{int(self.activation)}"

    @classmethod
    def from_string(cls, string):
        parts = string.strip().split("|")
        if custom_len(parts) == 6:
            return cls(
                product_id = parts[0].strip(),
                name = parts[1].strip(),
                category = parts[2].strip(),
                price = parts[3].strip(),
                stock = parts[4].strip(),
                activation = parts[5].strip()
            )
        return None

# File handling functions
def read_file(filename):
    if not os.path.exists(filename):
        return []

    file = open(filename, "r")
    lines = []
    for line in file:
        lines.append(line.strip())

    file.close()
    return lines

def write_file(filename, data):
    file = open(filename, "w")
    for line in data:
        file.write(f"{line}\n")

    file.close()
    return True

def append_file(filename, line):
    file = open(filename, "a")
    file.write(f"{line}\n")
    file.close()
    return True

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

# check existing of name
def name_exists(checkp_c, name):
    if checkp_c == "category":
        data = read_file(CATEGORIES_FILE)
    else:
        data = read_file(PRODUCTS_FILE)
    
    name_exists = False
    if data:
        for item_str in data:
            if checkp_c == "category":
                item = Category.from_string(item_str)
            else:
                item = Product.from_string(item_str)
            if item and item.name.upper() == name.upper():
                name_exists = True
                break
    return name_exists


# text decoration functions
def center_text(text, width=60, fill_char=" "):
    if custom_len(text) >= width:
        return text

    padding = width - custom_len(text)
    left_padding = padding // 2
    right_padding = padding - left_padding

    return fill_char * left_padding + text + fill_char * right_padding

def create_horizontal_line(width=60, line_char="-"):
    return line_char * width

def create_box(title, width=60):
    result = [create_horizontal_line(width, "=")]
    result += [center_text(title, width)]
    result += [create_horizontal_line(width, "=")]
    final_str = result[0] + "\n" + result[1] + "\n" + result[2]

    return final_str

# category functions
def manage_catageries():
    while True:
        clearScreen()
        print(create_box("Manage Categories"))

        print("1. View All Categories")
        print("2. Add New Category")
        print("3. Edit Category")
        print("4. Activate/Deactivate Category")
        print("0. Back to Main Menu")

        choice = input("\nPlease select an option: ")

        if choice == "1":
            clearScreen()
            print(create_box("Categories List"))
            view_categories()
            input("\nPress Enter to continue...")
            continue
        elif choice == "2":
            clearScreen()
            print(create_box("Add New Category"))
            add_category()
        elif choice == "3":
            clearScreen()
            print(create_box("Edit Category"))
            edit_category()
        elif choice == "4":
            clearScreen()
            print(create_box("Activate/Deactivate Category"))
            activate_deactivate_category()
        elif choice == "0":
            return True
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def view_categories():

    categories = read_file(CATEGORIES_FILE)
    if not categories:
        print("No categories found.")
        input("Press Enter to continue...")
        return

    print(f"\n{'Category ID':<15} | {'Name':<20} | {'Status':<10}")
    print(create_horizontal_line(60))

    for category_str in categories:
        category = Category.from_string(category_str)
        status = "Active" if category.activation else "Inactive"
        print(f"{category.category_id:<15} | {category.name:<20} | {status:<10}")

def add_category():
    catogeries = read_file(CATEGORIES_FILE)
    if not catogeries:
        new_id = "1"
    else:
        highest_id = 0
        for category_str in catogeries:
            category = Category.from_string(category_str)
            if highest_id < int(category.category_id.replace("CA", "")):
                highest_id = int(category.category_id.replace("CA", ""))
        new_id = str(highest_id + 1)

    new_id = generate_id(category_id=new_id)
    view_categories()
    print(f"\nNew Category ID: {new_id}")

    while True:
        name = input("Category Name (Enter 0 to cancel): ")
        if name == "0":
            print("Operation cancelled.")
            input("Press Enter to Categories Menu...")
            return False
        if not name:
            print("Category Name cannot be empty. Please try again.\n")
            continue
            
        is_exists = name_exists("category", name)
                    
        if is_exists:
            print("Category name already exists. Please try again.\n")
            continue

        break

    while True:
        activation = input("Activate category? (y/n): ").lower()
        if activation == "y":
            activation = True
            break
        elif activation == "n":
            activation = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue

    new_category = Category(new_id, name, activation)
    append_file(CATEGORIES_FILE, new_category)

    print(f"Category '{name}' added successfully!")
    input("\nPress Enter to continue...")
    return True

def edit_category():

    view_categories()
    categories = read_file(CATEGORIES_FILE)
    while True:
        category_id = input("\nEnter the category ID to edit (Enter 0 to cancel): ").upper()

        if category_id == "0":
            print("Operation cancelled.")
            input("Press Enter to continue...")
            return False
        
        if not category_id:
            print("Category ID cannot be empty. Please try again.")
            continue
        break

    found = False
    for category_str in categories:
        category = Category.from_string(category_str)
        if category and category.category_id == category_id:
            found = True
            break
    if not found:
        print("Category not found.")
        input("Press Enter to continue...")
        return False

    while True:
        name = input(f"New Category Name (Press enter to keep old category name)(current: {category.name}): ")
        if not name:
            name = category.name
            break
        is_exists = name_exists("category", name)
                    
        if is_exists:
            print("Category name already exists. Please try again.\n")
            continue
        break

    activation = category.activation

    updated_category = Category(category.category_id, name, activation)
    updated_categories = []
    for c in categories:
        if c == category_str:
            updated_categories.append(updated_category)
        else:
            updated_categories.append(c)

    print("\nEdit successfully!")
    input("Press Enter to Continue...")
    write_file(CATEGORIES_FILE, updated_categories)

def activate_deactivate_category():

    categories = read_file(CATEGORIES_FILE)

    view_categories()
    while True:
        category_id = input("\nEnter the category ID to activate/deactivate (Enter 0 to cancel): ").upper()

        if category_id == "0":
            print("Operation cancelled.")
            input("Press Enter to continue...")
            return False
        
        if not category_id:
            print("Category ID cannot be empty. Please try again.")
            continue
        break

    found = False
    for category_str in categories:
        category = Category.from_string(category_str)
        if category and category.category_id == category_id:
            found = True
            break
    if not found:
        print("Category not found.")
        input("Press Enter to continue...")
        return False

    print(f"\nCategory Name: {category.name}")
    print(f"Current Status: {'Active' if category.activation else 'Inactive'}")

    while True:
        activation = input("Activate/Deactivate category? (y/n): ").lower()
        if activation == "y":
            if category.activation:
                products = read_file(PRODUCTS_FILE)
                has_linked_products = False
                for product_str in products:
                    product = Product.from_string(product_str)
                    if product and product.category == category.category_id:
                        has_linked_products = True
                        break

                if has_linked_products:
                    view_products(category_id=category_id)
                    print(f"Cannot deactivate category '{category.name}'. Products are still linked to this category.")
                    input("Press Enter to continue...")
                    return False
                else:
                    category.activation = not category.activation
            else:
                category.activation = not category.activation
            break
        elif activation == "n":
            print("No changes made.")
            input("Press Enter to continue...")
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue

    updated_category = Category(category.category_id, category.name, category.activation)
    updated_categories = []
    for c in categories:
        if c == category_str:
            updated_categories.append(updated_category)
        else:
            updated_categories.append(c)
    write_file(CATEGORIES_FILE, updated_categories)
    print(f"Category '{category.name}' has been {'activated' if category.activation else 'deactivated'}.")
    input("\nPress Enter to continue...")
    return True

def manage_products():
    while True:
        clearScreen()
        print(create_box("Manage Products"))

        print("1. View All Products")
        print("2. Add New Product")
        print("3. Edit Product")
        print("4. Activate/Deactivate Product")
        print("0. Back to Main Menu")

        choice = input("\nPlease select an option: ")

        if choice == "1":
            clearScreen()
            print(create_box("All Product"))
            view_products(filter=1)
            input("\nPress Enter to continue...")
            continue
        elif choice == "2":
            clearScreen()
            print(create_box("Add New Product"))
            add_product()
        elif choice == "3":
            clearScreen()
            print(create_box("Edit Product"))
            edit_product()
        elif choice == "4":
            clearScreen()
            print(create_box("Activate/Deactivate Product"))
            activate_deactivate_product()
        elif choice == "0":
            return True
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def view_products(category_id=None, filter=None):

    categories = read_file(CATEGORIES_FILE)
    if category_id:
        for category_str in categories:
            category = Category.from_string(category_str)
            if category and category_id == category.category_id:
                title = f"Products in {category.name}"
                break

    products = read_file(PRODUCTS_FILE)
    if not products:
        print("No products found.")
        input("Press Enter to continue...")
        return

    category_names = {}
    for category_str in categories:
        category = Category.from_string(category_str)
        if category:
            category_names[category.category_id] = category.name

    filtered_products = []
    for product_str in products:
        product = Product.from_string(product_str)
        if category_id and category_id != product.category:
            continue
        filtered_products.append(product)

    if not filtered_products:
        if category_id:
            print("No products found in this category.")
        else:
            print("No active products found.")
        input("Press Enter to continue...")
        return

    if not category_id and filter == 1:
        print("\nSort Products By: ")
        print("1. Name (A-Z)")
        print("2. Name (Z-A)")
        print("3. Price (Low to High)")
        print("4. Price (High to Low)")
        print("5. Stock (Low to High)")

        sortChoice = input("\nSelect sorting option, otherwise sort by Product ID: ")

        i = 0
        while i < len(filtered_products):
            j = 0
            while j < len(filtered_products) - i - 1:
                swap = False
                if sortChoice == "1":
                    if filtered_products[j].name.lower() > filtered_products[j+1].name.lower():
                        swap = True
                elif sortChoice == "2":
                    if filtered_products[j].name.lower() < filtered_products[j+1].name.lower():
                        swap = True
                elif sortChoice == "3":
                    if filtered_products[j].price > filtered_products[j+1].price:
                        swap = True
                elif sortChoice == "4":
                    if filtered_products[j].price < filtered_products[j+1].price:
                        swap = True
                elif sortChoice == "5":
                    if filtered_products[j].stock > filtered_products[j+1].stock:
                        swap = True

                if swap:
                    temp = filtered_products[j]
                    filtered_products[j] = filtered_products[j+1]
                    filtered_products[j+1] = temp
                j+=1
            i+=1

    print(f"\n{'Product ID':<10} | {'Name':<20} | {'Category':<15} | {'Price(RM)':<10} | {'Stock':<8} | {'Status':<10}")

    print(create_horizontal_line(90))

    for product in filtered_products:
        if len(product.name) > 20:
            displayName = product.name[:17] + "..."
        else:
            displayName = product.name

        category_name = category_names.get(product.category)
        displayCategory = category_name
        if len(category_name) > 15:
            displayCategory = category_name[:12] + "..."
        else:
            displayCategory = category_name

        status = "Active" if product.activation else "Inactive"
        print(f"{product.product_id:<10} | {displayName:<20} | {displayCategory:<15} | {product.price:<10.2f} | {product.stock:<8} | {status:<10}")

def add_product():

    products = read_file(PRODUCTS_FILE)
    if not products:
        new_id = "1"
    else:
        highest_id = 0
        for product_str in products:
            product = Product.from_string(product_str)
            if highest_id < int(product.product_id.replace("PR", "")):
                highest_id = int(product.product_id.replace("PR", ""))
        new_id = str(highest_id + 1)

    new_id = generate_id(product_id=new_id)
    view_products()
    print(f"New Product ID: {new_id}")

    while True:
        name = input("Product Name (Enter 0 to cancel): ")
        if name == "0":
            print("Operation cancelled.")
            input("Press Enter to continue...")
            return False
        if not name:
            print("Product Name cannot be empty. Please try again.")
            continue
        is_exists = name_exists("product", name)
                    
        if is_exists:
            print("Product name already exists. Please try again.\n")
            continue
        break

    while True:
        categories = read_file(CATEGORIES_FILE)
        active_categories = []
        for category_str in categories:
            category = Category.from_string(category_str)
            if category and category.activation:
                active_categories.append(category)
                print(f"{category.category_id}: {category.name}")
        if not active_categories:
            print("No active categories found. Please create a category first.")
            input("Press Enter to continue...")
            return False
        category_id = input("Select Category ID: ").upper()
        if not category_id:
            print("Category ID cannot be empty. Please try again.")
            continue
        valid_category = False
        for category in active_categories:
            if str(category.category_id).strip() == str(category_id).strip():
                valid_category = True
                break
        if not valid_category:
            print("Invalid Category ID. Please try again.")
            continue
        break

    while True:
        price = input("Product Price: ")
        if not price:
            print("Product Price cannot be empty. Please try again.")
            continue
        if not price.replace('.', '', 1).isdigit():
            print("Invalid price format. Please enter a valid number.")
            continue
        break

    while True:
        stock = input("Product Stock: ")
        if not stock:
            print("Product Stock cannot be empty. Please try again.")
            continue
        if not stock.isdigit():
            print("Invalid stock format. Please enter a valid number.")
            continue
        break

    while True:
        activation = input("Activate product? (y/n): ").lower()
        if activation == "y":
            activation = True
            break
        elif activation == "n":
            activation = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue

    new_product = Product(new_id, name, category_id, price, stock, activation)
    append_file(PRODUCTS_FILE, new_product)

    print(f"Product '{name}' added successfully!")
    input("\nPress Enter to continue...")
    return True

def edit_product():
    view_products()
    while True:
        product_id = input("\nEnter the product ID to edit (Enter 0 to cancel): ").upper()

        if product_id == "0":
            print("Operation cancelled.")
            input("Press Enter to continue...")
            return False
        
        if not product_id:
            print("Product ID cannot be empty. Please try again.")
            continue
        break

    products = read_file(PRODUCTS_FILE)

    found = False
    for product_str in products:
        product = Product.from_string(product_str)
        if product and product.product_id == product_id:
            found = True
            break
    if not found:
        print("Product not found.")
        input("Press Enter to continue...")
        return False

    while True:
        name = input(f"New Product Name (Press enter to keep old product name)(current: {product.name}): ")
        if not name:
            name = product.name
            break
        is_exists = name_exists("Product", name)
                    
        if is_exists:
            print("Product name already exists. Please try again.\n")
            continue
        break
    
    while True:
        categories = read_file(CATEGORIES_FILE)
        active_categories = []
        for category_str in categories:
            category = Category.from_string(category_str)
            if category and category.activation:
                active_categories.append(category)
                print(f"{category.category_id}: {category.name}")
        if not active_categories:
            print("No active categories found. Please create a category first.")
            input("Press Enter to continue...")
            return False
        category_id = input(f"Select Category ID (Press enter to keep old category)(current: {product.category}): ").upper()
        if not category_id:
            category_id = product.category
            break
        valid_category = False
        for category in active_categories:
            if category.category_id == category_id:
                valid_category = True
                break
        if not valid_category:
            print("Invalid Category ID. Please try again.")
            continue
        break

    while True:
        price = input(f"New Product Price (Press enter to keep old price)(current: {product.price}): ")
        if not price:
            price = product.price
            break
        if not price.replace('.', '', 1).isdigit():
            print("Invalid price format. Please enter a valid number.")
            continue
        break

    while True:
        stock = input(f"New Product Stock (Press enter to keep old stock)(current: {product.stock}): ")
        if not stock:
            stock = product.stock
            break
        if not stock.isdigit():
            print("Invalid stock format. Please enter a valid number.")
            continue
        break


    updated_product = Product(product.product_id, name, category_id, price, stock, product.activation)
    updated_products = []
    for p in products:
        if p == product_str:
            updated_products.append(updated_product)
        else:
            updated_products.append(p)

    write_file(PRODUCTS_FILE, updated_products)

    print(f"Product '{name}' updated successfully!")
    input("\nPress Enter to continue...")
    return True

def activate_deactivate_product():

    view_products()
    while True:
        product_id = input("\nEnter the product ID to activate/deactivate (Enter 0 to cancel): ").upper()

        if product_id == "0":
            print("Operation cancelled.")
            input("Press Enter to continue...")
            return False
        
        if not product_id:
            print("Product ID cannot be empty. Please try again.")
            continue
        break

    products = read_file(PRODUCTS_FILE)

    found = False
    for product_str in products:
        product = Product.from_string(product_str)
        if product and product.product_id == product_id:
            found = True
            break
    if not found:
        print("Product not found.")
        input("Press Enter to continue...")
        return False

    while True:
        print(f"Current Status: {'Active' if product.activation else 'Inactive'}")
        activation = input("Activate/Deactivate product? (y/n): ").lower()
        if activation == "y":
            product.activation = not product.activation
            break
        elif activation == "n":
            print("No changes made.")
            input("Press Enter to continue...")
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue

    updated_product = Product(product.product_id, product.name, product.category, product.price, product.stock, product.activation)
    updated_products = []
    for p in products:
        if p == product_str:
            updated_products.append(updated_product)
        else:
            updated_products.append(p)

    write_file(PRODUCTS_FILE, updated_products)

    print(f"Product '{product.name}' status updated successfully!")
    input("\nPress Enter to continue...")
    return True

def main():
    while True:
        clearScreen()
        print(create_box("Inventory Management System"))

        print("\n1. Manage Categories")
        print("2. Manage Products")
        print("0. Exit")

        choice = input("\nPlease select an option: ")

        if choice == "1":
            manage_catageries()
        elif choice == "2":
            manage_products()
        elif choice == "0":
            clearScreen()
            print("Exiting the system...")
            time.sleep(1)
            exit()
        else:
            print("Invalid choice. Please try again.")
            input("Press enter to continue...")

if __name__ == "__main__":
    main()