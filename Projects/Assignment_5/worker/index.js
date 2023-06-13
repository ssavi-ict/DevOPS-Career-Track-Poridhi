"use strict";
import { addNewsToDB } from "./db.js";
import { redisChannel } from "./configs.js";
import { getNewsAnalysis } from "./helper.js";
import { deleteNewsFromCache, redisClient } from "./redis.js";

const exprensiveWorker = async (newsText) =>{
    try{
        const newsTextAnalysis = getNewsAnalysis(newsText);
        await addNewsToDB(newsTextAnalysis);
        await deleteNewsFromCache();
    }catch{
        console.log({error});
    }
};

const main = async() => {
    const subscriber = redisClient.duplicate();
    subscriber.connect();

    subscriber.on("error", (err) => {
        console.log("Error Connecting Redis", err);
    });

    subscriber.on("connect", () => {
        console.log('Connected to Redis');
    });

    subscriber.on('ready', () =>{
        console.log('Subscriber is Ready');
        subscriber.subscribe(redisChannel, async(message) => {
            console.log(`Worker Server: ${message}`);
            await exprensiveWorker(message);
        });
    });
};

main();