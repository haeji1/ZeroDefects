from bokeh.embed import json_item
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.domain.correlation.model.correlation_query_request import CorrelationQueryRequest
from app.domain.correlation.service.correlation_analysis_service import analyze_correlation

correlation_router = APIRouter(prefix="/api", tags=['correlation'])


@correlation_router.post("/correlation")
async def get_correlation_analysis(request_body: CorrelationQueryRequest):
    print("\n\nrequest_body:", request_body)
    if request_body.queryType != "time" and request_body.queryType != "step":
        raise HTTPException(status_code=404, detail="queryType must be 'time' or 'step'")
    plots = analyze_correlation(request_body)
    plot_json = [json_item(plot, f"my_plot_{idx}") for idx, plot in enumerate(plots)]
    if plot_json is None:
        raise HTTPException(status_code=404, detail="Correlation analysis failed.")
    return JSONResponse(status_code=200, content=plot_json)
