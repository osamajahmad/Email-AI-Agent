from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["Demo Authentication"],
)

templates = Jinja2Templates(directory="app/templates")


DEMO_PASSWORD = "demo123"
AUTHORIZED_DOMAIN = "@cspsolutions.com"


@router.get("/login")
def login_page(request: Request):
    """
    Display demo login page.

    This is not production authentication.
    Later, this should be replaced with Microsoft enterprise login.
    """

    demo_user = request.cookies.get("demo_user")

    if demo_user:
        return RedirectResponse(
            url="/",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "",
        },
    )


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    """
    Demo login route.

    Accepts only CSP Solutions emails and a demo password.
    """

    cleaned_email = email.strip().lower()

    if not cleaned_email.endswith(AUTHORIZED_DOMAIN):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Please use a CSP Solutions email address.",
            },
        )

    if password != DEMO_PASSWORD:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Invalid demo password.",
            },
        )

    response = RedirectResponse(
        url="/",
        status_code=303,
    )

    response.set_cookie(
        key="demo_user",
        value=cleaned_email,
        httponly=True,
        samesite="lax",
    )

    return response


@router.get("/logout")
def logout():
    """
    Log out the demo user.
    """

    response = RedirectResponse(
        url="/login",
        status_code=303,
    )

    response.delete_cookie("demo_user")

    return response