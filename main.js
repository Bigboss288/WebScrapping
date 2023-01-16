const request = require('request');
const cheerio = require('cheerio');
const getTopGainerStockList = require('./topGainerStocks');
const moneycontrol_url = "https://www.moneycontrol.com/"
const tickertape_url = "https://www.tickertape.in/market-mood-index"
const fs = require("fs")
let buffer = fs.readFileSync('./marketMood.json');
let data = JSON.parse(buffer)
data=[]
fs.writeFileSync('marketMood.json',JSON.stringify(data));

request(moneycontrol_url, callback);           //request to money control
function callback(err, response, html) {
    if (err) {
        console.log(err);
    }
    else {
        getTopGainerStockslink(html);
    }
}

request(tickertape_url, (err, response, html) => {

    if (err) {
        console.log(err);
    }
    else {
        getMarketMood(html);
    }

});            //request to tickertape


function getTopGainerStockslink(html) {
    let $ = cheerio.load(html);
    let stocklist = $(".stkhead2")
    let stocklistlink = $(stocklist[1]).find("a").attr("href")
    getTopGainerStockList(stocklistlink)


    //advance decline gives us the overall mood of broader market 
    let advance_decline_ratio = $(".bartxt").find("span")
    advance = $(advance_decline_ratio[0]).text()
    decline = $(advance_decline_ratio[1]).text()

    data.push(
        {
            "advance" : `${advance}`,
            "decline" : `${decline}`,
        }
    )

    let stringdata = JSON.stringify(data)
fs.writeFileSync("marketMood.json",stringdata)
}

function getMarketMood(html){
    let $ = cheerio.load(html)

    let marketMoodIndex = $(".jsx-3769769187.value.typography-body-regular-xs.text-teritiary.pt8.lh-100");
    let marketMoodText = $(".jsx-3769769187.text-primary.desktop--only.text-18.font-medium");
    let marketMood = $(marketMoodText[1]).text()
    let marketMoodprev = $(marketMoodIndex[0]).text();
    let marketMoodcurr = $(marketMoodIndex[1]).text();

    

    data.push(
        {
            "PreviosMarketMoodIndex" : `${marketMoodprev}`,
            "CurrentMarketMoodIndex" : `${marketMoodcurr}`,
            "currentMarketStatus" : `${marketMood}`
        }
    )

    let stringdata = JSON.stringify(data)
fs.writeFileSync("marketMood.json",stringdata)
}



console.log("Http Request")