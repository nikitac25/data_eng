const DB_NAME = process.env.MONGO_INITDB_DATABASE;

db = db.getSiblingDB(DB_NAME);

db.createCollection("sessions");
