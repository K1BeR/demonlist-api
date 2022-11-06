from bs4 import BeautifulSoup


async def create_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'lxml')


async def get_name(soup: BeautifulSoup, owner: str) -> str:
    return soup.select_one(f'.{owner}-info__name').text


async def get_img_title(soup: BeautifulSoup, name):
    return soup.find('img', f'user-info__{name}')['title']


async def get_group(soup: BeautifulSoup, group_number: int, owner: str):
    return soup.findAll('div', f'{owner}-info__group')[group_number].select(f'.{owner}-info__value')[1].text


async def get_category(soup: BeautifulSoup, category_number: int):
    demons = list()
    for demon in soup.findAll('div', 'user-info__category')[category_number].findAll('div', 'user-info__link-wrap'):
        demons.append(demon.text.replace('\n', ''))
    return demons


async def get_contributors(soup: BeautifulSoup):
    return soup.find('div', 'level-info__verifier').text


async def get_description(soup: BeautifulSoup):
    return soup.find('div', 'level-info__description').text


async def get_video(soup: BeautifulSoup):
    return soup.find('div', 'level-info__video').iframe['src']


async def get_demons(soup: BeautifulSoup):
    return soup.select('.level-panel__container')


async def get_level_name(soup: BeautifulSoup):
    return soup.find('span', 'level-panel__name').text


async def get_level_holder(soup: BeautifulSoup):
    return soup.find('span', 'level-panel__holder').text


async def get_level_link(soup: BeautifulSoup):
    return soup.find('a', 'level-panel__link')['href']


async def get_level_video(soup: BeautifulSoup):
    return soup.find('a', 'level-panel__link--img-container')['href']


async def get_whitelisted_players(soup: BeautifulSoup):
    return soup.findAll('li', 'list__item')


async def get_text(soup: BeautifulSoup):
    return soup.text.replace(' ', '').replace('\n', '').replace('\r', '')


async def get_profile_link(soup: BeautifulSoup):
    return soup.find('a', {'href': '/profile'})


async def handle_response(res):
    if res.status == 200:
        pass
    else:
        raise RuntimeError(await res.text())
