# ZipFileCache:

Provide a ZipFileCache class, which can support reading files using the compressed package path + file path in the compressed package, with memory and disk cache mechanism.

    class ZipFileCache
        __init__
            (* : Set 0 to off )
            zip_ref_cache_size     = 8        *The number of caches for compressed files
            file_cache_size        = 128      *Number of memory cache files
            disk_cache_dir         = "/tmp"   Disk cache path (enabled depending on disk_cache_limit)
            disk_cache_limit       = 1024     *The maximum number of disk caches
            disk_cleanup_interval  = 120      *The number of seconds to clear the disk cache

        read_file(self, zip_path, file_path)
            zip_path    : Archive path
            file_path   : The path of the file inside the archive

            return      : bytes object

        read_files(self, zip_path, file_paths):  
            zip_path    : Archive path
            file_paths  : The path tuple or list of files inside the archive

            return      : bytes objects tuple 
