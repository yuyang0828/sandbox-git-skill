from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder

LOGSTR = '********************====================########## '

class EasyShoppingSkill(MycroftSkill):
    
    def __init__(self):
        MycroftSkill.__init__(self)
        self.log.info(LOGSTR + "_init_ EasyShoppingSkill")


    def initialize(self):
        self.log.info(LOGSTR + "initialize EasyShoppingSkill")

    @intent_handler('view.goods.intent')
    def handle_view_goods(self, message):
        self.speak('Taking a photo now. Please wait a second for me to get the result.')
        self.speak('I find some goods here, you can ask me whatever goods you want.')

    @intent_handler('is.there.any.goods.intent')
    def handle_is_there_any_goods(self, message):
        self.speak('yes, I find some goods in front of you')
 
            
    @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    def handle_view_item_in_hand(self, message):
        self.speak('Taking a photo now. Please wait a second for me to get the result.')
        self.speak('The item is possible to be something. You can ask me any details about the item now, such as brand, color or complete information.')


    @intent_handler(IntentBuilder('AskItemCategory').require('Category').build())
    def handle_ask_item_category(self, message):
        self.speak('I am talking about the category of the item')

    @intent_handler(IntentBuilder('AskItemColor').require('Color').build())
    def handle_ask_item_color(self, message):
        self.speak('I am talking about the color of the item')

    @intent_handler(IntentBuilder('AskItemBrand').require('Brand').build())
    def handle_ask_item_brand(self, message):
        self.speak('I am talking about the brand of the item')

    @intent_handler(IntentBuilder('AskItemKw').require('Kw').build())
    def handle_ask_item_keywords(self, message):
        self.speak('I am talking about the keywords of the item')

    @intent_handler(IntentBuilder('AskItemInfo').require('Info').build())
    def handle_ask_item_complete_info(self, message):
        self.speak('I am speaking the complete information of the item')

    @intent_handler(IntentBuilder('FinishOneItem').require('Finish').build())
    def handle_finish_current_item(self, message):
        self.speak('Got you request. Let\'s continue shopping!')




def create_skill():
    return EasyShoppingSkill()
