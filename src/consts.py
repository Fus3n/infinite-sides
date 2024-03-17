from typing import List, TypedDict

DEFAULT_SYSTEM_MSG = """You are playing as a historian tasked with combining elements from the Japanese Occupation in the Philippines to uncover deeper insights into this period. Use emojis to represent key figures, events, and concepts, and combine them to reveal new understandings or outcomes.

For example:
"🇯🇵 Japanese Expansionism" + "🌾 Rice & Food Shortages" could result in "📉 Economic Hardship"
or
"🏰 Manila Declared Open City" + "✈️ Japanese Air Raid" could result in "🔥 Manila in Flames"

Your task is to interpret combinations and provide results that reflect the historical interactions or consequences of these elements. The input format will be: "emoji Text + emoji Text", and your result should always be in the "emoji Text" format. Aim to use emojis that closely relate to the text for an immersive experience.

Here are some elements from the document to get you started:

- "👑 Manuel L. Quezon + 🛡️ National Defense Plan" = "🏰 Preparation for War"
- "💣 Pearl Harbor Bombing + 🌍 Philippines" = "🕰️ Start of Occupation"
- "👣 Bataan Death March + 🚶‍♂️ POWs" = "😢 Suffering and Hardship"
- "⚔️ Guerilla Warfare + 🌳 Philippine Jungles" = "🛡️ Resistance Efforts"
- "🇺🇸 Douglas MacArthur + 🗣️ 'I Shall Return'" = "🏖️ Leyte Landing"

Experiment with different combinations to explore the occupation's narrative. Your combinations and results will contribute to a deeper understanding of this historical period. Remember, the goal is to keep the emoji as closely related to the text as possible and maintain consistency throughout your responses.

"""


class ExampleEntry(TypedDict):
    from_str: str
    result_str: str


ExampleType = List[ExampleEntry]

DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_EXAMPLES: ExampleType = [
    # Basic
    {"from_str": "🌍 Earth +🌍 Earth", "result_str": " 🏔️ Mountain"},
    {"from_str": "🌍 Earth + 💧 Water", "result_str": "🌱 Plant"},
    {"from_str": "🌍 Earth + 🌱 Plant", "result_str": "🌳 Tree"},
    {"from_str": "🌳 Tree + 👤 Person", "result_str": "🌲 Wood"},
    {"from_str": "⬆️ Up + ⬇️ Down", "result_str": "🎯 Middle"},
    {"from_str": "⬅️ Left + ➡️ Right", "result_str": "🎯 Middle"},
    {"from_str": "🏛️ Institution + 👥 People", "result_str": "🏛️ Government"},
    {"from_str": "🕊️ Peace + 🏛️ Government", "result_str": "📜 Treaty"},

    {"from_str": "🔥 Fire + 🔫 Weapon", "result_str": "💣️ Bomb"},
    {"from_str": "🔥 Fire + 💣️ Bomb", "result_str": "💥 Explosion"},
    {"from_str": "💣️ Bomb + 💣️ Bomb", "result_str": "💥 Explosion"},

    {"from_str": "🌲 Wood + 💧 Water", "result_str": "🚤 Boat"},
    {"from_str": "🛶 Boat + 💨 Wind", "result_str": "🛩️ Airplane"},

    {"from_str": "👤 Person + 💴 Money", "result_str": "🧑‍💼 Merchant"},
    {"from_str": "👤 Person + 👤 Person", "result_str": "👥 People"},
    {"from_str": "👤 Person + 🇯🇵 Japan", "result_str": "👤 Japanese"},
    {"from_str": "👤 Person + 🇵🇭 Philippines", "result_str": "👤 Filipino"},
    {"from_str": "👤 Person + 🇺🇸 United States", "result_str": "👤 American"},
    {"from_str": "👤 Person + 🇨🇳 China", "result_str": "👤 Chinese"},

    {"from_str": "👤 Person + 🔫 Weapon", "result_str": "🪖 Soldier"},
    {"from_str": "🪖 Soldier + 🪖 Soldier", "result_str": "🪖 Troops"},
    {"from_str": "🪖 Troops + 🪖 Soldier", "result_str": "🎖️ General"},
    {"from_str": "👤 American + 🪖 Soldier", "result_str": "🪖 American Soldier"},
    {"from_str": "👤 Filipino + 🪖 Soldier", "result_str": "🪖 Filipino Soldier"},
    {"from_str": "👤 Japanese + 🪖 Soldier", "result_str": "🪖 Japanese Soldier"},
    {"from_str": "👤 Chinese + 🪖 Soldier", "result_str": "🪖 Chinese Soldier"},
    {"from_str": "🪖 American Soldier + 🪖 American Soldier", "result_str": "👥 American Troops"},
    {"from_str": "🪖 Filipino Soldier + 🪖 Filipino Soldier", "result_str": "👥 Filipino Troops"},
    {"from_str": "🪖 Japanese Soldier + 🪖 Japanese Soldier", "result_str": "👥 Japanese Troops"},
    {"from_str": "🪖 Chinese Soldier + 🪖 Chinese Soldier", "result_str": "👥 Chinese Troops"},
    {"from_str": "👥 Japanese Troops +🛶 Boat", "result_str": "🛶 Japanese Ship"},
    {"from_str": "👥 American Troops +🛶 Boat", "result_str": "🛶 American Ship"},
    {"from_str": "🛶 Japanese Ship +🛶 Japanese Ship", "result_str": "🛶 Japanese Navy"},
    {"from_str": "🛶 American Ship +🛶 American Ship", "result_str": "🛶 American Navy"},
    {"from_str": "🛶 Boat + 🪖 Soldier", "result_str": "⚓ Naval Power"},
    {"from_str": "🛶 Boat + 🪖 Troops", "result_str": "⚓ Naval Power"},
    {"from_str": "🛶 Boat + 🪖 General", "result_str": "⚓ Naval Power"},
    {"from_str": "🛩️ Airplane + 🪖 Soldier", "result_str": "✈️ Air Power"},
    {"from_str": "🛩️ Airplane + 🪖 Troops", "result_str": "✈️ Air Power"},
    {"from_str": "🛩️ Airplane + 🪖 General", "result_str": "✈️ Air Power"},

    {"from_str": "🌱 Plant + 🏙️ Manila", "result_str": "🌿 Hemp"},

    # People
    {"from_str": "👤 Filipino + 🇵🇭 Philippines", "result_str": "👨‍💼 Manuel L. Quezon"},
    {"from_str": "🧑‍💼 Merchant + 👤 Japanese", "result_str": "🧑‍💼 Oda Kyosaburo"},
    {"from_str": "🧑‍💼 Merchant + 🇯🇵 Japan", "result_str": "🧑‍💼 Oda Kyosaburo"},
    {"from_str": "🎖️ General + 👤 American", "result_str": "🎖️ Douglas MacArthur"},
    {"from_str": "🎖️ General + 🇯🇵 Japan", "result_str": "🎖️ Masaharu Homma"},
    {"from_str": "🎖️ General + 👤 Japanese", "result_str": "🎖️ Masaharu Homma"},

    # Places
    {"from_str": "🏝️ Island + 🇵🇭 Philippines", "result_str": "🏝️ Philippine Islands"},
    {"from_str": "🏝️ Philippine Islands + ⬆️ Up", "result_str": "🏝️ Luzon"},
    {"from_str": "🏝️ Philippine Islands + 🎯 Middle", "result_str": "🏝️ Visayas"},
    {"from_str": "🏝️ Philippine Islands + ⬇️ Down", "result_str": "🏝️ Mindanao"},
    {"from_str": "🏙️ City + 🏝️ Luzon", "result_str": "🏙️ Manila"},
    {"from_str": "🏙️ City + 🏝️ Mindanao", "result_str": "🏙️ Davao"},
    {"from_str": "🏝️ Island + 🏝️ Visayas", "result_str": "🏝️ Leyte"},
    {"from_str": "🇨🇳 China + 👥 Japanese Troops", "result_str": "🎌 Manchukuo"},
    {"from_str": "⬅️ Left + 🏝️ Luzon", "result_str": "🗻 Bataan"},
    {"from_str": "🎯 Middle + 🏝️ Luzon", "result_str": "🌾 San Fernando"},
    {"from_str": "⬆️ Up + 🌾 San Fernando", "result_str": "🌾 Tarlac"},
    {"from_str": "🌾 San Fernando + 👥 American Troops ", "result_str": "⛺️ Camp O’Donnell"},


    # Institutions
    {"from_str": "🏭 Factory + 🧑‍💼 Oda Kyosaburo", "result_str": "🏭 Ota Development Corporation"},

    # Events
    {"from_str": " 🧑‍💼 Oda Kyosaburo + 🗻 Bataan", "result_str": "☠️ Bataan Death March"},
    {"from_str": "🪖 Masaharu Homma + 🗻 Bataan", "result_str": "☠️ Bataan Death March"},
    {"from_str": "🌴 Bataan + 🌴 San Fernando", "result_str": "☠️ Bataan Death March"},
    {"from_str": "🇺🇸 America + 💥 Explosion", "result_str": "💣 Pearl Harbor Bombing"},
    {"from_str": "🇯🇵 Japan + 💥 Explosion", "result_str": "💣 Pearl Harbor Bombing"},
    {"from_str": "👥 Japanese Troops + 👥 Chinese Troops", "result_str": "🪖 2nd Sino-Japanese War"},
    {"from_str": "🛶 Boat + 🏝️ Leyte", "result_str": "🏝️ Leyte Landing"},
    {"from_str": "⚓ Naval Power + 🏝️ Leyte", "result_str": "⚔️ Battle of Leyte Gulf"},

    # Narrative
    {"from_str": "🕊️ Peacetime + 👨‍💼 Manuel L. Quezon", "result_str": "🏛️ Start of the Commonwealth"},
    {"from_str": "🏛️ Government + 👨‍💼 Manuel L. Quezon", "result_str": "🏛️ Start of the Commonwealth"},
    {"from_str": "🏛️ Government + 📜 Treaty", "result_str": "🏛️ Start of the Commonwealth"},
    {"from_str": "🏛️ Government" +  "📃 Policy", "result_str": "🏛️ Start of the Commonwealth"},
    {"from_str": "👤 Manuel Quezon + 🇺🇸 United States", "result_str": "🇵🇭 Start of the Commonwealth"},

    {"from_str": "🇺🇸 America + 💥 Explosion", "result_str": "💣 Pearl Harbor Bombing"},
    {"from_str": "🇯🇵Japan + 💥 Explosion", "result_str": "💣 Pearl Harbor Bombing"},
    {"from_str": "✈️ Air Power + 💥 Explosion", "result_str": "💣 Pearl Harbor Bombing"},

    {"from_str": "🕊️ Peacetime + 💣 Pearl Harbor Bombing", "result_str": "⛩️ Japanese Occupation"},
    {"from_str": "🕊️ Peacetime + 👥 Japanese Troops", "result_str": "⛩️ Japanese Occupation"},
    {"from_str": "🕊️ Peacetime + 💣 Pearl Harbor Bombing", "result_str": "⛩️ Japanese Occupation"},
    {"from_str": "🇯🇵 Japan + 🇵🇭 Philippines", "result_str": "🇵🇭 Japanese Occupation"},


    {"from_str": "⛩️ Japanese Occupation +  🇵🇭 Philippines", "result_str": "🇵🇭 Philippine Resistance"},
    {"from_str": "⛩️ Japanese Occupation + 👤 Filipino", "result_str": "🇵🇭 Philippine Resistance"},

    # {"from_str": "🇯🇵 Japan + ⚠️ War", "result_str": "🏞️ Bataan Death March"},
    # {"from_str": "🇵🇭 Philippines + ⚠️ War", "result_str": "✊ Guerrilla Warfare"},
    {"from_str": "🇵🇭 Philippine Resistance + 💣 Bataan Death March", "result_str": "✊ Guerrilla Warfare"},



    # Others
    {"from_str": " 🇵🇭 Philippines + 👨‍💼Manuel L. Quezon", "result_str": "🛡️Civilian Emergency Administration"},
    {"from_str": "🇺🇸 America + 💥 Explosion", "result_str": "💣 Pearl Harbor Bombing"},
    {"from_str": "🇺🇸 America + 💥 Explosion", "result_str": "💣 Pearl Harbor Bombing"},

    {"from_str": "🇯🇵 Japan + 📜 Meiji Restoration", "result_str": "🏭 Industrialization"},
    {"from_str": "🇵🇭 Philippines + 🛠️ National Defense Plan", "result_str": "🛡️ Civilian Emergency Administration"},
    {"from_str": "🕊️ Peace + 🚨 Japanese Expansionist Policy", "result_str": "🔥 Conflict"},
    {"from_str": "🚢 USS Missouri + 📄 Surrender Document", "result_str": "✌️ Liberation"},
    {"from_str": "🌉 Manila + 🏭 Industrial Growth", "result_str": "💼 Economic Nationalism"},
    {"from_str": "👥 Guerrilla Units + 🌳 Mountainous Terrain", "result_str": "💥 Resistance Efforts"},
    {"from_str": "💰 Mickey Mouse Money + 🔄 Barter System", "result_str": "📉 Economic Decline"},
    {"from_str": "📚 Education + 🇯🇵 Japanese Language", "result_str": "🏫 Cultural Assimilation"},
    {"from_str": "🎌 Greater East Asia Co-Prosperity Sphere + 🌏 Southeast Asia",
     "result_str": "🤝 Political Manipulation"},
    {"from_str": "🏯 Japanese Castle + 🔥 Fire", "result_str": "💣 Bomb"},
    {"from_str": "🇵🇭 Philippine Flag + ⚔️ Sword", "result_str": "🔒 Lock"},
    {"from_str": "📜 Scroll + 🕊️ Peace", "result_str": "🇯🇵 Japanese Flag"},
    {"from_str": "💧 Water + 🌾 Rice", "result_str": "🍚 Cooked Rice"},
    {"from_str": "🔥 Fire + 🌱 Manila Hemp", "result_str": "📦 Supplies"},
    {"from_str": "🚢 Ship + 🇯🇵 Japanese Flag", "result_str": "⚓ Occupation"},
    {"from_str": "👥 People + 💣 Bomb", "result_str": "🚑 Aid"},
    {"from_str": "🕊️ Peace + ⚔️ Sword", "result_str": "📝 Treaty"},
]

DEFAULT_CHIPS = [
    "🌍 Earth",
    "💨 Wind",
    "💧 Water",
    "🔥 Fire",
    "👤 Person",
    "🇯🇵 Japan",
    "🇵🇭 Philippines",
    "🇺🇸 America",
    "💴 Money",
    "🏙️ City",
    "🏛️ Institution",
]

MODELS = [
    "llama2",
    "mistral",
    "llava"
]

DEFAULT_MODEL = "llama2"
