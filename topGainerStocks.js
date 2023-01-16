const request = require('request');
const cheerio = require('cheerio');
const fs = require("fs")
let buffer = fs.readFileSync("./stockData.json")
let data = JSON.parse(buffer);

function getTopGainerStockList(url) {
    request(url, callback);
    function callback(err, response, html) {
        if (err) {
            console.log(err);
        }
        else {
            getTopGainerStocks(html);
        }
    }

    function getTopGainerStocks(html){
        let $ = cheerio.load(html)
        let stockName
        let stockListTableTr = $(".bsr_table.hist_tbl_hm").find("table tbody tr")
        let stockLast5DayData=[]
        let temp = []

        data=[]
        fs.writeFileSync("data.json",JSON.stringify(data)) //clearing previos day data

        for(let i=0;i<stockListTableTr.length;i++){
           if(i%7==0){
            stockName = $(stockListTableTr[i]).find("td:first span h3").text()
            stockPrice = $(stockListTableTr[i]).find("td:nth-child(4)").text()
            stockGain = $(stockListTableTr[i]).find("td:nth-child(7)").text()
            stockLast5Day = $(stockListTableTr[i]).find("td.performance div")
            temp=[]
            for(let i=0;i<stockLast5Day.length;i++){
                if(i%2==0){
                    stockLast5DayData.push($(stockLast5Day[i]).find("div p:nth-child(2) strong").text())
                }
            }

           

            data.push(
                {
                    "StockName": `${stockName}`,
                    "StockPrice": `${stockPrice}`,
                    "% Gain" : `${stockGain}`,
                    "Price-5daysAgo": `${stockLast5DayData[0]}`,
                    "Price-4daysAgo":`${stockLast5DayData[1]}`,
                    "Price-3daysAgo":`${stockLast5DayData[2]}`,
                    "Price-2daysAgo":`${stockLast5DayData[3]}`,
                    "Price-1daysAgo":`${stockLast5DayData[4]}`,
                }
            )

            let stringdata = JSON.stringify(data)
            fs.writeFileSync("stockData.json",stringdata)

           }
        }

        
    }
}

module.exports = getTopGainerStockList
