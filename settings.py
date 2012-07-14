# -*- coding: utf-8 -*-
#<piximcat-gae A Pixmicat! Google App Engine Clone>
#Copyright (C) 2011-2012  Eric Chen<fshiori@gmail.com>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from google.appengine.api import images

config = {}
#/*---- Part 1：程式基本設定 ----*/
# 伺服器常態設定
DEBUG = False #除錯模式
config['TIME_ZONE'] = 'Asia/Taipei' # 時區設定 需遵照pytz時區設定標準
config['PIXMICAT_LANGUAGE'] = 'zh_TW' # 語系語定(尚未實作)
config['HTTP_UPLOAD_DIFF'] = 50 # HTTP上傳所有位元組與實際位元組之允許誤差值

# 圖片FileIO設定
config['FILEIO_BACKEND'] = '' # 圖片FileIO後端指定 'GAE_BlobProperty', 'GAE_BlobStore' or 'ImageShack'(尚未實作)
config['IMAGESHACK_API_KEY'] = '' # Only ImageShack need.(尚未實作)
config['CACHE_PIC'] = 1 # 快取圖片 (啟動：1 關閉：0 , 僅在FILEIO_BACKEND為GAE_BlobProperty有效)

#/*---- Part 2：板面各項細部功能設定 ----*/
TITLE = 'Pixmicat!-GAE' # 網頁標題
config['HOME'] = '/' # 回首頁的連結
config['TOP_LINKS'] = '' # 頁面右上方的額外連結，請直接以[<a href="網址" rel="_blank">名稱</a>]格式鍵入，如果不需要開新視窗可刪除rel一段
config['ADMIN_PASS'] = 'futaba' # 管理員密碼
config['IDSEED'] = 'id種' # 生成ID之隨機種子

# 管理員キャップ(Cap)設定 (啟用條件：開啟使用；名稱輸入識別名稱，E-mail輸入#啟動密碼)
config['CAP_ENABLE'] = 1 # 是否使用管理員キャップ (使用：1 不使用：0)
config['CAP_NAME'] = 'futaba' # 管理員キャップ識別名稱
config['CAP_PASS'] = 'futaba' # 管理員キャップ啟動密碼 (在E-mail一欄輸入#啟動密碼)
config['CAP_SUFFIX'] = ' ★' # 管理員キャップ後綴字元 (請務必有★以便程式防止偽造，或可自行修改程式的防偽造部份)
config['CAP_ISHTML'] = 1 # 管理員キャップ啟動後內文是否接受HTML標籤 (是：1 否：0)

# 功能切換
config['USE_FLOATFORM'] = 1 # 新增文章表單使用自動隱藏 (是：1 否：0)
config['USE_SEARCH'] = 1 # 開放搜尋功能 (是：1 否：0)
config['USE_UPSERIES'] = 1 # 是否啟用連貼機能 [開主題後自動指向到主題下以方便連貼] (是：1 否：0)
config['RESIMG'] = 1 # 回應附加圖檔機能 (開啟：1 關閉：0)
config['AUTO_LINK'] = 1 # 討論串文字內的URL是否自動作成超連結 (是：1 否：0)
config['KILL_INCOMPLETE_UPLOAD'] = 1 # 自動刪除上傳不完整附加圖檔 (是：1 否：0)
config['ALLOW_NONAME'] = 1 # 是否接受匿名發送 (強制砍名：2 是：1 否：0)
config['DISP_ID'] = 2 # 顯示ID (強制顯示：2 選擇性顯示：1 永遠不顯示：0)
config['CLEAR_SAGE'] = 0 # 使用不推文模式時清除E-mail中的「sage」關鍵字 (是：1 否：0)
config['USE_QUOTESYSTEM'] = 1 # 是否打開引用瀏覽系統 [自動轉換>>No.xxx文字成連結並導引] (是：1 否：0)
config['SHOW_IMGWH'] = 1 # 是否顯示附加圖檔之原檔長寬尺寸 (是：1 否：0)
config['USE_CATEGORY'] = 1 # 是否開啟使用類別標籤分類功能 (是：1 否：0)
config['USE_RE_CACHE'] = 1 # 是否使用回應頁面顯示快取功能 (是：1 否：0)
config['USE_XHTML'] = 1 # 是否回傳 XHTML 檔頭讓瀏覽器以更嚴格的方式解析 [僅限瀏覽器支援者] (是：1 否：0)

# 封鎖設定
config['BAN_CHECK'] = 0 # 綜合性封鎖檢查功能 (關閉：0, 開啟：1)
config['BANPATTERN'] = [] # IP/Hostname封鎖黑名單
config['DNSBLSERVERS'] = ['sbl-xbl.spamhaus.org', 'list.dsbl.org', 'bl.blbl.org', 'bl.spamcop.net'] # DNSBL伺服器列表 
config['DNSBLWHLIST'] = [] # DNSBL白名單 (請輸入IP位置)
config['BAD_STRING'] = ['dummy_string', 'dummy_string2'] # 限制出現之文字
config['BAD_FILEMD5'] = ['dummy', 'dummy2'] # 限制上傳附加圖檔之MD5檢查碼

# 附加圖檔限制
config['MAX_KB'] = 1024 # 附加圖檔上傳容量限制KB (GAE內定為最高1MB)
config['STORAGE_LIMIT'] = 1 # 附加圖檔總容量限制功能 (啟動：1 關閉：0)
config['STORAGE_MAX'] = 30000 # 附加圖檔總容量限制上限大小 (單位：KB)
config['ALLOW_UPLOAD_EXT'] = 'GIF|JPG|PNG|BMP|SWF' # 接受之附加圖檔副檔名 (送出前表單檢查用，用 | 分隔)

# 連續投稿時間限制
config['RENZOKU'] = 60 # 連續投稿間隔秒數
config['RENZOKU2'] = 60 # 連續貼圖間隔秒數

# 預覽圖片相關限制
config['USE_THUMB'] = 1 # 使用預覽圖機能 (使用：1 不使用：0)
config['MAX_W'] = 250 # 討論串本文預覽圖片寬度 (超過則自動縮小)
config['MAX_H'] = 250 # 討論串本文預覽圖片高度
config['MAX_RW'] = 125 # 討論串回應預覽圖片寬度 (超過則自動縮小)
config['MAX_RH'] = 125 # 討論串回應預覽圖片高度
config['STORAGE_RESIZE_PIC'] = 1 # 儲存預覽圖片 (啟動：1 關閉：0)
config['CACHE_RESIZE_PIC'] = 1 # 快取預覽圖片 (啟動：1 關閉：0)
#預覽圖生成設定
config['THUMB_SETTING'] = {
                           'Format' : images.JPEG, # 預覽圖格式
                           'Quality' : 75, #預覽圖品質
                           }

#外觀設定
config['ADDITION_INFO'] = '' # 可在表單下顯示額外文字
config['LIMIT_SENSOR'] = {'ByPostCountCondition' : 500} # 文章自動刪除機制設定
config['PAGE_DEF'] = 15 # 一頁顯示幾篇討論串
config['ADMIN_PAGE_DEF'] = 20 # 管理模式下，一頁顯示幾筆資料
config['RE_DEF'] = 10 # 一篇討論串最多顯示之回應筆數 (超過則自動隱藏，全部隱藏：0)
config['RE_PAGE_DEF'] = 30 # 回應模式一頁顯示幾筆回應內容 (分頁用，全部顯示：0)
config['MAX_RES'] = 30 # 回應筆數超過多少則不自動推文 (關閉：0)
config['MAX_AGE_TIME'] = 0 # 討論串可接受推文的時間範圍 (單位：小時，討論串存在超過此時間則回應皆不再自動推文 關閉：0)
config['COMM_MAX'] = 2000 # 內文接受Bytes數 (注意：中文字為2Bytes)
config['BR_CHECK'] = 0 # 文字換行行數上限 (不限：0)
config['STATIC_HTML_UNTIL'] = -1 # 更新文章時自動生成的靜態網頁至第幾頁止 (全部生成：-1 僅入口頁：0)
config['DEFAULT_NOTITLE'] = '無標題' # 預設文章標題
config['DEFAULT_NONAME'] = '無名氏' # 預設文章名稱
config['DEFAULT_NOCOMMENT'] = '無內文' # 預設文章內文

#/*---- Part 3：Anti-SPAM 防止垃圾訊息機器人發文 ----*/
config['reCAPTCHA'] = 1 # 使用reCAPTCHA防止機器人