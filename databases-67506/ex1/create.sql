CREATE TABLE plane(
  id INTEGER PRIMARY KEY,
  model VARCHAR(50) NOT NULL,
  creationYear INTEGER NOT NULL
);
CREATE TABLE pilot(
  id INTEGER PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);
CREATE TABLE flight(
  id INTEGER PRIMARY KEY,
  flightDate TIMESTAMP NOT NULL,
  planeId INTEGER NOT NULL,
  FOREIGN KEY (planeId) REFERENCES plane (id) ON DELETE CASCADE
);
CREATE TABLE pilots(
  pilotId INTEGER NOT NULL,
  flightId INTEGER NOT NULL,
  FOREIGN KEY (pilotId) REFERENCES pilot (id) ON DELETE CASCADE,
  FOREIGN KEY (flightId) REFERENCES flight (id) ON DELETE CASCADE
);
CREATE TABLE ticket(
  lineNumber INTEGER NOT NULL CHECK (1 <= lineNumber and lineNumber <= 20),
  letter CHAR(1) NOT NULL CHECK ('A' <= letter and letter <= 'J'),
  cost INTEGER NOT NULL CHECK(cost > 0),
  flightID INTEGER NOT NULL,
  PRIMARY KEY (lineNumber, letter, flightID),
  FOREIGN KEY (flightID) REFERENCES flight (id) ON DELETE CASCADE
);
CREATE TABLE normalTicket(
  lineNumber INTEGER NOT NULL,
  letter CHAR(1) NOT NULL,
  flightID INTEGER NOT NULL,
  PRIMARY KEY (lineNumber, letter, flightID),
  FOREIGN KEY (lineNumber, letter, flightID) REFERENCES ticket (lineNumber, letter, flightID) ON DELETE CASCADE  
);
CREATE TABLE VIPTicket(
  lineNumber INTEGER NOT NULL,
  letter CHAR(1) NOT NULL,
  flightID INTEGER NOT NULL,
  PRIMARY KEY (lineNumber, letter, flightID),
  FOREIGN KEY (lineNumber, letter, flightID) REFERENCES ticket (lineNumber, letter, flightID) ON DELETE CASCADE  
);
CREATE TABLE customer(
  id INTEGER PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  birthDate DATE,
  phoneNumber INTEGER NOT NULL
);
CREATE TABLE VIPCustomer(
  id INTEGER PRIMARY KEY,
  score INTEGER NOT NULL CHECK (score > 0),
  FOREIGN KEY (id) REFERENCES customer (id) ON DELETE CASCADE  
);
CREATE TABLE normalOrders(
  customerID INTEGER NOT NULL,
  lineNumber INTEGER NOT NULL,
  letter CHAR(1) NOT NULL,
  flightID INTEGER NOT NULL,
  PRIMARY KEY (customerID, lineNumber, letter, flightID),
  FOREIGN KEY (lineNumber, letter, flightID) REFERENCES normalTicket (lineNumber, letter, flightID) ON DELETE CASCADE,
  FOREIGN KEY (customerID) REFERENCES customer (id) ON DELETE CASCADE
);
CREATE TABLE VIPOrders(
  VIPCustomerID INTEGER NOT NULL,
  lineNumber INTEGER NOT NULL,
  letter CHAR(1) NOT NULL,
  flightID INTEGER NOT NULL,
  PRIMARY KEY (VIPCustomerID, lineNumber, letter, flightID),
  FOREIGN KEY (lineNumber, letter, flightID) REFERENCES VIPTicket (lineNumber, letter, flightID) ON DELETE CASCADE,
  FOREIGN KEY (VIPCustomerID) REFERENCES VIPCustomer (id) ON DELETE CASCADE
);