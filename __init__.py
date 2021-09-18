
from mycroft import MycroftSkill, intent_handler
from mycroft.util import LOG
from mycroft.skills.context import adds_context, removes_context
from adapt.intent import IntentBuilder

import cv2
from requests import Session
import os
import sys
from multiprocessing import Process

sys.path.append('/opt/mycroft/skills/sandbox-git-skill')
from cvAPI import getDetail, getObjLabel


def take_photo():
    LOG.info('**************************###======================== take photo process start')
    cap = cv2.VideoCapture(0)
    # cap.isOpened()
    # i = 0
    while (1):
        ret, frame = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow('capture', frame)

    cap.release()
    cv2.destroyAllWindows()
    LOG.info('**************************###======================== take photo process end')
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
        self.log.info("**************************###=============================== _init_")

    def initialize(self):
        self.log.info("**************************###=============================== initialize")

    # @intent_handler('view.items.intent')
    # def handle_view_goods(self, message):
        # self.speak_dialog('take.photo')
        # take_photo_process = Process(target=take_photo)
        # take_photo_process.start()
        # take_photo_process.join()
        # try:
        #     objLabel = getObjLabel(
        #         '/opt/mycroft/skills/sandbox-git-skill/photo/multi.jpeg')
        #     objNum = int(objLabel['objectNum'])
        #     if objNum > 1:
        #         self.speak_dialog('there.are')
        #         label_chose = self.ask_selection(
        #             self.flavors, 'which_one', min_conf=0.8, numeric=True)
        #     elif objNum == 1:
        #         self.speak_dialog('there.is')
        #     else:
        #         self.speak_dialog('there.no', expect_response=True)

        # except Exception as e:
        #     self.log.exception("Error: {0}".format(e))
        #     self.speak_dialog(
        #         "exception", {"action": "calling computer vision API"}, expect_response=True)

        # self.log.error("###=============================== view goods intent")


    @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    # @adds_context('getDetailContext')
    def handle_view_item_in_hand(self, message):
        self.speak_dialog('take.photo')
        take_photo_process = Process(target=take_photo)
        take_photo_process.start()
        take_photo_process.join()

        try:
            # TODO: change the image file path
            detail = getDetail.getDetail(
                '/opt/mycroft/skills/sandbox-git-skill/photo/white.png')

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
