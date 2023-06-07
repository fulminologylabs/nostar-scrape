# TODO instead of schemas
# take a functional approach
# and map websocket events
# to DB schema
# Also reference the Event DataClass from pynostr
from dacite import from_dict
from pynostr.event import Event, EventKind
from repository.models import TextNote
# TODO NEXT -
# (1) Test from_dict operation - using examples/test_process.py
# (2) Go from dataclass to SQLAlchemy Model - using examples/test_process.py
"""
Example Event (text_note):  
[
    "EVENT",
    {
        "id": "cd720b23163210ebddec88bc4e74d83c9667cdf11b95d376865315c686ed34eb", 
        "pubkey": "11d0b66747887ba9a6d34b23eb31287374b45b1a1b161eac54cb183c53e00ef7", 
        "created_at": 1684947090, 
        "kind": 1, 
        "tags": [
            [
                "e", 
                "f9f30e37adffe3afe12fda2f8db4502ece334f261273a9a0be7e8adb29b35145"
            ], 
            [
                "p", 
                "9eefd04d32ab5da8de12d7b83201578ea095a676acf3a692ec1b0b202ae4e16f"]
        ], 
        "content": "I'll take a large lill\u00f6rdag please.\n\n\ud83d\ude0e\ud83e\udd19\ud83d\udc47\ud83c\udf7b\n\nnostr:nevent1qqs0nucwx7kllca0uyha5tudk3gzan3nfunpyuaf5zl8azkm9xe4z3gpzamhxue69uhhyetvv9ujumn0wd68ytnzv9hxgtczyz0wl5zdx244m2x7zttmsvsp2782p9dxw6k08f5jasdskgp2unsk7qcyqqqqqqgncdx20", 
        "sig": "6c66e42dd481a0769148be33932a643672710f0ed83eeaaf4af5fe0f53e52b810a924ba2498354b8b00a54f065f4de0d92c42c70fdb39a2da67ac97baf4f9ae0"
    }
]
"""
def tag_to_dict(e: Event) -> dict:
    """
        Takes in a tag list from an Event and returns a dict
        where the Tag keys (#e, #p). See constants.SUPPORTED_TAGS
    """
    tag_dict = 

def map_text_note(event: Event, job_id: int) -> TextNote:
    """
        TODO return a type that can be 
        directly injected into the DB
    """
    return TextNote(
        event=EventKind.TEXT_NOTE,
        job_id=job_id,
    )

def get_text_note(id: int) -> TextNote:
    pass
# def _convert_raw(event: list) -> Event:
#     if event[0] == "EVENT":
#         t_event = from_dict(
#             data_class=Event,
#             data=event[1]
#         )
#         # assert t_event == Event(
#         # content="", 
#         # pubkey="", 
#         # created_at=0, 
#         # kind=EventKind.TEXT_NOTE, 
#         # tags=[[], []], 
#         # id="", 
#         # sig=""
#         # )
#         return t_event
#     else:
#         raise ValueError("This is not a Nostr Event.")
    
def handle_text_note_bulk(events: list) -> list[Event]:
    """
        TODO implement
        - takes in a text note event list
            and returns a dataclass type
            that can be mapped to our DB
            models
    """
    try:
        return [
            _convert_raw(evt) for evt in events
        ]
    except Exception as e:
        # TODO error handling
        print(
            f"Failed to convert raw event to event \
            dataclass in bulk function with error: {e}"
        )
        raise e

def handle_text_note(event: list) -> Event:
    """
        TODO IMPLEMENT  
        -   Takes in a text note event and
            returns a dataclass that can be mapped
            to our DB models
    """
    try:
        return _convert_raw(event)
    except Exception as e:
        # TODO error handling
        print(
            f"Failed to convert raw event to event \
            dataclass in single handle function with error: {e}"
        )
        raise e
