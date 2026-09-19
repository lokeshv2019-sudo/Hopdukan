CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name_hi VARCHAR(100),
    name_en VARCHAR(100),
    parent_id INT
);

CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    logo_url VARCHAR(255)
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name_hi VARCHAR(255),
    name_en VARCHAR(255),
    brand_id INT,
    category_id INT,
    weight VARCHAR(50),
    unit VARCHAR(20),
    barcode VARCHAR(50),
    photo_url VARCHAR(255)
);

CREATE TABLE sellers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(50),
    city VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE rates (
    id SERIAL PRIMARY KEY,
    item_id INT,
    seller_id INT,
    wholesale_price DECIMAL(10,2),
    retail_price DECIMAL(10,2),
    source VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
