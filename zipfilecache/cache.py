import zipfile  
import os  
import hashlib  
import threading  
import time  
from collections import OrderedDict  
from functools import lru_cache  
  
class ThreadSafeLRUCache:    
    '''
    线程安全的LRU缓存
    '''
    def __init__(self, maxsize=128):    
        self.cache = OrderedDict()    
        self.lock = threading.Lock()    
        self.maxsize = maxsize    
    def __contains__(self, key):  
        with self.lock:  
            return key in self.cache  
    def get(self, key, default=None):    
        with self.lock:    
            return self.cache.get(key, default)    
    def put(self, key, value):    
        with self.lock:    
            if key in self.cache:    
                del self.cache[key]    
            elif len(self.cache) >= self.maxsize:    
                self.cache.popitem(last=False)    
            self.cache[key] = value 

class ZipFileCache:  
    def __init__(self, zip_ref_cache_size=128, file_cache_size=128, disk_cache_dir='./tmp', disk_cache_limit=1024, disk_cleanup_interval=120):  
        '''
        初始化机制:
        (* 设置为0关闭这个缓存功能)
        zip_ref_cache_size          *压缩文件缓存数量
        file_cache_size             *内存缓存数量
        disk_cache_dir              磁盘缓存路径(启用取决于disk_cache_limit)
        disk_cache_limit            *磁盘缓存最大数量
        disk_cleanup_interval       *定时清除磁盘缓存秒数
        '''
        self.zip_ref_cache = ThreadSafeLRUCache(zip_ref_cache_size)  
        self.file_cache = ThreadSafeLRUCache(file_cache_size)  
        self.disk_cache_dir = disk_cache_dir  
        self.disk_cache_limit = disk_cache_limit  
        self.disk_cleanup_interval = disk_cleanup_interval  

        self.zip_ref_enable = zip_ref_cache_size > 0
        self.file_cache_enable = file_cache_size > 0
        self.disk_cache_enable = disk_cache_limit > 0


        if disk_cleanup_interval > 0:
            self.last_cleanup = time.time()  
            self.disk_cleanup_thread = threading.Thread(target=self._disk_cleanup_loop, daemon=True)  
            self.disk_cleanup_thread.start()  
  
    def _disk_cleanup_loop(self):  
        while True:  
            time.sleep(self.disk_cleanup_interval)  
            self._cleanup_disk_cache()  
  
    def _cleanup_disk_cache(self):  
        if len(os.listdir(self.disk_cache_dir)) > self.disk_cache_limit:  
            files = sorted(os.listdir(self.disk_cache_dir), key=lambda x: os.path.getmtime(os.path.join(self.disk_cache_dir, x)))  
            for file in files[:-self.disk_cache_limit]:  
                os.remove(os.path.join(self.disk_cache_dir, file))  
  
    def _get_disk_cache_path(self, zip_path, file_path):  
        hasher = hashlib.md5()  
        hasher.update((zip_path + file_path).encode('utf-8'))  
        return os.path.join(self.disk_cache_dir, hasher.hexdigest())  
  
    def read_file(self, zip_path, file_path):  
        '''
        zip_path 压缩包路径
        file_path 文件在压缩包内部的路径
        '''
        zip_key = (zip_path, 'zip_ref')  
        file_key = (zip_path, file_path)  
  
        # Check file cache  
        if self.disk_cache_enable and file_key in self.file_cache:  
            return self.file_cache.get(file_key)  
  
        # Check disk cache  
        disk_path = self._get_disk_cache_path(zip_path, file_path)  
        if os.path.exists(disk_path):  
            with open(disk_path, 'rb') as f:  
                content = f.read()  
                self.file_cache.put(file_key, content)  
                return content  
  
        # Check zip ref cache  
        zip_ref = self.zip_ref_cache.get(zip_key)  
        if zip_ref is None:  
            zip_ref = zipfile.ZipFile(zip_path, 'r')  
            self.zip_ref_cache.put(zip_key, zip_ref)  
  
        # Read from zip file  
        with zip_ref.open(file_path, 'r') as f:  
            content = f.read()  
  
        # Save to disk cache  
        if self.disk_cache_enable:
            os.makedirs(self.disk_cache_dir, exist_ok=True)  
            with open(disk_path, 'wb') as f:  
                f.write(content)  
  
        # Save to file cache  
        if self.file_cache_enable:
            self.file_cache.put(file_key, content)  
  
        return content  

    def read_files(self, zip_path, file_paths):  
        '''
        zip_path 压缩包路径
        file_paths 文件在压缩包内部的路径元组or列表
        '''
        return [self.read_file(zip_path, file_path) for file_path in file_paths]  
  
    
    def __del__(self):  
        # Close all zip files  
        for zip_ref in self.zip_ref_cache.cache.values():  
            zip_ref.close()

# if __name__ == "__main__":
#     # z = ZipFileCache(zip_ref_cache_size = 8, file_cache_size=16, disk_cache_dir='./tmp', disk_cache_limit=128, disk_cleanup_interval=1)
#     # a,b,c,d,e,f = z.read_files("1.zip",("1.png","2.png","3.png","4.png","5.png","6.png"))
#     # with zipfile.ZipFile("1.zip", 'r') as zip_ref:  
#     #     zip_info_list = zip_ref.infolist()  
#     #     for zip_info in zip_info_list:  
#     #         print(zip_info.filename)
#     # while 1:
#     #     pass
#     pass