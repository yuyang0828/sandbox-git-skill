
import queue
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util import LOG
from mycroft.skills.context import adds_context, removes_context
from adapt.intent import IntentBuilder
import time
import cv2
from requests import Session
import os
import sys
from multiprocessing import Process, Queue, Pipe

sys.path.append('/opt/mycroft/skills/sandbox-git-skill')
from cvAPI import getDetail, getObjLabel


def take_photo(queue):
    LOG.info('========================>>>>>>>>>>>>> take photo process start')
    cap = cv2.VideoCapture(0)
    # img_num = 1
    # flag = 0
    img_name = 'cap_img_' + str(time.time()) + '.jpg'
    img_path = '/opt/mycroft/skills/sandbox-git-skill/photo/' + img_name



    #<-- Take photo in specific time duration -->
    cout = 0
    while True:
        ret, frame = cap.read()
        cv2.waitKey(1)
        cv2.imshow('capture', frame)
        cout += 1 
        if cout == 50:
            queue.put(frame)
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
    LOG.info('========================>>>>>>>>>>>>>>> take photo process end')
    os._exit(0)


def generate_str(possible_list):
    res = ''
    if len(possible_list) == 3:
        res = possible_list[0] + ' ' + \
            possible_list[1] + ' and ' + possible_list[2]
    elif len(possible_list) == 2:
        res = possible_list[0] + ' and ' + possible_list[1]
    elif len(possible_list) == 1:
        res = possible_list[0]

    return res


class EasyShoppingSkill(MycroftSkill):
    
    def __init__(self):
        MycroftSkill.__init__(self)
        self.category_str = ''
        self.color_str = ''
        self.brand_str = ''
        self.kw_str = ''
        self.img_multi = ''
        self.img_hand = ''
        self.log.info("**************************###=============================== _init_")


    def initialize(self):
        self.log.info("**************************###=============================== initialize")
        # self.register_intent_file('view.goods.intent', self.handle_view_goods)
        # self.register_intent_file('is.there.any.goods.intent', self.handle_is_there_any_goods)
        #self.register_entity_file('category.entity')
        #self.register_entity_file('location.entity')


    def take_photo(self, case):
        self.log.error('========================>>>>>>>>>>>>> self take photo process start')
        cap = cv2.VideoCapture(0)
    
        img_name = 'cap_img_' + str(time.time()) + '.jpg'
        img_path = '/opt/mycroft/skills/sandbox-git-skill/photo/' + img_name

        #<-- Take photo in specific time duration -->
        cout = 0
        while True:
            ret, frame = cap.read()
            cv2.waitKey(1)
            cv2.imshow('capture', frame)
            cout += 1 
            if cout == 50:
                self.log.info(case)
                if case == 'mulit':
                    self.img_multi = frame
                elif case == 'hand':
                    self.img_hand = frame
                else:
                    raise Exception
                self.log.info(type(frame))
                self.log.info(frame)
                self.log.info(type(self.img_multi))
                cv2.imwrite(img_path, frame)
                break

        cap.release()
        cv2.destroyAllWindows()
        self.log.error('========================>>>>>>>>>>>>>>> self take photo process end')


    @intent_handler('view.goods.intent')
    def handle_view_goods(self, message):
        self.speak_dialog('view.goods')
        # conn1, conn2 = Pipe()
        # take_photo_process = Process(target=take_photo,args = (conn1,))
        # take_photo_process.start()
        # take_photo_process.join()

        # LOG.error('######## ========================>>>>>>>>>>>>>>> get photo')
        # self.img_multi = conn2.recv()
        
        take_photo_process = Process(target=self.take_photo, args=('multi',))
        # take_photo_process.daemon = True
        take_photo_process.start()
        take_photo_process.join()

        self.log.info('######## ========================>>>>>>>>>>>>>>> get photo')
        self.log.info(type(self.img_multi))
        self.log.info(self.img_multi)

        
        self.speak('I find some goods here, you can ask me whatever goods you want.', expect_response=True)

    @intent_handler('is.there.any.goods.intent')
    def handle_is_there_any_goods(self, message):
        self.log.error(type(self.img_multi))
        try:
            # TODO: change image path
            self.img_multi = '/opt/mycroft/skills/sandbox-git-skill/photo/multi.jpeg'
            objectlist = getObjLabel.getObjectsThenLabel(self.img_multi)
            label_list = []
            loc_list = []
            detected = 0

            category_label = message.data.get('category')

            for obj in objectlist['objectList']:
                label_list.append(obj['name'])
                loc_list.append(obj['loc'])
            
            
            for i in range(0,len(label_list)):
                self.label_str = generate_str(label_list[i])
                self.label_str = self.label_str.lower()
                # self.log.error("=============================")
                # self.log.error(self.label_str)
                # self.log.error(loc_list)

                self.log.error(category_label)
            
                if category_label is not None:
                    if category_label in self.label_str:
                        self.speak_dialog('yes.goods',
                                        {'category': category_label,
                                        'location': loc_list[i]})
                        detected = 1
                        break
                else:
                    continue

            if detected == 0:
                self.speak_dialog('no.goods',
                {'category': category_label})

        except Exception as e:
            self.log.error("**************************###============================= Error: {0}".format(e))
            self.speak_dialog(
                "exception", {"action": "calling computer vision API"})


    def handle_no_context2(self, message):
        self.speak('Please let me have a look at what\'s in front of you first.')
        take_photo = self.ask_yesno('do.you.want.to.take.a.photo')
        if take_photo == 'yes':
            self.handle_view_goods(message)
        elif take_photo == 'no':
            self.speak('OK. I won\'t take photo')
        else:
            self.speak('I cannot understand what you are saying')




    @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    # @adds_context('getDetailContext')
    def handle_view_item_in_hand(self, message):
        self.speak_dialog('take.photo')
        img_queue = Queue()
        take_photo_process = Process(target=take_photo, args=((img_queue),))
        take_photo_process.start()
        take_photo_process.join()
        self.img_hand = img_queue.get()
        LOG.info('========================>>>>>>>>>>>>>>> get photo')
        print(type(self.img_hand))
        print(self.img_hand)

        try:
            # TODO: change the image file path
            self.img_hand = '/opt/mycroft/skills/sandbox-git-skill/photo/1.jpeg'
            detail = getDetail.getDetail(self.img_hand)

            self.category_str = generate_str(detail['objectLabel'])
            # self.category_str = ''

            if self.category_str != '':
                self.set_context('getDetailContext')
                self.speak_dialog(
                    'item.category', {'category': self.category_str}, expect_response=True)

                self.brand_str = generate_str(detail['objectLogo'])

                color_list = []
                for color in detail['objectColor']:
                    color_list.append(color['colorName'])
                self.color_str = generate_str(color_list)

                self.kw_str = ' '.join(detail['objectText'])

            else:
                self.remove_context('getDetailContext')
                self.speak(
                    'I cannot understand what is in your hand. Maybe turn around it and let me see it again', expect_response=True)
                

        except Exception as e:
            self.log.error("**************************###============================= Error: {0}".format(e))
            self.speak_dialog(
                "exception", {"action": "calling computer vision API"})
    
    def handle_ask_item_detail(self, detail, detail_str):
        if detail_str == '':
            self.speak_dialog(
            'cannot.get', {'detail': detail}, expect_response=True)
        else:
            dialog_str = 'item.' + detail
            self.speak_dialog(dialog_str, {detail: detail_str}, expect_response=True)

    @intent_handler(IntentBuilder('AskItemCategory').require('Category').require('getDetailContext').build())
    def handle_ask_item_category(self, message):
        self.handle_ask_item_detail('category', self.category_str)

    @intent_handler(IntentBuilder('AskItemColor').require('Color').require('getDetailContext').build())
    def handle_ask_item_color(self, message):
        self.handle_ask_item_detail('color', self.color_str)

    @intent_handler(IntentBuilder('AskItemBrand').require('Brand').require('getDetailContext').build())
    def handle_ask_item_brand(self, message):
        self.handle_ask_item_detail('brand', self.brand_str)

    @intent_handler(IntentBuilder('AskItemKw').require('Kw').require('getDetailContext').build())
    def handle_ask_item_keywords(self, message):
        self.handle_ask_item_detail('keyword', self.kw_str)

    @intent_handler(IntentBuilder('AskItemInfo').require('Info').require('getDetailContext').build())
    def handle_ask_item_complete_info(self, message):
        if self.color_str == '':
            self.handle_ask_item_detail('color', self.color_str)
        else:
            self.speak_dialog('item.complete.info', {
                          'category': self.category_str, 'color': self.color_str})
        self.handle_ask_item_detail('brand', self.brand_str)
        self.handle_ask_item_detail('keyword', self.kw_str)


    @intent_handler(IntentBuilder('FinishOneItem').require('Finish').require('getDetailContext').build())
    @removes_context('getDetailContext')
    def handle_finish_current_item(self, message):
        self.speak('Got you request. Let\'s continue shopping!')
        self.types_str = ''
        self.color_str = ''
        self.logo_str = ''
        self.kw_str = ''

    @intent_handler(IntentBuilder('NoContext').one_of('Category', 'Color', 'Brand', 'Kw', 'Info'))
    def handle_no_context(self, message):
        self.speak('Please let me have a look at what\'s on your hand first.')
        take_photo = self.ask_yesno('do.you.want.to.take.a.photo')
        if take_photo == 'yes':
            self.handle_view_item_in_hand(message)
        elif take_photo == 'no':
            self.speak('OK. I won\'t take photo')
        else:
            self.speak('I cannot understand what you are saying')




def create_skill():
    return EasyShoppingSkill()
