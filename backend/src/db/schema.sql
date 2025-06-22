DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS points_of_sale;
DROP TABLE IF EXISTS driver_status;
DROP TABLE IF EXISTS driver;
DROP TABLE IF EXISTS vehicle_type;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS load_type;
DROP TABLE IF EXISTS status_type_for_orders;
DROP TABLE IF EXISTS orders;

CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO role(name) VALUES ('admin'), ('manager'), ('operator'), ('driver');

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    telephone TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role (id)
);

CREATE TABLE points_of_sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnpj TEXT UNIQUE NOT NULL,
    telephone TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE driver_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO driver_status(name) VALUES ('active'), ('inactive'), ('traveling'), ('under maintenance');

CREATE TABLE driver (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cnh TEXT UNIQUE NOT NULL,
    driver_status_id INTEGER DEFAULT 2,
    FOREIGN KEY (driver_status_id) REFERENCES driver_status (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE vehicle_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO vehicle_type(name) VALUES ('van'), ('light truck'), ('medium truck'), ('heavy truck');

CREATE TABLE vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate TEXT UNIQUE NOT NULL,
    model TEXT NOT NULL,
    vehicle_type_id INTEGER NOT NULL,
    capacity TEXT NOT NULL,
    driver_id INTEGER NOT NULL,
    FOREIGN KEY (vehicle_type_id) REFERENCES vehicle_type (id),
    FOREIGN KEY (driver_id) REFERENCES driver (id)
);

CREATE TABLE load_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO load_type(name) VALUES ('medicines'), ('heat-sensitive drugs'), ('cosmetics'), ('supplements'), ('hospital products'), ('medical equipment'), ('hygiene and well-being'), ('others');

CREATE TABLE status_type_for_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO status_type_for_orders(name) VALUES ('pending'), ('in transit'), ('delivered'), ('canceled');

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    points_of_sale_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    weight_kg INTEGER NOT NULL,
    distance_km INTEGER NOT NULL,
    load_type_id INTEGER NOT NULL,
    status_id INTEGER DEFAULT 1,
    shipping_cost INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (points_of_sale_id) REFERENCES points_of_sale (id),
    FOREIGN KEY (driver_id) REFERENCES driver (id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle (id),
    FOREIGN KEY (load_type_id) REFERENCES load_type (id),
    FOREIGN KEY (status_id) REFERENCES status_type_for_orders (id)
);
