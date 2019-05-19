"""
Created on 2018年4月11日
配置文件读取
@author: hujing
"""
import configparser


class Config:
    
    def __init__(self):
        self.configPath = 'config.ini'
        self.con = configparser.ConfigParser()
        self.con.read(self.configPath, encoding='utf-8')
    
    def ifDefault(self, name):
        """
        判断该进程是否为默认选中
        :param name: 进程名
        """
        try:
            if self.con.get('default', name) == '1':
                return True
            return False
        except:
            return False
    
    def getReferral(self, name):
        """
        获取进程的介绍
        :param name: 进程名
        """
        
        try:
            return '' + self.con.get('referral', name)
        except:
            return ''
        
    def updateDefault(self, names):
        """
        更新默认选中的进程
        :param names: 进程名列表
        """
        # 拿到default域下的所有key
        keys = self.con.options('default')
        # 先将所有的默认都删除
        for key in keys:
            self.con.set('default', key, '0')
        # 便利names
        for name in names:
            self.con.set('default', name, '1')
        # 将修改写入  
        with open(self.configPath, 'w', encoding='utf-8') as fw:   #循环写入
            self.con.write(fw)


if __name__ == '__main__':
    conf = Config()
    names = ['chrome.exe', 'python.exe']
    conf.updateDefault(names)
