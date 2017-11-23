#!/usr/bin/env python3
#coding=utf-8

import asyncio
import uvloop
import aiohttp
from pprint import pprint
import json
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def autocomCode(postid: str) -> str:
	url = 'https://www.kuaidi100.com/autonumber/autoComNum'
	headers = {
    'Pragma': 'no-cache',
    'Origin': 'https://www.kuaidi100.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'no-cache',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://www.kuaidi100.com/',
    'Content-Length': '0',
    'DNT': '1',
	}
	data = (('resultv2','1'),('text', postid))
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.post(url=url,params=data) as resp:
			#pprint(await resp.text())
			#pprint(resp.content_type)
			jresp =  json.loads(await resp.text())
			return jresp['auto'][0]['comCode']
 
async def query(ptype: str, postid: str) -> str:
	url = 'https://www.kuaidi100.com/query'
	headers = {
    'Pragma': 'no-cache',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'no-cache',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://www.kuaidi100.com/',
	}
	params = (
    ('type', ptype),
    ('postid', postid),
	)
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url=url,params=params) as resp:
			#pprint(await resp.text())
			jresp = json.loads(await resp.text())
			return jresp['data']

async def main(postids: list):
	for postid in postids:
		pprint(postid)
		ptype = await autocomCode(postid)
		queryResult = await query(ptype,postid)
		pprint(queryResult)

if __name__ == '__main__':
	postid = input('Please enter the postal service number (sperate with comma): ')
	#pprint(postid)
	postids = postid.split(',')
	loop = asyncio.get_event_loop() # Get eventloop
	loop.run_until_complete(main(postids))

