import datetime
from pathlib import Path

import pytest

from .parsers import parse_updates

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def about() -> bytes:
    return FIXTURES_ROOT.joinpath("about.html").open("rb").read()


def test_parse_updates(about: bytes):
    updates = list(parse_updates(about))
    assert len(updates) == 25
    assert updates[0]["date"] == datetime.date(2023, 5, 12)
    assert (
        updates[0]["content"]
        == """\n<img src="https://farmrpg.com/img/items/2nd_birthday.png" alt=""><br>\n"""
        """<br>\nIT IS OUR 2ND BIRTHDAY.<br>\nWhat a journey it has been! It\'s hard to """
        """fathom that today marks the second anniversary of Farm RPG\'s release. The """
        """game has come a long way from its initial version, and the improvements are """
        """undeniable. To all those who have been with us since the beginning, we extend """
        """our heartfelt gratitude, and to all those who join us daily and make our """
        """community a warm and welcoming place, we thank you as well. Let\'s all enjoy """
        """the festivities together! """
    )
    assert (
        updates[0]["clean_content"]
        == """\n<img src="https://farmrpg.com/img/items/2nd_birthday.png" alt=""><br>\n"""
        """<br>\nIT IS OUR 2ND BIRTHDAY.<br>\nWhat a journey it has been! It\'s hard to """
        """fathom that today marks the second anniversary of Farm RPG\'s release. The """
        """game has come a long way from its initial version, and the improvements are """
        """undeniable. To all those who have been with us since the beginning, we extend """
        """our heartfelt gratitude, and to all those who join us daily and make our """
        """community a warm and welcoming place, we thank you as well. Let\'s all enjoy """
        """the festivities together! """
    )
    assert (
        updates[0]["text_content"]
        == """IT IS OUR 2ND BIRTHDAY.\nWhat a journey it has been! It's hard to fathom """
        """that today marks the second anniversary of Farm RPG's release. The game has """
        """come a long way from its initial version, and the improvements are undeniable. """
        """To all those who have been with us since the beginning, we extend our heartfelt """
        """gratitude, and to all those who join us daily and make our community a warm """
        """and welcoming place, we thank you as well. Let's all enjoy the festivities together!"""
    )

    assert (
        updates[7]["text_content"]
        == """INTRODUCING BORGEN BUCKS
- Borgen has a deal for ya... every 10,000 AC you spend on the Wheel, at his Camp or cracking the Vault will earn you a Borgen Buck
- To help you track your progress, a progress bar has been added to the bottom of the Wheel, the Vault and Borgen's Camp
- The new Borgen Buck currency will unlock a new shop in May that Borgen runs with some very highly sought after items, if you have enough bucks...
- For more info, check out Borgen Bucks

IOS NOTIFICATIONS IN BETA:
- IN BETA: The Crop Harvest Notifications are now in Beta for players using an iOS device
- IN BETA: When you hit 'Plant All', your iOS app should ask you if you want to allow notifications. If you have any trouble, try going Home > top-right refresh and you may need to completely close out / re-open the iOS app
- IN BETA: It is possible you might need to update the iOS app from the App Store if you are not getting the notifications!

SMALL UPDATES:
- Two new high level craftable items -> Steel Vise and Red Trunk
- Vault Codes Cracked stat added to Profiles
- Some stats have been added to the bottom of your Bank History Log"""  # noqa: E501
    )

    assert updates[10]["date"] == datetime.date(2023, 4, 15)
    assert (
        updates[10]["content"]
        == """\nSOME CLARIFICATIONS:<br>\n- First, we hope you are enjoying the event!<br>"""
        """\n- Next, the bonuses that are active now are on until Sunday Evening 4/16<br>"""
        """\n- Special Help Requests that ask for Eggs are active until the end of the """
        """month 4/30<br>\n- Eggs will continue to drop all month long, including more """
        """ways to acquire each Egg<br>\n- The Hickory Omelette is a permanent meal, but """
        """the Crunchy Omelette is only cookable until 4/30<br>\n- So, you still have """
        """plenty of time to get more Eggs, don't panic! """
    )

    assert updates[20]["date"] == datetime.date(2023, 3, 24)
    assert (
        updates[20]["content"]
        == """\nSMALL UPDATES:<br>\n- New craftable item: <a href="item.php?id=743" """
        """class="close-panel"><img src="/img/items/211.png" alt="Step Ladder" class="itemimgsm"></a>"""
        """<span style="display:none">Step Ladder</span><br>\n- Reduced some height """
        """in My Kitchen to reduce scrolling<br>\n- The option to hide some alert """
        """notices at the top of Home have been added<br>\n- When fish are BITING, """
        """the color has been changed from green to gray<br>\n<br>\nNEW GREETING CARDS"""
        """<br>\n- There are new items, called \'Greeting Cards\', that you can buy at """
        """the <a href="flea.php" class="close-panel" style="color: """
        """crimson;font-weight:bold;text-decoration:underline">Flea Market</a>, but """
        """they can also be obtained from other players or from Help Requests or """
        """Friendship Rewards.<br>\n- This is an optional way to simply say \'Thank """
        """You\' or \'Congrats\' with a greeting card that can be placed in a mailbox. """
        """The cards aren\'t worth anything, but are just a nice token.<br>\n- More """
        """cards will appear in future updates as there\'s a lot of farming puns we """
        """need to use for special greeting cards. """
    )
