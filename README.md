# 📦 Inventory Management System (Stationery Store)

![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

A simple console-based inventory management system that supports product and category management.

## 🌟 Features

### 📂 Category Management
- **View All Categories**: Display all categories with their ID, name, and status
- **Add New Category**: Create a new category with an auto-generated ID
- **Edit Category**: Update an existing category name
- **Activate/Deactivate Category**: Toggle category status (cannot deactivate if products are linked)

### 📦 Product Management
- **View All Products**: Display all products with sorting options (by name, price, or stock)
- **Add New Product**: Add a new product with auto-generated ID, name, category, price, and stock
- **Edit Product**: Update an existing product's name, category, price, or stock quantity
- **Activate/Deactivate Product**: Toggle product status

## 🔑 Key Considerations

### Data Structure
A single product is represented using a `Product` class with attributes: `product_id`, `name`, `category`, `price`, `stock`, and `activation`. A `Category` class is similarly used for categories. Multiple products are stored as a list of `Product` objects loaded from a text file at runtime.

### Data Storage
Inventory data is saved in plain text files (`products.txt`, `categories.txt`). Each record is stored as a pipe-delimited (`|`) string, one record per line. This ensures data is not lost when the application closes, and the format is simple to read and write without any external libraries.

### User Interaction
The user interacts with the application through a command-line interface (CLI). A numbered menu is displayed at each screen, and the user enters a number to select an option. Input validation is applied at every step to guide the user toward correct entries.

### Error Handling
- **Product/Category not found**: If the user enters a Product ID or Category ID that does not exist, the system displays a "not found" message and returns to the menu without crashing.
- **Invalid input**: If the user enters a non-numeric value for price or stock, the system displays an error message and prompts the user to re-enter the value.
- **Empty input**: All required fields (name, ID, price, stock) are validated to ensure they are not left blank.
- **Linked category**: A category cannot be deactivated if products are still linked to it, preventing broken references.

### Technology Choice
Python was chosen because it is straightforward to implement a CLI application with minimal setup. Python's built-in `os` and `time` modules provide everything needed for file I/O and timestamps without requiring any third-party packages. It is also easy to read and maintain, which suits the scope of this project.

## 🚀 Getting Started

### Prerequisites
- Python 3.6+ installed on your system

### Installation (Windows)
1. Download or clone the source files
2. Place `Inventory_Management_System.py` in your desired directory
3. Click `run.bat` or type below command to run the application:
   ```
   python Inventory_Management_System.py
   ```
### Installation (macOS)
1. Download or clone the source files
2. Place `Inventory_Management_System.py` in your desired directory
3. Open Terminal and run the following command
   ```
   python3 Inventory_Management_System.py
   ```

## 💻 How to Use

### Main Menu
```
============================================================
               Inventory Management System
============================================================
1. Manage Categories
2. Manage Products
0. Exit
```

### Manage Categories
1. View all categories
2. Add a new category (ID is auto-generated)
3. Edit an existing category name
4. Activate or deactivate a category

### Manage Products
1. View all products (with sorting options)
2. Add a new product (must select from existing active categories)
3. Edit an existing product (name, category, price, stock)
4. Activate or deactivate a product

## 📁 File Structure
- `Inventory_Management_System.py` - Main application file
- `products.txt` - Product inventory data (auto-created on first product added)
- `categories.txt` - Product category data (auto-created on first category added)

## 📝 Notes
- Product IDs and Category IDs are auto-generated sequentially.
- A product must belong to an active category. If no active categories exist, a product cannot be added.