from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder

LOGSTR = '********************====================########## '


class EasyShoppingSkill(MycroftSkill):
    
    def __init__(self):
        MycroftSkill.__init__(self)
        self.category_str = ''
        self.color_str = ''
        self.brand_str = ''
        self.kw_str = ''
        self.log.info(LOGSTR + "_init_ EasyShoppingSkill")

    # ============================ use case 1 ============================
    @intent_handler('view.goods.intent')
    def handle_view_goods(self, message):
        self.speak_dialog('take.photo')
        self.speak('I find some goods here, you can ask me whatever goods you want.')

    @intent_handler('is.there.any.goods.intent')
    def handle_is_there_any_goods(self, message):
        # in real application, label_str will return from CV API
        label_str = ['milk', 'drink', 'bottle']
        category_label = message.data.get('category')
        loc = 'left top'

        if category_label in label_str:
            self.speak_dialog('yes.goods',{'category': category_label,'location': loc})

        else:
            self.speak_dialog('no.goods',{'category': category_label})

    # ============================ use case 2 ============================
    @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    def handle_view_item_in_hand(self, message):
        self.speak_dialog('take.photo')

        # in real application, we will call CV API to get the following information
        self.category_str = 'milk'
        self.color_str = 'black and white'
        self.brand_str = 'Dutch Lady'
        self.kw_str = 'pure farm, protein'
        self.speak_dialog('item.category', {'category': self.category_str})
        

    
    def handle_ask_item_detail(self, detail, detail_str):
        dialog_str = 'item.' + detail
        self.speak_dialog(dialog_str, {detail: detail_str})

    @intent_handler(IntentBuilder('AskItemCategory').require('Category').build())
    def handle_ask_item_category(self, message):
        self.handle_ask_item_detail('category', self.category_str)

    @intent_handler(IntentBuilder('AskItemColor').require('Color').build())
    def handle_ask_item_color(self, message):
        self.handle_ask_item_detail('color', self.color_str)

    @intent_handler(IntentBuilder('AskItemBrand').require('Brand').build())
    def handle_ask_item_brand(self, message):
        self.handle_ask_item_detail('brand', self.brand_str)

    @intent_handler(IntentBuilder('AskItemKw').require('Kw').build())
    def handle_ask_item_keywords(self, message):
        self.handle_ask_item_detail('keyword', self.kw_str)

    @intent_handler(IntentBuilder('AskItemInfo').require('Info').build())
    def handle_ask_item_complete_info(self, message):
        # in real application, color_str maybe empty
        if self.color_str == '':
            self.handle_ask_item_detail('color', self.color_str)
        else:
            self.speak_dialog('item.complete.info', {
                          'category': self.category_str, 'color': self.color_str})
        self.handle_ask_item_detail('brand', self.brand_str)
        self.handle_ask_item_detail('keyword', self.kw_str)


    @intent_handler(IntentBuilder('FinishOneItem').require('Finish').build())
    def handle_finish_current_item(self, message):
        self.speak('Got you request. Let\'s continue shopping!')
        self.types_str = ''
        self.color_str = ''
        self.logo_str = ''
        self.kw_str = ''

def create_skill():
    return EasyShoppingSkill()
