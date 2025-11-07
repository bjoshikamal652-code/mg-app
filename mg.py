from fastapi import FastAPI, Request, Form
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from cs import register, login, home

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="kjoshi")

@app.post("/register")
def u_register(request: Request, email: str = Form(""), contact_number: str = Form("")):
    if not register(email, contact_number):
        return JSONResponse(content={"msg": "user already registered"}, status_code = 409)
    request.session["email"] = email
    request.session["contact_number"] = contact_number
    return JSONResponse(content={"msg": f"user registered {email or contact_number}"}, status_code = 200)

@app.post("/login")
def u_login(request: Request, email: str = Form(""), contact_number: str = Form("")):
    if not login(email, contact_number):
        return JSONResponse(content={"msg": "user not registered"}, status_code = 403)
    request.session["email"] = email
    request.session["contact_number"] = contact_number
    return JSONResponse(content={"msg": f"user logged in {email or contact_number}"}, status_code = 200)

@app.get("/home")
def u_home(request: Request, email: str = "", contact_number: str = ""):
    email = request.session.get("email")
    contact_number = request.session.get("contact_number")
    if not email or contact_number:
        return JSONResponse(content={"msg": "user not logged in"}, status_code = 403)

    if not home(email, contact_number):
        return JSONResponse(content={"msg": "user not logged in"}, status_code = 403)

    return JSONResponse(content={"msg": f"Welcome user {email or contact_number}"}, status_code = 200)

@app.get("/logout")
def u_logout(request: Request):
    email = request.session.get("email")
    contact_number = request.session.get("contact_number")
    if not email or contact_number:
        return JSONResponse(content={"msg": "user not in session"}, status_code = 403)
    request.session.pop("email" or "contact_number", None)
    return JSONResponse(content={"msg": f"user logged out {email or contact_number}"}, status_code = 200)
