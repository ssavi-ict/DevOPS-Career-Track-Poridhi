"use strict";

// configs
export const PORT = 5029;

// db configs
const sqlHost = "localhost";
const sqlUser = "root";
const sqlPassword = "password";
const sqlDatabase = "mydb";
export const sqlTable = "mytable";

// configs
export const dbConfigs = {
  host: sqlHost,
  user: sqlUser,
  password: sqlPassword,
  database: sqlDatabase,
};

// redis configs
const redisUsername = process.env.REDIS_USERNAME || "";
const redisPassword = process.env.REDIS_PASSWORD || "password";
const redisHost = process.env.REDIS_HOST || "localhost";
const redisPort = process.env.REDIS_PORT || "6379";

const redisUrl = `redis://${redisUsername}:${redisPassword}@${redisHost}:${redisPort}`;
export const redisConfigs = {url: redisUrl};