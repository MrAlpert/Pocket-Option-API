import time, logging, math, asyncio, json
from datetime import datetime
import talib.abstract as ta
import numpy as np
import pandas as pd
from finta import TA
import freqtrade.vendor.qtpylib.indicators as qtpylib
from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync

start = time.perf_counter()

min_payout = 85

api = PocketOptionAsync(demo)

async def get_payout(dat):
    data = dat
    full_payout = await api.payout()
    for pair in full_payout:
        if full_payout[pair] > min_payout:
            p = {}
            p['name'] = pair
            p['payout'] = full_payout[pair]
            data.append(p)
    return data

async def get_df(dat):
    data = dat
    tasks = {}
    async with asyncio.TaskGroup() as tg:
        for pair in data:
            task = tg.create_task(api.history(pair['name'], 60))
            tasks[pair['name']] = task
        await asyncio.sleep(5)
        for pair in tasks:
            try:
                res = await asyncio.shield(tasks[pair])
            except asyncio.CancelledError:
                res = None
            print(res)
            #df = await api.get_candles(pair['name'], 60, 9000)
            #print(df)
            #df2 = await api.history(pair['name'], 60)
            #print(df2)
            # ts = datetime.timestamp(df.loc[len(df)-1]['time'])
            # for i in range(1, len(df2)):
            #     ts2 = datetime.timestamp(df2.loc[len(df2)-i]['time'])
            #     if ts2 > ts:
            #         data = {'time': df2.loc[len(df2)-i]['time'], 'open': df2.loc[len(df2)-i]['open'], 'close': df2.loc[len(df2)-i]['close'], 'high': df2.loc[len(df2)-i]['high'], 'low': df2.loc[len(df2)-i]['low']}
            #         df = df._append(data, ignore_index = True)
            #pair['dataframe'] = df2
    return data


# Main part of the code
async def main(data):
    # The api automatically detects if the 'ssid' is for real or demo account
    dat = await get_payout(data)
    dat = await get_df(dat)

     # Returns a dictionary asset: payout
    print(dat)
    #candles = await api.get_candles("EURUSD_otc", 60, 9000)
    #print(candles)
    #candles = await api.history("EURUSD_otc", 60)
    #print(candles)

    # Candles are returned in the format of a list of dictionaries
    #candles = await api.history("EURUSD_otc", 15)
    #print(candles)

if __name__ == '__main__':
    data = []
    asyncio.run(main(data))

