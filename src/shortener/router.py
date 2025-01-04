from fastapi import APIRouter

from .models.shortlink import ShortLink, LinkRequest

router = APIRouter()

sl_list = [ShortLink(
    original_url="674141414141426e65587039483054524a546e32394d4d68564d6c72632d50595773637132426e33516348476d4d485746375134326b4d535266757064627373374677307069423236465f344b767135484d617761525a526b4a764668783353796664576b6137524d5073567246312d483177636c6e593d",
    passcode="473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8",
    salt="14993c0aed9d7ee4089f82ac0c14c9b0",
    redirect_string="J3JDa")]


@router.get("/r/{redirect_string}")
def get_shortlink(redirect_string: str, passcode: str | None = None):
    sl = [el for el in sl_list if el.redirect_string == redirect_string]
    if len(sl) == 0:
        return "no url found"

    return sl[0].decode_url(passcode)

@router.post("/")
def create_shortlink(link_request: LinkRequest):
    shortlink = link_request.generate_shortlink()
    return {"shortlink": shortlink}
