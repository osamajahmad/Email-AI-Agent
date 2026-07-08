from fastapi import HTTPException, Request, status


AUTHORIZED_DOMAIN = "@cspsolutions.com"


def get_demo_user_from_request(request: Request):
    """
    Read the current demo user from the browser cookie.

    This is demo authentication only.
    In production, this should be replaced with Microsoft enterprise authentication.
    """

    demo_user = request.cookies.get("demo_user", "").strip().lower()

    if not demo_user:
        return None

    if not demo_user.endswith(AUTHORIZED_DOMAIN):
        return None

    return demo_user


def require_demo_user(request: Request):
    """
    Protect API/backend routes.

    If the user is not logged in through the demo login page,
    the request is rejected.
    """

    demo_user = get_demo_user_from_request(request)

    if not demo_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Demo login required.",
        )

    return demo_user