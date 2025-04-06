from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_openai
from urllib.parse import urlparse

app = FastAPI(title="SHL Assessment Recommender API")

class RecommendationRequest(BaseModel):
    input: str  # Full SHL URL or slug

@app.post("/recommend", response_class=JSONResponse)
async def recommend_assessments(req: RecommendationRequest):
    user_input = req.input.strip()
    
    # Determine if it's a full URL or slug
    if user_input.startswith("http"):
        url = user_input
        parsed_url = urlparse(url)
        slug = parsed_url.path.strip("/").split("/")[-1]
    else:
        slug = user_input.strip().strip("/")
        url = f"https://www.shl.com/solutions/products/product-catalog/view/{slug}/"

    try:
        dom = scrape_website(url)
        body = extract_body_content(dom)
        cleaned = clean_body_content(body)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Scraping failed: {str(e)}"})

    # Instruction to LLM
    instruction = f"""
You are helping HR professionals identify relevant SHL Assessments.

From the SHL job description text below, do the following:

1. Suggest the **most likely job title** if it's not obvious from the slug: `{slug}`.
2. Recommend up to 10 individual SHL Assessments for this role.
3. Output only a **markdown table** with the following columns:

- Assessment Name (as markdown link to SHL catalog)
- Remote Testing Support (Yes/No)
- Adaptive/IRT Support (Yes/No)
- Duration (e.g., 20 mins)
- Test Type (e.g., Cognitive, Personality, etc.)
"""

    try:
        chunks = split_dom_content(cleaned)
        llm_output = parse_with_openai(chunks, instruction)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"OpenAI parsing failed: {str(e)}"})

    # Parse markdown table to structured JSON
    try:
        import re
        from markdown_table_parser import MarkdownTable

        table = MarkdownTable(llm_output)
        parsed = table.to_dict()
        return {"job_slug": slug, "recommendations": parsed}
    except Exception as e:
        return JSONResponse(status_code=200, content={"markdown_table": llm_output, "warning": "Failed to parse table to JSON, returning raw markdown instead."})
