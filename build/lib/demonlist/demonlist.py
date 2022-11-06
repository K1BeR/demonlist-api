from functools import wraps
from exceptions import *
from utils import *
from client import Client, Response
from endpoints import *
import json


class Demonlist(Client):
    def catch_exception(fun):
        """
        A decorator taking action if an exception has been raised.
        """
        @wraps(fun)
        async def wrapper(self, *args, **kwargs):
            try:
                return await fun(self, *args, **kwargs)
            except Exception as e:
                await self.disconnect()
                print(e)
                raise e

        return wrapper

    def is_logged_in(fun):
        """
        A decorator that checks whether the user is logged into the account.
        """
        @wraps(fun)
        async def wrapper(self, *args, **kwargs):
            response = await self.request("get", LISTS[DemonListType.main])

            soup = await create_soup(response.body)
            link = await get_profile_link(soup)

            if link:
                return await fun(self, *args, **kwargs)
            else:
                raise NotLoggedIn("Call sign_in() before")
        return wrapper

    @catch_exception
    async def sign_in(self, login, password) -> bool:
        """
        Logging in to the account.

        :param login: user's login
        :type login: str
        :param password: user's password
        :type password: str
        :raise exceptions.WrongCredentials: If credentials are invalid
        :return: True if the account was successfully logged in
        :rtype: bool
        """
        endpoint = API_ENDPOINTS["sign_in"]
        response = await self.request(
            endpoint["method"],
            endpoint["path"],
            data={
                "login": login,
                "password": password,
                "action": endpoint["action"],
            }
        )
        print(response.body)
        if json.loads(response.body)["status"] == JsonStatus.ok.value:
            return True
        raise WrongCredentials()

    @catch_exception
    async def get_player_stats(self, player_id) -> dict:
        """
        Returns the user's statistics by his id.

        :param player_id: id of player
        :type player_id: int or str
        :return: User's statistic
        :rtype: dict
        """
        endpoint = API_ENDPOINTS["get_player_stats"]
        response = await self.request(endpoint["method"], endpoint["path"] + str(player_id))

        soup = await create_soup(response.body)

        result = {
            "name": await get_name(soup, "user"),
            "country": await get_img_title(soup, "country"),
            "badge": await get_img_title(soup, "badge"),
            "rank": await get_group(soup, 0, "user"),
            "score": await get_group(soup, 1, "user"),
            "hardest": await get_group(soup, 2, "user"),
            "verified": await get_category(soup, 0),
            "main": await get_category(soup, 1),
            "basic": await get_category(soup, 2),
            "extended": await get_category(soup, 3),
            "beyond": await get_category(soup, 4),
        }
        return result

    @catch_exception
    async def get_country_stats(self, country_name: str, list_type: CountryListType) -> dict:
        """
        Returns the country's statistics by his name.

        :param country_name: Name of country
        :type country_name: str
        :param list_type: Type of list
        :type list_type: CountryListType
        :return: Country's statistics
        :rtype: dict
        """
        endpoint = API_ENDPOINTS["get_country_stats"]
        response = await self.request(endpoint["method"], endpoint["path"] + f"flag={country_name}.png&list_type={list_type.value}")

        soup = await create_soup(response.body)

        if list_type == CountryListType.main:
            result = {
                "name": await get_name(soup, "user"),
                "players": await get_category(soup, 0),
            }
        else:
            result = {
                "name": await get_name(soup, "user"),
                "rank": await get_group(soup, 0, "user"),
                "score": await get_group(soup, 1, "user"),
                "hardest": await get_group(soup, 2, "user"),
                "main": await get_category(soup, 0),
                "basic": await get_category(soup, 1),
                "extended": await get_category(soup, 2),
                "beyond": await get_category(soup, 3),
            }
        return result

    @catch_exception
    async def get_level_info(self, level_id) -> dict:
        """
        Returns information about the level by its id.

        :param level_id: Id of level
        :type level_id: str or int
        :return: Information about the level
        :rtype: dict
        """
        endpoint = API_ENDPOINTS["get_level_info"]
        response = await self.request(endpoint["method"], endpoint["path"] + str(level_id))

        soup = await create_soup(response.body)

        result = {
            "name": await get_name(soup, "level"),
            "contributors": await get_contributors(soup),
            "description": await get_description(soup),
            "video": await get_video(soup),
            "password": await get_group(soup, 0, "level"),
            "id": await get_group(soup, 1, "level"),
            "length": await get_group(soup, 2, "level"),
            "object count": await get_group(soup, 3, "level"),
            "created in": await get_group(soup, 4, "level"),
            "max score": await get_group(soup, 5, "level"),
            "min score": await get_group(soup, 6, "level"),
            "song": await get_group(soup, 7, "level"),
            "gdbrowser": await get_group(soup, 8, "level"),
        }

        return result

    @catch_exception
    async def get_top(self, list_type: DemonListType) -> list:
        """
        Returns list of levels in order of difficulty.

        :param list_type: Type of list
        :type list_type: DemonListType
        :return: List of levels
        :rtype: list
        """
        response = await self.request("get", LISTS[list_type])

        soup = await create_soup(response.body)

        demons = list()
        for demon in await get_demons(soup):
            demons.append({
                "name": await get_level_name(demon),
                "holder": await get_level_holder(demon),
                "link": await get_level_link(demon),
                "video": await get_level_video(demon),
            })

        return demons

    @catch_exception
    async def get_whitelist(self) -> list:
        """
        Returns list of whitelisted players.

        :return: List of whitelisted players
        :rtype: list
        """
        endpoint = API_ENDPOINTS["get_whitelist"]
        response = await self.request(endpoint["method"], endpoint["path"])

        soup = await create_soup(response.body)

        players = list()
        for player in await get_whitelisted_players(soup):
            players.append(await get_text(player))

        return players

    @catch_exception
    @is_logged_in
    async def submit_record(self, level: str, progress: int, video: str, note: str) -> Response:
        """
        Sending a record.

        :param note: Additional notes you'd like to pass on to the list moderator receiving your submission
        :type note: str
        :param video: Video confirming the legitimacy of your record
        :type video: str
        :param progress: The progress made as percentage
        :type progress: int
        :param level: The name of level on which record was set
        :type level: str
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["submit_record"]
        data = {
            "level": level,
            "progress": progress,
            "video": video,
            "note": note,
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def add_level_main(self, name: str, level_id: int,
                             length_minutes: int, length_seconds: int,
                             objects: int, version: str, verifier: str,
                             holder: str, creator: str, video: str,
                             song_link: str, score: int, min_percent: int,
                             preview: object,
                             password: str = "", description: str = "") -> Response:
        """
        Adding a level to the main list.

        :param description: Optional Description of the level
        :type description: str
        :param video: Verification video
        :type video: str
        :param level_id: Id of the level
        :type level_id: int
        :param name: Name of the level
        :type name: str
        :param length_minutes: Length of the level in minutes
        :type length_minutes: int
        :param length_seconds: Seconds
        :type length_seconds: int
        :param objects: Quantity of objects
        :type objects: int
        :param version: The version in which the level was created
        :type version: str
        :param verifier: Verifier of the level
        :type verifier: str
        :param holder: Holder of the level
        :type holder: str
        :param creator: Creator of the level
        :type creator: str
        :param song_link: Link to the song
        :type song_link: str
        :param score: Quantity of points given for passing
        :type score: int
        :param min_percent: Minimum percentage for inclusion in the list
        :type min_percent: int
        :param preview: Image preview file
        :type preview: object
        :param password: Optional password to copy the level
        :type password: str
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["add_level_main"]
        data = {
            "name": name,
            "level_id": level_id,
            "length_minutes": length_minutes,
            "length_seconds": length_seconds,
            "objects": objects,
            "version": version,
            "password": password,
            "description": description,
            "verifier": verifier,
            "holder": holder,
            "creator": creator,
            "video": video,
            "song_link": song_link,
            "score": score,
            "min_percent": min_percent,
            "preview": preview,
            "action": endpoint["action"],
            "0": preview,
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def add_level_future(self, name: str, video: str, score: int, verifer: str, preview: object, ) -> Response:
        """
        Adding a level to the future list.

        :param video: Verification video
        :type video: str
        :param verifer: Verifier of the level
        :type verifer: str
        :param name: Name of the level
        :type name: str
        :param score: Quantity of points given for passing
        :type score: int
        :param preview: Image preview file
        :type preview: object
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["add_level_future"]
        data = {
            "name": name,
            "video": video,
            "score": score,
            "verifer": verifer,
            "preview": preview,
            "action": endpoint["action"],
            "0": preview
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def add_record(self, user: str, level: str, progress: int, video: str) -> Response:
        """
        Adding a record.

        :param video: Verification video
        :type video: str
        :param user: Name of user
        :type user: str
        :param level: Name of level
        :type level: str
        :param progress: Progress of passage
        :type progress: str
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["add_record"]
        data = {
            "user": user,
            "level": level,
            "progress": progress,
            "video": video,
            "action": endpoint["action"],
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def change_nickname(self, old_user: str, new_user: str) -> Response:
        """
        Changing a nickname of the user.

        :param old_user: Old name of the user
        :type old_user: str
        :param new_user: New name of the user
        :type old_user: str
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["change_nick"]
        data = {
            "old_user": old_user,
            "new_user": new_user,
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def change_country(self, login: str, flag: str) -> Response:
        """
        Changing a country of the user.

        :param login: Name of the user
        :type login: str
        :param flag: File name with the flag (including the extension, e. g. ".png")
        :type flag: str
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["change_country"]
        data = {
            "login": login,
            "flag": flag,
            "action": endpoint["action"],
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def change_badge(self, login: str, badge: Badge) -> Response:
        """
        Changing a badge of the user.

        :param login: Name of the user
        :type login: str
        :param badge: Badge of the user
        :type badge: Badge
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["change_badge"]
        data = {
            "login": login,
            "badge": badge.value,
            "action": endpoint["action"],
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def ban_user(self, name: str, months: int) -> Response:
        """
        Banning the user.

        :param name: Name of the user
        :type name: str
        :param months: Time for which you want to block the user in months
        :type months: int
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["ban_user"]
        data = {
            "name": name,
            "time": months,
            "action": endpoint["action"],
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def unban_user(self, name: str) -> Response:
        """
        Unbanning the user.

        :param name: Name of the user
        :type name: str
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["unban_user"]
        data = {
            "name": name,
            "action": endpoint["action"],
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def whitelist_user(self, name: str) -> Response:
        """
        Adding the user to whitelist.

        :param name: Name of the user
        :type name: str
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["whitelist_user"]
        data = {
            "name": name,
            "action": endpoint["action"],
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def unwhitelist_user(self, whitelist_id: int) -> Response:
        """
        Removing the user from whitelist.

        :param whitelist_id: Id of the whitelist record
        :type whitelist_id: int
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["whitelist_user"]
        data = {
            "id": whitelist_id,
            "action": endpoint["action"],
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    @catch_exception
    @is_logged_in
    async def requests(self, request_id: int, action: RequestsAction) -> Response:
        """
        Update the request.

        :param request_id: Id of the request
        :type request_id: int
        :param action: Action you want to do
        :type action: RequestsAction
        :raise exceptions.NotLoggedIn: If user wasn't logged in
        :return: Response from the site
        :rtype: Response
        """
        endpoint = API_ENDPOINTS["requests"]
        data = {
            "id": request_id,
            "action": action.value,
        }
        response = await self.request(endpoint["method"], endpoint["path"], data=data)

        return response

    catch_exception = staticmethod(catch_exception)
    is_logged_in = staticmethod(is_logged_in)

