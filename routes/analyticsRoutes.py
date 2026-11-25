
from fastapi import (
    APIRouter,
    Depends
)

from services.authService import VerifyAdminKey

from services.analyticsService import GetSupportAnalytics

from datetime import date
from fastapi import HTTPException, Query
from fastapi.responses import Response

from services.reportService import (
    GetAnalyticsReport,
    GenerateTicketCSV
)


router = APIRouter(
    prefix="/api/analytics",
    tags=["Support Analytics"],
    dependencies=[Depends(VerifyAdminKey)]
)


@router.get("/overview")
def GetAnalyticsOverview():

    return GetSupportAnalytics()





def ValidateDateRange(start_date, end_date):

    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=422,
            detail="Start date cannot exceed end date"
        )


@router.get("/report")
def GetFilteredAnalytics(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None)
):

    ValidateDateRange(start_date, end_date)

    return GetAnalyticsReport(
        start_date=start_date,
        end_date=end_date
    )


@router.get("/export")
def ExportTicketReport(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None)
):

    ValidateDateRange(start_date, end_date)

    content = GenerateTicketCSV(
        start_date=start_date,
        end_date=end_date
    )

    filename = "novatech_support_report.csv"

    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"',
            "Cache-Control": "no-store"
        }
    )

