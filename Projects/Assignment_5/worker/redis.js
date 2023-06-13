"use strict";
import { redisConfigs } from "./configs.js";
import { createClient } from "redis";

export const redisClient = createClient(redisConfigs);

export const deleteNewsFromCache = async () =>{
    await redisClient.connect();
    await redisClient.del("news");
    redisClient.disconnect()
};