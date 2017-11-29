#!/usr/bin/env python3
#coding=utf-8
__author__ = "Feather Zhang"
import asyncio
import uvloop
import aiohttp
from pprint import pprint
import json
# Using libuv for eventloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())



async def autocomCode(postid: str) -> str:
	url = 'https://www.kuaidi100.com/autonumber/autoComNum'
	# Set header for POST request.
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
	# The Parameters for request.
	data = (('resultv2','1'),('text', postid))


	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.post(url=url,params=data) as resp:
			# A dirty hack for JSON serialize. Bypass 'Type mismatch'
			jResp =  json.loads(await resp.text())
			return jResp['auto'][0]['comCode']
 

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
	# Set parameters
	params = (
    ('type', ptype),
    ('postid', postid),
	)


	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url=url,params=params) as resp:
			# Another dirty hack as usual.
			jResp = json.loads(await resp.text())
			return jResp['data']


async def main(postids: list):
	# I don't have a container that supports __aiter__, so I have to use 'for', not 'async for'
	for postid in postids:
		print('Get postid: '+postid)
		# Avoids type keyword
		ptype = await autocomCode(postid)
		queryResult = await query(ptype,postid)
		pprint(queryResult)
		print('\n'*2) # For better format


if __name__ == '__main__':
	# I may use something other than user input, just settle on this for now.
	postid = input('Please enter the postal service number (sperate with comma): ')
	# Batch input process
	postids = postid.split(',')
	loop = asyncio.get_event_loop() # Get eventloop
	loop.run_until_complete(main(postids))

