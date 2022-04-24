from score import Scoreboard
 
myScoreboard = Scoreboard('filepath(不會用到)','週三上3',"http://140.112.175.15:3000")
 
# 傳UID
# myScoreboard.add_UID("ABCDEF01")   # example
# 大小寫都可以，記得補0
myScoreboard.add_UID("2090c5a3") # 記得補0
 
# 拿分數
# 方法1: 直接打開網址http://192.168.50.165:3000
# 方法2
print( myScoreboard.getCurrentScore() )
