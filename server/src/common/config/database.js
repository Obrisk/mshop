const mysql = require('think-model-mysql');
require('dotenv').config({ path: './dev.env' })

module.exports = {
    handle: mysql,
    database: process.env.DB_NAME,
    prefix: process.env.DB_PREFIX,
    encoding: 'utf8mb4',
    host: '127.0.0.1',
    port: '3306',
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    dateStrings: true
};
