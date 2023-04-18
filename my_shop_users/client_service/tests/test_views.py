from django.test import TestCase
import json

class TestViewsIsDisplayed(TestCase):
    """
    Test whether the data from cookie and template are displayed on the pages
    """
    
    def test_displayed_items_in_bussket(self):
        items_bussket_dict = ''

        if items_bussket_dict == '':
            items_bussket_dict = {"items_bussket": []}

        items_bussket_dict["items_bussket"].append(
            {"name_items": 'name',
            "price": 20,
            "items_info_description": 'description',
            "id_item": 100000}
        )
        self.client.cookies['all_item_bussket'] = json.dumps(items_bussket_dict)    


        response = self.client.get('/checkout/')
        self.assertTemplateUsed(response, 'checkout.html')