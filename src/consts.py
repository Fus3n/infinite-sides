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
    {"from_str": "🌱 Oak Saplings + 🦴 Bone Meal", "result_str": "🌳 Oak Tree"},
    {"from_str": "🌿 Wheat + 🌾 Wheat", "result_str": "🍞 Bread"},
    {"from_str": "🥚 Egg + 🥚 Egg", "result_str": "🐣 Chick"},
    {"from_str": "🧊 Ice Block + 🔥 Torch", "result_str": "💧 Water Source"},
    {"from_str": "🧱 Brick + 🍶 Water Bottle", "result_str": "🏺 Clay"},
    {"from_str": "🏹 Bow + 🎣 Fishing Rod" , "result_str": "🛶 Trident"}
]

MODELS = [
    "llama2",
    "llava",
]

DEFAULT_MODEL = "llama2"