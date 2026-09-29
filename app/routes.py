from fastapi import (
    APIRouter,
    Request,
    Form,
    Depends
)

from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .database import (
    get_db,
    save_user,
    save_plan,
    get_user,
    get_original_plan,
    get_plan,
    update_plan,
    get_all_users,
    get_all_plans
)

from .gemini_generator import generate_workout_gemini

from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .updated_plan import update_workout_plan

from .admin_auth import verify_admin


router = APIRouter()


# ============================================================
# HOME PAGE
# ============================================================

@router.get("/")
async def home(request: Request):

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ============================================================
# FEEDBACK PAGE
# ============================================================

@router.get(
    "/feedback",
    response_class=HTMLResponse
)
async def feedback_page(request: Request):

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="feedback.html",
        context={}
    )


# ============================================================
# GENERATE WORKOUT
# ============================================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
async def generate_workout(
    request: Request,

    user_id: str = Form(...),
    username: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),

    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Check whether user already exists
    # --------------------------------------------------------

    existing_user = get_user(
        db,
        user_id
    )

    if existing_user:

        # Existing users should go to feedback/update page
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="feedback.html",
            context={
                "user_id": existing_user.user_id,
                "username": existing_user.username,
                "age": existing_user.age,
                "weight": existing_user.weight,
                "goal": existing_user.goal,
                "intensity": existing_user.intensity,

                "error": (
                    "This User ID already exists. "
                    "You can provide feedback below to update "
                    "your existing workout plan."
                )
            }
        )

    # --------------------------------------------------------
    # Generate workout using Gemini
    # --------------------------------------------------------

    workout_plan = generate_workout_gemini(
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    # --------------------------------------------------------
    # Generate nutrition tip
    # --------------------------------------------------------

    nutrition_tip = generate_nutrition_tip_with_flash(
        goal=goal
    )

    # --------------------------------------------------------
    # Save user
    # --------------------------------------------------------

    save_user(
        db=db,
        user_id=user_id,
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    # --------------------------------------------------------
    # Save generated plan
    # --------------------------------------------------------

    save_plan(
        db=db,
        user_id=user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    # --------------------------------------------------------
    # Display generated result
    # --------------------------------------------------------

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user_id": user_id,
            "username": username,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,

            "workout_plan": workout_plan,

            "original_plan": workout_plan,

            "nutrition_tip": nutrition_tip
        }
    )


# ============================================================
# SUBMIT FEEDBACK
# ============================================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
async def submit_feedback(
    request: Request,

    user_id: str = Form(...),
    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    user = get_user(
        db,
        user_id
    )

    if not user:

        return request.app.state.templates.TemplateResponse(
            request=request,
            name="feedback.html",
            context={
                "error": "User ID not found."
            }
        )

    # --------------------------------------------------------
    # Get original workout plan
    # --------------------------------------------------------

    original_plan = get_original_plan(
        db,
        user_id
    )

    if not original_plan:

        return request.app.state.templates.TemplateResponse(
            request=request,
            name="feedback.html",
            context={
                "error": (
                    "No workout plan found for this user."
                )
            }
        )

    # --------------------------------------------------------
    # Generate updated workout plan
    # --------------------------------------------------------

    updated_plan = update_workout_plan(
        original_plan=original_plan,
        feedback=feedback,
        username=user.username,
        goal=user.goal,
        intensity=user.intensity
    )

    # --------------------------------------------------------
    # Save updated plan
    # --------------------------------------------------------

    update_plan(
        db=db,
        user_id=user_id,
        updated_plan=updated_plan,
        feedback=feedback
    )

    # --------------------------------------------------------
    # Get complete plan information
    # --------------------------------------------------------

    plan = get_plan(
        db,
        user_id
    )

    # --------------------------------------------------------
    # Display updated result
    # --------------------------------------------------------

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="result.html",
        context={

            "user_id": user.user_id,
            "username": user.username,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,

            "workout_plan": updated_plan,

            "original_plan": original_plan,
            "updated_plan": updated_plan,

            "nutrition_tip": plan.nutrition_tip,

            "feedback": feedback,

            "success": (
                "Your workout plan has been successfully updated!"
            )
        }
    )


# ============================================================
# ADMIN LOGIN PAGE
# ============================================================

@router.get(
    "/admin/login",
    response_class=HTMLResponse
)
async def admin_login_page(
    request: Request
):

    # If already logged in, go directly to dashboard
    if request.session.get("admin_logged_in"):

        return RedirectResponse(
            url="/view-all-users",
            status_code=303
        )

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={}
    )


# ============================================================
# ADMIN LOGIN
# ============================================================

@router.post(
    "/admin/login",
    response_class=HTMLResponse
)
async def admin_login(
    request: Request,

    username: str = Form(...),
    password: str = Form(...)
):

    # --------------------------------------------------------
    # Verify credentials
    # --------------------------------------------------------

    if not verify_admin(
        username,
        password
    ):

        return request.app.state.templates.TemplateResponse(
            request=request,
            name="admin_login.html",
            context={
                "error": "Invalid admin username or password."
            }
        )

    # --------------------------------------------------------
    # Create admin session
    # --------------------------------------------------------

    request.session["admin_logged_in"] = True

    request.session["admin_username"] = username

    # --------------------------------------------------------
    # Redirect to admin dashboard
    # --------------------------------------------------------

    return RedirectResponse(
        url="/view-all-users",
        status_code=303
    )


# ============================================================
# ADMIN DASHBOARD / VIEW ALL USERS
# ============================================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
async def view_all_users(
    request: Request,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # SECURITY CHECK
    # --------------------------------------------------------

    if not request.session.get("admin_logged_in"):

        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )

    # --------------------------------------------------------
    # Get all users
    # --------------------------------------------------------

    users = get_all_users(db)

    # --------------------------------------------------------
    # Get all plans
    # --------------------------------------------------------

    plans = get_all_plans(db)

    # --------------------------------------------------------
    # Organize plans by user ID
    # --------------------------------------------------------

    plans_by_user = {
        plan.user_id: plan
        for plan in plans
    }

    # --------------------------------------------------------
    # Display admin dashboard
    # --------------------------------------------------------

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users,
            "plans_by_user": plans_by_user,

            "admin_username": request.session.get(
                "admin_username"
            )
        }
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

@router.get("/admin/logout")
async def admin_logout(
    request: Request
):

    # Remove admin session
    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )