import datetime
from pathlib import Path

import pytest

from .parsers import parse_updates

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def about() -> bytes:
    return FIXTURES_ROOT.joinpath("about.html").open("rb").read()


@pytest.fixture
def about2() -> bytes:
    return FIXTURES_ROOT.joinpath("about2.html").open("rb").read()


def test_parse_updates(about: bytes):
    updates = list(parse_updates(about))
    assert len(updates) == 437
    assert updates[2].id == 446
    assert updates[2].date == datetime.date(2023, 5, 12)
    assert (
        updates[2].content
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
        updates[2].clean_content
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
        updates[2].text_content
        == """IT IS OUR 2ND BIRTHDAY.\nWhat a journey it has been! It's hard to fathom """
        """that today marks the second anniversary of Farm RPG's release. The game has """
        """come a long way from its initial version, and the improvements are undeniable. """
        """To all those who have been with us since the beginning, we extend our heartfelt """
        """gratitude, and to all those who join us daily and make our community a warm """
        """and welcoming place, we thank you as well. Let's all enjoy the festivities together!"""
    )

    assert (
        updates[9].text_content
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

    assert updates[12].date == datetime.date(2023, 4, 15)
    assert (
        updates[12].content
        == """\nSOME CLARIFICATIONS:<br>\n- First, we hope you are enjoying the event!<br>"""
        """\n- Next, the bonuses that are active now are on until Sunday Evening 4/16<br>"""
        """\n- Special Help Requests that ask for Eggs are active until the end of the """
        """month 4/30<br>\n- Eggs will continue to drop all month long, including more """
        """ways to acquire each Egg<br>\n- The Hickory Omelette is a permanent meal, but """
        """the Crunchy Omelette is only cookable until 4/30<br>\n- So, you still have """
        """plenty of time to get more Eggs, don't panic! """
    )

    assert updates[22].date == datetime.date(2023, 3, 24)
    assert (
        updates[22].content
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
    assert (
        updates[22].clean_content
        == """\nSMALL UPDATES:<br>\n- New craftable item: <a href="https://farmrpg.com/index.php#!/item.php?id=743">"""
        """<img src="https://farmrpg.com/img/items/211.png" alt="Step Ladder" style=";width:25px;height:25px" width="25" height="25">"""  # noqa: E501
        """</a><span style="display:none">Step Ladder</span><br>\n- Reduced some height in """
        """My Kitchen to reduce scrolling<br>\n- The option to hide some alert notices at """
        """the top of Home have been added<br>\n- When fish are BITING, the color has been """
        """changed from green to gray<br>\n<br>\nNEW GREETING CARDS<br>\n- There are new """
        """items, called \'Greeting Cards\', that you can buy at the """
        """<a href="https://farmrpg.com/index.php#!/flea.php" """
        """style="color: crimson;font-weight:bold;text-decoration:underline">Flea Market</a>, """
        """but they can also be obtained from other players or from Help Requests or Friendship """
        """Rewards.<br>\n- This is an optional way to simply say \'Thank You\' or \'Congrats\' """
        """with a greeting card that can be placed in a mailbox. The cards aren\'t worth """
        """anything, but are just a nice token.<br>\n- More cards will appear in future """
        """updates as there\'s a lot of farming puns we need to use for special greeting cards. """
    )

    assert (
        updates[24].text_content
        == """NEW CRAFTABLE ITEMS:
- Added on 3/17, the Green Top Hat is craftable until 3/31 --> Green Top Hat
- Added today, there are 3 other new items you can craft
- Wooden Table, Fancy Chair and Fancy Pan Flute

LARGE NET LAUNCHER SETTING IN BETA
- IN BETA: If you have the Large Net Launcher Farm Supply perk, you can go to Settings and set it to use between 10 and 50 large nets per click now
- IN BETA: This setting reduces clicks even more, but you have to be careful of your inventory cap to make full use of the setting

SMALL UPDATES:
- There is a chance now every 10 minutes that fish start biting more in a Fishing Location
- This means when you fish there, you'll get 2-3 more fish per bait (similar to the event bonus)
- The chance of this happening is 1 out of 10 every 10 minutes and the bonus will last 10 minutes
- On the Craftable Items list, Crafting XP has been added for quick reference

HIDE HELP REQUESTS IN ALPHA
- IN ALPHA: You can hide Help Requests now, just go into one you want to hide and scroll to the bottom to hide it
- IN ALPHA: It will then show in a 'Requests Hidden' view that is at the bottom of the Help Needed section"""  # noqa: E501
    )


def test_parse_updates2(about2: bytes):
    updates = list(parse_updates(about2))
    assert (
        updates[0].content
        == """
JUNE STARTER PACK AVAILABLE:<br>
- This month, the starter pack contains Holger\'s Lunch Box<br>
- The Lunch Box has a number of meals, including a new item -&gt; Lemon Cream Pie<br>
- Lemon Cream Pie allows you to use 5x Arnold Palmers per tap and is pretty handy<br>
- Also, look for the quest \'Sweet Days of Summer\' for an extra bonus!<br>
- You can get the Starter Pack here -&gt; <a href="gold.php" class="close-panel" style="color: crimson;font-weight:bold;text-decoration:underline">Gold</a><br>
<br>
MEDIUM UPDATES:<br>
- The <a href="soap.php" class="close-panel" style="color: crimson;font-weight:bold;text-decoration:underline">Soap Shop</a> has been updated with new items<br>
- There are new June Raptor types available in RFC<br>
- In your Raptor Pen, check out RaptorDex. This is a great new way to track all of your Raptor types at a glance. You can see which you have unlocked and tap to filter your Raptor Pen by each type.<br>
- There are a couple rare items moving around the Explore locations this month. Keep an eye out!<br>
- There are a few perks on sale a the <a href="supply.php" class="close-panel" style="color: crimson;font-weight:bold;text-decoration:underline">Farm Supply</a><br>
<br>
DEVELOPMENT BREAK<br>
- A lot of content dropped in May and with that firestream is going to take a 2-week break from development.<br>
- In his absence, <strong>Forcepath</strong> will be working hard to drop nightmarish quests while <strong>Tenfoo</strong> occasionally helps. Keep an eye out for new help requests, passwords or quizzes!<br>
"""  # noqa: E501
    )

    assert (
        updates[0].clean_content
        == """
JUNE STARTER PACK AVAILABLE:<br>
- This month, the starter pack contains Holger's Lunch Box<br>
- The Lunch Box has a number of meals, including a new item -&gt; Lemon Cream Pie<br>
- Lemon Cream Pie allows you to use 5x Arnold Palmers per tap and is pretty handy<br>
- Also, look for the quest 'Sweet Days of Summer' for an extra bonus!<br>
- You can get the Starter Pack here -&gt; <a href="https://farmrpg.com/index.php#!/gold.php" style="color: crimson;font-weight:bold;text-decoration:underline">Gold</a><br>
<br>
MEDIUM UPDATES:<br>
- The <a href="https://farmrpg.com/index.php#!/soap.php" style="color: crimson;font-weight:bold;text-decoration:underline">Soap Shop</a> has been updated with new items<br>
- There are new June Raptor types available in RFC<br>
- In your Raptor Pen, check out RaptorDex. This is a great new way to track all of your Raptor types at a glance. You can see which you have unlocked and tap to filter your Raptor Pen by each type.<br>
- There are a couple rare items moving around the Explore locations this month. Keep an eye out!<br>
- There are a few perks on sale a the <a href="https://farmrpg.com/index.php#!/supply.php" style="color: crimson;font-weight:bold;text-decoration:underline">Farm Supply</a><br>
<br>
DEVELOPMENT BREAK<br>
- A lot of content dropped in May and with that firestream is going to take a 2-week break from development.<br>
- In his absence, <strong>Forcepath</strong> will be working hard to drop nightmarish quests while <strong>Tenfoo</strong> occasionally helps. Keep an eye out for new help requests, passwords or quizzes!<br>
"""  # noqa: E501
    )

    assert (
        updates[0].text_content
        == """JUNE STARTER PACK AVAILABLE:
- This month, the starter pack contains Holger's Lunch Box
- The Lunch Box has a number of meals, including a new item -> Lemon Cream Pie
- Lemon Cream Pie allows you to use 5x Arnold Palmers per tap and is pretty handy
- Also, look for the quest 'Sweet Days of Summer' for an extra bonus!
- You can get the Starter Pack here -> Gold

MEDIUM UPDATES:
- The Soap Shop has been updated with new items
- There are new June Raptor types available in RFC
- In your Raptor Pen, check out RaptorDex. This is a great new way to track all of your Raptor types at a glance. You can see which you have unlocked and tap to filter your Raptor Pen by each type.
- There are a couple rare items moving around the Explore locations this month. Keep an eye out!
- There are a few perks on sale a the Farm Supply

DEVELOPMENT BREAK
- A lot of content dropped in May and with that firestream is going to take a 2-week break from development.
- In his absence, Forcepath will be working hard to drop nightmarish quests while Tenfoo occasionally helps. Keep an eye out for new help requests, passwords or quizzes!"""  # noqa: E501
    )
