

def is_search_crawler(user_agent):
    spiders = ('bot',
               'slurp',
               'spider',
               'archiver',
               'facebook',
               'lycos',
               'scooter',
               'altavista',
               'teoma',
               'domainreanimator.com',
               'python-urllib',
               'yandeximages',
               'plukkie',
               'buzzsumo',
               'clickagy',
               'kraken',
               'wotbox',
               'nutch',
               'contextad',
               'pinterest',
               'deusu',
               'go-http-client',
               'yeti',
               'ltx71',
               'qwantify',
               'teoma',
               'alexa',
               'froogle',
               'inktomi',
               'looksmart',
               'url_spider_sql',
               'firefly',
               'nationaldirectory',
               'ask jeeves',
               'tecnoseek',
               'infoseek',
               'crawler',
               'www.galaxy.com',
               'webmaster',
               'scooter',
               'james bond',
               'slurp',
               'msnbot',
               'appie',
               'fast',
               'webbug',
               'spade',
               'zyborg',
               'rabaz',
               'feedfetcher-google',
               'technoratisnoop',
               'rankivabot',
               'mediapartners-google',
               'yandex',
               'stackrambler',
               'dotbot',
               'updown.io',
               'go 1.1 package http',
               'python-requests',
               'libwww-perl',
               'sogou',
               'expanse',
               'zoominfobot',
               'go http package',
               'apache-httpclient',
               'netsystemsresearch',
               'panscient.com',
               'aiohttp',
               'gdnplus',
               'catexplorador',
               'scrapy',
               'masscan',
               'wget',
               'java/1')
    for s in spiders:
        if s in user_agent.lower():
            return True
    return False
