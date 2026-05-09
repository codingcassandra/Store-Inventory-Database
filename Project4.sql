use project4;

# new user
DELIMITER $$
CREATE PROCEDURE registerNewUser(
    IN p_username VARCHAR(255),
    IN p_pass VARCHAR(255)
)
BEGIN

    IF EXISTS (SELECT 1 FROM users WHERE username = p_username) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username already exists';
    ELSE
        INSERT INTO users (username, pass, userRole)
        VALUES (p_username, p_pass, 2);
    END IF;
END $$
DELIMITER ;

# validates credentials
DELIMITER $$
CREATE PROCEDURE loginWithCreds(
    IN p_username VARCHAR(255),
    IN p_pass VARCHAR(255)
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM users
        WHERE username = p_username AND pass = p_pass
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid username or password';
    ELSE
        SELECT id, username, userRole
        FROM users
        WHERE username = p_username AND pass = p_pass;
    END IF;
END $$
DELIMITER ;

# adds a new product  
DELIMITER $$
CREATE PROCEDURE submitNewProduct(
    IN p_name VARCHAR(255),
    IN p_price DECIMAL(10,2)
)
BEGIN
    IF p_price <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Price must be greater than 0';
    ELSE
        INSERT INTO product (prodName, price)
        VALUES (p_name, p_price);
    END IF;
END $$
DELIMITER ;

# edits an already existing product
DELIMITER $$
CREATE PROCEDURE editExistingProduct(
    IN p_id INT,
    IN p_name VARCHAR(255),
    IN p_price DECIMAL(10,2)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM product WHERE id = p_id) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Product ID does not exist';
    ELSEIF p_price <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Price must be greater than 0';
    ELSE
        UPDATE product
        SET prodName = p_name,
            price = p_price
        WHERE id = p_id;
    END IF;
END $$
DELIMITER ;


# adds up the total sales 
DELIMITER $$
CREATE PROCEDURE getSalesTotal()
BEGIN
    SELECT IFNULL(SUM(total), 0) AS totalSales
    FROM sale;
END $$
DELIMITER ;

# gets all the products 
DELIMITER $$
CREATE PROCEDURE getAllProducts()
BEGIN
    SELECT id, prodName, price
    FROM product;
END $$
DELIMITER ;


# processes new orders
DELIMITER $$
CREATE PROCEDURE submitOrder(
    IN p_prodID INT,
    IN p_userID INT,
    IN p_qty INT
)
BEGIN
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_total DECIMAL(10,2);


    IF NOT EXISTS (SELECT 1 FROM product WHERE id = p_prodID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid product ID';


    ELSEIF NOT EXISTS (SELECT 1 FROM users WHERE id = p_userID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid user ID';

   
    ELSEIF p_qty <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantity must be greater than 0';

    ELSE

        SELECT price INTO v_price
        FROM product
        WHERE id = p_prodID;

        SET v_total = v_price * p_qty;

        INSERT INTO sale (prodID, userID, qty, total)
        VALUES (p_prodID, p_userID, p_qty, v_total);

    
        SELECT v_total AS totalPrice;
    END IF;
END $$
DELIMITER ;


# gets order history
DELIMITER $$
CREATE PROCEDURE viewCustomerOrders(
    IN p_userID INT
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = p_userID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid user ID';
    ELSE
        SELECT s.saleID, p.prodName, s.qty, s.total
        FROM sale s
        JOIN product p ON s.prodID = p.id
        WHERE s.userID = p_userID;
    END IF;
END $$
DELIMITER ;


# cancels an existing order
DELIMITER $$
CREATE PROCEDURE cancelOrder(
    IN p_saleID INT,
    IN p_userID INT
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM sale
        WHERE saleID = p_saleID AND userID = p_userID
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Order not found or not owned by user';
    ELSE
        DELETE FROM sale
        WHERE saleID = p_saleID AND userID = p_userID;
    END IF;
END $$
DELIMITER ;
