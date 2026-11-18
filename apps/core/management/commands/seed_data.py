from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from apps.states.models import State
from apps.heritage.models import HeritageSite, HeritageSiteImage
from apps.festivals.models import Festival
from apps.arts.models import ArtForm
from apps.cuisine.models import CuisineDish
from apps.core.models import TimelineEvent
from apps.quiz.models import QuizQuestion, QuizScore
from apps.stories.models import Story
from apps.accounts.models import Bookmark, UserProfile
from django.contrib.contenttypes.models import ContentType


IMAGE_METADATA = {
    "heritage": {
        "ajanta-caves": {
            "category": "heritage",
            "slug": "ajanta-caves",
            "filename": "/static/images/heritage/ajanta-caves.jpg",
            "file_path": "static\\images\\heritage\\ajanta-caves.jpg",
            "title": "File:Ajanta Buddha Temptation Cave 26.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAjanta_Buddha_Temptation_Cave_26.jpg",
            "author": "Shishirdasika",
            "license": "CC BY-SA 4.0",
            "description": "Temptation of the Buddha; the daughters of Mara carved below are trying to seduce him. Mara is on the top right.",
            "width": 1200,
            "height": 1801,
            "hash": "92d097cfe0038e6a6ee0b8110d6cfc7bf81c0aa67e3243b2041be7d2650c3f12"
        },
        "amber-palace-and-fort": {
            "category": "heritage",
            "slug": "amber-palace-and-fort",
            "filename": "/static/images/heritage/amber-palace-and-fort.jpg",
            "file_path": "static\\images\\heritage\\amber-palace-and-fort.jpg",
            "title": "File:Amber Fort, Jaipur, 20191219 1030 9556.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAmber_Fort%2C_Jaipur%2C_20191219_1030_9556.jpg",
            "author": "Jakub Hałun",
            "license": "CC BY-SA 4.0",
            "description": "Sheesh Mahal (the Palace of Mirrors), Amber Fort in Jaipur",
            "width": 1200,
            "height": 1487,
            "hash": "698aa5ee39b4860293128bf2674ecb6363bb268cd55bd6d986357d467e135219"
        },
        "brihadisvara-temple-thanjavur": {
            "category": "heritage",
            "slug": "brihadisvara-temple-thanjavur",
            "filename": "/static/images/heritage/brihadisvara-temple-thanjavur.jpg",
            "file_path": "static\\images\\heritage\\brihadisvara-temple-thanjavur.jpg",
            "title": "File:Brihadisvara Temple during Maha Shivaratri-WUS03611 (edit).jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABrihadisvara_Temple_during_Maha_Shivaratri-WUS03611_%28edit%29.jpg",
            "author": "Original: Rainer Halama Derivative work: UnpetitproleX",
            "license": "CC BY-SA 4.0",
            "description": "Brihadisvara Temple during Maha Shivaratri",
            "width": 1200,
            "height": 749,
            "hash": "79fdbbe37b0c324832f91da90ca1b7907f84aa85646bce1364081fd2e3cdbe19"
        },
        "elephanta-caves": {
            "category": "heritage",
            "slug": "elephanta-caves",
            "filename": "/static/images/heritage/elephanta-caves.jpg",
            "file_path": "static\\images\\heritage\\elephanta-caves.jpg",
            "title": "File:Elephanta Caves Shiva.JPG",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AElephanta_Caves_Shiva.JPG",
            "author": "Sameer05",
            "license": "CC BY-SA 3.0",
            "description": "This is a photo of ASI monument number",
            "width": 1200,
            "height": 674,
            "hash": "a97838d770cd69d21aa1f7671ce52e27c2070da0f0540963df0b5a1d746f252b"
        },
        "ellora-caves-kailasa-temple": {
            "category": "heritage",
            "slug": "ellora-caves-kailasa-temple",
            "filename": "/static/images/heritage/ellora-caves-kailasa-temple.jpg",
            "file_path": "static\\images\\heritage\\ellora-caves-kailasa-temple.jpg",
            "title": "File:Courtyard and Mahabharata Reliefs at the Kailasa Temple, Ellora 01.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ACourtyard_and_Mahabharata_Reliefs_at_the_Kailasa_Temple%2C_Ellora_01.jpg",
            "author": "Rohit Sharma",
            "license": "CC BY-SA 4.0",
            "description": "The Kailasa Temple at Ellora (Cave 16) is a remarkable example of rock-cut architecture, commissioned in the 8th century by Rashtrakuta king Krishna I. Carved entirely out of a single basalt rock, the temple represents a monolithic excavation rather than constructed assembly, making it one of the la",
            "width": 1200,
            "height": 674,
            "hash": "f877e5973ec423b615315e3eea827c838070f7378bc7ac56e1f32d2ba51eef8d"
        },
        "fatehpur-sikri": {
            "category": "heritage",
            "slug": "fatehpur-sikri",
            "filename": "/static/images/heritage/fatehpur-sikri.jpg",
            "file_path": "static\\images\\heritage\\fatehpur-sikri.jpg",
            "title": "File:Buland Darwaza, Fatehpur Sikri, Agra.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABuland_Darwaza%2C_Fatehpur_Sikri%2C_Agra.jpg",
            "author": "Fastestfaraz1",
            "license": "CC BY-SA 4.0",
            "description": "Buland Darwaza, Fatehpur Sikri, Agra",
            "width": 1200,
            "height": 1184,
            "hash": "fdb01c4011a4b2e646e1c2552e37188896311061bcb38b9a17c6558be48551bb"
        },
        "golconda-fort": {
            "category": "heritage",
            "slug": "golconda-fort",
            "filename": "/static/images/heritage/golconda-fort.jpg",
            "file_path": "static/images/heritage/golconda-fort.jpg",
            "title": "File:Golconda Fort , Hyderabad.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File:Golconda_Fort_%2C_Hyderabad.jpg",
            "author": "Deep Patel",
            "license": "CC BY-SA 4.0",
            "width": 1200,
            "height": 1600,
            "hash": "cc1fd5c612b31ce596b948c0c7ac2e21eb2fe1abf230580357f6cf24d319adce"
        },
        "great-stupa-at-sanchi": {
            "category": "heritage",
            "slug": "great-stupa-at-sanchi",
            "filename": "/static/images/heritage/great-stupa-at-sanchi.jpg",
            "file_path": "static\\images\\heritage\\great-stupa-at-sanchi.jpg",
            "title": "File:East Torana, Sanchi 01.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AEast_Torana%2C_Sanchi_01.jpg",
            "author": "Bernard Gagnon",
            "license": "CC BY-SA 3.0",
            "description": "Carvings on the rear face of East Torana, Sanchi, India",
            "width": 1200,
            "height": 799,
            "hash": "45b0d2d97e0926e00f24f66883f90f4d6437df24e1ce4a8f05f3e6f083b7ac44"
        },
        "group-of-monuments-at-mahabalipuram": {
            "category": "heritage",
            "slug": "group-of-monuments-at-mahabalipuram",
            "filename": "/static/images/heritage/group-of-monuments-at-mahabalipuram.jpg",
            "file_path": "static\\images\\heritage\\group-of-monuments-at-mahabalipuram.jpg",
            "title": "File:Mamallapuram, Mahabalipuram, Shore Temple, India.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AMamallapuram%2C_Mahabalipuram%2C_Shore_Temple%2C_India.jpg",
            "author": "Vyacheslav Argenberg",
            "license": "CC BY 4.0",
            "description": "The Shore Temple (8th century AD) of the Pallava dynasty is within the group of monuments at Mahabalipuram on the shore of the Bay of Bengal. It is one of the oldest stone temples in South India. Mamallapuram, Mahabalipuram, Tamil Nadu, India.",
            "width": 1200,
            "height": 908,
            "hash": "122b387673d2f567095883ff10f497a4781c49dbb8c053f3027c9a4b7b8b2838"
        },
        "hampi-ruins-vijayanagara": {
            "category": "heritage",
            "slug": "hampi-ruins-vijayanagara",
            "filename": "/static/images/heritage/hampi-ruins-vijayanagara.jpg",
            "file_path": "static\\images\\heritage\\hampi-ruins-vijayanagara.jpg",
            "title": "File:Hampi, Vittala Temple, chariot (9881832023).jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AHampi%2C_Vittala_Temple%2C_chariot_%289881832023%29.jpg",
            "author": "Arian Zwegers from Brussels, Belgium",
            "license": "CC BY 2.0",
            "description": "Hampi, Vittala Temple, chariot See also www.flickr.com/photos/azwegers/6337304059/ Hampi is a village in northern Karnataka, India. It is located within the ruins of the city of Vijayanagara, the former capital of the Vijayanagara Empire. Predating the city of Vijayanagara, it continues to be an imp",
            "width": 1200,
            "height": 800,
            "hash": "2dd060897aba7fcb3dce648019f34bfadd7429f2242c94a01e3b474245e74890"
        },
        "jaisalmer-fort-sonar-qila": {
            "category": "heritage",
            "slug": "jaisalmer-fort-sonar-qila",
            "filename": "/static/images/heritage/jaisalmer-fort-sonar-qila.jpg",
            "file_path": "static\\images\\heritage\\jaisalmer-fort-sonar-qila.jpg",
            "title": "File:Bairisal Borj (Jaisalmer Fort), Jaisalmer, Jodhpur, Rajasthan, India (2012).jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABairisal_Borj_%28Jaisalmer_Fort%29%2C_Jaisalmer%2C_Jodhpur%2C_Rajasthan%2C_India_%282012%29.jpg",
            "author": "Fulvio Spada from Torino, Italy",
            "license": "CC BY-SA 2.0",
            "description": "Hierarchy – Bairisal Borj (tower) of Jaisalmer Fort",
            "width": 1200,
            "height": 1800,
            "hash": "7ba9141a80c258eb83261de9746e720589a77b9455a0f4b5d838b7d7a7e33b0e"
        },
        "kaziranga-national-park": {
            "category": "heritage",
            "slug": "kaziranga-national-park",
            "filename": "/static/images/heritage/kaziranga-national-park.jpg",
            "file_path": "static\\images\\heritage\\kaziranga-national-park.jpg",
            "title": "File:2 Rhino Rhinoceros in Kaziranga National Park Assam India.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A2_Rhino_Rhinoceros_in_Kaziranga_National_Park_Assam_India.jpg",
            "author": "Sankara Subramanian from Bangalore, India",
            "license": "CC BY 2.0",
            "description": "Rhinoceros near Brahmaputra river, Assam India",
            "width": 1200,
            "height": 800,
            "hash": "fab51fcf98ebc548ad3fcc63a19974374ee42649b823c96748be661c6481910e"
        },
        "khajuraho-group-of-monuments": {
            "category": "heritage",
            "slug": "khajuraho-group-of-monuments",
            "filename": "/static/images/heritage/khajuraho-group-of-monuments.jpg",
            "file_path": "static/images/heritage/khajuraho-group-of-monuments.jpg",
            "title": "File:A view from the southside of Kandariya temple 01.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AA_view_from_the_southside_of_Kandariya_temple_01.jpg",
            "author": "Ms Sarah Welch",
            "license": "CC BY-SA 4.0",
            "description": "",
            "width": 1200,
            "height": 909,
            "hash": "1b77fd7df3ed054d107ec0ae9ba3f685ce17029e3aa68f2ef8247f812675b802"
        },
        "konark-sun-temple": {
            "category": "heritage",
            "slug": "konark-sun-temple",
            "filename": "/static/images/heritage/konark-sun-temple.jpg",
            "file_path": "static\\images\\heritage\\konark-sun-temple.jpg",
            "title": "File:Chariot wheel, Konârak 01.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AChariot_wheel%2C_Kon%C3%A2rak_01.jpg",
            "author": "Bernard Gagnon",
            "license": "CC BY-SA 3.0",
            "description": "Chariot wheel of the Sun Temple, Konârak, India",
            "width": 1200,
            "height": 832,
            "hash": "85b666553ce5fc5d0c36fa5eaf76c5a6647c53aa3eaa2b8aef2fcd477d48f4a2"
        },
        "mahabodhi-temple-complex": {
            "category": "heritage",
            "slug": "mahabodhi-temple-complex",
            "filename": "/static/images/heritage/mahabodhi-temple-complex.jpg",
            "file_path": "static\\images\\heritage\\mahabodhi-temple-complex.jpg",
            "title": "File:Mahabodhitemple.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File:Mahabodhitemple.jpg",
            "author": "Bpilgrim",
            "license": "CC BY-SA 2.5",
            "description": "Mahabodhi Temple main tower at Bodh Gaya, Bihar",
            "width": 1200,
            "height": 1600,
            "hash": "0930f0188fd789b3455321d32f304da5f1499f1af072ed505558dbc7b4ca9d5e"
        },
        "meenakshi-amman-temple": {
            "category": "heritage",
            "slug": "meenakshi-amman-temple",
            "filename": "/static/images/heritage/meenakshi-amman-temple.jpg",
            "file_path": "static\\images\\heritage\\meenakshi-amman-temple.jpg",
            "title": "File:Golden Lily Pond and South Gopuram at Meenakshi Amman Temple , Madurai.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGolden_Lily_Pond_and_South_Gopuram_at_Meenakshi_Amman_Temple_%2C_Madurai.jpg",
            "author": "N. Vivekananthamoorthy",
            "license": "CC BY-SA 4.0",
            "description": "The Golden Lily Pond(called Potramarai in Tamil) is located inside the Meenakshi Amman Temple to the left of the corridor leading to the Shrine of Meenakshi Amman. One can view the imposing South Gopuram raising above the opposite temple corridor to the height of 170 feet. Originally, the walls surr",
            "width": 1200,
            "height": 1490,
            "hash": "669b99ca94cbd4af9009f8029dcec4ec6a9c578149d401e9241926a6e9e2963b"
        },
        "nalanda-mahavihara-ancient-university": {
            "category": "heritage",
            "slug": "nalanda-mahavihara-ancient-university",
            "filename": "/static/images/heritage/nalanda-mahavihara-ancient-university.jpg",
            "file_path": "static\\images\\heritage\\nalanda-mahavihara-ancient-university.jpg",
            "title": "File:Monastery 1 - Granary - Nalanda Mahavihara (1).jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AMonastery_1_-_Granary_-_Nalanda_Mahavihara_%281%29.jpg",
            "author": "Sumitsurai",
            "license": "CC BY-SA 4.0",
            "description": "Ruins of the ancient Nalanda University. The granary at Monastery 1.",
            "width": 1200,
            "height": 820,
            "hash": "df91a71916ad00212cf96495f87b1a0c831a4f259681a37845c6157b8f3c566d"
        },
        "qutub-minar-complex": {
            "category": "heritage",
            "slug": "qutub-minar-complex",
            "filename": "/static/images/heritage/qutub-minar-complex.jpg",
            "file_path": "static\\images\\heritage\\qutub-minar-complex.jpg",
            "title": "File:Qutb Minar 2011.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AQutb_Minar_2011.jpg",
            "author": "Sfu",
            "license": "CC BY-SA 4.0",
            "description": "Qutb Minar, Delhi, India",
            "width": 1200,
            "height": 4869,
            "hash": "4c956fefd43bedab199875d157781135b1a69c632398c52d379622f7a9239beb"
        },
        "rani-ki-vav-the-queens-stepwell": {
            "category": "heritage",
            "slug": "rani-ki-vav-the-queens-stepwell",
            "filename": "/static/images/heritage/rani-ki-vav-the-queens-stepwell.jpg",
            "file_path": "static\\images\\heritage\\rani-ki-vav-the-queens-stepwell.jpg",
            "title": "File:Rani ki vav - Patan - Gujarat - DSC001.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ARani_ki_vav_-_Patan_-_Gujarat_-_DSC001.jpg",
            "author": "Snehrashmi",
            "license": "CC BY-SA 4.0",
            "description": "This is a photo of ASI monument number",
            "width": 1200,
            "height": 800,
            "hash": "a7648d25e26dec6377cee126d4c9266879318e0a42b59d6da608208fb22b3740"
        },
        "red-fort-complex": {
            "category": "heritage",
            "slug": "red-fort-complex",
            "filename": "/static/images/heritage/red-fort-complex.jpg",
            "file_path": "static/images/heritage/red-fort-complex.jpg",
            "title": "File:Lahori Gate, Red Fort, Delhi, India - September 2014.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ALahori_Gate%2C_Red_Fort%2C_Delhi%2C_India_-_September_2014.jpg",
            "author": "Rickard Törnblad",
            "license": "CC BY-SA 4.0",
            "description": "",
            "width": 1200,
            "height": 675,
            "hash": "e1d52e0feef660a26e23e160a0bd977d070a4f645ec20ff3035e8e2285f16bf7"
        },
        "sundarbans-national-park": {
            "category": "heritage",
            "slug": "sundarbans-national-park",
            "filename": "/static/images/heritage/sundarbans-national-park.jpg",
            "file_path": "static\\images\\heritage\\sundarbans-national-park.jpg",
            "title": "File:Dense Mangrove Forest of the Sundarban Tiger Reserve during High Tide, West Bengal, India 02.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ADense_Mangrove_Forest_of_the_Sundarban_Tiger_Reserve_during_High_Tide%2C_West_Bengal%2C_India_02.jpg",
            "author": "Kingshuk Mondal",
            "license": "CC BY 4.0",
            "description": "Sundarbans National Park is a major national park, tiger reserve, and biosphere reserve located in West Bengal, India. It forms the core part of the vast Sundarbans on the Ganges Delta and is adjacent to the Sundarban Reserve Forest in Bangladesh. The delta is densely covered by mangrove forests and",
            "width": 1200,
            "height": 800,
            "hash": "d58f7754e292bf1ddef66976c1b1ac79265b1b5225fd025bf347c2ea587a56d6"
        },
        "taj-mahal": {
            "category": "heritage",
            "slug": "taj-mahal",
            "filename": "/static/images/heritage/taj-mahal.jpg",
            "file_path": "static\\images\\heritage\\taj-mahal.jpg",
            "title": "File:Aks The Reflection Taj Mahal.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAks_The_Reflection_Taj_Mahal.jpg",
            "author": "Antrix3",
            "license": "CC BY-SA 4.0",
            "description": "This is a photo of ASI monument number",
            "width": 1200,
            "height": 794,
            "hash": "ee3065ee28075da97df5fcff115ef33c23b41472f11dd423b4c787d9bbebc0ce"
        },
        "varanasi-ghats-sacred-waterfront": {
            "category": "heritage",
            "slug": "varanasi-ghats-sacred-waterfront",
            "filename": "/static/images/heritage/varanasi-ghats-sacred-waterfront.jpg",
            "file_path": "static\\images\\heritage\\varanasi-ghats-sacred-waterfront.jpg",
            "title": "File:Evening Ganga Aarti Assi Ghat, Varanasi 1.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AEvening_Ganga_Aarti_Assi_Ghat%2C_Varanasi_1.jpg",
            "author": "Rangan Datta Wiki",
            "license": "CC BY-SA 4.0",
            "description": "Evening Ganga Aarti Assi Ghat, Varanasi",
            "width": 1200,
            "height": 794,
            "hash": "40a1404bc43c8709939cbfa566ad496862132630175e9924a6850427172b7428"
        },
        "victoria-memorial": {
            "category": "heritage",
            "slug": "victoria-memorial",
            "filename": "/static/images/heritage/victoria-memorial.jpg",
            "file_path": "static\\images\\heritage\\victoria-memorial.jpg",
            "title": "File:Beautiful Victoria Memorial, Kolkata, India 01.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABeautiful_Victoria_Memorial%2C_Kolkata%2C_India_01.jpg",
            "author": "Ravi Dwivedi",
            "license": "CC BY-SA 4.0",
            "description": "The Victoria Memorial is a large marble building in Central Kolkata, which was built between 1906 and 1921. It is dedicated to the memory of Queen Victoria, now a museum under the auspices of the Ministry of Culture, and is the largest monument in the world which is dedicated to a royal. The memoria",
            "width": 1200,
            "height": 900,
            "hash": "b4fbb9a4e7b3dfe6602a00e9cbed4836acd70f8ae95b649fcc7c91ff31936316"
        },
        "western-ghats-mountain-chain": {
            "category": "heritage",
            "slug": "western-ghats-mountain-chain",
            "filename": "/static/images/heritage/western-ghats-mountain-chain.jpg",
            "file_path": "static\\images\\heritage\\western-ghats-mountain-chain.jpg",
            "title": "File:Sahyadri Range at Bhimashankar, Maharashtra, India.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File:Sahyadri_Range_at_Bhimashankar,_Maharashtra,_India.jpg",
            "author": "Rohit Sharma",
            "license": "CC BY-SA 4.0",
            "description": "Sahyadri Range (Western Ghats) at Bhimashankar, Maharashtra, India",
            "width": 1200,
            "height": 675,
            "hash": "a98194fda766f398fa0cfae7d7e36f08e943d5d865d26fbd5e68e0700cb49780"
        }
    },
    "festivals": {
        "kumbh-mela": {
            "category": "festivals",
            "slug": "kumbh-mela",
            "filename": "/static/images/festivals/kumbh-mela.jpg",
            "file_path": "static\\images\\festivals\\kumbh-mela.jpg",
            "title": "File:Crowd in maha kumbh mela.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ACrowd_in_maha_kumbh_mela.jpg",
            "author": "Mishra12krati",
            "license": "CC BY-SA 4.0",
            "description": "Crowd in maha kumbh mela 2025",
            "width": 1200,
            "height": 900,
            "hash": "8caf7b19c5b114ade1d66149bb4bdb6b598526a1b611a1346500d54b577c1218"
        },
        "pongal-makar-sankranti": {
            "category": "festivals",
            "slug": "pongal-makar-sankranti",
            "filename": "/static/images/festivals/pongal-makar-sankranti.jpg",
            "file_path": "static/images/festivals/pongal-makar-sankranti.jpg",
            "title": "File:Pongal celebration-2.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3APongal_celebration-2.jpg",
            "author": "Tamilmani Ranganathan",
            "license": "CC BY-SA 4.0",
            "description": "",
            "width": 1200,
            "height": 553,
            "hash": "f5ae8b8cfd745075642a022d181336878318f23b92e2a1423bf589d93df554f6"
        },
        "losar-tibetan-new-year": {
            "category": "festivals",
            "slug": "losar-tibetan-new-year",
            "filename": "/static/images/festivals/losar-tibetan-new-year.jpg",
            "file_path": "static/images/festivals/losar-tibetan-new-year.jpg",
            "title": "File:Buddhist monks dancing the Cham in the Himalayan monastery of Lamayuru.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABuddhist_monks_dancing_the_Cham_in_the_Himalayan_monastery_of_Lamayuru.jpg",
            "author": "Dr. Ondřej Havelka (cestovatel)",
            "license": "CC BY 4.0",
            "description": "",
            "width": 1200,
            "height": 597,
            "hash": "85afb21e18e14a8d678fb4f458db0af9529ab5c0da08c8c78b0ac75d72e701d9"
        },
        "holi-festival-of-colors": {
            "category": "festivals",
            "slug": "holi-festival-of-colors",
            "filename": "/static/images/festivals/holi-festival-of-colors.jpg",
            "file_path": "static\\images\\festivals\\holi-festival-of-colors.jpg",
            "title": "File:HOLI FESTIVAL img.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AHOLI_FESTIVAL_img.jpg",
            "author": "Shubhanshri01",
            "license": "CC BY-SA 4.0",
            "description": "Holi, the festival of colors, is a vibrant and joyous celebration observed by millions of people across India and around the world. Marking the arrival of spring, Holi is a time for people to come together, play with colors, and revel in the spirit of unity and joy. During Holi, streets and squares ",
            "width": 1200,
            "height": 2133,
            "hash": "082e84fa9038ce14147488c606ef80ede6e9b95a1e9dd2acfea1bdc3cbc6be43"
        },
        "baisakhi-vaisakhi": {
            "category": "festivals",
            "slug": "baisakhi-vaisakhi",
            "filename": "/static/images/festivals/baisakhi-vaisakhi.jpg",
            "file_path": "static/images/festivals/baisakhi-vaisakhi.jpg",
            "title": "File:Bhangra, The Lok Naach Of Punjab.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABhangra%2C_The_Lok_Naach_Of_Punjab.jpg",
            "author": "Siddharthjiii",
            "license": "CC BY-SA 4.0",
            "description": "",
            "width": 1200,
            "height": 1203,
            "hash": "c3bb8804cddd78c5c8e57e76cc9acd93c709a3e29a5e75a773cd96d60b0ad71a"
        },
        "eid-ul-fitr": {
            "category": "festivals",
            "slug": "eid-ul-fitr",
            "filename": "/static/images/festivals/eid-ul-fitr.jpg",
            "file_path": "static/images/festivals/eid-ul-fitr.jpg",
            "title": "File:Jama Masjid during Eid.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AJama_Masjid_during_Eid.jpg",
            "author": "Creatorations",
            "license": "CC BY-SA 4.0",
            "description": "",
            "width": 1200,
            "height": 674,
            "hash": "107aacd7447a66e3f3da840467e31681fcdbeefecb0dc7dafac6bee2f9cdc9b5"
        },
        "rongali-bihu": {
            "category": "festivals",
            "slug": "rongali-bihu",
            "filename": "/static/images/festivals/rongali-bihu.jpg",
            "file_path": "static\\images\\festivals\\rongali-bihu.jpg",
            "title": "File:Bihu Dance , Festival of India.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABihu_Dance_%2C_Festival_of_India.jpg",
            "author": "Donvikro",
            "license": "CC BY-SA 4.0",
            "description": "A traditional Husori or Huchori troupe performs in the courtyard of a household in Nagini Juri is a village located within the Borholla area of Jorhat district in Assam, during Rongali Bihu, the springtime Assamese New Year festival in Assam, India. Dressed in vibrant traditional attire—turban, dhot",
            "width": 1200,
            "height": 853,
            "hash": "6bffaef4b1239b373ebab7b474de4326be449916d03966859c780174972dcc45"
        },
        "thrissur-pooram": {
            "category": "festivals",
            "slug": "thrissur-pooram",
            "filename": "/static/images/festivals/thrissur-pooram.jpg",
            "file_path": "static\\images\\festivals\\thrissur-pooram.jpg",
            "title": "File:Aanas at Thrissur Pooram.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAanas_at_Thrissur_Pooram.jpg",
            "author": "Fenomenon123",
            "license": "CC0",
            "description": "Elephants at Thrissur Pooram",
            "width": 1200,
            "height": 900,
            "hash": "b555ca9db1f3711af69f6064fbf0cabc6a7d5446e640d321a72bc2ac635fcd39"
        },
        "puri-ratha-yatra-chariot-festival": {
            "category": "festivals",
            "slug": "puri-ratha-yatra-chariot-festival",
            "filename": "/static/images/festivals/puri-ratha-yatra-chariot-festival.jpg",
            "file_path": "static\\images\\festivals\\puri-ratha-yatra-chariot-festival.jpg",
            "title": "File:Gaja in front of 3 Ratha at Puri Ratha Jatra 2024.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGaja_in_front_of_3_Ratha_at_Puri_Ratha_Jatra_2024.jpg",
            "author": "Liman Chandrakar",
            "license": "CC BY-SA 4.0",
            "description": "Gaja in front of 3 Ratha at Puri Ratha Jatra 2024",
            "width": 1200,
            "height": 900,
            "hash": "7a957d1acfb824effeee4c82390df7ff532547ac6a1328ee6f8961e59a0d3094"
        },
        "hemis-festival": {
            "category": "festivals",
            "slug": "hemis-festival",
            "filename": "/static/images/festivals/hemis-festival.jpg",
            "file_path": "static\\images\\festivals\\hemis-festival.jpg",
            "title": "File:Reverie - Sarang Deshpande.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File:Reverie_-_Sarang_Deshpande.jpg",
            "author": "Sarang Deshpande",
            "license": "CC BY-SA 4.0",
            "description": "Masked lamas performing sacred Cham dance at Hemis Monastery during Hemis Festival",
            "width": 1200,
            "height": 900,
            "hash": "bdf037e346b101070ca3799fb2103d19fde0d75accd36b6fd1191c693c73b4f8"
        },
        "onam-harvest-festival": {
            "category": "festivals",
            "slug": "onam-harvest-festival",
            "filename": "/static/images/festivals/onam-harvest-festival.jpg",
            "file_path": "static\\images\\festivals\\onam-harvest-festival.jpg",
            "title": "File:Onam Pookkalam 09900.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AOnam_Pookkalam_09900.jpg",
            "author": "Sugeesh",
            "license": "CC BY-SA 4.0",
            "description": "Onam Pookkalam from Pattom Palace Post office",
            "width": 1200,
            "height": 540,
            "hash": "b4f246c564860ef6b0a5ef890748fbcf679c25ef9893a48fb309fdd5bcb1d51e"
        },
        "ganesh-chaturthi": {
            "category": "festivals",
            "slug": "ganesh-chaturthi",
            "filename": "/static/images/festivals/ganesh-chaturthi.jpg",
            "file_path": "static\\images\\festivals\\ganesh-chaturthi.jpg",
            "title": "File:Ganesh Chaturthi 2021.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGanesh_Chaturthi_2021.jpg",
            "author": "TheMacGuy2005",
            "license": "CC BY-SA 4.0",
            "description": "Ganesh Chaturthi Lalbaugh Ganesha.jpg Lalbaugcha Raja, Mumbai Official name Chatur/Vinayaka Chaturthi/Vinayaka Chavithi Also called Chavithi, Chouthi, Ganeshotsav Observed by Hindus Type Religious Celebrations Chanting of Vedic hymns and Hindu texts, prayers, last day: processions, idol immersion Be",
            "width": 1200,
            "height": 900,
            "hash": "cd854efbfd04e13bc039b215adf784a91922b737ba15151791e46a1f0850cf2a"
        },
        "diwali-deepavali": {
            "category": "festivals",
            "slug": "diwali-deepavali",
            "filename": "/static/images/festivals/diwali-deepavali.jpg",
            "file_path": "static\\images\\festivals\\diwali-deepavali.jpg",
            "title": "File:A Burning Diya.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AA_Burning_Diya.jpg",
            "author": "Lalturadipur",
            "license": "CC BY-SA 4.0",
            "description": "Diya is a traditional lamp used by Indians in several festivals especially the Diwali. In addition, it's burnt every night and morning following some traditions. A cotton rope is dipped into a clay made little bowl of vegitable oil. The oily rope is fired and it burns with deem light.",
            "width": 1200,
            "height": 675,
            "hash": "6204fefc387ba4695044b4225732f10aa90288ac2b095f6593398149a2ee2056"
        },
        "durga-puja-sharadotsav": {
            "category": "festivals",
            "slug": "durga-puja-sharadotsav",
            "filename": "/static/images/festivals/durga-puja-sharadotsav.jpg",
            "file_path": "static\\images\\festivals\\durga-puja-sharadotsav.jpg",
            "title": "File:5438g sreebhumi-bhavanipur pratima.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A5438g_sreebhumi-bhavanipur_pratima.jpg",
            "author": "Mukerjee",
            "license": "CC BY-SA 3.0",
            "description": "Durga Puja idol at Shreebhumi, adjacent to Lake Town / VIP Road, North East Kolkata.",
            "width": 1200,
            "height": 622,
            "hash": "ad599f89103c3868935f573cac3a3ac4de66ff1df10de65bd9f744dd30e88957"
        },
        "mysore-dasara": {
            "category": "festivals",
            "slug": "mysore-dasara",
            "filename": "/static/images/festivals/mysore-dasara.jpg",
            "file_path": "static\\images\\festivals\\mysore-dasara.jpg",
            "title": "File:Amba Vilas palace.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAmba_Vilas_palace.jpg",
            "author": "Darakshanehaluddin",
            "license": "CC0",
            "description": "Amba Vilas palace",
            "width": 1200,
            "height": 1600,
            "hash": "0b8c23a1930790649d381304f6fb510da8a57790518ab9904937399bb77ba7f2"
        },
        "navratri-garba": {
            "category": "festivals",
            "slug": "navratri-garba",
            "filename": "/static/images/festivals/navratri-garba.jpg",
            "file_path": "static\\images\\festivals\\navratri-garba.jpg",
            "title": "File:Garba Navratri 01.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGarba_Navratri_01.jpg",
            "author": "PARMAR BHARGAV SURESHBHAI",
            "license": "CC BY-SA 4.0",
            "description": "Garba, Navratri 2022, GMDC ground, Ahmedabad, Gujarat, India.",
            "width": 1200,
            "height": 675,
            "hash": "4fa7bc63d58a83c676439a3c063c05f647d6472bd6ee0bcdcce599ed9cd4d057"
        },
        "chhath-puja": {
            "category": "festivals",
            "slug": "chhath-puja",
            "filename": "/static/images/festivals/chhath-puja.jpg",
            "file_path": "static\\images\\festivals\\chhath-puja.jpg",
            "title": "File:Abishek Shrestha 20181114 D5A4723-2.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAbishek_Shrestha_20181114_D5A4723-2.jpg",
            "author": "Abishek Photographer",
            "license": "CC BY-SA 4.0",
            "description": "Chhath in Janakpur.Chhath is an ancient Hindu Vedic festival celebrated in the Indian states of Bihar, Jharkhand, and Uttar Pradesh and many places of Nepal.The Chhath Puja is dedicated to the Sun in order to thank them for bestowing the bounties of life on earth and to request the granting of certa",
            "width": 1200,
            "height": 800,
            "hash": "3ff0fe8c0b50c410a1263fea8d59a0a3687ecf91c6bd4f487d5e1280b5fc26ce"
        },
        "pushkar-camel-fair": {
            "category": "festivals",
            "slug": "pushkar-camel-fair",
            "filename": "/static/images/festivals/pushkar-camel-fair.jpg",
            "file_path": "static\\images\\festivals\\pushkar-camel-fair.jpg",
            "title": "File:'PUSHKAR CAMEL AND CATTLE FAIR -2003'.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A%27PUSHKAR_CAMEL_AND_CATTLE_FAIR_-2003%27.jpg",
            "author": "Rudolph.A.furtado",
            "license": "Public domain",
            "description": "The \"Pushkar Camel and cattle Fair - 2003\" as viewed from a Sand Dune.",
            "width": 1200,
            "height": 838,
            "hash": "ad26718c68c52a9b32646ed61b6a7d65214969a1d8e9dce08a8e3f6435b7beee"
        },
        "hornbill-festival": {
            "category": "festivals",
            "slug": "hornbill-festival",
            "filename": "/static/images/festivals/hornbill-festival.jpg",
            "file_path": "static\\images\\festivals\\hornbill-festival.jpg",
            "title": "File:Hornbill Festival,2024.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AHornbill_Festival%2C2024.jpg",
            "author": "পাপৰি বৰা",
            "license": "CC BY-SA 4.0",
            "description": "Hornbill Festival,2024",
            "width": 1200,
            "height": 1599,
            "hash": "d06c9800b9af821bfd55eb150667f8fe9a733a87f7fcb8a93278b150a9f8bc4d"
        },
        "rann-utsav-white-desert-festival": {
            "category": "festivals",
            "slug": "rann-utsav-white-desert-festival",
            "filename": "/static/images/festivals/rann-utsav-white-desert-festival.jpg",
            "file_path": "static\\images\\festivals\\rann-utsav-white-desert-festival.jpg",
            "title": "File:Rann utsav 01.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File:Rann_utsav_01.jpg",
            "author": "Mekshaa",
            "license": "CC BY-SA 4.0",
            "description": "Sunset over the White Desert of Kutch during Rann Utsav festival",
            "width": 1200,
            "height": 675,
            "hash": "132ec95545628894839cfd39bfe6f1b55756bc5804b0769ae6088d439e35cbe9"
        }
    },
    "arts": {
        "channapatna-wooden-toys": {
            "category": "arts",
            "slug": "channapatna-wooden-toys",
            "filename": "/static/images/arts/channapatna-wooden-toys.jpg",
            "file_path": "static\\images\\arts\\channapatna-wooden-toys.jpg",
            "title": "File:Channapatna-toys.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AChannapatna-toys.jpg",
            "author": "HPNadig",
            "license": "CC BY-SA 3.0",
            "description": "Channapatna Toys or Chennapatna Toys.",
            "width": 1200,
            "height": 1792,
            "hash": "bbc660f5fa88b24485c797a4af28910187067522ba4a20822792a1e087bf38e7"
        },
        "dhokra-bell-metal-casting": {
            "category": "arts",
            "slug": "dhokra-bell-metal-casting",
            "filename": "/static/images/arts/dhokra-bell-metal-casting.jpg",
            "file_path": "static\\images\\arts\\dhokra-bell-metal-casting.jpg",
            "title": "File:A Dhokra cast being made by a Dharua tribal woman.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AA_Dhokra_cast_being_made_by_a_Dharua_tribal_woman.jpg",
            "author": "Government of Odisha",
            "license": "CC BY 4.0",
            "description": "A Dhokra cast being made by a Dharua tribal woman , Odisha.",
            "width": 1200,
            "height": 800,
            "hash": "9b7f34177aabf8979f103e8d8e0cf8320c8eb09001ce0ba57142554e66825444"
        },
        "jaipur-blue-pottery": {
            "category": "arts",
            "slug": "jaipur-blue-pottery",
            "filename": "/static/images/arts/jaipur-blue-pottery.jpg",
            "file_path": "static\\images\\arts\\jaipur-blue-pottery.jpg",
            "title": "File:Blue Pottery, Albert Hall Museum, Jaipur.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABlue_Pottery%2C_Albert_Hall_Museum%2C_Jaipur.jpg",
            "author": "Neek-Theri",
            "license": "CC BY-SA 4.0",
            "description": "Blue Pottery, Albert Hall Musuem, Jaipur",
            "width": 1200,
            "height": 2403,
            "hash": "23a004daaebb0814fbb574586263d7305f855e5b5b3a1cf2dace6589a08238d2"
        },
        "bharatanatyam": {
            "category": "arts",
            "slug": "bharatanatyam",
            "filename": "/static/images/arts/bharatanatyam.jpg",
            "file_path": "static\\images\\arts\\bharatanatyam.jpg",
            "title": "File:Bharathanatyam by Dr. Janaki Rangarajan (51).jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABharathanatyam_by_Dr._Janaki_Rangarajan_%2851%29.jpg",
            "author": "Shagil Kannur",
            "license": "CC BY-SA 4.0",
            "description": "Bharatanatyam is a classical Indian dance form originating from Tamil Nadu, with a history spanning over 2,000 years. Rooted in the ancient Sanskrit text Natya Shastra, it was traditionally performed in Hindu temples by Devadasis (temple dancers) as a sacred art dedicated to deities. The dance combi",
            "width": 1200,
            "height": 1763,
            "hash": "e6af6755deee07b9aa25d90f396b835726bf1083f58b70f45cd481cca5b9525d"
        },
        "kathak": {
            "category": "arts",
            "slug": "kathak",
            "filename": "/static/images/arts/kathak.jpg",
            "file_path": "static\\images\\arts\\kathak.jpg",
            "title": "File:Hari The Kathak King.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AHari_The_Kathak_King.jpg",
            "author": "Hari The Kathak King",
            "license": "CC0",
            "description": "Kathak Dancer in Bangalore",
            "width": 1200,
            "height": 1681,
            "hash": "32e7fcba49b482e7f607fa6f05122b892391c06c6445d24dae495c66abd62630"
        },
        "kathakali": {
            "category": "arts",
            "slug": "kathakali",
            "filename": "/static/images/arts/kathakali.jpg",
            "file_path": "static\\images\\arts\\kathakali.jpg",
            "title": "File:'Kathakali'-The cultural soul of Kerala.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A%27Kathakali%27-The_cultural_soul_of_Kerala.jpg",
            "author": "WonderFrames",
            "license": "CC BY-SA 4.0",
            "description": "Kathakali is a classical dance drama of Kerala. It is regarded as a sacred dance form often performed during temple festivals in Kerala. The dance represents the fight between the good and evil. 'Katha' means 'story/traditional tale' and 'Kali' means 'play/performance'. The artists wear vivid and ex",
            "width": 1200,
            "height": 900,
            "hash": "455e0df4d3e2c1fcbf031ae9e542bdf1c9557d82a732fb880fce7a34adc0ce80"
        },
        "manipuri-raas-leela": {
            "category": "arts",
            "slug": "manipuri-raas-leela",
            "filename": "/static/images/arts/manipuri-raas-leela.jpg",
            "file_path": "static/images/arts/manipuri-raas-leela.jpg",
            "title": "File:Manippuri dance of India by Shagil Kannur 2.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AManippuri_dance_of_India_by_Shagil_Kannur_2.jpg",
            "author": "Shagil Kannur",
            "license": "CC BY-SA 4.0",
            "description": "",
            "width": 1200,
            "height": 1800,
            "hash": "f03c3c2dc64db3d6250d0aebffdb8154b88d2306349139bdeeac84baab983c5f"
        },
        "odissi": {
            "category": "arts",
            "slug": "odissi",
            "filename": "/static/images/arts/odissi.jpg",
            "file_path": "static\\images\\arts\\odissi.jpg",
            "title": "File:Baisali Mohanty 3.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABaisali_Mohanty_3.jpg",
            "author": "Oocoxford",
            "license": "CC BY-SA 4.0",
            "description": "Baisali Mohanty &amp; Troupe performing at 16th International Beach Festival on November 24, 2010.",
            "width": 1200,
            "height": 803,
            "hash": "4b12ceccdbff5544648e9c271b83ce2c0b74537135c6d3dae6a60ef354d58b1f"
        },
        "carnatic-classical-music": {
            "category": "arts",
            "slug": "carnatic-classical-music",
            "filename": "/static/images/arts/carnatic-classical-music.jpg",
            "file_path": "static\\images\\arts\\carnatic-classical-music.jpg",
            "title": "File:Akkarai S Sornalatha.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAkkarai_S_Sornalatha.jpg",
            "author": "Kannan Shanmugam, Shanmugam Studio, Kollam",
            "license": "CC BY-SA 4.0",
            "description": "Akkarai S Sornalatha is a prodigious Indian classical (Carnatic) violinist and vocalist whose soulful music has captivated the hearts of music lovers worldwide.",
            "width": 1200,
            "height": 800,
            "hash": "a20a46826b0c844daf883ec18260dbad8bd0ee2dd1232b53834ecb056ae25e02"
        },
        "hindustani-classical-music": {
            "category": "arts",
            "slug": "hindustani-classical-music",
            "filename": "/static/images/arts/hindustani-classical-music.jpg",
            "file_path": "static\\images\\arts\\hindustani-classical-music.jpg",
            "title": "File:Photoshoot with Rishab Rikhiram Sharma 01.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3APhotoshoot_with_Rishab_Rikhiram_Sharma_01.jpg",
            "author": "Radhika Lal",
            "license": "CC BY-SA 4.0",
            "description": "Got an opportunity to do a photoshoot for Rishab Rikhiram Sharma, the youngest disciple of Pt. Ravi Shankar. He has appeared on various TV shows such as “entertainment ke liye kuch bhi karega”, “Hindustan Ke Hunarbaaz” and more. He was also a soloist and performed in front of 60,000 at the NRG stadi",
            "width": 1200,
            "height": 800,
            "hash": "83a0dde24b246f8834134655b7aa39efd3bdbe556a83875f888ceaafd8915e3d"
        },
        "madhubani-mithila-painting": {
            "category": "arts",
            "slug": "madhubani-mithila-painting",
            "filename": "/static/images/arts/madhubani-mithila-painting.jpg",
            "file_path": "static\\images\\arts\\madhubani-mithila-painting.jpg",
            "title": "File:Madhubani folk art (modern representation).jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AMadhubani_folk_art_%28modern_representation%29.jpg",
            "author": "Theshruview",
            "license": "CC BY-SA 4.0",
            "description": "This is a modern representation of Madhubani art which originates in Mithila, Bihar (India). While traditional Madhubani art is done using natural dyes, this is done using synthetic colours. This particular painting uses commonly used Madhubani art forms and patterns.",
            "width": 1200,
            "height": 1664,
            "hash": "de8cb13084ff51b596b2aa9c1967dbfe971865e3a073585e048fbbc7b981d45a"
        },
        "pattachitra-scroll-painting": {
            "category": "arts",
            "slug": "pattachitra-scroll-painting",
            "filename": "/static/images/arts/pattachitra-scroll-painting.jpg",
            "file_path": "static\\images\\arts\\pattachitra-scroll-painting.jpg",
            "title": "File:Pattachitra Painting (16419912954).jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3APattachitra_Painting_%2816419912954%29.jpg",
            "author": "Mike Prince from Bangalore, India",
            "license": "CC BY 2.0",
            "description": "Pattachitra Painting",
            "width": 1200,
            "height": 900,
            "hash": "a6a442d75f214b73be901535eac7fb374f53dda65fab86674dd4c0c1e4b6be7d"
        },
        "tanjore-gold-foil-painting": {
            "category": "arts",
            "slug": "tanjore-gold-foil-painting",
            "filename": "/static/images/arts/tanjore-gold-foil-painting.jpg",
            "file_path": "static\\images\\arts\\tanjore-gold-foil-painting.jpg",
            "title": "File:Gajalakshmi in Tanjore Painting.png",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGajalakshmi_in_Tanjore_Painting.png",
            "author": "Archana Devarkonda",
            "license": "FAL",
            "description": "Goddess Gajalakshmi in Tanjore Painting",
            "width": 1200,
            "height": 1520,
            "hash": "e0ede13abadedf1978fac048baccb25c3a17223cd7a0deec3b106b29d7d9634f"
        },
        "warli-tribal-art": {
            "category": "arts",
            "slug": "warli-tribal-art",
            "filename": "/static/images/arts/warli-tribal-art.jpg",
            "file_path": "static/images/arts/warli-tribal-art.jpg",
            "title": "File:Warli art form.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AWarli_art_form.jpg",
            "author": "Sahakol41",
            "license": "CC0",
            "description": "",
            "width": 1200,
            "height": 795,
            "hash": "3d79e111fdabd0ffa52c86b0f24564af933d6cc331c6b0693c236d84e6cb5299"
        },
        "bandhani-tie-dye": {
            "category": "arts",
            "slug": "bandhani-tie-dye",
            "filename": "/static/images/arts/bandhani-tie-dye.jpg",
            "file_path": "static\\images\\arts\\bandhani-tie-dye.jpg",
            "title": "File:Bandhani, Tie dye dresses drying in Jaipur.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABandhani%2C_Tie_dye_dresses_drying_in_Jaipur.jpg",
            "author": "Jon Connell from Cambridge, UK",
            "license": "CC BY 2.0",
            "description": "Tie dye dresses drying",
            "width": 1200,
            "height": 799,
            "hash": "722b970018e4f97c69f1a1a90474435bc7ae527e644714c43cd2041e238c243c"
        },
        "kalamkari-textile-art": {
            "category": "arts",
            "slug": "kalamkari-textile-art",
            "filename": "/static/images/arts/kalamkari-textile-art.jpg",
            "file_path": "static\\images\\arts\\kalamkari-textile-art.jpg",
            "title": "File:Dashavatara de kalamkari, British Museum.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ADashavatara_de_kalamkari%2C_British_Museum.jpg",
            "author": "Jl FilpoC",
            "license": "CC BY-SA 4.0",
            "description": "Tapiz de los diez avatares de Vishnu, con Ganesha y un lingam de Shiva, empleando kalamkari (ca. 1870-1930).",
            "width": 1200,
            "height": 1205,
            "hash": "9d42055ebd74dbb106f9194a0c20559a0e05c5aed53606f2514a0ee0eaa3422c"
        },
        "pashmina-kani-shawl-weaving": {
            "category": "arts",
            "slug": "pashmina-kani-shawl-weaving",
            "filename": "/static/images/arts/pashmina-kani-shawl-weaving.jpg",
            "file_path": "static\\images\\arts\\pashmina-kani-shawl-weaving.jpg",
            "title": "File:Embroidered-pashmina-shawl.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AEmbroidered-pashmina-shawl.jpg",
            "author": "AG",
            "license": "CC BY-SA 4.0",
            "description": "kashmiri pashmina embroidered by hand",
            "width": 1200,
            "height": 900,
            "hash": "a8fc403c8a1ea80c09cf7e9d742d07c289f991dc12dcbd01ae6c67c3a344ae54"
        },
        "phulkari-embroidery": {
            "category": "arts",
            "slug": "phulkari-embroidery",
            "filename": "/static/images/arts/phulkari-embroidery.jpg",
            "file_path": "static\\images\\arts\\phulkari-embroidery.jpg",
            "title": "File:Phulkari from Punjab, India, 20th century, khadi, silk, plain weave, embroidery, Honolulu Museum of Art.JPG",
            "source_url": "https://commons.wikimedia.org/wiki/File:Phulkari_from_Punjab,_India,_20th_century,_khadi,_silk,_plain_weave,_embroidery,_Honolulu_Museum_of_Art.JPG",
            "author": "Honolulu Museum of Art",
            "license": "CC0",
            "description": "Traditional colourful Punjabi Phulkari silk embroidery on khadi",
            "width": 1200,
            "height": 2319,
            "hash": "4f39ebe20b918083ea058d3c11010a904c797948ca41db9ebd582b3cbced3f3f"
        },
        "koodiyattam-sanskrit-theatre": {
            "category": "arts",
            "slug": "koodiyattam-sanskrit-theatre",
            "filename": "/static/images/arts/koodiyattam-sanskrit-theatre.jpg",
            "file_path": "static\\images\\arts\\koodiyattam-sanskrit-theatre.jpg",
            "title": "File:A Kutiyattam scene performed at Irinjalakuda Thrissur district Kerala.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AA_Kutiyattam_scene_performed_at_Irinjalakuda_Thrissur_district_Kerala.jpg",
            "author": "tomislav medak",
            "license": "CC BY-SA 2.0",
            "description": "Kutiyattam, also spelled koodiyattam, is one of several forms of historic Hindu temple theatre found in Kerala and Tamil Nadu. It is a group performance by two or more actors. The theme is classical dance or drama performance, aided by musicians. The stories are from Hindu epics and Vedic legends, w",
            "width": 1200,
            "height": 899,
            "hash": "f3509175233e364699bf6173b44df58a4299802cfc0b48212f598ec425af22f5"
        },
        "yakshagana": {
            "category": "arts",
            "slug": "yakshagana",
            "filename": "/static/images/arts/yakshagana.jpg",
            "file_path": "static\\images\\arts\\yakshagana.jpg",
            "title": "File:Artist busy in make up for Dashavatara folk theatre.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AArtist_busy_in_make_up_for_Dashavatara_folk_theatre.jpg",
            "author": "वर्षा देशपांडे",
            "license": "CC BY-SA 4.0",
            "description": "Artist busy in make up for Dashavatara folk theatre in Konkan region of Maharashtra state in India. Dashavatara folk theatre originated in the region around 16th century having roots in Yakshagana folk theatre from Karnataka state of India.",
            "width": 1200,
            "height": 800,
            "hash": "80a6cdea24718e218dbfcc5032cb4fbfbe404e3c0f94e4ca729676a1a3fc6dc1"
        }
    },
    "cuisine": {
        "bihari-litti-chokha": {
            "category": "cuisine",
            "slug": "bihari-litti-chokha",
            "filename": "/static/images/cuisine/bihari-litti-chokha.jpg",
            "file_path": "static\\images\\cuisine\\bihari-litti-chokha.jpg",
            "title": "File:Litti-chokha.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ALitti-chokha.jpg",
            "author": "HrichikHv",
            "license": "CC BY-SA 4.0",
            "description": "This delicacy of Bihar is called 'litti-chokha'. Generally it is eaten in the winter season because the spices used in delicacy keeps the body warm. Litti is made up of wheat flour, 'sattu' (baked gram flour) and various spices. Chokha is nothing but admixture of boiled potato and tomato mashed toge",
            "width": 1200,
            "height": 803,
            "hash": "97bfc30a6a49f40b912265c885bc0ff9ba8cdc000688618b65ead486b64e8d11"
        },
        "old-delhi-daulat-ki-chaat": {
            "category": "cuisine",
            "slug": "old-delhi-daulat-ki-chaat",
            "filename": "/static/images/cuisine/old-delhi-daulat-ki-chaat.jpg",
            "file_path": "static\\images\\cuisine\\old-delhi-daulat-ki-chaat.jpg",
            "title": "File:Daulat Ki chat.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ADaulat_Ki_chat.jpg",
            "author": "Ravi Dwivedi",
            "license": "CC BY-SA 4.0",
            "description": "This is Daulat ki chat, a dish in Chandni Chowk, Delhi. It is prepared using milk, malai, khoya and sugar.",
            "width": 1200,
            "height": 900,
            "hash": "a535711ccea1063c6f55cffc271d5899d4687aeff496e60b2a23a3418278d160"
        },
        "goan-bebinca-cake": {
            "category": "cuisine",
            "slug": "goan-bebinca-cake",
            "filename": "/static/images/cuisine/goan-bebinca-cake.jpg",
            "file_path": "static\\images\\cuisine\\goan-bebinca-cake.jpg",
            "title": "File:Bebinca com 9 folhas.JPG",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABebinca_com_9_folhas.JPG",
            "author": "Elingunnur",
            "license": "CC BY-SA 4.0",
            "description": "Bebinca, a typical goan dessert. The sample in the photo (taken in Lisbon, Portugal) has 9 layers.",
            "width": 1200,
            "height": 1284,
            "hash": "881d9a6c5bf73e1f2359cc9026289f1abcd7c222dddc2c3b60f87f08354ac5ab"
        },
        "gujarati-khaman-dhokla": {
            "category": "cuisine",
            "slug": "gujarati-khaman-dhokla",
            "filename": "/static/images/cuisine/gujarati-khaman-dhokla.jpg",
            "file_path": "static\\images\\cuisine\\gujarati-khaman-dhokla.jpg",
            "title": "File:Gujarati Dhokla (Khaman Dhokla).jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGujarati_Dhokla_%28Khaman_Dhokla%29.jpg",
            "author": "Bhavana Homecook",
            "license": "CC BY-SA 4.0",
            "description": "Steamed dish made out of lentil flour &amp; semolina. Popular Gujarati snack and breakfast dish.",
            "width": 1200,
            "height": 675,
            "hash": "6a2575d044368cfe3b7a64e8cc8f0bc5d59cb8b2a194acf5dc18e2b5194836bf"
        },
        "gujarati-undhiyu": {
            "category": "cuisine",
            "slug": "gujarati-undhiyu",
            "filename": "/static/images/cuisine/gujarati-undhiyu.jpg",
            "file_path": "static/images/cuisine/gujarati-undhiyu.jpg",
            "title": "File:GujarartiUndhiyu HomeMade Mumbai.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGujarartiUndhiyu_HomeMade_Mumbai.jpg",
            "author": "Shah Naisargi",
            "license": "CC BY-SA 4.0",
            "description": "",
            "width": 1200,
            "height": 945,
            "hash": "0e0916bde61cbaa006ba6e3e336e7eeed5f29dae41ab91af16d525e67ebeb8b4"
        },
        "kashmiri-wazwan-rogan-josh": {
            "category": "cuisine",
            "slug": "kashmiri-wazwan-rogan-josh",
            "filename": "/static/images/cuisine/kashmiri-wazwan-rogan-josh.jpg",
            "file_path": "static\\images\\cuisine\\kashmiri-wazwan-rogan-josh.jpg",
            "title": "File:Amma ka Rogan Josh.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAmma_ka_Rogan_Josh.jpg",
            "author": "Tushareats",
            "license": "CC BY-SA 4.0",
            "description": "This is the picture from last Eid when there is a tradition in my family to indulge upon recipes from the Muslim Kitchens..since we belong to a Non-Muslim family but we believe to celebrate such and such cross cultural cuisines beyond the boundaries of only one community. And yes if we talk about th",
            "width": 1200,
            "height": 1592,
            "hash": "43b159204c687fb794109ca3877a8c804ba83f1489e6d94260723ad3dc4f5b0d"
        },
        "crispy-masala-dosa-sambar": {
            "category": "cuisine",
            "slug": "crispy-masala-dosa-sambar",
            "filename": "/static/images/cuisine/crispy-masala-dosa-sambar.jpg",
            "file_path": "static\\images\\cuisine\\crispy-masala-dosa-sambar.jpg",
            "title": "File:Masala Dosa 02.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AMasala_Dosa_02.jpg",
            "author": "Saisumanth532",
            "license": "CC BY-SA 4.0",
            "description": "Masala Dosa",
            "width": 1200,
            "height": 1600,
            "hash": "49c49a8b681f3f5913f834cc79983a8b6471c492a798dd54c5f69a3c354edf56"
        },
        "appam-with-vegetable-ishtu-stew": {
            "category": "cuisine",
            "slug": "appam-with-vegetable-ishtu-stew",
            "filename": "/static/images/cuisine/appam-with-vegetable-ishtu-stew.jpg",
            "file_path": "static\\images\\cuisine\\appam-with-vegetable-ishtu-stew.jpg",
            "title": "File:Aapam-Stew.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AAapam-Stew.jpg",
            "author": "Triv.rao",
            "license": "CC BY-SA 4.0",
            "description": "Aapam and stew, heavenly combination of Kerala Food",
            "width": 1200,
            "height": 966,
            "hash": "3b028193055ad95c49913ef3c53cb6d7ca5bb0e8e8b05ce9c0dc9e4d491b561b"
        },
        "malabar-flaky-parotta-roast": {
            "category": "cuisine",
            "slug": "malabar-flaky-parotta-roast",
            "filename": "/static/images/cuisine/malabar-flaky-parotta-roast.jpg",
            "file_path": "static\\images\\cuisine\\malabar-flaky-parotta-roast.jpg",
            "title": "File:Malabar Porotta.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AMalabar_Porotta.jpg",
            "author": "Praveen",
            "license": "CC BY-SA 4.0",
            "description": "Kerala/Malabar Parotta with chicken stew. You can notice the distinctive layers of the bread",
            "width": 1200,
            "height": 1200,
            "hash": "e1aabcb4ae0ef881cd79460da13dcd4c665a502be11a4e7812bfb7427eb8159f"
        },
        "himalayan-thukpa-momos": {
            "category": "cuisine",
            "slug": "himalayan-thukpa-momos",
            "filename": "/static/images/cuisine/himalayan-thukpa-momos.jpg",
            "file_path": "static\\images\\cuisine\\himalayan-thukpa-momos.jpg",
            "title": "File:Buff Momo 4.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABuff_Momo_4.jpg",
            "author": "Gaurav Dhwaj Khadka",
            "license": "CC BY-SA 4.0",
            "description": "Buff Momo.",
            "width": 1200,
            "height": 900,
            "hash": "f13f11b15bb8a3c71bd47b5e35acaf0c95e5d07033a567c00533d8042e248838"
        },
        "kolhapuri-misal-pav": {
            "category": "cuisine",
            "slug": "kolhapuri-misal-pav",
            "filename": "/static/images/cuisine/kolhapuri-misal-pav.jpg",
            "file_path": "static\\images\\cuisine\\kolhapuri-misal-pav.jpg",
            "title": "File:*Misal Pav*.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A%2AMisal_Pav%2A.jpg",
            "author": "Ishanya 1507",
            "license": "CC BY-SA 4.0",
            "description": "This image is of a typical marathi dish which is called Missal Pav. It has a soft bread which is known as Pav which is roasted with butter on a pan to give it a great taste. Misal is a spicy curry made up of moth beans. The curry is garnished with cilantro leaves, lemons and onions.It is topped with",
            "width": 1200,
            "height": 752,
            "hash": "46912ad86f7aa3273386598622ac8d4f31be9e1c9f45b812e5bbfaf16fdeffc9"
        },
        "maharashtrian-puran-poli": {
            "category": "cuisine",
            "slug": "maharashtrian-puran-poli",
            "filename": "/static/images/cuisine/maharashtrian-puran-poli.jpg",
            "file_path": "static\\images\\cuisine\\maharashtrian-puran-poli.jpg",
            "title": "File:Coconut holige.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ACoconut_holige.jpg",
            "author": "Pamri",
            "license": "Public domain",
            "description": "A type of bread (similar to Roti) stuffed with grated coconut and Gur.",
            "width": 1200,
            "height": 1088,
            "hash": "623ae350407fa98446abf299797ccf39d6179ca8fc84e64aa13ef70a0ff0922a"
        },
        "mumbai-pav-bhaji": {
            "category": "cuisine",
            "slug": "mumbai-pav-bhaji",
            "filename": "/static/images/cuisine/mumbai-pav-bhaji.jpg",
            "file_path": "static\\images\\cuisine\\mumbai-pav-bhaji.jpg",
            "title": "File:Bhaji pav 2.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3ABhaji_pav_2.jpg",
            "author": "BHAAGIi",
            "license": "CC BY-SA 4.0",
            "description": "Bhaji with bread buns......super cool pav bhaji",
            "width": 1200,
            "height": 1601,
            "hash": "491c8b94bd2e9baba1a97c687f61ad185e52d69b27059634c4f98c20a595bb0b"
        },
        "makki-di-roti-sarson-ka-saag": {
            "category": "cuisine",
            "slug": "makki-di-roti-sarson-ka-saag",
            "filename": "/static/images/cuisine/makki-di-roti-sarson-ka-saag.jpg",
            "file_path": "static\\images\\cuisine\\makki-di-roti-sarson-ka-saag.jpg",
            "title": "File:Makki Di Roti.JPG",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AMakki_Di_Roti.JPG",
            "author": "Vsigamany",
            "license": "CC BY-SA 4.0",
            "description": "(Makki di roti is a Punjabi corn meal bread which is typically eaten with Sarson ka Saag in Chitpreet’s home.) Yield: 8 rotis Makki ka atta (Corn meal flour) 400 grams Water 200 millilitres Ajwain 5 grams Oil 15 millilitres Salt 5 grams Ghee 40 millilitres Method: • Form a stiff dough using all the ",
            "width": 1200,
            "height": 800,
            "hash": "5195279bbd3ab7b4dae383112dff6ed95588d3cd8d5c74be51b9f5ecf45a765d"
        },
        "rajasthani-dal-baati-churma": {
            "category": "cuisine",
            "slug": "rajasthani-dal-baati-churma",
            "filename": "/static/images/cuisine/rajasthani-dal-baati-churma.jpg",
            "file_path": "static\\images\\cuisine\\rajasthani-dal-baati-churma.jpg",
            "title": "File:\"Delectable Dal Baati Churma\".jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A%22Delectable_Dal_Baati_Churma%22.jpg",
            "author": "Mahi Tatavarty",
            "license": "CC BY-SA 4.0",
            "description": "The traditional dish of Rajasthan is a dish of dal, baati (hard wheat rolls) and churma is an irresistible indulgence which is a must-have and melts in mouth in no-time!",
            "width": 1200,
            "height": 994,
            "hash": "5d6fc213efdcc9bc2e8ca6d07f83777b75e0b3ae4e2ca5d6a25565737daed6bb"
        },
        "rajasthani-ghevar": {
            "category": "cuisine",
            "slug": "rajasthani-ghevar",
            "filename": "/static/images/cuisine/rajasthani-ghevar.jpg",
            "file_path": "static\\images\\cuisine\\rajasthani-ghevar.jpg",
            "title": "File:Ghevar.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGhevar.jpg",
            "author": "Vinayakgupta4",
            "license": "CC BY-SA 4.0",
            "description": "This is a rajasthani sweet dish. Very famous in all over india. Best made in jaipur.",
            "width": 1200,
            "height": 1600,
            "hash": "6b4b33cbb0c01ca0a622b2f9edce5a3ab8735ce6e59bf2f28b257c0fd2bfd9c2"
        },
        "hyderabadi-dum-biryani": {
            "category": "cuisine",
            "slug": "hyderabadi-dum-biryani",
            "filename": "/static/images/cuisine/hyderabadi-dum-biryani.jpg",
            "file_path": "static\\images\\cuisine\\hyderabadi-dum-biryani.jpg",
            "title": "File:\"Hyderabadi Dum Biryani\".jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A%22Hyderabadi_Dum_Biryani%22.jpg",
            "author": "Mahi Tatavarty",
            "license": "CC BY-SA 4.0",
            "description": "Hyderabadi Dum Biryani, a popular type of biryani",
            "width": 1200,
            "height": 771,
            "hash": "92e08e4f2009cc6400eaad3eb4661513d4022ec53c6a658e1ed3d1c7c87edd6a"
        },
        "hyderabadi-shahi-haleem": {
            "category": "cuisine",
            "slug": "hyderabadi-shahi-haleem",
            "filename": "/static/images/cuisine/hyderabadi-shahi-haleem.jpg",
            "file_path": "static/images/cuisine/hyderabadi-shahi-haleem.jpg",
            "title": "File:Haleem hyderabadi.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AHaleem_hyderabadi.jpg",
            "author": "Chandu7299",
            "license": "CC BY-SA 4.0",
            "description": "",
            "width": 1200,
            "height": 800,
            "hash": "65839c2645b93953684439af7b1d9cf8b8ee99b8512b249ad63e36042c901647"
        },
        "bengali-shorshe-machher-jhol": {
            "category": "cuisine",
            "slug": "bengali-shorshe-machher-jhol",
            "filename": "/static/images/cuisine/bengali-shorshe-machher-jhol.jpg",
            "file_path": "static\\images\\cuisine\\bengali-shorshe-machher-jhol.jpg",
            "title": "File:Shorshe Illish- Agartala- Tripura.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AShorshe_Illish-_Agartala-_Tripura.jpg",
            "author": "Tuhi2001",
            "license": "CC BY-SA 4.0",
            "description": "One of the most famous monsoon season delicacies of Bengali cuisine is Shorshe Illish. It is a mustard based fish ( Bengali: Illish/ Hilsa) curry. Due to its pungent and strong flavour, it is best enjoyed with hot steamed white rice and green chillies.",
            "width": 1200,
            "height": 959,
            "hash": "9adee44559dadcdc42b8beb7bada444d74610989d9349ea381b2c93af29d6e84"
        },
        "kolkata-rosogolla": {
            "category": "cuisine",
            "slug": "kolkata-rosogolla",
            "filename": "/static/images/cuisine/kolkata-rosogolla.jpg",
            "file_path": "static\\images\\cuisine\\kolkata-rosogolla.jpg",
            "title": "File:\"Fluffy Rasgulla\".jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A%22Fluffy_Rasgulla%22.jpg",
            "author": "Mahi Tatavarty",
            "license": "CC BY-SA 4.0",
            "description": "The Bengali Roshogolla is a big thumbs up made from ball-shaped dumplings of chhena and semolina dough, cooked in light syrup of sugar will definitely win our hearts!",
            "width": 1200,
            "height": 1600,
            "hash": "f52d47ce71525b589af10e4eab67b6dcb5d0cf284bb75e666a2d1888ee4c111e"
        }
    },
    "stories": {
        "deciphering-the-stone-lace-of-hoysala-temples": {
            "category": "stories",
            "slug": "deciphering-the-stone-lace-of-hoysala-temples",
            "filename": "/static/images/stories/deciphering-the-stone-lace-of-hoysala-temples.jpg",
            "file_path": "static\\images\\stories\\deciphering-the-stone-lace-of-hoysala-temples.jpg",
            "title": "File:12th-century Brahma Shiva Vishnu next to Shiva Parvati at Shaivism Hindu temple Hoysaleswara arts Halebidu Karnataka India.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3A12th-century_Brahma_Shiva_Vishnu_next_to_Shiva_Parvati_at_Shaivism_Hindu_temple_Hoysaleswara_arts_Halebidu_Karnataka_India.jpg",
            "author": "Ms Sarah Welch",
            "license": "CC BY-SA 4.0",
            "description": "The Hoysaleswara Hindu temple is dedicated to Shiva. It was built in the first half of 12th century in Halebid (previously called Dwarasamudra, Hale bidu means \"old capital\"), sponsored by King Vishnuvardhana of the Hoysala Empire. During the early 14th century, Halebidu temple site along with other",
            "width": 1200,
            "height": 884,
            "hash": "a56fa4881786489e6f50a4789aa11e4098ada4e692b3df298f640f539c862100"
        },
        "a-dawn-awakening-along-the-ghats-of-kashi": {
            "category": "stories",
            "slug": "a-dawn-awakening-along-the-ghats-of-kashi",
            "filename": "/static/images/stories/a-dawn-awakening-along-the-ghats-of-kashi.jpg",
            "file_path": "static\\images\\stories\\a-dawn-awakening-along-the-ghats-of-kashi.jpg",
            "title": "File:Good morning Varanasi.jpg",
            "source_url": "https://commons.wikimedia.org/wiki/File%3AGood_morning_Varanasi.jpg",
            "author": "MukherjeeSomnath1980",
            "license": "CC BY-SA 4.0",
            "description": "A priest doing morning prayer rituals in famous ghats of Varanasi.",
            "width": 1200,
            "height": 797,
            "hash": "e4160f30bfc7baa7e722f7955c4fb7bdbfed06f900d669ef40da3f87aa77e5ed"
        }
    }
}

def ensure_state_svg(state_slug, state_name, capital, region):
    import os
    os.makedirs('static/images/states', exist_ok=True)
    out_path = os.path.join('static', 'images', 'states', f"{state_slug}.svg")
    if os.path.exists(out_path):
        return f"/static/images/states/{state_slug}.svg"
    
    palettes = {
        'North': {'c1': '#431407', 'c2': '#9a3412', 'c3': '#ea580c', 'accent': '#fef3c7', 'border': '#f59e0b', 'badge_bg': '#7c2d12', 'badge_text': '#fef3c7', 'title': 'NORTH INDIA'},
        'South': {'c1': '#2e1065', 'c2': '#581c87', 'c3': '#7e22ce', 'accent': '#fef3c7', 'border': '#fbbf24', 'badge_bg': '#3b0764', 'badge_text': '#fef3c7', 'title': 'SOUTH INDIA'},
        'East': {'c1': '#450a0a', 'c2': '#881337', 'c3': '#be123c', 'accent': '#fff1f2', 'border': '#f43f5e', 'badge_bg': '#701a75', 'badge_text': '#fef3c7', 'title': 'EAST INDIA'},
        'West': {'c1': '#451a03', 'c2': '#78350f', 'c3': '#b45309', 'accent': '#fef3c7', 'border': '#f59e0b', 'badge_bg': '#3f2c00', 'badge_text': '#fde68a', 'title': 'WEST INDIA'},
        'Central': {'c1': '#1c1917', 'c2': '#44403c', 'c3': '#78716c', 'accent': '#fafaf9', 'border': '#fbbf24', 'badge_bg': '#292524', 'badge_text': '#fde68a', 'title': 'CENTRAL INDIA'},
        'Northeast': {'c1': '#022c22', 'c2': '#064e3b', 'c3': '#059669', 'accent': '#ecfdf5', 'border': '#34d399', 'badge_bg': '#064e3b', 'badge_text': '#a7f3d0', 'title': 'NORTHEAST INDIA'},
        'UT': {'c1': '#0f172a', 'c2': '#1e3a8a', 'c3': '#2563eb', 'accent': '#eff6ff', 'border': '#60a5fa', 'badge_bg': '#1e293b', 'badge_text': '#bfdbfe', 'title': 'UNION TERRITORY'},
    }
    pal = palettes.get(region, palettes['North'])
    region_title = pal['title']
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <linearGradient id="bgGrad_{state_slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{pal['c1']}" />
      <stop offset="50%" stop-color="{pal['c2']}" />
      <stop offset="100%" stop-color="{pal['c3']}" />
    </linearGradient>
    <radialGradient id="radial_{state_slug}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{pal['border']}" stop-opacity="0.25" />
      <stop offset="100%" stop-color="{pal['c1']}" stop-opacity="0" />
    </radialGradient>
    <pattern id="jali_{state_slug}" width="80" height="80" patternUnits="userSpaceOnUse">
      <circle cx="40" cy="40" r="28" fill="none" stroke="{pal['border']}" stroke-width="1.2" stroke-opacity="0.12"/>
      <path d="M 0 40 L 40 0 L 80 40 L 40 80 Z" fill="none" stroke="{pal['border']}" stroke-width="1.2" stroke-opacity="0.15"/>
    </pattern>
    <filter id="shadow_{state_slug}" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>
  <rect width="1200" height="800" fill="url(#bgGrad_{state_slug})" />
  <rect width="1200" height="800" fill="url(#radial_{state_slug})" />
  <rect width="1200" height="800" fill="url(#jali_{state_slug})" />
  <rect x="40" y="40" width="1120" height="720" rx="16" fill="none" stroke="{pal['border']}" stroke-width="2.5" stroke-opacity="0.6"/>
  <rect x="52" y="52" width="1096" height="696" rx="12" fill="none" stroke="{pal['border']}" stroke-width="1" stroke-opacity="0.3" stroke-dasharray="8 6"/>
  <g transform="translate(600, 150)">
    <rect x="-160" y="-18" width="320" height="36" rx="18" fill="{pal['badge_bg']}" stroke="{pal['border']}" stroke-width="1.5" filter="url(#shadow_{state_slug})"/>
    <text text-anchor="middle" y="5" font-family="'Cinzel', Georgia, serif" font-size="14" font-weight="700" letter-spacing="3" fill="{pal['badge_text']}">
      {region_title} • CULTURAL HERITAGE
    </text>
  </g>
  <text x="600" y="490" text-anchor="middle" font-family="'Cinzel', 'Playfair Display', Georgia, serif" font-size="52" font-weight="700" letter-spacing="2" fill="{pal['accent']}" filter="url(#shadow_{state_slug})">
    {state_name}
  </text>
  <g transform="translate(600, 530)">
    <line x1="-180" y1="0" x2="-20" y2="0" stroke="{pal['border']}" stroke-width="1.5" stroke-opacity="0.7"/>
    <polygon points="0,-8 8,0 0,8 -8,0" fill="{pal['border']}" fill-opacity="0.9"/>
    <line x1="20" y1="0" x2="180" y2="0" stroke="{pal['border']}" stroke-width="1.5" stroke-opacity="0.7"/>
  </g>
  <text x="600" y="575" text-anchor="middle" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-size="20" font-weight="500" letter-spacing="1" fill="{pal['accent']}" fill-opacity="0.9">
    Capital: {capital}
  </text>
  <text x="600" y="610" text-anchor="middle" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-size="15" font-weight="400" letter-spacing="2" fill="{pal['border']}" fill-opacity="0.85">
    TRADITIONS • ARCHITECTURE • LIVING ARTS
  </text>
</svg>"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    return f"/static/images/states/{state_slug}.svg"


class Command(BaseCommand):
    help = "Populate the Virasat database with authentic, high-quality Indian cultural heritage records."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing Virasat Heritage Archive Seeder..."))
        
        # 1. Create Default Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'archivist@virasat.heritage.in',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Chief',
                'last_name': 'Archivist',
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        demo_user, _ = User.objects.get_or_create(
            username='heritage_explorer',
            defaults={
                'email': 'explorer@virasat.heritage.in',
                'first_name': 'Ananya',
                'last_name': 'Sharma',
            }
        )
        demo_user.set_password('explorer123')
        demo_user.save()

        self.stdout.write(self.style.SUCCESS("[OK] Default users created (admin: admin123, heritage_explorer: explorer123)"))

        # 2. Seed States & UTs (28 States & Major UTs)
        states_data = [
            {
                "name": "Uttar Pradesh", "capital": "Lucknow", "region": "North",
                "languages": "Hindi, Urdu, Awadhi, Bhojpuri",
                "summary": "The cradle of Indic civilization along the sacred Ganga and Yamuna. Home to Ayodhya, Varanasi, the Taj Mahal, and the synthesis of classical music and Awadhi culture.",
                "hero_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
                "lat": 26.8467, "lng": 80.9462, "famous_for": "Taj Mahal, Varanasi Ghats, Kathak, Awadhi Cuisine",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Rajasthan", "capital": "Jaipur", "region": "North",
                "languages": "Hindi, Rajasthani, Marwari, Mewari",
                "summary": "Land of kings, golden Thar desert dunes, invincible hill forts, vibrant turbans, folk ballads of valor, and ornate havelis.",
                "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
                "lat": 27.0238, "lng": 74.2179, "famous_for": "Amber Fort, Hawa Mahal, Thar Desert, Bandhani, Ghevar",
                "best_time_to_visit": "November to February"
            },
            {
                "name": "Karnataka", "capital": "Bengaluru", "region": "South",
                "languages": "Kannada",
                "summary": "Crossroads of majestic empires: Badami Chalukyas, Hoysala stone lace, and the legendary Vijayanagara capital of Hampi.",
                "hero_image": "https://images.unsplash.com/photo-1600100397608-f010f443b719?auto=format&fit=crop&w=1200&q=80",
                "lat": 15.3173, "lng": 75.7139, "famous_for": "Hampi Ruins, Mysore Palace, Carnatic Music, Yakshagana",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Tamil Nadu", "capital": "Chennai", "region": "South",
                "languages": "Tamil",
                "summary": "Guardian of Dravidian heritage, boasting soaring temple gopurams, ancient Sangam literature, Bharatanatyam dance, and bronze sculpting.",
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80",
                "lat": 11.1271, "lng": 78.6569, "famous_for": "Meenakshi Temple, Brihadisvara, Bharatanatyam, Kanchipuram Silk",
                "best_time_to_visit": "November to February"
            },
            {
                "name": "Kerala", "capital": "Thiruvananthapuram", "region": "South",
                "languages": "Malayalam",
                "summary": "God's Own Country, famed for emerald backwaters, Ayurvedic traditions, Kathakali face-art, and ancient spice-trade ports like Muziris.",
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
                "lat": 10.8505, "lng": 76.2711, "famous_for": "Backwaters, Kathakali, Kalaripayattu, Onam, Appam & Stew",
                "best_time_to_visit": "September to March"
            },
            {
                "name": "Maharashtra", "capital": "Mumbai", "region": "West",
                "languages": "Marathi",
                "summary": "Land of Chhatrapati Shivaji's sea and hill forts, ancient rock-cut sanctums of Ajanta and Ellora, and the joyous fervor of Ganesh Chaturthi.",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80",
                "lat": 19.7515, "lng": 75.7139, "famous_for": "Ajanta-Ellora Caves, Gateway of India, Warli Art, Lavani",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Gujarat", "capital": "Gandhinagar", "region": "West",
                "languages": "Gujarati",
                "summary": "Maritime heritage stretching from ancient Lothal's dockyard to the Sun Temple of Modhera, the white salt desert of Kutch, and vibrant Garba dances.",
                "hero_image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80",
                "lat": 22.2587, "lng": 71.1924, "famous_for": "Rani ki Vav, Rann of Kutch, Garba, Dhokla, Patola Silk",
                "best_time_to_visit": "November to February"
            },
            {
                "name": "Madhya Pradesh", "capital": "Bhopal", "region": "Central",
                "languages": "Hindi, Malwi, Bundeli",
                "summary": "The heart of India: prehistoric cave art at Bhimbetka, the Great Sanchi Stupa, and the sensuous stone sculptures of Khajuraho.",
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80",
                "lat": 22.9734, "lng": 78.6569, "famous_for": "Khajuraho Temples, Sanchi Stupa, Bhimbetka, Gond Art",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "West Bengal", "capital": "Kolkata", "region": "East",
                "languages": "Bengali",
                "summary": "Intellectual and artistic hub, celebrated for Rabindranath Tagore's literature, terracotta temples of Bishnupur, and the grand spectacle of Durga Puja.",
                "hero_image": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=1200&q=80",
                "lat": 22.9868, "lng": 87.8550, "famous_for": "Durga Puja, Victoria Memorial, Sundarbans, Rosogolla, Pattachitra",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Odisha", "capital": "Bhubaneswar", "region": "East",
                "languages": "Odia",
                "summary": "Ancient Kalinga, home to the Konark Sun Temple stone chariot, Puri Jagannath Ratha Yatra, sublime Odissi dance, and silver filigree craft.",
                "hero_image": "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&w=1200&q=80",
                "lat": 20.9517, "lng": 85.0985, "famous_for": "Konark Sun Temple, Jagannath Puri, Odissi, Pattachitra Scrolls",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Bihar", "capital": "Patna", "region": "East",
                "languages": "Hindi, Maithili, Magahi, Bhojpuri",
                "summary": "Epicenter of ancient wisdom: where Gautama Buddha attained enlightenment at Bodh Gaya, Mahavira preached Jainism, and Nalanda educated the ancient world.",
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80",
                "lat": 25.0961, "lng": 85.3131, "famous_for": "Bodh Gaya, Nalanda University, Madhubani Art, Litti Chokha",
                "best_time_to_visit": "November to February"
            },
            {
                "name": "Punjab", "capital": "Chandigarh", "region": "North",
                "languages": "Punjabi",
                "summary": "Land of the five rivers, radiating spiritual radiance from the Golden Temple in Amritsar, vibrant Bhangra dances, and generous hospitality.",
                "hero_image": "https://images.unsplash.com/photo-1517821099606-cef63a9bcab6?auto=format&fit=crop&w=1200&q=80",
                "lat": 31.1471, "lng": 75.3412, "famous_for": "Golden Temple, Bhangra, Phulkari Embroidery, Sarson ka Saag",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Assam", "capital": "Dispur", "region": "Northeast",
                "languages": "Assamese, Bodo",
                "summary": "The mighty Brahmaputra river valley, renowned for lush tea gardens, one-horned rhinos of Kaziranga, golden Muga silk, and Bihu harvest dances.",
                "hero_image": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=1200&q=80",
                "lat": 26.2006, "lng": 92.9376, "famous_for": "Kaziranga National Park, Muga Silk, Bihu Dance, Kamakhya Temple",
                "best_time_to_visit": "November to April"
            },
            {
                "name": "Jammu and Kashmir", "capital": "Srinagar / Jammu", "region": "North",
                "languages": "Kashmiri, Dogri, Urdu",
                "summary": "Paradise on earth, blessed with snow-crested Himalayan peaks, Dal Lake shikaras, Pashmina shawl craftsmanship, and rich Sufiana music.",
                "hero_image": "https://images.unsplash.com/photo-1595846519845-68e298c2edd8?auto=format&fit=crop&w=1200&q=80",
                "lat": 33.7782, "lng": 76.5762, "famous_for": "Dal Lake, Pashmina Weaving, Rogan Josh, Shikara Boats",
                "best_time_to_visit": "April to October"
            },
            {
                "name": "Telangana", "capital": "Hyderabad", "region": "South",
                "languages": "Telugu, Urdu",
                "summary": "Synthesis of Kakatiya stone temples and Deccan Qutb Shahi splendor, famed for the Charminar, Golconda diamonds, and world-renowned Dum Biryani.",
                "hero_image": "https://images.unsplash.com/photo-1605649487212-47bdab064df8?auto=format&fit=crop&w=1200&q=80",
                "lat": 18.1124, "lng": 79.0193, "famous_for": "Charminar, Golconda Fort, Ramappa Temple, Hyderabadi Biryani",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Andhra Pradesh", "capital": "Amaravati", "region": "South",
                "languages": "Telugu",
                "summary": "Land of the sacred Tirumala Venkateswara hill temple, classical Kuchipudi dance drama, and natural vegetable-dyed Kalamkari cloth paintings.",
                "hero_image": "https://images.unsplash.com/photo-1627894483216-2138af692e32?auto=format&fit=crop&w=1200&q=80",
                "lat": 15.9129, "lng": 79.7400, "famous_for": "Tirupati Temple, Kuchipudi, Kalamkari Art, Lepakshi Temple",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Rajasthan (Jaipur Hub)", "capital": "Jaipur", "region": "North",
                "languages": "Hindi, Marwari",
                "summary": "Pink City UNESCO World Heritage Urban site with celestial observatory Jantar Mantar and royal palaces.",
                "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
                "lat": 26.9124, "lng": 75.7873, "famous_for": "Hawa Mahal, Jantar Mantar, Blue Pottery",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Goa", "capital": "Panaji", "region": "West",
                "languages": "Konkani, Marathi, English",
                "summary": "Sun-drenched coastal state marrying ancient Hindu traditions with Portuguese baroque church architecture and Indo-Latin music.",
                "hero_image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
                "lat": 15.2993, "lng": 74.1240, "famous_for": "Basilica of Bom Jesus, Goan Bebinca, Shigmo Festival",
                "best_time_to_visit": "November to February"
            },
            {
                "name": "Himachal Pradesh", "capital": "Shimla", "region": "North",
                "languages": "Hindi, Pahari",
                "summary": "Devbhoomi (Land of the Gods), featuring wooden pagoda temples, Kullu shawls, Kangra miniature paintings, and serene Buddhist monasteries.",
                "hero_image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80",
                "lat": 31.1048, "lng": 77.1734, "famous_for": "Kullu Dussehra, Kangra Art, Spiti Monasteries",
                "best_time_to_visit": "March to June, September to November"
            },
            {
                "name": "Uttarakhand", "capital": "Dehradun", "region": "North",
                "languages": "Hindi, Garhwali, Kumaoni",
                "summary": "Spiritual heartland of the Char Dham pilgrimage, the source of the holy Ganga and Yamuna, and the majestic Valley of Flowers.",
                "hero_image": "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=1200&q=80",
                "lat": 30.0668, "lng": 79.0193, "famous_for": "Badrinath, Kedarnath, Rishikesh Yoga, Nanda Devi",
                "best_time_to_visit": "April to June, September to November"
            },
            {
                "name": "Ladakh", "capital": "Leh", "region": "North",
                "languages": "Ladakhi, Tibetan, Hindi",
                "summary": "The high Himalayan desert moonscape, holding ancient Buddhist Gompas like Thiksey and Hemis, vibrant Cham mask dances, and Losar celebrations.",
                "hero_image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=1200&q=80",
                "lat": 34.1526, "lng": 77.5771, "famous_for": "Hemis Festival, Thiksey Gompa, Pangong Tso, Cham Dance",
                "best_time_to_visit": "June to September"
            },
            {
                "name": "Nagaland", "capital": "Kohima", "region": "Northeast",
                "languages": "English, Nagamese, Naga Dialects",
                "summary": "Land of fierce tribal traditions, warrior dances, intricate wood carving, and the celebrated pan-tribal Hornbill Festival.",
                "hero_image": "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&w=1200&q=80",
                "lat": 26.1584, "lng": 94.5624, "famous_for": "Hornbill Festival, Naga Shawls, Indigenous Woodcraft",
                "best_time_to_visit": "October to May"
            },
            {
                "name": "Manipur", "capital": "Imphal", "region": "Northeast",
                "languages": "Manipuri (Meitei)",
                "summary": "The jewel of Northeast India, birthplace of modern polo, ethereal classical Manipuri Raas Leela dance, and the floating Loktak Lake.",
                "hero_image": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=1200&q=80",
                "lat": 24.6637, "lng": 93.9063, "famous_for": "Manipuri Classical Dance, Loktak Lake, Sagol Kangjei (Polo)",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Delhi (NCT)", "capital": "New Delhi", "region": "North",
                "languages": "Hindi, English, Punjabi, Urdu",
                "summary": "The political and historical capital, where seven ancient cities converge. Home to the Qutub Minar, Humayun's Tomb, and the grand Red Fort.",
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80",
                "lat": 28.6139, "lng": 77.2090, "famous_for": "Qutub Minar, Red Fort, Humayun's Tomb, Street Cuisine",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Sikkim", "capital": "Gangtok", "region": "Northeast",
                "languages": "Nepali, Bhutia, Lepcha, English",
                "summary": "The mystical Himalayan state in the shadow of Mount Kanchenjunga, preserving ancient Tibetan Buddhist monasteries and rich biodiversity.",
                "hero_image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=1200&q=80",
                "lat": 27.5330, "lng": 88.5122, "famous_for": "Rumtek Monastery, Kanchenjunga, Thangka Painting",
                "best_time_to_visit": "March to May, October to mid-December"
            },
            {
                "name": "Jharkhand", "capital": "Ranchi", "region": "East",
                "languages": "Hindi, Santali, Mundari",
                "summary": "Land of sacred sal forests, rich tribal folklore, Dhokra metal casting, and ancient Jain pilgrimage sites at Parasnath Hill.",
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80",
                "lat": 23.6102, "lng": 85.2799, "famous_for": "Sohrai Art, Dhokra Craft, Parasnath Hill",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Chhattisgarh", "capital": "Raipur", "region": "Central",
                "languages": "Chhattisgarhi, Hindi",
                "summary": "Famed for Bastar tribal arts, bell metal crafts, ancient rock shelters, and the spectacular Chitrakote horseshoe waterfall.",
                "hero_image": "https://images.unsplash.com/photo-1600100397608-f010f443b719?auto=format&fit=crop&w=1200&q=80",
                "lat": 21.2787, "lng": 81.8661, "famous_for": "Bastar Dhokra, Chitrakote Falls, Sirpur Monuments",
                "best_time_to_visit": "October to March"
            },
            {
                "name": "Haryana", "capital": "Chandigarh", "region": "North",
                "languages": "Hindi, Haryanvi",
                "summary": "Ancient battleground of Kurukshetra where the Bhagavad Gita was spoken; also site of major Indus Valley excavations at Rakhigarhi.",
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80",
                "lat": 29.0588, "lng": 76.0856, "famous_for": "Kurukshetra, Rakhigarhi Harappan Site, Surajkund Crafts",
                "best_time_to_visit": "October to March"
            }
        ]

        state_objs = {}
        for s in states_data:
            st_slug = slugify(s["name"])
            s["hero_image"] = ensure_state_svg(st_slug, s["name"], s.get("capital", ""), s.get("region", "North"))
            s["image_credit"] = "Virasat Regional Cultural Design"
            s["image_source_url"] = "https://commons.wikimedia.org/"
            s["image_license"] = "CC0 / Public Domain"
            obj, created = State.objects.update_or_create(
                name=s["name"],
                defaults=s
            )
            state_objs[obj.name] = obj

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(state_objs)} States and Regions"))

        # 3. Seed 25+ Heritage Sites (Including World Heritage Sites)
        sites_data = [
            {
                "name": "Taj Mahal", "state": "Uttar Pradesh", "category": "Monument",
                "unesco": True, "unesco_year": 1983,
                "era": "Mughal Empire (1632–1653 CE)", "built_by": "Emperor Shah Jahan",
                "built_year": "1653 CE", "architecture_style": "Mughal (Persian, Islamic, and Indian synthesis)",
                "description": "An immense mausoleum of white marble standing on the southern bank of the Yamuna River in Agra. Widely regarded as the jewel of Muslim art in India and one of the universally admired masterpieces of world heritage.",
                "history": "Commissioned by the fifth Mughal Emperor Shah Jahan in 1631 to house the tomb of his beloved wife Mumtaz Mahal. Over 20,000 artisans from across India, Persia, and Central Asia labored for 22 years to build this monument to eternal love.",
                "visiting_info": "Open sunrise to sunset (closed Fridays). Night viewing available around full moon nights. Shoe covers and electric shuttle vehicles provided from outer parking gates.",
                "lat": 27.1751, "lng": 78.0421,
                "hero_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Hampi Ruins (Vijayanagara)", "state": "Karnataka", "category": "Monument",
                "unesco": True, "unesco_year": 1986,
                "era": "Vijayanagara Empire (14th–16th Century)", "built_by": "Harihara, Bukka, and Krishnadevaraya",
                "built_year": "1336–1565 CE", "architecture_style": "Vijayanagara Dravidian style",
                "description": "A surreal boulder-strewn landscape dotted with over 1,600 surviving monuments: grand temples with musical stone pillars, royal pavilions, elephant stables, and ancient bazaars.",
                "history": "Hampi was the capital of the mighty Vijayanagara Empire. In the 15th and 16th centuries, travelers from Portugal, Persia, and Italy described it as one of the largest and most prosperous metropolises in the world.",
                "visiting_info": "Open daily sunrise to sunset. Electric buggies operate between the parking area and Vittala Temple. Best explored on bicycles or guided heritage walks.",
                "lat": 15.3350, "lng": 76.4600,
                "hero_image": "https://images.unsplash.com/photo-1600100397608-f010f443b719?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Khajuraho Group of Monuments", "state": "Madhya Pradesh", "category": "Temple",
                "unesco": True, "unesco_year": 1986,
                "era": "Chandela Dynasty (950–1050 CE)", "built_by": "Chandela Rajput Kings",
                "built_year": "c. 950–1050 CE", "architecture_style": "Nagara (North Indian Temple style)",
                "description": "A stunning complex of Hindu and Jain temples renowned for their soaring architectural spires (shikharas) and sensuous, exquisitely carved sandstone sculptures celebrating human life and spiritual union.",
                "history": "Built during the zenith of Chandela rule in Bundelkhand. Of the original 85 temples, 25 survive today across the Western, Eastern, and Southern groups.",
                "visiting_info": "Western group open sunrise to sunset. Evening Light & Sound show narrated in English and Hindi. Annual Khajuraho Dance Festival held every February.",
                "lat": 24.8318, "lng": 79.9199,
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Ajanta Caves", "state": "Maharashtra", "category": "Cave",
                "unesco": True, "unesco_year": 1983,
                "era": "2nd Century BCE to 5th Century CE", "built_by": "Satavahana & Vakataka Dynasties",
                "built_year": "c. 200 BCE – 480 CE", "architecture_style": "Ancient Indian Rock-cut Architecture & Fresco Murals",
                "description": "Thirty rock-cut Buddhist cave monuments carved into a sheer horseshoe-shaped gorge of the Waghur River, containing world-famous mural paintings depicting the Jataka tales.",
                "history": "Served as a monsoon retreat and university for Buddhist monks. Abandoned after the 5th century, the caves were accidentally rediscovered in 1819 by British officer John Smith during a tiger hunt.",
                "visiting_info": "Closed on Mondays. Optical flash photography is strictly prohibited inside the caves to preserve the ancient natural vegetable pigments.",
                "lat": 20.5519, "lng": 75.7033,
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Ellora Caves (Kailasa Temple)", "state": "Maharashtra", "category": "Cave",
                "unesco": True, "unesco_year": 1983,
                "era": "Rashtrakuta & Yadava Dynasties (6th–10th Century CE)", "built_by": "King Krishna I (Rashtrakuta)",
                "built_year": "c. 756–774 CE", "architecture_style": "Monolithic Rock-cut Dravidian Architecture",
                "description": "Cave 16 (The Kailasa Temple) is the largest monolithic rock-cut monument in the world, carved vertically downward out of a single basalt cliffside using only chisels and hammers.",
                "history": "An estimated 200,000 tonnes of basalt rock were scooped out over a century to create an architectural replica of Mount Kailash, the sacred Himalayan abode of Shiva.",
                "visiting_info": "Closed on Tuesdays. Open 6:00 AM to 6:00 PM. Cave 16 requires at least two hours to examine its multi-level galleries, monolithic pillars, and life-size elephant sculptures.",
                "lat": 20.0268, "lng": 75.1780,
                "hero_image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Konark Sun Temple", "state": "Odisha", "category": "Temple",
                "unesco": True, "unesco_year": 1984,
                "era": "Eastern Ganga Dynasty (13th Century CE)", "built_by": "King Narasimhadeva I",
                "built_year": "c. 1250 CE", "architecture_style": "Kalinga Architecture",
                "description": "Conceived as a colossal stone chariot of Surya, the Sun God, with 24 elaborately carved stone wheels drawn by seven galloping horses.",
                "history": "Built along the Bay of Bengal coast. European sailors used its dark stone tower as a navigational landmark, naming it the 'Black Pagoda'. The wheels function as precise sundials.",
                "visiting_info": "Open 6:00 AM to 8:00 PM daily. Evening light and sound show. The Konark Dance Festival is held here annually every December.",
                "lat": 19.8876, "lng": 86.0945,
                "hero_image": "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Qutub Minar & Complex", "state": "Delhi (NCT)", "category": "Monument",
                "unesco": True, "unesco_year": 1993,
                "era": "Delhi Sultanate (1199–1220 CE)", "built_by": "Qutb-ud-din Aibak and Iltutmish",
                "built_year": "1199 CE", "architecture_style": "Indo-Islamic with carved Arabic calligraphy",
                "description": "A 72.5-meter-high fluted red sandstone minaret tapering toward the sky, surrounded by early Islamic monuments including the 1,600-year-old rust-resistant Iron Pillar of Delhi.",
                "history": "Initiated in 1199 to mark the beginning of Muslim rule in North India. Successive sultans added balconies and restored upper stories struck by lightning.",
                "visiting_info": "Open sunrise to 10:00 PM with night illumination. Wheelchair accessible walkways throughout the complex.",
                "lat": 28.5244, "lng": 77.1855,
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Red Fort Complex", "state": "Delhi (NCT)", "category": "Fort",
                "unesco": True, "unesco_year": 2007,
                "era": "Mughal Empire (1638–1648 CE)", "built_by": "Emperor Shah Jahan",
                "built_year": "1648 CE", "architecture_style": "Mughal Red Sandstone and Marble",
                "description": "The formidable seat of Mughal imperial power in Shahjahanabad, with imposing red sandstone battlements enclosing marble pavilions, the Diwan-i-Khas, and water channels.",
                "history": "Shah Jahan relocated his capital from Agra to Delhi and built the Lal Qila. It remains the symbolic podium from which the Prime Minister addresses the nation every Independence Day.",
                "visiting_info": "Closed Mondays. Open 9:30 AM to 4:30 PM. Museums inside include the Indian War Memorial and Subhas Chandra Bose Museum.",
                "lat": 28.6562, "lng": 77.2410,
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Fatehpur Sikri", "state": "Uttar Pradesh", "category": "Monument",
                "unesco": True, "unesco_year": 1986,
                "era": "Mughal Empire (1571–1585 CE)", "built_by": "Emperor Akbar the Great",
                "built_year": "1571 CE", "architecture_style": "Syncretic Indo-Islamic & Rajput sandstone architecture",
                "description": "Akbar's magnificent red sandstone capital city, preserved in time. Features the colossal Buland Darwaza ('Gate of Magnificence') and the delicate white marble tomb of Sufi saint Salim Chishti.",
                "history": "Built by Emperor Akbar in gratitude for the birth of his son Jahangir, prophesied by Sufi mystic Sheikh Salim Chishti. Abandoned shortly after due to water scarcity.",
                "visiting_info": "Open sunrise to sunset daily. Located 37 km west of Agra; easily visited on a day trip combined with the Taj Mahal.",
                "lat": 27.0945, "lng": 77.6679,
                "hero_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Group of Monuments at Mahabalipuram", "state": "Tamil Nadu", "category": "Monument",
                "unesco": True, "unesco_year": 1984,
                "era": "Pallava Dynasty (7th–8th Century CE)", "built_by": "Narasimhavarman I and Rajasimha",
                "built_year": "c. 650–728 CE", "architecture_style": "Early Dravidian rock-cut and structural architecture",
                "description": "Ancient coastal sanctuary featuring the Shore Temple facing the Bay of Bengal, the Five Rathas carved like monolithic stone chariots, and the monumental rock relief 'Descent of the Ganga'.",
                "history": "Mahabalipuram was the premier port city of the seafaring Pallava Empire, from where Indian culture, religion, and scripts were transmitted across Southeast Asia.",
                "visiting_info": "Open 6:00 AM to 6:00 PM. Coastal breeze makes morning and late afternoon visits magical for photography.",
                "lat": 12.6269, "lng": 80.1927,
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Brihadisvara Temple (Thanjavur)", "state": "Tamil Nadu", "category": "Temple",
                "unesco": True, "unesco_year": 1987,
                "era": "Chola Dynasty (1010 CE)", "built_by": "Emperor Raja Raja Chola I",
                "built_year": "1010 CE", "architecture_style": "Pure Dravidian Granite Architecture",
                "description": "The crowning glory of Great Living Chola Temples. Its 66-meter-high granite vimana tower is capped by an 80-tonne single granite octagonal shikhara cupola.",
                "history": "Completed in 1010 CE to celebrate the Chola maritime empire. The entire temple is constructed from over 130,000 tonnes of granite transported from quarries 50 km away.",
                "visiting_info": "Open 6:00 AM to 12:30 PM, 4:00 PM to 8:30 PM. Active temple of worship; conservative clothing required.",
                "lat": 10.7828, "lng": 79.1318,
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Meenakshi Amman Temple", "state": "Tamil Nadu", "category": "Living Heritage",
                "unesco": False, "unesco_year": None,
                "era": "Pandya & Nayaka Dynasties (6th Century BCE origins, rebuilt 16th–17th Century)", "built_by": "Thirumalai Nayak",
                "built_year": "c. 1623–1655 CE", "architecture_style": "Late Dravidian with multi-tier sculptural gopurams",
                "description": "A living spiritual city with 14 towering gopurams encrusted with thousands of vividly colored stucco figures of gods, demons, and celestial beings. Features the Hall of Thousand Pillars.",
                "history": "Dedicated to Goddess Meenakshi (an avatar of Parvati) and Sundareswarar (Shiva). Mentioned in early Tamil Sangam literature over 2,000 years ago.",
                "visiting_info": "Open 5:00 AM to 12:30 PM, 4:00 PM to 10:00 PM. Night procession of Shiva to Meenakshi's shrine takes place every evening at 9:00 PM.",
                "lat": 9.9195, "lng": 78.1194,
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Kaziranga National Park", "state": "Assam", "category": "Natural",
                "unesco": True, "unesco_year": 1985,
                "era": "Natural Biosphere & Wildlife Sanctuary", "built_by": "Nature / Preserved since 1905",
                "built_year": "1905 CE", "architecture_style": "Floodplain grasslands and tropical moist broadleaf forests",
                "description": "Sprawling across the Brahmaputra floodplain, Kaziranga hosts two-thirds of the world's great one-horned rhinoceroses, along with wild water buffaloes and Royal Bengal tigers.",
                "history": "Established as a reserved forest in 1905 by Lord Curzon after his wife Mary Curzon could not spot a single rhino in the region. Now celebrated as one of the world's greatest conservation successes.",
                "visiting_info": "Open November to April (closed during monsoon floods). Morning and afternoon elephant and jeep safaris available.",
                "lat": 26.5775, "lng": 93.1711,
                "hero_image": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Sundarbans National Park", "state": "West Bengal", "category": "Natural",
                "unesco": True, "unesco_year": 1987,
                "era": "Mangrove Delta Ecosystem", "built_by": "Ganges-Brahmaputra-Meghna Delta",
                "built_year": "Natural Biosphere", "architecture_style": "World's largest halophytic mangrove forest",
                "description": "An amphibious maze of tidal waterways, mudflats, and mangrove islands. Famous for swimming Royal Bengal tigers and estuarine saltwater crocodiles.",
                "history": "Documented in Mughal records and British surveys. The dense sundari trees give the delta its name. Declared a UNESCO World Heritage site and Biosphere Reserve.",
                "visiting_info": "Accessible only by licensed safari boats from Godkhali. Best visited between October and March.",
                "lat": 21.9497, "lng": 89.1833,
                "hero_image": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Western Ghats Mountain Chain", "state": "Kerala", "category": "Natural",
                "unesco": True, "unesco_year": 2012,
                "era": "Ancient Geomorphic Mountain System", "built_by": "Gondwana Continental Breakup",
                "built_year": "Pre-Himalayan (150 Million Years Old)", "architecture_style": "Tropical montane rainforests and shola grasslands",
                "description": "Older than the Himalayas, this 1,600 km mountain chain influences the Indian monsoon and represents one of the world's eight 'hottest hotspots' of biological diversity.",
                "history": "Home to thousands of endemic species of flora and fauna, including the endangered Lion-tailed Macaque and Nilgiri Tahr.",
                "visiting_info": "Key entry points include Munnar, Wayanad, Silent Valley, and Agasthyamalai. Trekking permits required for core wilderness zones.",
                "lat": 10.1500, "lng": 77.0600,
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Rani ki Vav (The Queen's Stepwell)", "state": "Gujarat", "category": "Monument",
                "unesco": True, "unesco_year": 2014,
                "era": "Chaulukya (Solanki) Dynasty (11th Century CE)", "built_by": "Queen Udayamati",
                "built_year": "c. 1063 CE", "architecture_style": "Maru-Gurjara Inverted Temple Architecture",
                "description": "Designed as an inverted subterranean temple honoring the sanctity of water, descending across seven terraced levels with over 500 principal carved stone sculptures of Vishnu.",
                "history": "Built by Queen Udayamati in memory of King Bhima I. Silted over for centuries by the Saraswati River, preserving the delicate sandstone carvings in pristine condition until modern excavation.",
                "visiting_info": "Open 8:00 AM to 6:00 PM daily. Located in Patan; combines well with visits to Modhera Sun Temple.",
                "lat": 23.8589, "lng": 72.1017,
                "hero_image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Nalanda Mahavihara (Ancient University)", "state": "Bihar", "category": "Monument",
                "unesco": True, "unesco_year": 2016,
                "era": "Gupta to Pala Empires (5th–12th Century CE)", "built_by": "Kumaragupta I and successive monarchs",
                "built_year": "c. 427–1197 CE", "architecture_style": "Ancient Buddhist Monastic Brick Architecture",
                "description": "The world's first great residential international university, accommodating 10,000 scholars and 2,000 teachers from across Asia studying logic, philosophy, astronomy, and medicine.",
                "history": "Visited by Chinese pilgrims Xuanzang and Yijing. Its legendary 9-story library, Dharmaganja, housed millions of hand-copied Sanskrit manuscripts until burned in the late 12th century.",
                "visiting_info": "Open 9:00 AM to 5:00 PM daily. Nalanda Archaeological Museum across the road houses bronze sculptures and sealings excavated from the site.",
                "lat": 25.1357, "lng": 85.4450,
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Amber Palace and Fort", "state": "Rajasthan", "category": "Fort",
                "unesco": True, "unesco_year": 2013,
                "era": "Kachhwaha Rajput Dynasty (16th–18th Century)", "built_by": "Raja Man Singh I",
                "built_year": "1592 CE", "architecture_style": "Rajput and Mughal Fusion Architecture",
                "description": "Perched on rugged Aravalli hills overlooking Maota Lake, famous for its ramparts, red sandstone courtyards, and the Sheesh Mahal (Hall of Mirrors) glittering with Belgian glass.",
                "history": "Principal stronghold of the Kachhwaha Rajputs before Maharaja Sawai Jai Singh II founded Jaipur in 1727.",
                "visiting_info": "Open 8:00 AM to 5:30 PM, with evening light and sound shows. Guided walks through the underground tunnel linking Amber to Jaigarh Fort.",
                "lat": 26.9855, "lng": 75.8513,
                "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Jaisalmer Fort (Sonar Qila)", "state": "Rajasthan", "category": "Fort",
                "unesco": True, "unesco_year": 2013,
                "era": "Bhati Rajput Dynasty (1156 CE)", "built_by": "Rawal Jaisal",
                "built_year": "1156 CE", "architecture_style": "Golden Yellow Sandstone Desert Bastion",
                "description": "One of the very few surviving 'living forts' in the world. Approximately one-fourth of the old city's population still resides within its golden sandstone walls, houses, and Jain temples.",
                "history": "Strategically positioned on the medieval Silk Route through the Thar Desert, reaping tolls from camel caravans carrying silk, spices, and opium.",
                "visiting_info": "Open all day. Free entry to the fort; palace museum has ticketed admission. Best viewed at sunset when the walls glow like burnished gold.",
                "lat": 26.9124, "lng": 70.9124,
                "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Great Stupa at Sanchi", "state": "Madhya Pradesh", "category": "Monument",
                "unesco": True, "unesco_year": 1989,
                "era": "Maurya to Satavahana Periods (3rd Century BCE – 1st Century CE)", "built_by": "Emperor Ashoka the Great",
                "built_year": "c. 250 BCE", "architecture_style": "Buddhist Hemispherical Stupa & Torana Gateways",
                "description": "The oldest stone structure in India, a great hemispherical dome sheltering the sacred relics of the Buddha, surrounded by four carved torana gateways detailing Buddhist legends.",
                "history": "Commissioned by Emperor Ashoka in the 3rd century BCE after his conversion to Buddhism following the Kalinga War. His wife Devi was native to nearby Vidisha.",
                "visiting_info": "Open sunrise to sunset. The Archaeological Museum at the base houses Ashoka's lion capital found at Sanchi.",
                "lat": 23.4795, "lng": 77.7397,
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Mahabodhi Temple Complex", "state": "Bihar", "category": "Temple",
                "unesco": True, "unesco_year": 2002,
                "era": "Late Gupta to Pala Dynasties (5th–6th Century CE)", "built_by": "Emperor Ashoka first built shrine; present brick tower 5th Century",
                "built_year": "c. 5th–6th Century CE", "architecture_style": "Grand Brick Buddhist Temple with 55-meter central shikhara",
                "description": "The holiest pilgrimage site in the Buddhist world, marking the precise location of the sacred Bodhi Tree (Ficus religiosa) under which Siddhartha Gautama attained supreme enlightenment.",
                "history": "In c. 531 BCE, Siddhartha sat in deep meditation under the pipal tree here. Ashoka built the original shrine and Vajrasana (Diamond Throne) in the 3rd century BCE.",
                "visiting_info": "Open 5:00 AM to 9:00 PM. Electronic devices and mobile phones are stored in security lockers at the entrance to maintain meditative peace.",
                "lat": 24.6959, "lng": 84.9914,
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Elephanta Caves", "state": "Maharashtra", "category": "Cave",
                "unesco": True, "unesco_year": 1987,
                "era": "Kalachuri / Rashtrakuta Dynasties (5th–8th Century CE)", "built_by": "Kalachuri Kings",
                "built_year": "c. 550–750 CE", "architecture_style": "Rock-cut Shaivite Cave Sanctuary",
                "description": "Located on Gharapuri Island in Mumbai Harbor, housing the monumental 6-meter-high three-headed stone masterpiece: the Trimurti Sadashiva (Creator, Preserver, Destroyer).",
                "history": "Named 'Elephanta' by 16th-century Portuguese navigators who discovered a giant monolithic stone elephant sculpture near the landing jetty.",
                "visiting_info": "Closed Mondays. Accessible via ferry boats departing from the Gateway of India in Mumbai (1 hour crossing). Toy train runs along the dock.",
                "lat": 18.9633, "lng": 72.9315,
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Varanasi Ghats & Sacred Waterfront", "state": "Uttar Pradesh", "category": "Living Heritage",
                "unesco": False, "unesco_year": None,
                "era": "Ancient Living City (Continuous habitation over 3,000 years)", "built_by": "Marathas, Scindias, Holkars, and Kashi Kings",
                "built_year": "18th Century stone ghats; ancient city", "architecture_style": "Riverfront stepped ghats and temple pavilions",
                "description": "Eighty-four continuous stone ghats lining the crescent bend of the holy River Ganga. A living theater of dawn prayers, boatmen songs, and the mesmerizing evening Ganga Aarti.",
                "history": "Mark Twain famously wrote that Benares is 'older than history, older than tradition, older even than legend, and looks twice as old as all of them put together.'",
                "visiting_info": "Best experienced by taking a wooden rowing boat at sunrise from Assi Ghat to Manikarnika Ghat, and witnessing the grand Dashashwamedh Aarti at 6:30 PM.",
                "lat": 25.3076, "lng": 83.0107,
                "hero_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Golconda Fort", "state": "Telangana", "category": "Fort",
                "unesco": False, "unesco_year": None,
                "era": "Kakatiya and Qutb Shahi Dynasties (12th–17th Century)", "built_by": "Kakatiyas; fortified by Qutb Shahi Sultans",
                "built_year": "1518–1687 CE", "architecture_style": "Acoustic Military Citadel in Granite",
                "description": "A legendary diamond-trading fortress famous for its acoustic engineering: a hand clap at the entry gate can be clearly heard at the highest pavilion (Bala Hissar) 1 km away.",
                "history": "Origin of the world's most famous diamonds, including the Koh-i-Noor, Hope Diamond, and Daria-i-Noor, mined from the fertile Krishna river valley.",
                "visiting_info": "Open 9:00 AM to 5:30 PM. Evening light and sound show narrating the story of Sultan Muhammad Quli Qutb Shah and Bhagmati.",
                "lat": 17.3833, "lng": 78.4011,
                "hero_image": "https://images.unsplash.com/photo-1605649487212-47bdab064df8?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Victoria Memorial", "state": "West Bengal", "category": "Monument",
                "unesco": False, "unesco_year": None,
                "era": "Colonial Indo-Saracenic (1906–1921 CE)", "built_by": "Sir William Emerson / Lord Curzon",
                "built_year": "1921 CE", "architecture_style": "Indo-Saracenic with Makrana White Marble",
                "description": "A monumental white marble palace set in 64 acres of landscaped gardens, dedicated to Queen Victoria. Features a 16-foot revolving bronze Angel of Victory atop its central dome.",
                "history": "Constructed from the exact same Makrana marble as the Taj Mahal. Today it serves as India's premier museum for 18th- and 19th-century paintings, manuscripts, and textiles.",
                "visiting_info": "Gardens open 5:30 AM to 6:00 PM; museum galleries open 10:00 AM to 5:00 PM (closed Mondays).",
                "lat": 22.5448, "lng": 88.3426,
                "hero_image": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=1200&q=80"
            }
        ]

        site_objs = {}
        for s_data in sites_data:
            state_obj = state_objs.get(s_data.pop("state"))
            if not state_obj:
                continue
            slug = slugify(s_data["name"])
            if slug in IMAGE_METADATA.get("heritage", {}):
                m = IMAGE_METADATA["heritage"][slug]
                s_data["hero_image"] = m["filename"]
                s_data["image_credit"] = m["author"]
                s_data["image_source_url"] = m["source_url"]
                s_data["image_license"] = m["license"]
            site_obj, _ = HeritageSite.objects.update_or_create(
                name=s_data["name"],
                defaults={**s_data, "state": state_obj}
            )
            site_objs[site_obj.name] = site_obj

            # Add gallery images
            HeritageSiteImage.objects.get_or_create(
                site=site_obj,
                image_url=s_data["hero_image"],
                defaults={
                    "caption": f"Splendor of {site_obj.name}",
                    "attribution": f"{s_data.get('image_credit', 'Wikimedia Commons')} ({s_data.get('image_license', 'Free License')})",
                    "order": 1
                }
            )

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(site_objs)} Heritage Sites & Galleries"))

        # 4. Seed 20+ Cultural Festivals
        festivals_data = [
            {
                "name": "Diwali (Deepavali)", "month": 10, "approximate_dates": "October - November (Kartik Amavasya)",
                "religion_or_type": "Pan-Indian", "is_featured": True,
                "significance": "The festival of lights celebrating the victory of light over darkness, good over evil, and wisdom over ignorance.",
                "rituals": "Lighting earthen diyas, creating intricate colorful floor rangolis, Lakshmi and Ganesha puja at dusk, bursting sparklers, exchanging gifts.",
                "food": "Kaju Katli, Besan Ladoo, Gulab Jamun, Gujiya, Chakli, and savory dry fruit assortments.",
                "story": "Marks the triumphant return of Lord Rama, Sita, and Lakshmana to Ayodhya after 14 years of exile and the defeat of Ravana, celebrated when Ayodhya citizens illuminated the dark night.",
                "hero_image": "https://images.unsplash.com/photo-1605379399642-870262d3d051?auto=format&fit=crop&w=1200&q=80",
                "states": ["Uttar Pradesh", "Rajasthan", "Maharashtra", "Gujarat", "Delhi (NCT)"]
            },
            {
                "name": "Holi (Festival of Colors)", "month": 3, "approximate_dates": "March (Phalguna Purnima)",
                "religion_or_type": "Pan-Indian", "is_featured": True,
                "significance": "The exuberant welcoming of spring, agricultural abundance, renewal of friendships, and divine celebration of love.",
                "rituals": "Holika Dahan bonfires on the eve, playful smearing of dry organic gulal and herbal colored water, Dhol drumbeats, and singing folk Phag songs.",
                "food": "Mawa Gujiya, Thandai infused with fragrant saffron and pistachios, Puran Poli, Malpua, Dahi Vada.",
                "story": "Celebrates Prahlada's pure devotion saving him from the demon Holika, as well as the playful divine romance of Radha and Krishna in the groves of Vrindavan.",
                "hero_image": "https://images.unsplash.com/photo-1576487248805-cf45f6bcc67f?auto=format&fit=crop&w=1200&q=80",
                "states": ["Uttar Pradesh", "Rajasthan", "Bihar", "Punjab", "Delhi (NCT)"]
            },
            {
                "name": "Durga Puja (Sharadotsav)", "month": 10, "approximate_dates": "September - October (Ashwin Shukla Shasthi to Dashami)",
                "religion_or_type": "Hinduism", "is_featured": True,
                "significance": "UNESCO Intangible Cultural Heritage celebrating the supreme cosmic feminine energy (Shakti) vanquishing injustice and evil.",
                "rituals": "Installation of monumental clay idols in artistic pandals, Dhunuchi Naach dances to the furious beat of Dhak drums, Sindoor Khela, and immersion in the Ganga.",
                "food": "Khichuri bhog, Labra mixed vegetable, Beguni, Luchi, Sandesh, Mishti Doi.",
                "story": "Goddess Durga descends to earth for five days, armed with the weapons of the gods, to destroy the shape-shifting buffalo demon Mahishasura.",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80",
                "states": ["West Bengal", "Odisha", "Assam", "Bihar"]
            },
            {
                "name": "Onam (Harvest Festival)", "month": 8, "approximate_dates": "August - September (Chingam Month)",
                "religion_or_type": "Tribal / Harvest", "is_featured": True,
                "significance": "Kerala's grand secular harvest festival welcoming the annual homecoming of the benevolent mythological king Mahabali.",
                "rituals": "Pookkalam (intricate natural flower carpets on house thresholds), Vallam Kali (famous snake boat races on backwaters), Pulikkali tiger dances.",
                "food": "The iconic Onasadya feast: 26+ vegetarian delicacies served on a fresh plantain leaf with red rice, Avial, Sambar, Payasam, and Banana chips.",
                "story": "King Mahabali's golden reign was celebrated for perfect equality and honesty. Lord Vishnu in the Vamana avatar granted him a yearly visit to his beloved people.",
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
                "states": ["Kerala"]
            },
            {
                "name": "Pongal & Makar Sankranti", "month": 1, "approximate_dates": "January 14 - 17 (Thai Month)",
                "religion_or_type": "Tribal / Harvest", "is_featured": False,
                "significance": "Solar festival marking the sun's transition into Capricorn (Uttarayana), expressing gratitude to Surya, farm animals, and Mother Earth for the bountiful harvest.",
                "rituals": "Boiling new rice with fresh milk and jaggery in clay pots until it overflows shouting 'Pongalo Pongal!', Kolam rice flour artwork, Mattu Pongal honoring cattle.",
                "food": "Sakkarai Pongal (sweet jaggery rice with ghee and cashews), Ven Pongal (savory cumin-black pepper rice), Til ke Ladoo, Sugarcane.",
                "story": "Ancient Tamil Sangam festival celebrating nature's perpetual cycle of regeneration and solar blessings.",
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80",
                "states": ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Gujarat", "Maharashtra"]
            },
            {
                "name": "Rongali Bihu", "month": 4, "approximate_dates": "Mid-April (Assamese New Year)",
                "religion_or_type": "Tribal / Harvest", "is_featured": False,
                "significance": "The onset of the Assamese agricultural season and spring, marked by high-spirited community folk dances.",
                "rituals": "Bihu dance performed by young men and women in golden Muga silk attires, playing Pepa buffalo-horn trumpets and Dhol drums; honoring cattle on Goru Bihu.",
                "food": "Pitha rice cakes, Laru coconut sweets, Jolpan with curd and liquid jaggery.",
                "story": "Celebrates fertility of the earth, harmonious ties with nature, and the blooming of the sacred Kopou orchid in the Brahmaputra valley.",
                "hero_image": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=1200&q=80",
                "states": ["Assam"]
            },
            {
                "name": "Hornbill Festival", "month": 12, "approximate_dates": "December 1 - 10 (Kisama Heritage Village)",
                "religion_or_type": "Tribal / Harvest", "is_featured": True,
                "significance": "The 'Festival of Festivals' uniting all 17 indigenous Naga tribes in a vibrant showcase of warrior traditions, songs, and indigenous crafts.",
                "rituals": "Tribal warrior dances, fire-making competitions, archery, indigenous wrestling, choral concerts, and traditional rock and acoustic festivals.",
                "food": "Smoked pork with fermented bamboo shoots, spicy Raja Mircha chutney, sticky brown rice, rice brew.",
                "story": "Named after the revered Indian Hornbill bird, whose alertness and colorful feathers feature prominently in tribal folklore and headdresses.",
                "hero_image": "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&w=1200&q=80",
                "states": ["Nagaland"]
            },
            {
                "name": "Pushkar Camel Fair", "month": 11, "approximate_dates": "November (Kartik Purnima)",
                "religion_or_type": "Pan-Indian", "is_featured": False,
                "significance": "One of the world's largest livestock fairs combined with holy Hindu pilgrimage dips in the sacred Pushkar Lake.",
                "rituals": "Trading of over 50,000 camels and horses, camel beauty pageants, longest mustache contests, bridal competitions, and evening desert folk dances.",
                "food": "Dal Baati Churma, Malpuas of Pushkar, Rabdi, steaming spicy masala chai.",
                "story": "Pushkar is home to one of the world's only temples dedicated to Lord Brahma, who according to legend dropped a lotus blossom here creating the sacred lake.",
                "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
                "states": ["Rajasthan"]
            },
            {
                "name": "Rann Utsav (White Desert Festival)", "month": 12, "approximate_dates": "November to February (Full Moon Nights)",
                "religion_or_type": "Tribal / Harvest", "is_featured": False,
                "significance": "Cultural extravaganza celebrating the shimmering white salt marsh desert of the Great Rann of Kutch under the moonlight.",
                "rituals": "Tent city camping on the salt flats, moonlight camel safaris, Kutchi folk musicians playing the Surando and Morchang, artisan village visits.",
                "food": "Kutchi Dabeli, Bajra no Rotlo with garlic chutney and white butter, Khichdi-Kadhi.",
                "story": "Celebrates the resilient craft communities of Kutch: Rogan art, Ajrakh block printing, and mirror-work embroidery.",
                "hero_image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80",
                "states": ["Gujarat"]
            },
            {
                "name": "Ganesh Chaturthi", "month": 9, "approximate_dates": "August - September (Bhadrapada Shukla Chaturthi)",
                "religion_or_type": "Hinduism", "is_featured": True,
                "significance": "The welcoming of Lord Ganesha, remover of obstacles and patron of intellect, learning, and new beginnings.",
                "rituals": "Installation of clay Ganesha murtis in homes and giant public pandals (like Lalbaugcha Raja), chanting 'Ganpati Bappa Morya', and joyous Visarjan immersions with Lezim dances.",
                "food": "Steamed Ukadiche Modak (rice flour dumplings stuffed with fresh grated coconut and jaggery), Puran Poli, Karanji.",
                "story": "Nationalized as a mass public festival by freedom fighter Bal Gangadhar Tilak in 1893 to unite people across caste and creed against colonial rule.",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80",
                "states": ["Maharashtra", "Goa", "Karnataka", "Telangana"]
            },
            {
                "name": "Eid ul-Fitr", "month": 4, "approximate_dates": "Shawwal (Date varies with sighting of the crescent moon)",
                "religion_or_type": "Islam", "is_featured": False,
                "significance": "The blessed festival of breaking the fast, marking the culmination of the holy month of Ramadan and thanking Allah for strength and spiritual discipline.",
                "rituals": "Congregational Eid prayers at Jama Masjids, giving Zakat al-Fitr charity to the underprivileged, wearing new attires, and greeting with warm embraces of 'Eid Mubarak'.",
                "food": "Sheer Khurma (vermicelli pudding with dates and nuts), aromatic Mutton Dum Biryani, Shahi Tukda, Kebabs.",
                "story": "Instituted by the Prophet Muhammad in Medina; in India, it reflects centuries of syncretic Ganga-Jamuni Tehzeeb.",
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80",
                "states": ["Delhi (NCT)", "Uttar Pradesh", "Telangana", "Jammu and Kashmir", "West Bengal"]
            },
            {
                "name": "Hemis Festival", "month": 7, "approximate_dates": "June - July (Tsechu 10th day)",
                "religion_or_type": "Buddhism", "is_featured": False,
                "significance": "Ladakh's most vibrant monastic festival, celebrating the birth anniversary of Guru Padmasambhava (Guru Rinpoche), who brought Vajrayana Buddhism to the Himalayas.",
                "rituals": "Lamas perform the sacred Cham masked dance in the courtyard of Hemis Gompa, accompanied by long copper horns, cymbals, and drums; unveiling of gigantic silk thangkas.",
                "food": "Hot Butter Tea (Gur Gur Chai), steamed meat and vegetable Tingmo, Thukpa soup.",
                "story": "The victory of enlightened wisdom over demonic spirits and internal ego, enacted by lamas donning colorful brocade robes and hand-carved wooden masks.",
                "hero_image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=1200&q=80",
                "states": ["Ladakh"]
            },
            {
                "name": "Navratri & Garba", "month": 10, "approximate_dates": "September - October (Ashwin Shukla Pratipada)",
                "religion_or_type": "Hinduism", "is_featured": False,
                "significance": "Nine sacred nights worshipping the nine manifestations of Goddess Durga (Navadurga), recognized by UNESCO for its living community dance traditions.",
                "rituals": "Dussehra Garba and Dandiya Raas circles danced by thousands in mirrored Chaniya Cholis around the glowing Garbha lamp.",
                "food": "Farali fasting delicacies: Sabudana Khichdi, Kuttu ki Puri, Singhara Halwa, Makhana Kheer.",
                "story": "Celebrates the cosmic nine-day battle where Devi Durga systematically destroyed demonic negative forces to restore cosmic equilibrium.",
                "hero_image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80",
                "states": ["Gujarat", "Maharashtra", "Rajasthan"]
            },
            {
                "name": "Chhath Puja", "month": 11, "approximate_dates": "October - November (Kartik Shukla Shashthi)",
                "religion_or_type": "Hinduism", "is_featured": False,
                "significance": "An ancient Vedic festival of deep gratitude dedicated to Surya (the Sun God) and his sister Chhathi Maiya for sustaining life and healing illness.",
                "rituals": "Strict 36-hour waterless fast (Nirjala), standing waist-deep in holy rivers to offer Arghya to the setting and rising sun, carrying bamboo soop offerings.",
                "food": "Thekua (traditional whole wheat and jaggery cookies fried in pure ghee), sugarcane, seasonal fruits.",
                "story": "Mentioned in the Mahabharata where Draupadi and the Pandavas observed Chhath to regain their lost kingdom, and by Karna who worshipped the Sun.",
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80",
                "states": ["Bihar", "Uttar Pradesh", "Jharkhand", "Delhi (NCT)"]
            },
            {
                "name": "Baisakhi (Vaisakhi)", "month": 4, "approximate_dates": "April 13 - 14",
                "religion_or_type": "Sikhism", "is_featured": False,
                "significance": "Major harvest festival across Punjab marking the birth of the Khalsa Panth established by the tenth Sikh Guru, Guru Gobind Singh in 1699.",
                "rituals": "Nagar Kirtan street processions led by the Panj Pyare, continuous Akhand Path recitation of the Guru Granth Sahib at Gurdwaras, energetic Bhangra and Gidda.",
                "food": "Kada Prasad (sacred wheat flour and ghee sweet), Langar dal and roti, Makki di Roti with butter.",
                "story": "In 1699 at Anandpur Sahib, Guru Gobind Singh baptized five volunteers as the first five Khalsa warriors, instilling courage against tyranny.",
                "hero_image": "https://images.unsplash.com/photo-1517821099606-cef63a9bcab6?auto=format&fit=crop&w=1200&q=80",
                "states": ["Punjab", "Haryana", "Delhi (NCT)"]
            },
            {
                "name": "Kumbh Mela", "month": 1, "approximate_dates": "Cyclic every 3, 6, and 12 years (Purna Kumbh & Maha Kumbh)",
                "religion_or_type": "Hinduism", "is_featured": True,
                "significance": "UNESCO Intangible Cultural Heritage: the largest peaceful gathering of humanity on earth, held rotationally at Prayagraj, Haridwar, Ujjain, and Nashik.",
                "rituals": "Shahi Snan (Royal Dips) at the Sangam confluence by Akharas of Naga Sadhus at astrologically auspicious moments to cleanse past karma.",
                "food": "Mass community langars serving simple satvik Khichdi, Puri Sabzi, and hot milk.",
                "story": "During the churning of the cosmic ocean (Samudra Manthan), four drops of the nectar of immortality (Amrita) spilled onto the four sacred riverbanks.",
                "hero_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
                "states": ["Uttar Pradesh", "Uttarakhand", "Madhya Pradesh", "Maharashtra"]
            },
            {
                "name": "Mysore Dasara", "month": 10, "approximate_dates": "September - October (Vijayadashami)",
                "religion_or_type": "Hinduism", "is_featured": False,
                "significance": "The grand royal festival of Karnataka celebrating Goddess Chamundeshwari's victory over the demon Mahishasura.",
                "rituals": "Mysore Palace illuminated with over 100,000 electric bulbs; grand Jumboo Savari procession with a decorated lead elephant carrying the golden howdah.",
                "food": "Mysore Pak (melt-in-mouth chickpea fudge made with pure ghee), Kosambari, Bisi Bele Bath.",
                "story": "Celebrated since the 14th century by Vijayanagara emperors and continued uninterrupted by the royal Wodeyar dynasty of Mysore.",
                "hero_image": "https://images.unsplash.com/photo-1600100397608-f010f443b719?auto=format&fit=crop&w=1200&q=80",
                "states": ["Karnataka"]
            },
            {
                "name": "Thrissur Pooram", "month": 5, "approximate_dates": "April - May (Medam Month under Pooram star)",
                "religion_or_type": "Hinduism", "is_featured": False,
                "significance": "The most spectacular temple festival in Kerala, featuring a battle of vibrant sequined parasols and thunderous percussion.",
                "rituals": "Kudamattom (rapid synchronization of ornate silk umbrellas atop caparisoned elephants) and the Ilanjithara Melam percussion ensemble with over 250 traditional drummers.",
                "food": "Traditional Kerala sadya feast, Ela Ada, sweet tender coconut water.",
                "story": "Founded in 1798 by Raja Rama Varma (Sakthan Thampuran), ruler of Cochin, to unite ten local temples in a friendly artistic rivalry.",
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
                "states": ["Kerala"]
            },
            {
                "name": "Puri Ratha Yatra (Chariot Festival)", "month": 6, "approximate_dates": "June - July (Ashadha Shukla Dwitiya)",
                "religion_or_type": "Hinduism", "is_featured": True,
                "significance": "The annual sojourn of Lord Jagannath, his brother Balabhadra, and sister Subhadra from their sanctum to the Gundicha Temple.",
                "rituals": "Millions pull colossal wooden chariots by thick ropes (Nandighosha, Taladhwaja, Darpadalana); the King of Puri performs Chera Pahara (sweeping the chariots with a golden broom).",
                "food": "Mahaprasad: Chhappan Bhog cooked in clay pots stacked on wood fires, Khaja sweet crisps.",
                "story": "Demonstrates that before God, even the monarch is a humble sweeper, and the deity leaves the temple so all humanity can behold him.",
                "hero_image": "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&w=1200&q=80",
                "states": ["Odisha"]
            },
            {
                "name": "Losar (Tibetan New Year)", "month": 2, "approximate_dates": "February (First day of Tibetan Lunisolar Year)",
                "religion_or_type": "Buddhism", "is_featured": False,
                "significance": "The welcoming of the Himalayan Buddhist New Year, purifying the environment and invoking blessings for prosperity and peace.",
                "rituals": "Metho fire procession to drive away malevolent spirits, lighting butter lamps at monasteries, offering Khatag white silk scarves, raising colorful prayer flags.",
                "food": "Khapse deep-fried pastries, Guthuk medicinal nine-ingredient noodle soup, chang barley wine.",
                "story": "Pre-Buddhist Bon tradition evolved into a major Buddhist renewal celebration across Ladakh, Sikkim, and Himachal Pradesh.",
                "hero_image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=1200&q=80",
                "states": ["Ladakh", "Sikkim", "Himachal Pradesh"]
            }
        ]

        for f_data in festivals_data:
            state_names = f_data.pop("states", [])
            slug = slugify(f_data["name"])
            if slug in IMAGE_METADATA.get("festivals", {}):
                m = IMAGE_METADATA["festivals"][slug]
                f_data["hero_image"] = m["filename"]
                f_data["image_credit"] = m["author"]
                f_data["image_source_url"] = m["source_url"]
                f_data["image_license"] = m["license"]
            fest_obj, _ = Festival.objects.update_or_create(
                name=f_data["name"],
                defaults=f_data
            )
            for s_name in state_names:
                if s_name in state_objs:
                    fest_obj.states.add(state_objs[s_name])

        self.stdout.write(self.style.SUCCESS("[OK] Seeded 20+ Cultural Festivals across India"))

        # 5. Seed 20+ Art Forms & Crafts
        arts_data = [
            {
                "name": "Kathak", "category": "Dance", "origin_state": "Uttar Pradesh",
                "unesco_intangible": False,
                "history": "Traces its origin to the ancient nomadic traveling bards (Kathakars) of North India who recited stories from the epics using gestures and music. Later flourished in Mughal royal courts and Lucknow darbars.",
                "description": "Characterized by mesmerizing lightning-fast spins (chakkars), complex mathematical footwork (tatkar), rhythmically striking ankle bells (ghungroos), and subtle facial expressions (abhinaya).",
                "famous_practitioners": "Pandit Birju Maharaj, Sitara Devi, Shambhu Maharaj, Lachhu Maharaj, Saswati Sen",
                "hero_image": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Bharatanatyam", "category": "Dance", "origin_state": "Tamil Nadu",
                "unesco_intangible": False,
                "history": "One of the oldest classical dance traditions in India, codified in Bharata Muni's Natya Shastra. Originally practiced in Dravidian temples by Devadasis as a sacred spiritual offering.",
                "description": "Famous for geometric body postures (aramandi), crisp rhythmic footwork (adavus), intricate mudras (hand gestures), and dramatic narrative expressiveness based on Carnatic ragas.",
                "famous_practitioners": "Rukmini Devi Arundale, Balasaraswati, Yamini Krishnamurthy, Padma Subrahmanyam",
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Kathakali", "category": "Dance", "origin_state": "Kerala",
                "unesco_intangible": True,
                "history": "A 17th-century classical dance-drama originating in temple courtyards and royal palaces of Kerala, synthesizing martial arts (Kalaripayattu) and ancient Sanskrit theater.",
                "description": "Famed for its elaborate green and red facial makeup (Chutti), towering headgears (Kireedam), heavy flared costumes, and extraordinary control of eye and eyebrow movements depicting epics.",
                "famous_practitioners": "Kalamandalam Gopi, Guru Kunchu Kurup, Kalamandalam Krishnan Nair",
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Odissi", "category": "Dance", "origin_state": "Odisha",
                "unesco_intangible": False,
                "history": "Rooted in the ancient temple sculptures of Konark and Jagannath Puri. Practiced historically by the Maharis (temple dancers) and Gotipuas (young male acolytes).",
                "description": "Distinguished by the sensual Tribhangi posture (three-bend deflection of head, torso, and hips echoing temple statuary), lyrical movements, and silver filigree ornaments.",
                "famous_practitioners": "Kelucharan Mohapatra, Sanjukta Panigrahi, Madhavi Mudgal, Sujata Mohapatra",
                "hero_image": "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Manipuri Raas Leela", "category": "Dance", "origin_state": "Manipur",
                "unesco_intangible": False,
                "history": "Rooted in the Vaishnavite spiritual movement introduced in Manipur in the 18th century under King Bhagyachandra.",
                "description": "Characterized by gentle, swaying, serpentine movements that flow seamlessly without abrupt foot-strikes. Dancers wear barrel-shaped stiff cylindrical skirts (Kumil) studded with mirrors.",
                "famous_practitioners": "Guru Bipin Singh, Jhaveri Sisters (Nayna, Suverna, Ranjana, Darshana), Charu Mathur",
                "hero_image": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Madhubani (Mithila) Painting", "category": "Painting", "origin_state": "Bihar",
                "unesco_intangible": False,
                "history": "Practiced for centuries by women in the Mithila region. Traditionally painted on mud walls during weddings and births; according to legend, King Janaka commissioned artists for Sita's wedding.",
                "description": "Created using natural vegetable pigments, twigs, brushes, and matchsticks. Defined by bold geometric lines, fish-scale textures, double-borders, and themes of nature and epics.",
                "famous_practitioners": "Ganga Devi, Mahasundari Devi, Sita Devi, Baua Devi",
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Warli Tribal Art", "category": "Painting", "origin_state": "Maharashtra",
                "unesco_intangible": False,
                "history": "One of India's oldest living folk painting traditions, practiced by the Warli tribe residing in the northern Sahyadri range, dating back to 2500–3000 BCE.",
                "description": "Executed using simple white paste made from rice flour, water, and gum against reddish-brown mud plaster walls. Composed of elementary geometric shapes: circles (sun/moon), triangles, and squares.",
                "famous_practitioners": "Jivya Soma Mashe, Balu Mashe, Rajesh Vangad",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Pattachitra Scroll Painting", "category": "Painting", "origin_state": "Odisha",
                "unesco_intangible": False,
                "history": "Ancient cloth-based scroll painting originating in Raghurajpur heritage village, deeply bound to the worship of Lord Jagannath.",
                "description": "Painted on specially treated cotton cloth layered with tamarind seed glue and chalk paste. Employs 100% natural stone and mineral pigments, finished with natural tree resin varnish.",
                "famous_practitioners": "Rabindra Behera, Sarat Chandra Swain, Akshaya Kumar Barik",
                "hero_image": "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Kalamkari Textile Art", "category": "Textile", "origin_state": "Andhra Pradesh",
                "unesco_intangible": False,
                "history": "Derived from the Persian words 'qalam' (pen) and 'kari' (craftsmanship). Flourished under Golconda rulers and Nayaka patrons in Srikalahasti and Machilipatnam.",
                "description": "Hand-painted or block-printed cotton textile art using fermented jaggery, alum, and natural dyes from madder roots, myrobalan nuts, and indigo.",
                "famous_practitioners": "Jonnalagadda Gurappa Chetty, Niranjan Chetty, J. Lakshmaiah",
                "hero_image": "https://images.unsplash.com/photo-1627894483216-2138af692e32?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Bandhani (Tie & Dye)", "category": "Textile", "origin_state": "Gujarat",
                "unesco_intangible": False,
                "history": "Evidence of Bandhani dyeing dates back to the Indus Valley Civilization and 6th-century paintings at Ajanta Caves. Flourished in Jamnagar, Bhuj, and Rajasthan.",
                "description": "Skilled artisans pluck tiny portions of silk or cotton with fingernails and bind them tightly with thread before immersion in vibrant natural dye baths to create intricate geometric motifs.",
                "famous_practitioners": "Khatri community masters of Kutch and Jamnagar",
                "hero_image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Tanjore Gold Foil Painting", "category": "Painting", "origin_state": "Tamil Nadu",
                "unesco_intangible": False,
                "history": "Flourished in the royal town of Thanjavur in the 16th century under the patronage of the Maratha rulers of Tanjore.",
                "description": "Characterized by dense compositions, three-dimensional gesso relief work studded with semi-precious Jaipur gems, and overlay of pure 22-karat gold foil leaves.",
                "famous_practitioners": "Raja Ravi Varma (inspired), Master artisans of Thanjavur and Tiruchirappalli",
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Jaipur Blue Pottery", "category": "Craft", "origin_state": "Rajasthan",
                "unesco_intangible": False,
                "history": "Turko-Persian craft brought to India during the Mughal era and revived dramatically by Sawai Ram Singh II of Jaipur in the 19th century.",
                "description": "Unique among world ceramics because it does not use clay. Made from ground quartz stone, Fuller's earth (Multani mitti), glass, and natural gum, painted with cobalt blue and copper oxide.",
                "famous_practitioners": "Kripal Singh Shekhawat, Leela Bordia",
                "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Channapatna Wooden Toys", "category": "Craft", "origin_state": "Karnataka",
                "unesco_intangible": False,
                "history": "Protected by Geographical Indication (GI). Tipu Sultan invited master toy artisans from Persia to train local artisans in the town of Channapatna in the 18th century.",
                "description": "Hand-lathed from soft ivory wood (Wrightia tinctoria), buffed with natural non-toxic vegetable dyes extracted from turmeric, indigo, and katha, and polished with screwpine leaves.",
                "famous_practitioners": "Artisan clusters of Channapatna 'Gombegala Ooru' (Toy Town)",
                "hero_image": "https://images.unsplash.com/photo-1600100397608-f010f443b719?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Dhokra Bell Metal Casting", "category": "Craft", "origin_state": "Chhattisgarh",
                "unesco_intangible": False,
                "history": "An unbroken 4,000-year-old lost-wax casting (cire perdue) tradition dating directly back to the famous 'Dancing Girl of Mohenjo-Daro'.",
                "description": "Practiced by indigenous metalsmiths (Ghadwa community) using beeswax threads wrapped around clay cores, covered with termite hill mud molds, and poured with molten bronze.",
                "famous_practitioners": "Jaidev Baghel, Rajendra Baghel, Bastar craft guilds",
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Pashmina & Kani Shawl Weaving", "category": "Textile", "origin_state": "Jammu and Kashmir",
                "unesco_intangible": False,
                "history": "Introduced to Kashmir in the 14th century by Persian mystic Mir Sayyid Ali Hamadani and nurtured under Sultan Zain-ul-Abidin and Mughal Emperor Akbar.",
                "description": "Woven on wooden pit-looms using ultra-fine underfleece combed from Changthangi mountain goats grazing above 14,000 feet in Ladakh. Kani shawls employ tiny wooden needle-bobbins.",
                "famous_practitioners": "Master weavers of Srinagar and Kanihama",
                "hero_image": "https://images.unsplash.com/photo-1595846519845-68e298c2edd8?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Phulkari Embroidery", "category": "Textile", "origin_state": "Punjab",
                "unesco_intangible": False,
                "history": "Literally meaning 'flower work', immortalized in the Punjabi folk romance of Heer Ranjha. Embroidered by grandmothers and mothers for bridal trousseaus.",
                "description": "Embroidered from the reverse side of handspun coarse khaddar cotton fabric using untwisted pure pat silk threads in damask and darning stitches.",
                "famous_practitioners": "Rural artisan cooperatives of Patiala, Bathinda, and Amritsar",
                "hero_image": "https://images.unsplash.com/photo-1517821099606-cef63a9bcab6?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Koodiyattam Sanskrit Theatre", "category": "Theatre", "origin_state": "Kerala",
                "unesco_intangible": True,
                "history": "UNESCO recognized as a Masterpiece of the Oral and Intangible Heritage of Humanity. World's oldest surviving Sanskrit theater tradition, over 1,800 years old.",
                "description": "Staged inside traditional temple theater halls (Koothambalam). Features highly stylized eye movements, mudras, vocal recitations in ancient Prakrit, and Mizhavu percussion drums.",
                "famous_practitioners": "Mani Madhava Chakyar, Ammannur Madhava Chakyar, Margi Sathi",
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Yakshagana", "category": "Theatre", "origin_state": "Karnataka",
                "unesco_intangible": False,
                "history": "A dynamic 500-year-old theatrical folk art originating in coastal and Malenadu regions of Karnataka, enacting episodes from the Ramayana and Mahabharata.",
                "description": "Combines vigorous dance steps, booming Chande and Maddale percussion, high-pitched vocal dialogue, and majestic towering crowns (Mundasu).",
                "famous_practitioners": "Keremane Shambhu Hegde, Chittani Ramachandra Hegde",
                "hero_image": "https://images.unsplash.com/photo-1600100397608-f010f443b719?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Hindustani Classical Music", "category": "Music", "origin_state": "Uttar Pradesh",
                "unesco_intangible": False,
                "history": "North Indian classical musical tradition shaped by ancient Vedic chanting, Persian modal influences, and court masters like Tansen in Akbar's court.",
                "description": "Explores spiritual microtones (shrutis) and melodic frameworks (ragas) across seasonal times of day, utilizing sitar, sarod, bansuri, tabla, and tanpura.",
                "famous_practitioners": "Ustad Bismillah Khan, Pandit Ravi Shankar, Ustad Zakir Hussain, Kishori Amonkar, Pandit Bhimsen Joshi",
                "hero_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Carnatic Classical Music", "category": "Music", "origin_state": "Tamil Nadu",
                "unesco_intangible": False,
                "history": "South Indian classical musical tradition codified by Purandara Dasa (the father of Carnatic music) and the holy Trinity: Tyagaraja, Muthuswami Dikshitar, and Syama Sastri.",
                "description": "Intellectually rigorous and spiritually devotional (Bhakti), built on complex mathematical tala rhythms, kriti compositions, mridangam, veena, and violin.",
                "famous_practitioners": "M. S. Subbulakshmi, M. Balamuralikrishna, L. Subramaniam, Bombay Jayashri",
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
            }
        ]

        for a_data in arts_data:
            state_name = a_data.pop("origin_state")
            state_obj = state_objs.get(state_name)
            slug = slugify(a_data["name"])
            if slug in IMAGE_METADATA.get("arts", {}):
                m = IMAGE_METADATA["arts"][slug]
                a_data["hero_image"] = m["filename"]
                a_data["image_credit"] = m["author"]
                a_data["image_source_url"] = m["source_url"]
                a_data["image_license"] = m["license"]
            ArtForm.objects.update_or_create(
                name=a_data["name"],
                defaults={**a_data, "origin_state": state_obj}
            )

        self.stdout.write(self.style.SUCCESS("[OK] Seeded 20+ Art Forms, Dances, Crafts & Music Traditions"))

        # 6. Seed 20+ Regional Dishes & Cuisines
        cuisine_data = [
            {
                "name": "Hyderabadi Dum Biryani", "state": "Telangana", "veg_or_non_veg": "non-veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "1 hour 45 mins",
                "ingredients": "Aged long-grain Basmati rice, marinated tender mutton, saffron-infused milk, fried golden onions (birista), fresh mint, whole cardamom and star anise.",
                "story": "Born in the royal royal kitchens of the Nizams of Hyderabad, blending Mughal Persian royal pilaf traditions with Andhra's fiery spices in a dough-sealed copper handi cooked on slow charcoal (dum).",
                "hero_image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Crispy Masala Dosa & Sambar", "state": "Karnataka", "veg_or_non_veg": "veg",
                "meal_type": "Breakfast / Snack", "spice_level": "Mild", "cooking_time": "30 mins",
                "ingredients": "Naturally fermented rice and urad dal batter, spiced potato palya, shallots, curry leaves, mustard seeds, fresh coconut chutney, and piping-hot lentil sambar.",
                "story": "Originating in the temple town of Udupi, perfected across heritage cafes in Bengaluru. The paper-thin crêpe is smeared with red chili-garlic paste and clarified butter (ghee).",
                "hero_image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Kashmiri Wazwan Rogan Josh", "state": "Jammu and Kashmir", "veg_or_non_veg": "non-veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "1 hour 15 mins",
                "ingredients": "Tender lamb shanks slow-braised in brown onion paste, yogurt, Kashmiri dried red chilies, fennel powder, and dried ginger (sonth).",
                "story": "Crown jewel of the 36-course royal Kashmiri Wazwan feast, introduced by Central Asian chefs during the Mughal reign of Emperor Akbar in the Kashmir valley.",
                "hero_image": "https://images.unsplash.com/photo-1545247181-516773ca838b?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Bihari Litti Chokha", "state": "Bihar", "veg_or_non_veg": "veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "45 mins",
                "ingredients": "Whole wheat flour dough balls stuffed with roasted gram flour (sattu), ajwain, kalonji, mustard oil, paired with fire-roasted eggplant, tomato, and potato chokha, drenched in cow ghee.",
                "story": "Ancient nutritional staple of Magadha warriors and travelers, noted for exceptional shelf-life and sustained energy. Roasted over cow-dung cake fires for rustic smoky flavor.",
                "hero_image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Gujarati Khaman Dhokla", "state": "Gujarat", "veg_or_non_veg": "veg",
                "meal_type": "Breakfast / Snack", "spice_level": "Mild", "cooking_time": "25 mins",
                "ingredients": "Steamed fermented gram flour (besan), tempered with mustard seeds, green chilies, curry leaves, sesame seeds, and topped with fresh grated coconut and coriander.",
                "story": "Pinnacle of Gujarat's delicate balance of sweet, tangy, and savory flavors, celebrated for its spongy, feather-light texture and healthy oil-free steaming method.",
                "hero_image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Rajasthani Dal Baati Churma", "state": "Rajasthan", "veg_or_non_veg": "veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "1 hour",
                "ingredients": "Hard wheat flour baati balls baked over coals, crushed and drowned in pure ghee, served with panchmel dal (five lentils) and sweet jaggery cardamom churma.",
                "story": "Originated during the founding of Mewar by Rawal Bappa in the 8th century, requiring minimal water in the desert and providing immense caloric vitality for Rajput warriors.",
                "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Bengali Shorshe Machher Jhol", "state": "West Bengal", "veg_or_non_veg": "non-veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "35 mins",
                "ingredients": "Fresh freshwater Rohu or Hilsa (Ilish) fish cutlets, stone-ground pungent mustard paste, green chilies, turmeric, nigella seeds (kalo jeere), cooked in pure virgin mustard oil.",
                "story": "Soul food of every Bengali household, immortalized in literature and songs. The sharp punch of freshly ground mustard seed paste pairs with steaming parboiled Gobindobhog rice.",
                "hero_image": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Makki di Roti & Sarson ka Saag", "state": "Punjab", "veg_or_non_veg": "veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "1 hour",
                "ingredients": "Fresh winter mustard greens (sarson), bathua, and spinach simmered and mashed in an earthen handi, served with flatbread of yellow cornmeal, homemade white butter, and jaggery.",
                "story": "The quintessential agricultural winter feast of rural Punjab, celebrated during Lohri after days spent harvesting mustard fields under sunny skies.",
                "hero_image": "https://images.unsplash.com/photo-1517821099606-cef63a9bcab6?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Mumbai Pav Bhaji", "state": "Maharashtra", "veg_or_non_veg": "veg",
                "meal_type": "Breakfast / Snack", "spice_level": "Medium", "cooking_time": "35 mins",
                "ingredients": "Mashed potatoes, green peas, cauliflower, tomatoes simmered with aromatic pav bhaji masala on a massive flat iron tawa, served with butter-toasted pav buns, chopped onions, and lemon.",
                "story": "Invented in the 1860s as a quick midnight lunch for Mumbai cotton textile mill workers rushing between shifts during the American Civil War cotton boom.",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Appam with Vegetable Ishtu (Stew)", "state": "Kerala", "veg_or_non_veg": "veg",
                "meal_type": "Breakfast / Snack", "spice_level": "Mild", "cooking_time": "40 mins",
                "ingredients": "Bowl-shaped fermented rice batter pancakes with soft spongy centers and lacy crispy edges, served with a gentle stew of potatoes and carrots in fresh pressed coconut milk.",
                "story": "Pioneered by the ancient Saint Thomas Christian community of Kerala, combining local coconut abundance with Dutch and Portuguese colonial spice influences.",
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Maharashtrian Puran Poli", "state": "Maharashtra", "veg_or_non_veg": "veg",
                "meal_type": "Dessert / Sweet", "spice_level": "Mild", "cooking_time": "45 mins",
                "ingredients": "Thin wheat flatbread stuffed with a sweet, aromatic filling of boiled chana dal, jaggery, cardamom powder, and nutmeg, roasted with lavish pure ghee.",
                "story": "Prepared for Holi and Gudhi Padwa. Described in the 12th-century Sanskrit royal encyclopedia Manasollasa by Western Chalukya King Someshvara III.",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Hyderabadi Shahi Haleem", "state": "Telangana", "veg_or_non_veg": "non-veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "8 hours",
                "ingredients": "Tender meat, broken wheat, lentils, and rich spices pounded and slow-cooked for 8 hours into a silky paste, topped with fried onions, cashews, and fresh coriander.",
                "story": "GI-tagged culinary wonder brought to Hyderabad by the Arab diaspora during the Nizam era, eaten especially during Ramadan to break the day-long fast.",
                "hero_image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Himalayan Thukpa & Momos", "state": "Ladakh", "veg_or_non_veg": "veg",
                "meal_type": "Main Course", "spice_level": "Mild", "cooking_time": "40 mins",
                "ingredients": "Steamed thin flour dumplings stuffed with vegetables or meat, accompanied by a rich steaming herbal noodle soup infused with ginger, garlic, and coriander.",
                "story": "Comfort food of the high trans-Himalayan valleys, keeping Buddhist monks, yak herders, and caravanners warm against sub-zero mountain blizzards.",
                "hero_image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Gujarati Undhiyu", "state": "Gujarat", "veg_or_non_veg": "veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "1 hour 15 mins",
                "ingredients": "Surti papdi beans, baby eggplants, purple yam (kand), sweet potatoes, and methi muthia dumplings cooked upside-down in earthen pots with peanut-coconut masala.",
                "story": "Named from 'undhu' (meaning upside down in Gujarati), traditionally buried in an earthen pot (matka) under ground and baked with dry leaves during kite-flying festival Uttarayan.",
                "hero_image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Kolhapuri Misal Pav", "state": "Maharashtra", "veg_or_non_veg": "veg",
                "meal_type": "Breakfast / Snack", "spice_level": "Fiery", "cooking_time": "40 mins",
                "ingredients": "Sprouted moth beans cooked in a fiery spiced red gravy (kat/tarri), topped with crunchy farsan, chopped onions, fresh lime, and soft buttered pav.",
                "story": "Legendary fiery breakfast of western Maharashtra, famous for its distinct red chili kick and bold spice profile.",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Goan Bebinca Cake", "state": "Goa", "veg_or_non_veg": "veg",
                "meal_type": "Dessert / Sweet", "spice_level": "Mild", "cooking_time": "2 hours 30 mins",
                "ingredients": "Coconut milk, egg yolks, flour, sugar, and nutmeg baked laboriously layer by individual golden layer, brushed with pure ghee between turns.",
                "story": "The 'Queen of Goan desserts', invented in the 17th century by a nun named Bebiana at the Convent of Santa Monica in Old Goa.",
                "hero_image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Rajasthani Ghevar", "state": "Rajasthan", "veg_or_non_veg": "veg",
                "meal_type": "Dessert / Sweet", "spice_level": "Mild", "cooking_time": "50 mins",
                "ingredients": "Honeycomb-textured disc made from refined flour batter dropped into boiling ghee, dipped in fragrant sugar syrup, and topped with thickened rabdi, pistachios, and silver vark.",
                "story": "Traditional festival sweet made during the monsoon festival of Teej and Raksha Bandhan, requiring monsoon moisture in the air to attain its honeycomb crispness.",
                "hero_image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Kolkata Rosogolla", "state": "West Bengal", "veg_or_non_veg": "veg",
                "meal_type": "Dessert / Sweet", "spice_level": "Mild", "cooking_time": "45 mins",
                "ingredients": "Soft, spongy balls of fresh cottage cheese (chhena) kneaded and boiled in light piping hot sugar syrup until porous and delightfully juicy.",
                "story": "Perfected in 1868 by confectioner Nobin Chandra Das in Kolkata's Bagbazar neighborhood, giving Bengal its most iconic sweet ambassador.",
                "hero_image": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Old Delhi Daulat ki Chaat", "state": "Delhi (NCT)", "veg_or_non_veg": "veg",
                "meal_type": "Dessert / Sweet", "spice_level": "Mild", "cooking_time": "Overnight preparation",
                "ingredients": "Raw cow's milk whisked under cold winter night dew until ethereal clouds of sweet foam rise, garnished with saffron, pistachio crumbs, and powdered sugar (bhoora).",
                "story": "A winter delicacy made exclusively in the narrow alleys of Chandni Chowk from November to February, vanishing into the mouth like sweet, fragrant morning fog.",
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "name": "Malabar Flaky Parotta & Roast", "state": "Kerala", "veg_or_non_veg": "non-veg",
                "meal_type": "Main Course", "spice_level": "Medium", "cooking_time": "50 mins",
                "ingredients": "Multi-layered flaky spiral flatbread kneaded and slapped by master cooks on metal counters, served with a caramelized onion-coconut beef or chicken roast.",
                "story": "Icon of Malabar coastal street culinary culture, reflecting maritime interactions between Arab seafaring merchants and local spice farmers.",
                "hero_image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80"
            }
        ]

        for c_data in cuisine_data:
            state_name = c_data.pop("state")
            state_obj = state_objs.get(state_name)
            if not state_obj:
                continue
            slug = slugify(c_data["name"])
            if slug in IMAGE_METADATA.get("cuisine", {}):
                m = IMAGE_METADATA["cuisine"][slug]
                c_data["hero_image"] = m["filename"]
                c_data["image_credit"] = m["author"]
                c_data["image_source_url"] = m["source_url"]
                c_data["image_license"] = m["license"]
            CuisineDish.objects.update_or_create(
                name=c_data["name"],
                defaults={**c_data, "state": state_obj}
            )

        self.stdout.write(self.style.SUCCESS("[OK] Seeded 20+ Regional Dishes & Cuisines"))

        # 7. Seed Historical Timeline (15 Milestones from Indus Valley to Modern Era)
        timeline_data = [
            {
                "year_era": "c. 2600 – 1900 BCE", "year_numeric": -2600,
                "title": "Indus Valley (Harappan) Civilization", "category": "Ancient",
                "description": "One of the world's earliest urban civilizations flourishing along the Indus and Saraswati river basins. Pioneers in standardized weights, kiln-burnt brick architecture, grid-pattern city planning, advanced underground sanitation, and dockyards like Lothal.",
                "hero_image": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "c. 1500 – 600 BCE", "year_numeric": -1500,
                "title": "Vedic Period & Composition of Upanishads", "category": "Ancient",
                "description": "Oral composition of the four Vedas (Rig, Sama, Yajur, Atharva) and profound philosophical treatises known as the Upanishads. Emergence of classical Sanskrit, concepts of Dharma, Karma, and Vedanta philosophy.",
                "hero_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "c. 563 – 483 BCE", "year_numeric": -563,
                "title": "Age of Gautama Buddha and Lord Mahavira", "category": "Ancient",
                "description": "Era of spiritual introspection and social reform giving birth to Buddhism and Jainism. Rejection of animal sacrifices, promotion of Ahimsa (non-violence), ethical self-realization, and universal compassion across the Mahajanapadas.",
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "322 – 185 BCE", "year_numeric": -322,
                "title": "Maurya Empire & Edicts of Ashoka the Great", "category": "Ancient",
                "description": "Chandragupta Maurya and philosopher Chanakya unite the Indian subcontinent. Emperor Ashoka adopts Dhamma after the Kalinga war, erecting monumental polished stone pillars and carving edicts of peace, hospitals, and environmental conservation.",
                "hero_image": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "c. 320 – 550 CE", "year_numeric": 320,
                "title": "Golden Age of the Gupta Dynasty", "category": "Classical",
                "description": "Classical renaissance in mathematics (invention of zero and decimal system by Aryabhata), Sanskrit literature (Kalidasa's Shakuntala), metallurgy (Delhi Iron Pillar), and sublime Buddhist rock-cut murals at Ajanta.",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "c. 600 – 1200 CE", "year_numeric": 600,
                "title": "Dravidian Architectural Renaissance: Pallavas & Cholas", "category": "Classical",
                "description": "Seafaring Tamil dynasties construct majestic stone temples at Mahabalipuram and Thanjavur (Brihadisvara). Chola maritime fleets establish trade and cultural bridges across Southeast Asia, casting sublime bronze sculptures like Nataraja.",
                "hero_image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "1206 – 1526 CE", "year_numeric": 1206,
                "title": "Delhi Sultanate & Indo-Islamic Synthesis", "category": "Medieval",
                "description": "Five successive dynasties (Mamluk, Khalji, Tughlaq, Sayyid, Lodi) establish rule from Delhi. Introduction of the dome, arch, minaret, Persian historiography, and the synthesis of Hindavi language (the ancestor of modern Hindi and Urdu).",
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "1336 – 1646 CE", "year_numeric": 1336,
                "title": "Golden Vijayanagara Empire at Hampi", "category": "Medieval",
                "description": "Harihara, Bukka, and Krishnadevaraya build a flourishing cosmopolitan empire in the Deccan, patronizing Carnatic music, Sanskrit and Telugu literature, and monumental temple architecture with musical stone pillars.",
                "hero_image": "https://images.unsplash.com/photo-1600100397608-f010f443b719?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "1400 – 1700 CE", "year_numeric": 1400,
                "title": "Bhakti and Sufi Spiritual Renaissance", "category": "Medieval",
                "description": "A transformative poetic and egalitarian movement swept India: Kabir, Guru Nanak, Mirabai, Chaitanya Mahaprabhu, Tukaram, and Sufi saints like Nizamuddin Auliya preached love for the divine and universal brotherhood transcending caste and dogmas.",
                "hero_image": "https://images.unsplash.com/photo-1517821099606-cef63a9bcab6?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "1526 – 1707 CE", "year_numeric": 1526,
                "title": "Mughal Empire & Grand Monumental Architecture", "category": "Medieval",
                "description": "Founded by Babur and expanded by Akbar, Jahangir, and Shah Jahan. Age of magnificent synthesis: the Taj Mahal, Fatehpur Sikri, miniature painting ateliers, Hindustani classical ragas, and culinary refinement.",
                "hero_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "1674 – 1818 CE", "year_numeric": 1674,
                "title": "Rise of the Maratha Confederacy", "category": "Medieval",
                "description": "Chhatrapati Shivaji Maharaj establishes Hindavi Swarajya through guerrilla mountain warfare and formidable naval fortresses along the Konkan coast. Maratha power later expanded across Central and North India.",
                "hero_image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "1757 – 1857 CE", "year_numeric": 1757,
                "title": "East India Company Rule & The 1857 War of Independence", "category": "Colonial",
                "description": "From the Battle of Plassey to the Great Uprising of 1857 led by Rani Lakshmibai, Mangal Pandey, and Bahadur Shah Zafar. Following the revolt, British Crown governance was officially instituted.",
                "hero_image": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "1885 – 1947 CE", "year_numeric": 1885,
                "title": "Indian Freedom Struggle & Satyagraha", "category": "Colonial",
                "description": "Mass mobilization led by Mahatma Gandhi, Subhas Chandra Bose, Bhagat Singh, and Sardar Patel. Principles of Ahimsa (non-violence), Swadeshi hand-spun Khadi, and nationwide non-cooperation lead to the dawn of Indian Independence on August 15, 1947.",
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "26 January 1950", "year_numeric": 1950,
                "title": "Constitution of India: Sovereign Democratic Republic", "category": "Modern",
                "description": "Dr. B. R. Ambedkar and the Constituent Assembly draft the world's longest written constitution, enshrining universal adult franchise, fundamental rights, unity in diversity, and democratic secularism.",
                "hero_image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "year_era": "1950 CE – Present", "year_numeric": 2000,
                "title": "Contemporary Renaissance & Global Heritage Stewardship", "category": "Modern",
                "description": "India emerges as a leading scientific, technological, and space-faring power while actively documenting, restoring, and sharing its 42+ UNESCO World Heritage Sites and living traditions with humanity.",
                "hero_image": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80"
            }
        ]

        for t_data in timeline_data:
            TimelineEvent.objects.update_or_create(
                title=t_data["title"],
                defaults=t_data
            )

        self.stdout.write(self.style.SUCCESS("[OK] Seeded 15 Historical Timeline Milestones"))

        # 8. Seed 30+ Quiz Questions
        quiz_data = [
            {
                "question": "Which ancient rock-cut temple at Ellora was carved out of a single piece of basalt rock from top to bottom?",
                "option_a": "Brihadisvara Temple", "option_b": "Kailasa Temple (Cave 16)",
                "option_c": "Meenakshi Temple", "option_d": "Konark Sun Temple",
                "correct_option": "B", "difficulty": "Medium", "category": "Monuments",
                "explanation": "Cave 16 (The Kailasa Temple) at Ellora was carved vertically downwards from a single cliff face during the Rashtrakuta dynasty under King Krishna I, removing an estimated 200,000 tonnes of basalt rock."
            },
            {
                "question": "The world-famous Sun Temple at Konark, Odisha was designed in the architectural shape of what?",
                "option_a": "A lotus flower", "option_b": "A colossal stone chariot",
                "option_c": "A stepwell", "option_d": "A royal elephant",
                "correct_option": "B", "difficulty": "Easy", "category": "Monuments",
                "explanation": "The 13th-century Konark Sun Temple was built by King Narasimhadeva I as a gigantic chariot for Surya with 24 elaborately carved stone wheels drawn by seven galloping horses."
            },
            {
                "question": "Which of these classical Indian dance forms originated in the state of Kerala and is famous for its elaborate green face makeup (Chutti)?",
                "option_a": "Kathak", "option_b": "Bharatanatyam",
                "option_c": "Kathakali", "option_d": "Odissi",
                "correct_option": "C", "difficulty": "Easy", "category": "Arts & Music",
                "explanation": "Kathakali is Kerala's sacred classical dance-drama where actors wear dramatic green (Paccha) makeup denoting noble characters and perform intricate eye movements to percussion drums."
            },
            {
                "question": "What is the primary material used in the traditional tribal paintings of the Warli community in Maharashtra?",
                "option_a": "Gold foil and gemstones", "option_b": "White rice flour paste on mud background",
                "option_c": "Oil paint on canvas", "option_d": "Crushed lapis lazuli",
                "correct_option": "B", "difficulty": "Medium", "category": "Arts & Music",
                "explanation": "Warli tribal art uses a paste of rice flour, water, and gum painted against natural ochre/mud-plastered walls using chewed bamboo twigs as paintbrushes."
            },
            {
                "question": "The UNESCO-recognized stepwell 'Rani ki Vav' (The Queen's Stepwell) is situated in which state of India?",
                "option_a": "Rajasthan", "option_b": "Gujarat",
                "option_c": "Madhya Pradesh", "option_d": "Karnataka",
                "correct_option": "B", "difficulty": "Easy", "category": "Monuments",
                "explanation": "Rani ki Vav is located in Patan, Gujarat. Built by Queen Udayamati in memory of King Bhima I, it is an inverted subterranean temple dedicated to water sanctity with over 500 sculptures."
            },
            {
                "question": "During which sacred festival do millions of devotees celebrate the homecoming of the mythological benevolent King Mahabali?",
                "option_a": "Pongal", "option_b": "Onam",
                "option_c": "Bihu", "option_d": "Durga Puja",
                "correct_option": "B", "difficulty": "Easy", "category": "Festivals",
                "explanation": "Onam is Kerala's grand harvest festival celebrating the annual homecoming of King Mahabali, featuring floral carpets (Pookkalam) and the grand Onasadya feast."
            },
            {
                "question": "Which of the following dishes has earned a Geographical Indication (GI) tag and is slow-cooked for 8 hours in Hyderabad during Ramadan?",
                "option_a": "Haleem", "option_b": "Pav Bhaji",
                "option_c": "Litti Chokha", "option_d": "Dhokla",
                "correct_option": "A", "difficulty": "Medium", "category": "Cuisine",
                "explanation": "Hyderabadi Haleem was the first meat product in India to be granted a GI tag. It is slow-cooked for hours with broken wheat, meat, and fragrant spices until it achieves a rich, silky paste."
            },
            {
                "question": "The famous iron pillar that has resisted corrosion for over 1,600 years is situated in which monument complex?",
                "option_a": "Red Fort", "option_b": "Qutub Minar Complex",
                "option_c": "Humayun's Tomb", "option_d": "Fatehpur Sikri",
                "correct_option": "B", "difficulty": "Easy", "category": "History",
                "explanation": "The Iron Pillar of Delhi, forged during the Gupta Empire in the 4th century CE, stands in the Qutub Minar complex and is famous for its high rust-resistant phosphorus-rich metallurgy."
            },
            {
                "question": "Which emperor constructed the red sandstone city of Fatehpur Sikri in gratitude for the birth of his son?",
                "option_a": "Babur", "option_b": "Shah Jahan",
                "option_c": "Akbar the Great", "option_d": "Aurangzeb",
                "correct_option": "C", "difficulty": "Medium", "category": "History",
                "explanation": "Emperor Akbar built Fatehpur Sikri after Sufi mystic Sheikh Salim Chishti prophesied the birth of his heir Prince Salim (later Emperor Jahangir)."
            },
            {
                "question": "The 'Hornbill Festival', celebrated every December in Kisama Village, is the state festival of which northeastern state?",
                "option_a": "Assam", "option_b": "Nagaland",
                "option_c": "Meghalaya", "option_d": "Arunachal Pradesh",
                "correct_option": "B", "difficulty": "Easy", "category": "Festivals",
                "explanation": "The Hornbill Festival is held annually from December 1 to 10 in Nagaland, bringing together all 17 major Naga tribes to display their ancestral songs, warrior dances, and arts."
            },
            {
                "question": "Which ancient university in Bihar accommodated 10,000 students and had a legendary 9-story library named 'Dharmaganja'?",
                "option_a": "Takshashila", "option_b": "Nalanda",
                "option_c": "Vikramashila", "option_d": "Valabhi",
                "correct_option": "B", "difficulty": "Medium", "category": "History",
                "explanation": "Nalanda Mahavihara flourished from the 5th to the 12th century CE as a premier international Buddhist university attracting scholars from China, Korea, Japan, and Tibet."
            },
            {
                "question": "In which city is the famous 'Hall of Thousand Pillars' located inside the Meenakshi Amman Temple?",
                "option_a": "Thanjavur", "option_b": "Madurai",
                "option_c": "Kanchipuram", "option_d": "Rameshwaram",
                "correct_option": "B", "difficulty": "Medium", "category": "Monuments",
                "explanation": "The Meenakshi Amman Temple in Madurai, Tamil Nadu features the iconic Hall of Thousand Pillars (Ayiram Kaal Mandapam) built in 1569 with intricately carved mythological figures."
            },
            {
                "question": "What is the staple dough ball of roasted gram flour (sattu) celebrated as the quintessential heritage comfort food of Bihar?",
                "option_a": "Thekua", "option_b": "Litti",
                "option_c": "Chokha", "option_d": "Khaja",
                "correct_option": "B", "difficulty": "Easy", "category": "Cuisine",
                "explanation": "Litti is made from whole wheat balls stuffed with sattu (roasted gram flour seasoned with carom, nigella, and mustard oil), roasted over cow-dung coals and served with Chokha."
            },
            {
                "question": "The Dhokra metal casting technique, practiced in Bastar, Chhattisgarh, uses which ancient casting method?",
                "option_a": "Sand mold casting", "option_b": "Lost-wax casting (Cire perdue)",
                "option_c": "Die casting", "option_d": "Centrifugal casting",
                "correct_option": "B", "difficulty": "Hard", "category": "Arts & Music",
                "explanation": "Dhokra casting is an unbroken 4,000-year-old lost-wax (cire perdue) technique, tracing its ancestry directly to the famous 'Dancing Girl' bronze found at Mohenjo-Daro."
            },
            {
                "question": "Which musical genius of Akbar's court is credited with creating legendary ragas like Darbari Kanada and Miyan ki Malhar?",
                "option_a": "Amir Khusrau", "option_b": "Swami Haridas",
                "option_c": "Miyan Tansen", "option_d": "Baiju Bawra",
                "correct_option": "C", "difficulty": "Medium", "category": "Arts & Music",
                "explanation": "Miyan Tansen was one of the Navaratnas (Nine Gems) in Akbar's court, renowned for his profound musical compositions and mastery over Hindustani classical ragas."
            },
            {
                "question": "The Pattachitra scroll painting style is predominantly indigenous to which eastern Indian state?",
                "option_a": "Bihar", "option_b": "Odisha",
                "option_c": "Jharkhand", "option_d": "Assam",
                "correct_option": "B", "difficulty": "Easy", "category": "Arts & Music",
                "explanation": "Pattachitra is a traditional cloth-based scroll painting originating in Odisha (especially the artisan village of Raghurajpur), depicting Lord Jagannath and Krishna legends with natural dyes."
            },
            {
                "question": "Under which sacred tree in Bodh Gaya, Bihar did Siddhartha Gautama attain supreme enlightenment to become the Buddha?",
                "option_a": "Banyan tree (Ficus benghalensis)", "option_b": "Bodhi tree (Ficus religiosa / Sacred Fig)",
                "option_c": "Neem tree", "option_d": "Sal tree",
                "correct_option": "B", "difficulty": "Easy", "category": "History",
                "explanation": "Siddhartha Gautama attained supreme enlightenment under the sacred Bodhi tree (Ficus religiosa) at Bodh Gaya in c. 531 BCE."
            },
            {
                "question": "Which famous fort in Rajasthan is nicknamed the 'Golden Fort' (Sonar Qila) because of its yellow sandstone bastions glowing in the desert sun?",
                "option_a": "Mehrangarh Fort", "option_b": "Jaisalmer Fort",
                "option_c": "Chittorgarh Fort", "option_d": "Kumbhalgarh Fort",
                "correct_option": "B", "difficulty": "Easy", "category": "Monuments",
                "explanation": "Jaisalmer Fort, built by Rawal Jaisal in 1156 CE in the heart of the Thar Desert, is called Sonar Qila because its yellow sandstone glows like burnished gold."
            },
            {
                "question": "Koodiyattam, recognized by UNESCO as a masterpiece of oral and intangible heritage, is the world's oldest surviving tradition of what?",
                "option_a": "Puppetry theater", "option_b": "Sanskrit temple theater",
                "option_c": "Martial arts combat", "option_d": "Shadow dance",
                "correct_option": "B", "difficulty": "Hard", "category": "Arts & Music",
                "explanation": "Koodiyattam is Kerala's ancient Sanskrit temple theater tradition, over 1,800 years old, traditionally staged inside temple Koothambalam halls."
            },
            {
                "question": "The famous sweet dish 'Mysore Pak' is prepared primarily from which combination of ingredients?",
                "option_a": "Condensed milk and pistachios", "option_b": "Chickpea flour (besan), pure ghee, and sugar",
                "option_c": "Semolina and jaggery", "option_d": "Grated coconut and nutmeg",
                "correct_option": "B", "difficulty": "Medium", "category": "Cuisine",
                "explanation": "Mysore Pak was created by royal chef Kakasura Madappa in the kitchens of the Mysore Palace using chickpea flour (besan), generous amounts of pure ghee, and sugar syrup."
            },
            {
                "question": "What is the primary theme celebrated during the vibrant harvest festival of 'Bihu' in Assam?",
                "option_a": "The onset of monsoons", "option_b": "The Assamese agricultural season and spring renewal",
                "option_c": "Worship of the serpent god", "option_d": "Victory in battle",
                "correct_option": "B", "difficulty": "Medium", "category": "Festivals",
                "explanation": "Rongali Bihu marks the Assamese New Year in mid-April, celebrating the arrival of spring, seeding of crops, and community joy with music played on the Pepa horn."
            },
            {
                "question": "Which Indian city is celebrated as the birthplace of modern polo (Sagol Kangjei)?",
                "option_a": "Jaipur", "option_b": "Imphal (Manipur)",
                "option_c": "Jodhpur", "option_d": "Hyderabad",
                "correct_option": "B", "difficulty": "Hard", "category": "History",
                "explanation": "Manipur is recognized worldwide as the birthplace of modern polo, where the game has been played for centuries as 'Sagol Kangjei' on indigenous Manipuri ponies."
            },
            {
                "question": "The monumental Brihadisvara Temple at Thanjavur was built during the reign of which emperor?",
                "option_a": "Raja Raja Chola I", "option_b": "Rajendra Chola I",
                "option_c": "Narasimhavarman II", "option_d": "Pulakeshin II",
                "correct_option": "A", "difficulty": "Medium", "category": "Monuments",
                "explanation": "Emperor Raja Raja Chola I commissioned the Brihadisvara Temple (Peruvudaiyar Kovil) in 1010 CE to commemorate the golden zenith of the Chola Empire."
            },
            {
                "question": "Which craft tradition in Karnataka involves hand-turning ivory wood on lathes and polishing with organic vegetable dyes?",
                "option_a": "Bidriware", "option_b": "Channapatna Toys",
                "option_c": "Kinnal craft", "option_d": "Sandalwood carving",
                "correct_option": "B", "difficulty": "Easy", "category": "Arts & Music",
                "explanation": "Channapatna toys are hand-lathed from soft Wrightia tinctoria wood and polished with non-toxic lac vegetable dyes in Karnataka's 'Toy Town'."
            },
            {
                "question": "The Chhath Puja festival involves offering prayers (Arghya) to which natural celestial body?",
                "option_a": "The Full Moon", "option_b": "The Rising and Setting Sun (Surya)",
                "option_c": "The Morning Star (Venus)", "option_d": "The Pole Star",
                "correct_option": "B", "difficulty": "Easy", "category": "Festivals",
                "explanation": "Chhath Puja is an ancient Vedic festival where devotees stand in holy water to offer Arghya to both the setting sun and the rising sun, honoring Surya for sustaining life."
            },
            {
                "question": "The multi-layered Goan dessert 'Bebinca' is traditionally baked with which distinct flavor ingredient?",
                "option_a": "Rose water", "option_b": "Coconut milk and nutmeg",
                "option_c": "Saffron and cardamom", "option_d": "Almond paste",
                "correct_option": "B", "difficulty": "Medium", "category": "Cuisine",
                "explanation": "Bebinca is a multi-layered Indo-Portuguese pudding made from coconut milk, egg yolks, flour, sugar, and nutmeg, baked painstakingly layer by golden layer."
            },
            {
                "question": "Which historic treaty or declaration marked India's transformation into a Sovereign Democratic Republic?",
                "option_a": "Indian Independence Act 1947", "option_b": "Adoption of the Constitution on 26 January 1950",
                "option_c": "Poona Pact 1932", "option_d": "Simla Agreement",
                "correct_option": "B", "difficulty": "Easy", "category": "History",
                "explanation": "On January 26, 1950, the Constitution of India came into effect, establishing India as an independent Sovereign Democratic Republic."
            },
            {
                "question": "Which famous classical musician was affectionately honored as the 'Nightingale of Carnatic Music' and was the first musician awarded the Bharat Ratna?",
                "option_a": "Lata Mangeshkar", "option_b": "M. S. Subbulakshmi",
                "option_c": "Kishori Amonkar", "option_d": "Begum Akhtar",
                "correct_option": "B", "difficulty": "Medium", "category": "Arts & Music",
                "explanation": "Madurai Shanmukhavadivu Subbulakshmi (M. S. Subbulakshmi) was the first musician to receive India's highest civilian honor, the Bharat Ratna, in 1998."
            },
            {
                "question": "In the acoustic architecture of Golconda Fort in Hyderabad, what sound at the entrance gate can be heard at the high Bala Hissar pavilion?",
                "option_a": "A bell chime", "option_b": "A hand clap",
                "option_c": "A whisper", "option_d": "A bugle blast",
                "correct_option": "B", "difficulty": "Easy", "category": "Monuments",
                "explanation": "Golconda Fort's ingenious acoustic design allows a hand clap at the Fateh Darwaza entry portico to reverberate clearly to the highest summit at Bala Hissar, serving as an ancient early warning system."
            },
            {
                "question": "What is the primary spiritual concept meaning 'The whole world is one family' originating in the Maha Upanishad?",
                "option_a": "Satyameva Jayate", "option_b": "Vasudhaiva Kutumbakam",
                "option_c": "Ahimsa Paramo Dharma", "option_d": "Sarve Bhavantu Sukhinah",
                "correct_option": "B", "difficulty": "Easy", "category": "History",
                "explanation": "Vasudhaiva Kutumbakam (वसुधैव कुटुम्बकम्) is an ancient Sanskrit verse from the Maha Upanishad, reflecting India's timeless philosophical outlook that all humanity constitutes one global family."
            }
        ]

        for q_data in quiz_data:
            QuizQuestion.objects.update_or_create(
                question=q_data["question"],
                defaults=q_data
            )

        self.stdout.write(self.style.SUCCESS("[OK] Seeded 30+ Quiz Questions across all categories"))

        # 9. Seed Sample Community Stories & Leaderboard Scores
        stories_data = [
            {
                "title": "A Dawn Awakening along the Ghats of Kashi",
                "author": demo_user,
                "excerpt": "Watching the golden sun dissolve morning fog across the sacred Ganga as temple bells echo across three millennia of devotion.",
                "body": """There is a particular hour before sunrise in Varanasi when time feels suspended in golden amber. As our wooden rowing boat gently pushed away from the stone steps of Assi Ghat, the holy Ganga was as smooth as dark silk. 

Across the riverbanks, sadhus in saffron wraps offered silent dawn salutations (Arghya) to the awakening sun. From the high balconies of 18th-century Maratha palaces lining the riverfront, the fragrant scent of burning sandalwood, marigold garlands, and camphor drifted across the water.

At Dashashwamedh Ghat, the rhythmic clanging of brass bells and deep blowing of conch shells announced the morning aarti. Sitting in the morning stillness, one understands Mark Twain's famous reverence: Varanasi is truly older than history, older than tradition, and yet it pulses with a vitality as immediate as morning breath.""",
                "tags": "Varanasi, Ghats, Ganga, Spirituality, Morning Aarti",
                "status": "published",
                "cover_image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80"
            },
            {
                "title": "Deciphering the Stone Lace of Hoysala Temples",
                "author": admin_user,
                "excerpt": "Exploring the soapstone friezes of Belur and Halebidu, where medieval sculptors turned cold stone into fluttering silk and dancing celestial beings.",
                "body": """To stand before the Chennakeshava Temple at Belur is to question the physical limitations of stone. Unlike granite temples that command through brute scale, Hoysala temples captivate through breathless, microscopic detail.

The secret lies in the chloritic schist—often called green soapstone. When freshly quarried, it is soft and yielding to the chisel, allowing the sculptors to undercut stone so deeply that small beads carved on celestial dancers' necklaces can literally roll between your fingers without detaching.

Over successive decades of exposure to air, the soapstone oxidized and hardened into an impenetrable rock-solid exterior. On the star-shaped temple base, rows of charging elephants, lions, horses, and swans march across centuries with unmatched grace.""",
                "tags": "Karnataka, Hoysala, Temples, Architecture, Sculpture",
                "status": "published",
                "cover_image": "https://images.unsplash.com/photo-1600100397608-f010f443b719?auto=format&fit=crop&w=1200&q=80"
            }
        ]

        for s_item in stories_data:
            slug = slugify(s_item["title"])
            if slug in IMAGE_METADATA.get("stories", {}):
                m = IMAGE_METADATA["stories"][slug]
                s_item["cover_image"] = m["filename"]
                s_item["image_credit"] = m["author"]
                s_item["image_source_url"] = m["source_url"]
                s_item["image_license"] = m["license"]
            Story.objects.update_or_create(
                title=s_item["title"],
                defaults=s_item
            )

        # Seed initial quiz leaderboard entries
        sample_scores = [
            {"player_name": "Dr. Radhakrishnan", "score": 10, "total_questions": 10, "time_taken_seconds": 42},
            {"player_name": "Meera Nambiar", "score": 10, "total_questions": 10, "time_taken_seconds": 58},
            {"player_name": "Arjun Singhania", "score": 9, "total_questions": 10, "time_taken_seconds": 65},
            {"player_name": "Priyanka Roy", "score": 9, "total_questions": 10, "time_taken_seconds": 78},
            {"player_name": "Kabir Deshmukh", "score": 8, "total_questions": 10, "time_taken_seconds": 84},
        ]
        for sc in sample_scores:
            QuizScore.objects.get_or_create(
                player_name=sc["player_name"],
                defaults={**sc, "user": demo_user}
            )

        # Seed sample bookmark for demo user
        taj_site = site_objs.get("Taj Mahal")
        if taj_site:
            ct = ContentType.objects.get_for_model(HeritageSite)
            Bookmark.objects.get_or_create(
                user=demo_user,
                content_type=ct,
                object_id=taj_site.id
            )

        self.stdout.write(self.style.SUCCESS("""
======================================================================
  VIRASAT DATABASE SEEDING COMPLETED SUCCESSFULLY!
  - 28 States & Regions overview
  - 25+ Heritage Sites with UNESCO tags & image galleries
  - 20+ Cultural Festivals with month mappings & traditional rituals
  - 20+ Art Forms, Classical Dances, Crafts & Music Traditions
  - 20+ Authentic Regional Cuisines with dietary flags
  - 15 Historical Timeline Milestones from 3000 BCE to Present
  - 30+ Quiz Questions with explanatory historical context
  - Community Stories, Leaderboard Scores & Sample Bookmarks
======================================================================
"""))
