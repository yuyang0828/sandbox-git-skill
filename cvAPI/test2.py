

from multiprocessing import Process,Queue
import os
import cv2
import sys
import time
def putData(queue):
    print("\n************获得 putData 的pid:", os.getppid())
    print(">>>数据入队...")
    img = cv2.imread("/opt/mycroft/skills/sandbox-git-skill.yuyang0828/photo/1.jpeg")
    queue.put(img)
    print(">>>数据入队完毕！")

def getData(queue):
    time.sleep(0.0001)
    print("\n************获得 getData 的pid:", os.getppid())
    print("queue.empty()=", queue.empty())
    while not queue.empty():
        print(">>>数据出队中......")
        data = queue.get()
        cv2.imshow("picture", data)
        cv2.waitKey(0)
    print(">>>数据出入队完毕!\n")

if __name__ == '__main__':
    print("python的版本:", sys.version)
    print("获得父进程的pid:", os.getppid())

    # 如果Queue(N)不指定长度,默认最大(和硬件相关)
    queue = Queue()

    run_putData = Process(target=putData,args=(queue,))
    run_getData = Process(target=getData, args=(queue,))


    run_putData.start()
    run_getData.start()
    
    # 打印进程的 id
    print("run_putData.pid:", run_putData.pid)
    print("run_getData.pid:", run_getData.pid)
    run_putData.join()
    run_getData.join()

