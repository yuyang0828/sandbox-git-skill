from mycroft import MycroftSkill, intent_handler
from mycroft.skills.context import removes_context
from adapt.intent import IntentBuilder

LOGSTR = '********************====================########## '

def generate_str(possible_list):
    '''
    Generate string for Mycroft to speak it

    Args: 
        possible_list: array list with len = 3, each element is a string
    Returns:
        a string, e.g. possible_list = ['a', 'b', 'c'], res = 'a, b, and c'
    '''
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
        self.log.info(LOGSTR + "_init_ EasyShoppingSkill")

    # ============================ use case 1 ============================
    @intent_handler('view.goods.intent')
    def handle_view_goods(self, message):
        self.speak_dialog('take.photo')
        self.img_multi = ''
        self.img_hand = ''

        # suppose we use camera to take a photo here, 
        # then the function will return an image path
        self.img_multi = '/opt/mycroft/skills/sandbox-git-skill.yuyang0828/photo/multi.jpeg'

        self.speak('I find some goods here, you can ask me whatever goods you want.')


    @intent_handler('is.there.any.goods.intent')
    def handle_is_there_any_goods(self, message):
        if self.img_multi == '':
            # if self.img_multi == '', 
            # then it means that user hasn't invoked intent(handle_view_goods)
            self.handle_no_context1(message)
        else:
            # if self.img_multi != '', then in real application we will call CV API
            # then we can get the following two lists
            label_list = [['milk', 'drink', 'bottle'], ['milk', 'drink', 'bottle']]
            loc_list = ['left top', 'right top']

            category_label = message.data.get('category')
            detected = 0

            for i in range(len(label_list)):
                label_str = generate_str(label_list[i])
                label_str = label_str.lower()
        
                if category_label is not None:
                    if category_label in label_str:
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


    def handle_no_context1(self, message):
        self.speak('Please let me have a look at what\'s in front of you first.')



    # ============================ use case 2 ============================
    @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    def handle_view_item_in_hand(self, message):
        self.speak_dialog('take.photo')
        self.img_multi = ''
        self.img_hand = ''
        
        # suppose we use camera to take a photo here, 
        # then the function will return an image path
        self.img_hand = '/opt/mycroft/skills/sandbox-git-skill.yuyang0828/photo/2.jpeg'
   
        # suppose we call CV API here to get the result, 
        # the result will all be list, then we use generate_str() to create string
        self.category_str = generate_str(['milk', 'bottle', 'drink'])
        self.brand_str = generate_str(['Dutch Lady', 'Lady'])
        self.color_str = generate_str(['white', 'black', 'blue'])
        self.kw_str = ' '.join(['milk', 'bottle', 'protein', 'pure', 'farm'])

        # set the context
        self.set_context('getDetailContext')

        # speak dialog
        self.speak_dialog('item.category', {'category': self.category_str})

    def handle_ask_item_detail(self, detail, detail_str):
        if detail_str == '':
            self.speak_dialog(
            'cannot.get', {'detail': detail})
        else:
            dialog_str = 'item.' + detail
            self.speak_dialog(dialog_str, {detail: detail_str})

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
        self.img_hand = ''
        self.img_multi = ''

    @intent_handler(IntentBuilder('NoContext').one_of('Category', 'Color', 'Brand', 'Kw', 'Info'))
    def handle_no_context2(self, message):
        self.speak('Please let me have a look at what\'s on your hand first.')




def create_skill():
    return EasyShoppingSkill()
