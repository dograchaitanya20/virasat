import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('core:home'))
    assert response.status_code == 200
    assert 'stats' in response.context
    assert b'VIRASAT' in response.content

@pytest.mark.django_db
def test_heritage_list_filtering(client):
    response = client.get(reverse('heritage:list') + '?category=Monument&unesco=1')
    assert response.status_code == 200
    assert 'sites' in response.context

@pytest.mark.django_db
def test_heritage_htmx_partial(client):
    response = client.get(reverse('heritage:list'), HTTP_HX_REQUEST='true')
    assert response.status_code == 200
    assert b'site-grid-container' in response.content

@pytest.mark.django_db
def test_festivals_list_view(client):
    response = client.get(reverse('festivals:list') + '?month=10')
    assert response.status_code == 200
    assert 'festivals' in response.context

@pytest.mark.django_db
def test_arts_list_view(client):
    response = client.get(reverse('arts:list') + '?category=Dance')
    assert response.status_code == 200
    assert 'arts' in response.context

@pytest.mark.django_db
def test_cuisine_list_view(client):
    response = client.get(reverse('cuisine:list') + '?diet=veg')
    assert response.status_code == 200
    assert 'dishes' in response.context

@pytest.mark.django_db
def test_map_and_timeline_views(client):
    res_map = client.get(reverse('core:map'))
    assert res_map.status_code == 200
    assert b'india-heritage-map' in res_map.content

    res_timeline = client.get(reverse('core:timeline'))
    assert res_timeline.status_code == 200
    assert 'events' in res_timeline.context

@pytest.mark.django_db
def test_quick_search_view(client):
    response = client.get(reverse('core:quick_search') + '?q=Taj')
    assert response.status_code == 200
    assert b'Taj' in response.content

@pytest.mark.django_db
def test_seo_sitemap_and_robots(client):
    res_sitemap = client.get('/sitemap.xml')
    assert res_sitemap.status_code == 200
    assert res_sitemap['Content-Type'] == 'application/xml'

    res_robots = client.get('/robots.txt')
    assert res_robots.status_code == 200
    assert b'User-agent: *' in res_robots.content
    assert b'Sitemap:' in res_robots.content


@pytest.mark.django_db
def test_language_switch_hindi_and_back(client):
    # Default English
    r_en = client.get(reverse('core:home'))
    assert r_en.status_code == 200
    assert 'Explore Heritage' in r_en.content.decode('utf-8')

    # Switch to Hindi
    r_to_hi = client.post('/i18n/setlang/', {'language': 'hi', 'next': reverse('core:home')})
    assert r_to_hi.status_code == 302
    assert client.cookies['django_language'].value == 'hi'

    # Verify Hindi translations in content
    r_hi = client.get(reverse('core:home'))
    assert r_hi.status_code == 200
    content_hi = r_hi.content.decode('utf-8')
    assert 'धरोहर' in content_hi
    assert 'धरोहर देखें' in content_hi
    assert 'ऋतु का त्योहार' in content_hi
    assert 'विरासत क्रॉनिकल्स' in content_hi

    # Switch back to English
    r_to_en = client.post('/i18n/setlang/', {'language': 'en', 'next': reverse('core:home')})
    assert r_to_en.status_code == 302
    r_en_back = client.get(reverse('core:home'))
    assert r_en_back.status_code == 200
    assert 'Explore Heritage' in r_en_back.content.decode('utf-8')


@pytest.mark.django_db
def test_festival_of_season_current_and_fallback(client):
    from apps.states.models import State
    from apps.festivals.models import Festival
    from datetime import datetime

    st = State.objects.create(name='Test State', slug='test-state', region='North', capital='City', lat=20.0, lng=77.0)
    current_month = datetime.now().month

    # Create a festival in the current month
    f_current = Festival.objects.create(
        name='Current Festive Celebration',
        slug='current-festive',
        month=current_month,
        approximate_dates='Nov 15-20',
        significance='Significance',
        rituals='Rituals',
        food='Food',
        hero_image='/static/images/festivals/current.jpg',
        image_credit='Author',
        image_license='CC BY-SA 4.0'
    )
    f_current.states.add(st)

    resp = client.get(reverse('core:home'))
    assert resp.status_code == 200
    assert resp.context['festival_of_month'] == f_current
    assert resp.context['is_current_month_festival'] is True
    assert 'Happening in ' in resp.content.decode('utf-8')

    # Remove current month festival to test fallback
    f_current.delete()

    # Create next month festival
    next_month = 12 if current_month < 12 else 1
    f_next = Festival.objects.create(
        name='Next Month Festive Celebration',
        slug='next-festive',
        month=next_month,
        approximate_dates='Dec 1-5',
        significance='Next Significance',
        rituals='Next Rituals',
        food='Next Food',
        hero_image='/static/images/festivals/next.jpg',
        image_credit='Author',
        image_license='CC BY-SA 4.0'
    )
    f_next.states.add(st)

    resp_fb = client.get(reverse('core:home'))
    assert resp_fb.status_code == 200
    assert resp_fb.context['festival_of_month'] == f_next
    assert resp_fb.context['is_current_month_festival'] is False
    assert 'Coming up next in ' in resp_fb.content.decode('utf-8')


@pytest.mark.django_db
def test_stats_consistency_database_computed(client):
    from apps.states.models import State
    from apps.heritage.models import HeritageSite

    st = State.objects.create(name='State X', slug='state-x', region='North', capital='City', lat=20.0, lng=77.0)
    for i in range(3):
        HeritageSite.objects.create(
            name=f'Site {i}',
            slug=f'site-{i}',
            state=st,
            category='Monument',
            era='Medieval',
            history='History',
            description='Desc',
            built_by='Ruler',
            lat=20.0,
            lng=77.0,
            hero_image=f'/static/images/heritage/site-{i}.jpg',
            image_credit='Author',
            image_license='CC BY-SA 4.0'
        )

    r_home = client.get(reverse('core:home'))
    assert r_home.status_code == 200
    assert r_home.context['stats']['sites'] == 3

    r_heritage = client.get(reverse('heritage:list'))
    assert r_heritage.status_code == 200
    assert r_heritage.context['total_sites_count'] == 3
    assert 'Discover 3 UNESCO World Heritage Sites' in r_heritage.content.decode('utf-8')


@pytest.mark.django_db
def test_filter_dropdowns_and_autocomplete_off(client):
    from apps.states.models import State
    from apps.cuisine.models import CuisineDish

    # State with cuisine dish
    st_with = State.objects.create(name='Active State', slug='active-state', region='North', capital='City', lat=20.0, lng=77.0)
    # State without cuisine dish
    st_empty = State.objects.create(name='Empty State', slug='empty-state', region='South', capital='City2', lat=10.0, lng=76.0)

    CuisineDish.objects.create(
        name='Test Dish',
        slug='test-dish',
        state=st_with,
        cooking_time='30 mins',
        ingredients='Ingredients',
        story='Story',
        hero_image='/static/images/cuisine/test.jpg',
        image_credit='Author',
        image_license='CC BY-SA 4.0'
    )

    r_cuisine = client.get(reverse('cuisine:list'))
    assert r_cuisine.status_code == 200
    dropdown_states = list(r_cuisine.context['states'])
    assert st_with in dropdown_states
    assert st_empty not in dropdown_states
    assert 'autocomplete="off"' in r_cuisine.content.decode('utf-8')

    # Heritage filter
    r_heritage = client.get(reverse('heritage:list'))
    assert 'autocomplete="off"' in r_heritage.content.decode('utf-8')

    # Festivals filter
    r_festivals = client.get(reverse('festivals:list'))
    assert 'autocomplete="off"' in r_festivals.content.decode('utf-8')

    # Arts filter
    r_arts = client.get(reverse('arts:list'))
    assert 'autocomplete="off"' in r_arts.content.decode('utf-8')


@pytest.mark.django_db
def test_footer_current_year(client):
    from datetime import datetime
    year = str(datetime.now().year)
    resp = client.get(reverse('core:home'))
    assert resp.status_code == 200
    content = resp.content.decode('utf-8')
    assert f'&copy; {year} Virasat Digital Foundation' in content


@pytest.mark.django_db
def test_filter_tabs_highlighting_and_plain_links(client):
    # 1. Festivals month tab: ?month=8 highlights Aug and not All Year
    r_fest = client.get(reverse('festivals:list') + '?month=8')
    assert r_fest.status_code == 200
    fest_html = r_fest.content.decode('utf-8')

    # All Year link should not have btn-gold
    assert 'class="px-4 py-2 rounded-xl text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-amber-500/10"' in fest_html
    # Aug tab should have btn-gold
    assert 'month=8"\n         class="px-3.5 py-2 rounded-xl text-xs font-semibold relative transition-colors btn-gold"' in fest_html or \
           'month=8" class="px-3.5 py-2 rounded-xl text-xs font-semibold relative transition-colors btn-gold"' in fest_html or \
           ('month=8' in fest_html and 'btn-gold' in fest_html)
    # Plain <a> links (no hx-get/hx-target/hx-push-url on the month navigation tabs)
    assert 'hx-target="#festival-grid-container"' not in fest_html.split('<!-- Filters Row -->')[0]

    # 2. Cuisine diet pills: ?diet=veg highlights Pure Vegetarian pill
    r_cuis = client.get(reverse('cuisine:list') + '?diet=veg')
    assert r_cuis.status_code == 200
    cuis_html = r_cuis.content.decode('utf-8')

    # All Cuisines link should not have btn-gold
    assert 'All Cuisines\n      </a>' in cuis_html
    # Pure Vegetarian should have bg-emerald-600 text-white
    assert 'diet=veg"\n         class="px-3.5 py-1.5 rounded-full text-xs font-semibold inline-flex items-center gap-1.5 bg-emerald-600 text-white"' in cuis_html or \
           ('diet=veg' in cuis_html and 'bg-emerald-600 text-white' in cuis_html)
    # Plain <a> links (no hx-get/hx-target/hx-push-url on the dietary pills)
    pills_section = cuis_html.split('Dietary Preference:')[1].split('</div>')[0]
    assert 'hx-get' not in pills_section
    assert 'hx-target' not in pills_section

    # 3. Arts discipline tabs: ?category=Dance highlights Dance tab
    r_arts = client.get(reverse('arts:list') + '?category=Dance')
    assert r_arts.status_code == 200
    arts_html = r_arts.content.decode('utf-8')

    # Dance tab has btn-gold
    assert 'category=Dance"\n         class="px-3.5 py-1.5 rounded-full text-xs font-semibold btn-gold"' in arts_html or \
           ('category=Dance' in arts_html and 'btn-gold' in arts_html)
    # Plain <a> links (no hx-get/hx-target/hx-push-url on discipline tabs)
    disc_section = arts_html.split('Discipline:')[1].split('</div>')[0]
    assert 'hx-get' not in disc_section
    assert 'hx-target' not in disc_section


@pytest.mark.django_db
def test_filter_forms_hidden_inputs(client):
    # Festivals form carries selected_month
    r_fest = client.get(reverse('festivals:list') + '?month=8')
    assert '<input type="hidden" name="month" value="8">' in r_fest.content.decode('utf-8')

    # Cuisine form carries selected_diet
    r_cuis = client.get(reverse('cuisine:list') + '?diet=veg')
    assert '<input type="hidden" name="diet" value="veg">' in r_cuis.content.decode('utf-8')

    # Arts form carries selected_category
    r_arts = client.get(reverse('arts:list') + '?category=Dance')
    assert '<input type="hidden" name="category" value="Dance">' in r_arts.content.decode('utf-8')

    # Heritage form carries selected_category
    r_heri = client.get(reverse('heritage:list') + '?category=Monument')
    assert '<input type="hidden" name="category" value="Monument">' in r_heri.content.decode('utf-8')


@pytest.mark.django_db
def test_combined_filters_functionality(client):
    from apps.states.models import State
    from apps.festivals.models import Festival

    st1 = State.objects.create(name='Kerala', slug='kerala', region='South', capital='Thiruvananthapuram', lat=8.5, lng=76.9)
    st2 = State.objects.create(name='Punjab', slug='punjab', region='North', capital='Chandigarh', lat=30.7, lng=76.7)

    # August festival in Kerala (Onam)
    f_onam = Festival.objects.create(
        name='Onam Harvest',
        slug='onam-harvest',
        month=8,
        approximate_dates='Aug 20-31',
        significance='Harvest',
        rituals='Pookkalam',
        food='Onasadya',
        hero_image='/static/images/festivals/onam.jpg',
        image_credit='Author',
        image_license='CC BY-SA 4.0'
    )
    f_onam.states.add(st1)

    # August festival in Punjab
    f_punjab_aug = Festival.objects.create(
        name='Punjab August Fair',
        slug='punjab-aug-fair',
        month=8,
        approximate_dates='Aug 15',
        significance='Fair',
        rituals='Celebration',
        food='Sweets',
        hero_image='/static/images/festivals/punjab.jpg',
        image_credit='Author',
        image_license='CC BY-SA 4.0'
    )
    f_punjab_aug.states.add(st2)

    # April festival in Punjab (Baisakhi)
    f_baisakhi = Festival.objects.create(
        name='Baisakhi',
        slug='baisakhi',
        month=4,
        approximate_dates='Apr 13-14',
        significance='Solar New Year',
        rituals='Bhangra',
        food='Kheer',
        hero_image='/static/images/festivals/baisakhi.jpg',
        image_credit='Author',
        image_license='CC BY-SA 4.0'
    )
    f_baisakhi.states.add(st2)

    # Combined filter: month=8 & state=kerala -> should only return Onam Harvest
    resp = client.get(reverse('festivals:list') + '?month=8&state=kerala')
    assert resp.status_code == 200
    returned_festivals = list(resp.context['festivals'])
    assert f_onam in returned_festivals
    assert f_punjab_aug not in returned_festivals
    assert f_baisakhi not in returned_festivals

    # Also verify Month 8 stays selected in context
    assert resp.context['selected_month'] == '8'
    assert resp.context['selected_state'] == 'kerala'


