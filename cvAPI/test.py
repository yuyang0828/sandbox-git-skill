import base64
import multiprocessing
import os
import cv2
import time

# def writer_proc(q):      
#     try:         
#         q.put(1, block = False) 
#     except:         
#         pass   

# def reader_proc(q):      
#     try:         
#         print q.get(block = False) 
#     except:         
#         pass

def take_photo(img_queue):
    print('========================>>>>>>>>>>>>> take photo process start')
    cap = cv2.VideoCapture(0)
    # img_num = 1
    # flag = 0
    img_name = 'cap_img_' + str(time.time()) + '.jpg'
    img_path = '/opt/mycroft/skills/sandbox-git-skill.yuyang0828/photo/' + img_name

    # img_queue.put(1)



    #<-- Take photo in specific time duration -->
    cout = 0
    while True:
        ret, frame = cap.read()
        cv2.waitKey(1)
        cv2.imshow('capture', frame)
        cout += 1 
        if cout == 50:
            ss = base64.b64encode(frame)
            # img_queue.put(img_path, block=False)
            img_queue.put(frame)
            # conn.send(frame)
            cv2.imwrite(img_path, frame)
            # print(type(frame)) # ndarray
            break
            # img_name = 'cap_img_' + str(img_num) + '.jpg'
            # img_path = os.path.join('/opt/mycroft/skills/sandbox/photo', img_name)
            # for img_num in range(1,100):
            #     img_name = 'cap_img_' + str(img_num) + '.jpg'
            #     img_path = os.path.join('/opt/mycroft/skills/easyshopping-skill.camille7777/photo', img_name)
            #     if not(os.path.exists(img_path)):
            #         cv2.imwrite(img_path, frame)
            #         flag = 1
            #         cur_img_path = img_path
            #         break
            #     else:
            #         continue

        #<-- Take photo by pressing q key -->
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     img_name = 'cap_img_' + str(img_num) + '.jpg'
        #     img_path = os.path.join('/opt/mycroft/skills/take-item-photo-skill.maoyuejingxian/photo', img_name)
        #     for img_num in range(1,100):
        #         img_name = 'cap_img_' + str(img_num) + '.jpg'
        #         img_path = os.path.join('/opt/mycroft/skills/take-item-photo-skill.maoyuejingxian/photo', img_name)
        #         if not(os.path.exists(img_path)):
        #             cv2.imwrite(img_path, frame)
        #             flag = 1
        #             break
        #         else:
        #             continue
    cap.release()
    cv2.destroyAllWindows()
    print('========================>>>>>>>>>>>>>>> take photo process end')
    os._exit(0)



if __name__ == "__main__":
    lala = ''
    img_queue = multiprocessing.Queue()
    pp = multiprocessing.Process(target=take_photo, args=(img_queue,))
    pp.daemon = True
    pp.start()
    pp.join()
    print('finishdsfdfsd')
    time.sleep(0.0001)
    print("queue.empty()=", img_queue.empty())
    while not img_queue.empty():
        print(">>>数据出队中......")
        data = img_queue.get()
        cv2.imshow("picture", data)
        cv2.waitKey(0)
    # lala = img_queue.get(block=False)
    # print(type(lala))
    # print(lala)
    print('finish')

    


    # writer = multiprocessing.Process(target=writer_proc, args=(q,))  
    # writer.start()   

    # reader = multiprocessing.Process(target=reader_proc, args=(q,))  
    # reader.start()  

    # reader.join()  
    # writer.join()