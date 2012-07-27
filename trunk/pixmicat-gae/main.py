# -*- coding: utf-8 -*-
import string
import datetime
import logging
import time
import hashlib

from google.appengine.api import images
from webapp2_extras.i18n import gettext as _

from handler import BaseHandler
from models import Pixmicat

class MainPage(BaseHandler):
    def get(self, page_num=0):
        #如果瀏覽器支援XHTML標準MIME就輸出
        #todo
        #有啟動Gzip
        #todo
        context = {}
        context['config'] = self.app.config
        q = Pixmicat.all()
        q.order('-replytime')
        PAGE_DEF = self.app.config.get('PAGE_DEF')
        threads = q.fetch(limit=PAGE_DEF, offset=page_num * PAGE_DEF)
        #預測過舊文章和將被刪除檔案
        #todo
        context['formtop'] = True
        context['max_file_size'] = self.app.config.get('MAX_KB') * 1024
        context['allow_upload_ext'] = string.replace(self.app.config.get('ALLOW_UPLOAD_EXT'), '|', ', ')
        if self.app.config.get('STORAGE_LIMIT'):
            pass #todo
        for thread in threads:
            res_start = thread.count - self.app.config.get('RE_DEF') + 1
            if res_start < 1:
                res_start = 1
            res_amount = self.app.config.get('RE_DEF')
            hidden_reply = res_start - 1
            q = Pixmicat.all()
            q.filter('mainpost =', thread)
            q.order('createtime')
            posts = q.fetch(limit=res_amount, offset=res_start-1)
            for post in posts:
                name = post.name
        self.render_response('index.html', **context)
        
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        sub = self.request.get('sub')
        com = self.request.get('com')
        pwd = self.request.get('pwd')
        category = self.request.get('category')
        upfile = self.request.get('upfile')
        if upfile:
            upfile_name = self.request.POST.get('upfile').filename
        ip = self.request.remote_addr
        #todo : "RegistBegin" Hook Point
        #todo : 封鎖：IP/Hostname/DNSBL 檢查機能
        #封鎖：限制出現之文字
        for value in self.app.config.get('BAD_STRING'):
            if string.find(com, value) != -1 or string.find(sub, value) != -1 or string.find(name, value) != -1 or string.find(email, value) != -1:
                return self.render_error(_('regist_wordfiltered'))
        #todo: 檢查是否輸入櫻花日文假名
        #時間
        tmp = str(time.time()).split('.')
        tim = str('%03d' % int(tmp[1]))
        tim = '%s%s' % (tmp[0], tim[0:3])
        #如果有上傳檔案則處理附加圖檔
        if upfile:
            #check file size
            size = len(upfile)
            if size > self.app.config.get('MAX_KB') * 1024:
                return self.render_error(_('regist_upload_overlimit'))
            #檢查是否為可接受的檔案
            try:
                img = images.Image(upfile)
            except images.BadImageError:
                return self.render_error(_('regist_upload_notsupport'))
            allow_exts = self.app.config.get('ALLOW_UPLOAD_EXT').split('|') #接受之附加圖檔副檔名
            #判斷上傳附加圖檔之格式
            if img.format == images.JPEG:
                ext = 'jpg'
            elif img.format == images.PNG:
                ext = 'png'
            elif img.format == images.WEBP:
                ext = 'webp'
            elif img.format == images.BMP:
                ext = 'bmp'
            elif img.format == images.GIF:
                ext = 'gif'
            elif img.format == images.ICO:
                ext = 'ico'
            elif img.format == images.TIFF:
                ext = 'tiff'
            else:
                ext = 'xxx'
            allow = False
            for allow_ext in allow_exts:
                if string.lower(allow_ext) == ext:
                    allow = True
                    break
            if not allow:
                return self.render_error(_('regist_upload_notsupport')) #並無在接受副檔名之列
            #封鎖設定：限制上傳附加圖檔之MD5檢查碼
            m = hashlib.md5()
            m.update(upfile)
            md5chksum = m.hexdigest()
            #在封鎖設定內則阻擋
            for bad_filemd5 in self.app.config.get('BAD_FILEMD5'):
                if md5chksum == bad_filemd5:
                    return self.render_error(_('regist_upload_blocked'))
            #計算附加圖檔圖檔縮圖顯示尺寸
            maxw = self.app.config.get('MAX_W')
            maxh = self.app.config.get('MAX_H')
            if img.width > maxw or img.height > maxh:
                w2 = maxw * 1.0 / img.width
                h2 = maxh * 1.0 / img.height
                key = w2 if w2 < h2 else h2
            #$mes = _T('regist_uploaded', CleanStr($upfile_name));
        #檢查表單欄位內容並修整
        if len(name) > 100:
            return self.render_error(_('regist_nametoolong'))
        if len(email) > 100:
            return self.render_error(_('regist_emailtoolong'))
        if len(sub) > 100:
            return self.render_error(_('regist_topictoolong'))
        # E-mail / 標題修整
        email = string.replace(email, '\r\n', '')
        # 名稱修整
        name = string.replace(name, _('trip_pre'), _('trip_pre_fake')) # 防止トリップ偽造
        name = string.replace(name, self.app.config.get('CAP_SUFFIX'), _('cap_char_fake')) # 防止管理員キャップ偽造
        name = string.replace(name, '\r\n', '')
        
        self.render_error('123')    
        
