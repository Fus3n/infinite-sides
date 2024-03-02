from typing import List, TypedDict

DEFAULT_SYSTEM_MSG = """You are Infinit craft

when you are given 2 text with emoji.

Give something back that makes sense with relating text with emoji

for example: "🌍 Earth" + "💧 Water" could result in "🌱 Plant"
or "💧 Water" + "🔥 Fire" could result in "💨 Steam"
You need to create these depending on input. The input format will be: "emoji Text + emoji Text"
And your result should be "emoji Text" always.
And always try to keep the emoji as Closely related to the text as possible and stay consistent.
some examples:
"🌬️ Wind + 🌱 Plant" = 🌼 Dandelion
"🌍 Earth + 💧 Water" = 🌱 Plant
"🌍 Earth + 🔥 Fire" = 🌋 Lava
"🌍 Earth + 🔥 Fire" = 🌋 Lava
"🌋 Lava + 🌋 Lava" = 🌋 Volcano
"💧 Water + 🌬️ Wind" = 🌊 Wave

And the emoji and text can be anything, it is not limited to the example i gave, make ANYTHING and always return a response in the given format
"""

class ExampleEntry(TypedDict):
    from_str: str
    result_str: str

ExampleType = List[ExampleEntry]


DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_EXAMPLES: ExampleType = [
    {"from_str": "🌍 Earth + 💧 Water", "result_str": "🌱 Plant"},
    {"from_str": "💨 Wind + 🌱 Plant", "result_str": "🌼 Dandelion"},
    {"from_str": "🌍 Earth + 🔥 Fire", "result_str": "🌋 Lava"},
    {"from_str": "🌋 Lava + 🌋Lava", "result_str": "🌋 Volcano"},
    {"from_str": "💧 Water + 💨 Wind", "result_str": "🌊 Wave"},
    {"from_str": "🏔️ Mountain + ❄️ Snow", "result_str": "🌨️ Avalanche"},
    {"from_str": "🌞 Sun + ☔ Rain", "result_str": "🌈 Rainbow"},
]

DEFAULT_CHIPS = [
    "🌍 Earth",
    "💨 Wind",
    "💧 Water",
    "🔥 Fire",
]

MODELS = [
    "llama2",
    "mistral",
    "llava"
]

DEFAULT_MODEL = "llama2"