# coding=utf-8
# !/usr/bin/python

"""

作者 丢丢喵 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================Diudiumiao====================

"""

from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from Crypto.Cipher import AES
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode
import concurrent.futures
import urllib.request
import urllib.parse
import datetime
import binascii
import requests
import base64
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "https://css.gztzyyp.com"   # 首页 https://kea9da.com/home/

xurl1 = "https://chees.sxgtlj.com"

xurl2 = "https://kea9da.com"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
          }

class Spider(Spider):

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "4", "type_name": "自拍视频"},
                            {"type_id": "5", "type_name": "淫妻作乐"},
                            {"type_id": "142", "type_name": "热门探花"},
                            {"type_id": "64", "type_name": "国产传媒"},
                            {"type_id": "6", "type_name": "开放青年"},
                            {"type_id": "119", "type_name": "JVID专区"},
                            {"type_id": "139", "type_name": "SWAG专区"},
                            {"type_id": "60", "type_name": "直播录像"},
                            {"type_id": "157", "type_name": "AI换脸"},
                            {"type_id": "9", "type_name": "短视频"},
                            {"type_id": "140", "type_name": "无码破解"},
                            {"type_id": "39", "type_name": "动漫卡通"},
                            {"type_id": "58", "type_name": "女性向爱纯"},
                            {"type_id": "65", "type_name": "GIGA女战士"},
                            {"type_id": "141", "type_name": "男男视频"},
                            {"type_id": "40", "type_name": "无码中字"},
                            {"type_id": "43", "type_name": "熟女人妻"},
                            {"type_id": "44", "type_name": "美艳巨乳"},
                            {"type_id": "41", "type_name": "SM系列"},
                            {"type_id": "45", "type_name": "丝袜制服"},
                            {"type_id": "118", "type_name": "蕾丝边"},
                            {"type_id": "46", "type_name": "中文有码"},
                            {"type_id": "47", "type_name": "欧美系列"}],
                 }

        return result

    def decrypt_data(self, encrypted_base64_data):
        try:
            self._validate_decryption_input(encrypted_base64_data)
            key, iv = self._prepare_decryption_params()
            decoded_base64_str = self._custom_base64_decode(encrypted_base64_data)
            ciphertext = self._decode_base64_data(decoded_base64_str)
            decrypted_bytes = self._perform_aes_decryption(ciphertext, key, iv)
            plain_text = self._unpad_and_decode(decrypted_bytes)
            return self._parse_decryption_result(plain_text)
        except Exception as e:
            return self._handle_decryption_error(e)

    def _validate_decryption_input(self, encrypted_base64_data):
        if not encrypted_base64_data:
            raise ValueError("加密数据不能为空")

    def _prepare_decryption_params(self):
        aes_key_str = "22946bc50fd63164b79df55070a85a92"
        aes_iv_str = "kaixin1234567890"
        key = aes_key_str.encode('utf-8')
        iv = aes_iv_str.encode('utf-8')
        return key, iv

    def _custom_base64_decode(self, encoded_str):
        decoded_str = encoded_str.replace('-', '+').replace('_', '/')
        while len(decoded_str) % 4 != 0:
            decoded_str += '='
        return decoded_str

    def _decode_base64_data(self, decoded_base64_str):
        return base64.b64decode(decoded_base64_str)

    def _perform_aes_decryption(self, ciphertext, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_bytes = cipher.decrypt(ciphertext)
        return decrypted_bytes

    def _unpad_and_decode(self, decrypted_bytes):
        plain_text_bytes = unpad(decrypted_bytes, AES.block_size)
        plain_text = plain_text_bytes.decode('utf-8')
        return plain_text

    def _parse_decryption_result(self, plain_text):
        try:
            json_result = json.loads(plain_text)
            return json_result
        except json.JSONDecodeError as e:
            return plain_text

    def _handle_decryption_error(self, exception):
        raise Exception(f"解密失败: {str(exception)}")

    def homeVideoContent(self):
        try:
            data = self._fetch_latest_data()
            decrypted_data = self._decrypt_video_data(data['data'])
            pic_urls = self._fetch_picture_contents(decrypted_data['latest'])
            videos = self._build_video_list(decrypted_data['latest'], pic_urls)
            return {'list': videos}
        except Exception as e:
            return self._handle_home_content_error(e)

    def _fetch_latest_data(self):
        url = f'{xurl}/public2/json/latest.json'
        detail = requests.get(url=url, headers=headerx, timeout=10)
        detail.encoding = "utf-8"
        return detail.json()

    def _decrypt_video_data(self, encrypted_data):
        return self.decrypt_data(encrypted_data)

    def _fetch_picture_contents(self, latest_videos):
        pic_urls = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_vod = {
                executor.submit(requests.get, url=vod['titlepic'], headers=headerx): vod
                for vod in latest_videos
                            }
            for future in concurrent.futures.as_completed(future_to_vod):
                vod = future_to_vod[future]
                try:
                    response = future.result()
                    response.encoding = "utf-8"
                    pic_urls[vod['id']] = response.text
                except Exception as e:
                    pic_urls[vod['id']] = ""
        return pic_urls

    def _build_video_list(self, latest_videos, pic_urls):
        videos = []
        for vod in latest_videos:
            name = vod['title']
            id = vod['id']
            pic = pic_urls.get(id, "")
            date_obj = datetime.datetime.fromtimestamp(int(vod['newstime']))
            remark = date_obj.strftime('%Y-%m-%d')
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
                    }
            videos.append(video)
        return videos

    def _handle_home_content_error(self, exception):
        return {'list': []}

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        page = self._parse_page(pg)
        data = self._fetch_category_data(cid, page)
        if not data or 'data' not in data:
            return {'list': []}
        pic_urls = self._fetch_picture_urls(data['data'])
        videos = self._process_videos(data['data'], pic_urls)
        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def _parse_page(self, pg):
        try:
            return int(pg) if pg else 1
        except (ValueError, TypeError):
            return 1

    def _fetch_category_data(self, cid, page):
        try:
            url = f'{xurl}/public2/json/category/{cid}-{str(page)}.json'
            detail = requests.get(url=url, headers=headerx, timeout=10)
            detail.encoding = "utf-8"
            data = detail.json()
            return self.decrypt_data(data['data'])
        except Exception:
            return None

    def _fetch_picture_urls(self, vod_data):
        pic_urls = {}
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_vod = {
                    executor.submit(self._fetch_picture, vod['titlepic']): vod
                    for vod in vod_data
                                }
                for future in concurrent.futures.as_completed(future_to_vod):
                    vod = future_to_vod[future]
                    try:
                        pic_content = future.result()
                        pic_urls[vod['id']] = pic_content
                    except Exception:
                        pic_urls[vod['id']] = ""
        except Exception:
            pass
        return pic_urls

    def _fetch_picture(self, url):
        try:
            response = requests.get(url=url, headers=headerx, timeout=10)
            response.encoding = "utf-8"
            return response.text
        except Exception:
            return ""

    def _process_videos(self, vod_data, pic_urls):
        videos = []
        for vod in vod_data:
            try:
                name = vod.get('title', '')
                id = vod.get('id', '')
                pic = pic_urls.get(id, "")
                remark = self._format_date(vod.get('newstime', 0))
                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)
            except Exception:
                continue
        return videos

    def _format_date(self, timestamp):
        try:
            date_obj = datetime.datetime.fromtimestamp(int(timestamp))
            return date_obj.strftime('%Y-%m-%d')
        except Exception:
            return ""

    def detailContent(self, ids):
        result = {}
        videos = []
        if not ids:
            result['list'] = videos
            return result
        did = ids[0]
        data = self._fetch_video_detail(did)
        if not data:
            result['list'] = videos
            return result
        video_info = self._extract_video_info(data, did)
        videos.append(video_info)
        result['list'] = videos
        return result

    def _fetch_video_detail(self, did):
        try:
            url = f'{xurl}/public2/json/video/{did}.json'
            detail = requests.get(url=url, headers=headerx, timeout=10)
            detail.encoding = "utf-8"
            data = detail.json()
            return self.decrypt_data(data['data'])
        except Exception:
            return None

    def _extract_video_info(self, data, did):
        content = self._get_video_content(data)
        remarks = data.get('category_name', '')
        year = self._format_year(data.get('newstime', 0))
        area = self._get_area(data)
        xianlu = "乐哥1$$$乐哥2"
        bofang = self._format_play_url(data)
        return {
            "vod_id": did,
            "vod_remarks": remarks,
            "vod_year": year,
            "vod_area": area,
            "vod_content": content,
            "vod_play_from": xianlu,
            "vod_play_url": bofang
               }

    def _get_video_content(self, data):
        try:
            next_title = data['prev_and_next']['next']['title']
            return '乐哥为您介绍剧情' + next_title
        except Exception:
            return '乐哥为您介绍剧情'

    def _format_year(self, timestamp):
        try:
            date_obj = datetime.datetime.fromtimestamp(int(timestamp))
            return date_obj.strftime('%Y-%m-%d')
        except Exception:
            return ""

    def _get_area(self, data):
        try:
            return data['breadcrumb'][0]['title']
        except Exception:
            return ""

    def _format_play_url(self, data):
        try:
            mp4_url = data.get('mp4', '')
            m3u8_url = data.get('m3u8', '')
            return f"乐哥mp4${mp4_url}$$$乐哥m3u8${xurl1}{m3u8_url}"
        except Exception:
            return ""

    def playerContent(self, flag, id, vipFlags):
        result = {}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = id
        result["header"] = headerx
        return result

    def encrypt_aes_cbc_pkcs7_urlsafe(self, plaintext_str):
        try:
            key_str = "22946bc50fd63164b79df55070a85a92"
            iv_str = "kaixin1234567890"
            plaintext_bytes = self._encode_plaintext(plaintext_str)
            key = self._encode_key(key_str)
            iv = self._encode_iv(iv_str)
            cipher = self._create_cipher(key, iv)
            padded_bytes = self._pad_plaintext(plaintext_bytes)
            ciphertext = self._encrypt_data(cipher, padded_bytes)
            urlsafe_b64 = self._encode_urlsafe_base64(ciphertext)
            return urlsafe_b64
        except Exception:
            return ""

    def _encode_plaintext(self, plaintext_str):
        try:
            return plaintext_str.encode('utf-8')
        except Exception:
            return b""

    def _encode_key(self, key_str):
        try:
            return key_str.encode('utf-8')
        except Exception:
            return b""

    def _encode_iv(self, iv_str):
        try:
            return iv_str.encode('utf-8')
        except Exception:
            return b""

    def _create_cipher(self, key, iv):
        try:
            return AES.new(key, AES.MODE_CBC, iv)
        except Exception:
            raise

    def _pad_plaintext(self, plaintext_bytes):
        try:
            return pad(plaintext_bytes, AES.block_size)
        except Exception:
            raise

    def _encrypt_data(self, cipher, padded_bytes):
        try:
            return cipher.encrypt(padded_bytes)
        except Exception:
            raise

    def _encode_urlsafe_base64(self, ciphertext):
        try:
            standard_b64 = base64.b64encode(ciphertext).decode('utf-8')
            urlsafe_b64 = standard_b64.replace('+', '-').replace('/', '_').rstrip('=')
            return urlsafe_b64
        except Exception:
            return ""

    def searchContentPage(self, key, quick, pg):
        result = {}
        videos = []
        page = self._parse_page(pg)
        encrypted_key = self.encrypt_aes_cbc_pkcs7_urlsafe(key)
        data = self._fetch_search_data(encrypted_key, page)
        if data and 'data' in data:
            videos = self._process_search_results(data['data'])
        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def _parse_page(self, pg):
        try:
            return int(pg) if pg else 1
        except (ValueError, TypeError):
            return 1

    def _fetch_search_data(self, encrypted_key, page):
        try:
            response = requests.get(url=xurl2, headers=headerx, allow_redirects=False)
            url4 = response.headers.get('Location')
            url = f'{url4}/api/v2/search?keyword={encrypted_key}&classid=0&page={str(page)}'
            detail = requests.get(url=url, headers=headerx, timeout=10)
            detail.encoding = "utf-8"
            data = detail.json()
            return self.decrypt_data(data['data'])
        except Exception:
            return None

    def _process_search_results(self, search_data):
        videos = []
        for vod in search_data:
            try:
                video = self._create_video_item(vod)
                videos.append(video)
            except Exception:
                continue
        return videos

    def _create_video_item(self, vod):
        name = vod.get('title', '')
        id = vod.get('id', '')
        pic = "https://i02piccdn.sogoucdn.com/0aa7931c95f0b15a"
        remark = self._format_date(vod.get('newstime', 0))
        return {
            "vod_id": id,
            "vod_name": name,
            "vod_pic": pic,
            "vod_remarks": remark
               }

    def _format_date(self, timestamp):
        try:
            date_obj = datetime.datetime.fromtimestamp(int(timestamp))
            return date_obj.strftime('%Y-%m-%d')
        except Exception:
            return ""

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None





