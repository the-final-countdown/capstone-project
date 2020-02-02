CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    telephone TEXT,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    display_name TEXT,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    shares INTEGER NOT NULL,
    purchased_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    purchase_price FLOAT NOT NULL,
    sold_on DATETIME,
    sell_price FLOAT,
    finalized BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios (id),
    FOREIGN KEY (stock_id) REFERENCES stocks (id)
);

CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    company_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER NOT NULL,
    dt DATETIME NOT NULL,
    price_high FLOAT NOT NULL,
    price_low FLOAT NOT NULL,
    price_open FLOAT NOT NULL,
    price_close FLOAT NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stocks (id)
);