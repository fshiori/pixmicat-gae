# -*= coding: utf-8 -*-

#/*---- Part 1：程式基本設定 ----*/
# 伺服器常態設定
TIME_ZONE = 'Asia/Taipei' # 時區設定
PIXMICAT_LANGUAGE = 'zh-tw' # 語系語定

# FileIO設定
FILEIO_BACKEND = '' # Add 'GAE_BlobProperty', 'GAE_BlobStore' or 'ImageShack'.
IMAGESHACK_API_KEY = '' # Only ImageShack need.

#/*---- Part 2：板面各項細部功能設定 ----*/
TITLE = 'Pixmicat!-GAE' # 網頁標題
ADMIN_PASS = 'futaba' # 管理員密碼

# 附加圖檔限制
MAX_KB = 1024 # 附加圖檔上傳容量限制KB (GAE內定為最高1MB)

# 預覽圖片相關限制
MAX_W = 250 # 討論串本文預覽圖片寬度 (超過則自動縮小)
MAX_H = 250 # 討論串本文預覽圖片高度
MAX_RW = 125 # 討論串回應預覽圖片寬度 (超過則自動縮小)
MAX_RH = 125 # 討論串回應預覽圖片高度

#外觀設定
PAGE_DEF = 15 #一頁顯示幾篇討論串
RE_DEF = 10 #一篇討論串最多顯示之回應筆數 (超過則自動隱藏，全部隱藏：0)
RE_PAGE_DEF = 30 #回應模式一頁顯示幾筆回應內容 (分頁用，全部顯示：0)


