from calculator.models import UserSettings


class CreateSearchUrl():
    """Creates search urls for Redfin bot"""
    def __init__(self, user):
        self.user = user
        self.settings = None
        self.domain = "https://www.redfin.com/"
        self.city_url = None
        self.zipcode_url = None
        self.filters_url = None

    def get_user_settings(self):
        """attempts to retrieve user settings"""
        try:
            user_settings = UserSettings.objects.get(user=self.user)
            self.settings = user_settings
        except:
            print('Unable to get user settings')
            self.settings = None

    def create_city_url(self):
        """Takes setting values and creates relevant redfin search url"""
        if self.settings.city:
            self.settings.city = self.settings.city.title().replace(' ','-')
        if self.settings.minor_civil_div:
            self.city_url = f'minorcivildivision/{self.settings.city_code}/{self.settings.state}/{self.settings.city}/'
        else:
            self.city_url = f'city/{self.settings.city_code}/{self.settings.state}/{self.settings.city}/'

    def create_zipcode_url(self):
        if self.settings.zipcode:
            self.zipcode_url = f'zipcode/{self.settings.zipcode}/'

    def create_filters_url(self):
        url_parts = []
        if self.settings.prop_type:
            unit_string = '+'.join(type for type in [i.lower() for i in self.settings.prop_type])
            prop_type_fin = f'property-type={unit_string}'
            url_parts.append(prop_type_fin)

        if self.settings.min_price:
            stripped_min_price = self.settings.min_price.strip('$')
            min_price = f'min-price={stripped_min_price}'
            url_parts.append(min_price)

        if self.settings.max_price:
            stripped_max_price = self.settings.max_price.strip('$')
            max_price = f'max-price={stripped_max_price}'
            url_parts.append(max_price)

        if self.settings.min_beds:
            min_beds = f'min-beds={self.settings.min_beds}'
            url_parts.append(min_beds)

        if self.settings.max_beds:
            max_beds = f'max-beds={self.settings.max_beds}'
            url_parts.append(max_beds)

        if self.settings.min_baths:
            stripped_min_baths = self.settings.min_baths.strip('+')
            min_baths = f'min-baths={stripped_min_baths}'
            url_parts.append(min_baths)
        
        filters = ','.join(part for part in url_parts)

        self.filters_url = f'filter/{filters}'

    def get_complete_url(self):
        self.get_user_settings()
        if self.settings.city_code and self.settings.state and self.settings.city:
            self.create_city_url()
        elif self.settings.zipcode:
            self.create_zipcode_url()
        else:
            self.city_url = None
            self.zipcode_url = None

        if self.settings.min_price or self.settings.max_price or \
            self.settings.prop_type or self.settings.min_beds or \
            self.settings.max_beds or self.settings.min_baths:
                self.create_filters_url()

        if self.city_url:
            return f'{self.domain}{self.city_url}{self.filters_url}'
        elif self.zipcode_url:
            return f'{self.domain}{self.zipcode_url}{self.filters_url}'
        else:
            return None
        